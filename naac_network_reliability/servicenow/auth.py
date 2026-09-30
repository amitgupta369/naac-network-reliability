"""Set up bearer-token, OAuth client-credentials, or basic authentication."""

import requests

from .exceptions import ServiceNowError


def authenticate(session, config):
    """Choose token first, then OAuth client credentials, then basic auth."""
    if config["token"]:
        session.headers["Authorization"] = "Bearer " + config["token"]
    elif config["client_id"]:
        token = get_access_token(session, config)
        session.headers["Authorization"] = "Bearer " + token
    else:
        session.auth = (config["username"], config["password"])


def get_access_token(session, config):
    """Exchange client credentials for one access token per collection."""
    token_url = config["instance_url"] + "/oauth_token.do"
    form = {
        "grant_type": "client_credentials",
        "client_id": config["client_id"],
        "client_secret": config["client_secret"],
    }
    try:
        response = session.post(
            token_url,
            data=form,
            timeout=(5, 15),
            allow_redirects=False,
        )
        response.raise_for_status()
        if response.status_code != 200:
            raise ServiceNowError("ServiceNow OAuth returned an unexpected response.")
        payload = response.json()
    except (requests.RequestException, ValueError):
        raise ServiceNowError(
            "ServiceNow OAuth failed. Check client credentials and client-credentials grant configuration."
        ) from None

    if not isinstance(payload, dict):
        raise ServiceNowError("ServiceNow OAuth returned an invalid token response.")
    token = payload.get("access_token")
    token_type = payload.get("token_type", "Bearer")
    if not isinstance(token, str) or not token.strip() or "\r" in token or "\n" in token:
        raise ServiceNowError("ServiceNow OAuth did not return a valid access token.")
    if not isinstance(token_type, str) or token_type.lower() != "bearer":
        raise ServiceNowError("ServiceNow OAuth returned an unsupported token type.")
    return token
