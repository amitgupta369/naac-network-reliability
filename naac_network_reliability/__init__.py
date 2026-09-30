from nautobot.apps import NautobotAppConfig

class NetworkReliabilityConfig(NautobotAppConfig):
    name = "naac_network_reliability"
    verbose_name = "Network Reliability"
    version = "0.1.0"
    description = "Near-real-time operational metrics from external tools"
    base_url = "network-reliability"
    min_version = "3.1.0"
    max_version = "3.1.999"
    default_settings = {"source": {}, "servicenow": {}}

config = NetworkReliabilityConfig
