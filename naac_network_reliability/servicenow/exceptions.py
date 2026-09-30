"""Errors that can safely be shown on the dashboard."""


class ServiceNowError(Exception):
    """Use a helpful message without credentials or API response bodies."""
