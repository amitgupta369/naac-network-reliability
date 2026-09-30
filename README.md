# Network Reliability

Nautobot dashboard with sample availability and live ServiceNow P1/P2 incidents.

## Configuration

Merge into your existing PLUGINS_CONFIG in nautobot_config.py:

```python
import os

PLUGINS_CONFIG = {
    "naac_network_reliability": {
        "servicenow": {
            "instance_url": "https://YOUR_INSTANCE.service-now.com",
            "assignment_group_ids": [
                "0123456789abcdef0123456789abcdef",  # Replace with group sys_id
            ],
            "token": os.environ.get("SERVICENOW_TOKEN", ""),
            # Alternatively omit token and configure:
            # "username": os.environ["SERVICENOW_USERNAME"],
            # "password": os.environ["SERVICENOW_PASSWORD"],
            "excluded_states": ["6", "7", "8"],
        },
    },
}
```

Use assignment-group sys_ids, not names. Multiple groups are combined into one
count. Empty/invalid groups fail configuration rather than querying all incidents.
Store credentials in the deployment environment. Bearer token provisioning and
refresh are managed externally.

Open means active=true excluding states 6 (Resolved), 7 (Closed), 8 (Canceled).
Adjust excluded_states for your instance; [] uses active-only filtering.
P1 >= 1 is High risk; P2-only is Watch; zero open P1/P2 is Good. Configuration
and API failures show Unknown. Data refreshes on dashboard load/Refresh data.
Availability remains sample data.

View in ServiceNow opens a new tab with the same incident filters. Users may need
to sign in. Use a read-only service account with visibility of all configured
groups and read access to incident sys_id and priority. ServiceNow ACLs apply;
browser users with different permissions may see different counts. Incidents
can change during pagination or before opening the link.

