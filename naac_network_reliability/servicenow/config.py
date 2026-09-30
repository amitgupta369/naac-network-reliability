"""Check the connection settings from nautobot_config.py."""

from urllib.parse import urlsplit

from .exceptions import ServiceNowError


def validate_config(config):
    """Return connection settings, or explain what needs to be configured."""
    if not isinstance(config, dict):
        raise ServiceNowError("ServiceNow configuration must be a dictionary.")

    instance_url = config.get("instance_url", "")
    if not isinstance(instance_url, str):
        raise ServiceNowError("ServiceNow instance_url must be a string.")
    instance_url = instance_url.rstrip("/")

    try:
        url = urlsplit(instance_url)
        port = url.port  # Reading this also checks whether the port is valid.
    except ValueError:
        raise ServiceNowError("Configure a valid HTTPS ServiceNow instance URL.") from None

    if url.scheme != "https" or not url.hostname:
        raise ServiceNowError("Configure a valid HTTPS ServiceNow instance URL.")
    if url.username or url.password or url.path or url.query or url.fragment:
        raise ServiceNowError("ServiceNow instance_url must contain only the HTTPS address.")

    username = config.get("username", "")
    password = config.get("password", "")
    token = config.get("token", "")
    client_id = config.get("client_id", "")
    client_secret = config.get("client_secret", "")
    for value in [username, password, token, client_id, client_secret]:
        if not isinstance(value, str):
            raise ServiceNowError("ServiceNow credentials must be strings.")

    if (client_id and not client_secret) or (client_secret and not client_id):
        raise ServiceNowError("Configure both ServiceNow client_id and client_secret.")
    if not token and not client_id and not (username and password):
        raise ServiceNowError("Configure a bearer token, OAuth client credentials, or username/password.")

    return {
        "instance_url": instance_url,
        "username": username,
        "password": password,
        "token": token,
        "client_id": client_id,
        "client_secret": client_secret,
    }
