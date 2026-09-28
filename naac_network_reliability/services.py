"""Hardcoded phase 1 snapshot; external API integration will be added later."""

from datetime import datetime, timezone


class SourceError(Exception):
    """Reserved for user-facing errors from the future API integration."""


def fetch_snapshot(config):
    """Return sample devices using the dashboard's stable snapshot contract.

    ``config`` is reserved for the finalized third-party integration and is
    intentionally unused for now. No credentials or network calls are needed.
    """
    # Integration point: replace this list with devices from the finalized API.
    # Normalize each status to available, unavailable, or unknown and preserve
    # these field names so the dashboard and filters continue to work.
    devices = [
        {"id": "r1", "name": "router-01", "ip_address": "192.0.2.1", "status": "available"},
        {"id": "r2", "name": "router-02", "ip_address": "192.0.2.2", "status": "available"},
        {"id": "s1", "name": "switch-01", "ip_address": "192.0.2.3", "status": "available"},
        {"id": "s2", "name": "switch-02", "ip_address": "192.0.2.4", "status": "unavailable"},
        {"id": "f1", "name": "firewall-01", "ip_address": "192.0.2.5", "status": "unknown"},
    ]
    total = len(devices)
    available = sum(d["status"] == "available" for d in devices)
    unknown = sum(d["status"] == "unknown" for d in devices)
    return {
        "devices": devices, "total": total, "available": available,
        "unavailable": total - available - unknown, "unknown": unknown,
        "availability": round(100 * available / total, 2) if total else None,
        "fetched_at": datetime.now(timezone.utc),
    }
