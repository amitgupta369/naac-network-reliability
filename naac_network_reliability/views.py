from django.conf import settings
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import TemplateView

from .services import SourceError, fetch_snapshot
from .incidents import fetch_incident_summary
from .servicenow.exceptions import ServiceNowError


class DashboardView(LoginRequiredMixin, TemplateView):
    """Show reliability summary cards to logged-in users."""

    template_name = "naac_network_reliability/dashboard.html"

    def get_context_data(self, **kwargs):
        """Load the snapshot and pass it to the dashboard template."""
        context = super().get_context_data(**kwargs)

        # Source settings are reserved for the future API integration.
        app_config = settings.PLUGINS_CONFIG.get("naac_network_reliability", {})
        source_config = app_config.get("source", {})

        try:
            context["snapshot"] = fetch_snapshot(source_config)
        except SourceError as error:
            context["source_error"] = str(error)

        try:
            context["incidents"] = fetch_incident_summary(app_config.get("servicenow", {}))
        except ServiceNowError as error:
            context["incident_error"] = str(error)

        return context
