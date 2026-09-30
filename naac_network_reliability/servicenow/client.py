"""Reusable, read-only Table API transport; no incident or risk knowledge."""

import re
from urllib.parse import urlencode

import requests

from .exceptions import ServiceNowError
from .auth import authenticate


class ServiceNowClient:
    PAGE_SIZE = 500
    MAX_PAGES = 20

    def __init__(self, config):
        self.config = config

    @staticmethod
    def _validate_table(table):
        if not isinstance(table, str) or not re.fullmatch(r"[a-zA-Z0-9_]+", table):
            raise ServiceNowError("Invalid ServiceNow table name.")

    def list_url(self, table, query):
        self._validate_table(table)
        instance_url = self.config["instance_url"]
        parameters = urlencode({"sysparm_query": query})
        return f"{instance_url}/{table}_list.do?{parameters}"

    def get_records(self, table, query, fields):
        """Return complete results or raise; never return a truncated count.

        Query and fields are supplied by trusted resource code, not user input.
        Each request reads one page; records are combined before returning.
        """
        self._validate_table(table)
        instance_url = self.config["instance_url"]
        records = {}
        # sys_id is used to avoid counting the same record twice.
        selected_fields = ["sys_id"]
        for field in fields:
            if field not in selected_fields:
                selected_fields.append(field)
        with requests.Session() as session:
            session.headers.update({"Accept": "application/json"})
            authenticate(session, self.config)
            for page in range(self.MAX_PAGES):
                try:
                    response = session.get(
                        f"{instance_url}/api/now/table/{table}",
                        params={"sysparm_query": query + "^ORDERBYsys_id",
                                "sysparm_fields": ",".join(selected_fields),
                                "sysparm_display_value": "false",
                                "sysparm_limit": self.PAGE_SIZE,
                                "sysparm_offset": page * self.PAGE_SIZE},
                        timeout=(5, 15), allow_redirects=False,
                    )
                    response.raise_for_status()
                    if response.status_code != 200:
                        raise ServiceNowError("ServiceNow returned an unexpected response.")
                    payload = response.json()
                except (requests.RequestException, ValueError):
                    raise ServiceNowError("ServiceNow is unavailable. Check connectivity and API credentials.") from None
                if not isinstance(payload, dict):
                    raise ServiceNowError("ServiceNow returned an invalid table response.")
                rows = payload.get("result")
                if not isinstance(rows, list):
                    raise ServiceNowError("ServiceNow returned an invalid table response.")
                if not rows:
                    return list(records.values())
                for row in rows:
                    if not isinstance(row, dict) or not isinstance(row.get("sys_id"), str) or not row["sys_id"]:
                        raise ServiceNowError("ServiceNow returned incomplete records. Check read permissions.")
                    records[row["sys_id"]] = row
                # Short pages can occur with ACL filtering; request the next page.
        raise ServiceNowError("ServiceNow result limit reached; narrow the configured query.")
