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
            # Alternatively omit token and use OAuth client credentials:
            # "client_id": os.environ["SERVICENOW_CLIENT_ID"],
            # "client_secret": os.environ["SERVICENOW_CLIENT_SECRET"],
            # Or use basic authentication:
            # "username": os.environ["SERVICENOW_USERNAME"],
            # "password": os.environ["SERVICENOW_PASSWORD"],
            "excluded_states": ["6", "7", "8"],
        },
    },
}

# clientid 1f25f24be6c64983b51f4142ff017f69
# Client Secret JW-E*#z6N#4Eg3Kl}1bX;O4,,Y]aF3<R
```

Use assignment-group sys_ids, not names. Multiple groups are combined into one
count. Empty/invalid groups fail configuration rather than querying all incidents.
Store credentials in the deployment environment. For a manually supplied token, provisioning and
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


## OAuth client ID and client secret

Set client_id and client_secret in the servicenow configuration above, and leave
 token empty or omit it. The client POSTs form data to /oauth_token.do with
 grant_type=client_credentials, then uses the returned access token for all pages
 in that collection. A fresh token is requested on the next collection; there is
 no token persistence or automatic mid-request refresh. Authentication errors
 show Unknown on the dashboard.

Precedence: supplied token, then client credentials, then username/password.
Both client_id and client_secret are required when either is configured.
The ServiceNow OAuth application must support the client-credentials grant and
have access to the incident table and configured assignment groups. Client ID
and secret alone do not implement the authorization-code or refresh-token flows.

See the [ServiceNow client-credentials documentation](https://www.servicenow.com/docs/r/platform-security/authentication/client-credentials-grant-workflow.html).
