"""Build the incident filter and read incident priorities."""

import re

from .exceptions import ServiceNowError


def build_incident_query(config):
    """Use the same filter for API counts and the ServiceNow View link."""
    groups = config.get("assignment_group_ids", [])
    if not isinstance(groups, (list, tuple)) or not groups:
        raise ServiceNowError("Configure at least one assignment-group sys_id.")

    group_ids = []
    for group_id in groups:
        # A ServiceNow sys_id contains exactly 32 hexadecimal characters.
        if not isinstance(group_id, str) or not re.fullmatch(r"[0-9a-fA-F]{32}", group_id):
            raise ServiceNowError("Each assignment-group sys_id must contain 32 hexadecimal characters.")
        group_id = group_id.lower()
        if group_id not in group_ids:
            group_ids.append(group_id)

    excluded_states = config.get("excluded_states", ["6", "7", "8"])
    if not isinstance(excluded_states, (list, tuple)):
        raise ServiceNowError("ServiceNow excluded_states must be a list of numeric state values.")

    state_values = []
    for state in excluded_states:
        if not re.fullmatch(r"-?\d+", str(state)):
            raise ServiceNowError("ServiceNow excluded_states must contain numeric state values.")
        state_values.append(str(state))

    filters = [
        "active=true",
        "priorityIN1,2",
        "assignment_groupIN" + ",".join(group_ids),
    ]
    if state_values:
        filters.append("stateNOT IN" + ",".join(state_values))

    # ServiceNow uses ^ to join conditions with AND.
    return "^".join(filters)


def fetch_priorities(client, query):
    """Return priorities such as ['1', '2', '2'] for matching incidents."""
    records = client.get_records("incident", query, fields=["priority"])
    priorities = []
    for record in records:
        priority = record.get("priority")
        if priority not in ("1", "2"):
            raise ServiceNowError("ServiceNow returned incomplete incident fields. Check read permissions.")
        priorities.append(priority)
    return priorities
