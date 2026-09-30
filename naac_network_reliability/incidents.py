"""Count open incidents and choose the dashboard risk label."""

from datetime import datetime, timezone

from .servicenow.client import ServiceNowClient
from .servicenow.config import validate_config
from .servicenow.incidents import build_incident_query, fetch_priorities


def summarize_priorities(priorities):
    """One or more P1 incidents always means high risk."""
    p1_count = priorities.count("1")
    p2_count = priorities.count("2")

    if p1_count >= 1:
        risk = "high"
        risk_label = "High risk"
    elif p2_count >= 1:
        risk = "watch"
        risk_label = "Watch"
    else:
        risk = "good"
        risk_label = "Good"

    return {
        "p1": p1_count,
        "p2": p2_count,
        "total": p1_count + p2_count,
        "risk": risk,
        "risk_label": risk_label,
    }


def fetch_incident_summary(config):
    """Load ServiceNow incidents and prepare the dashboard card."""
    connection = validate_config(config)
    query = build_incident_query(config)
    client = ServiceNowClient(connection)

    priorities = fetch_priorities(client, query)
    summary = summarize_priorities(priorities)
    summary["list_url"] = client.list_url("incident", query)
    summary["fetched_at"] = datetime.now(timezone.utc)
    return summary
