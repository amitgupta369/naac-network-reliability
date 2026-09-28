from django.urls import path
from .views import DashboardView

app_name = "naac_network_reliability"
urlpatterns = [path("", DashboardView.as_view(), name="dashboard")]
