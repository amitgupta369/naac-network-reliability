from nautobot.apps.ui import NavMenuGroup, NavMenuItem, NavMenuTab

menu_items = (
    NavMenuTab(name="Network Reliability", groups=(
        NavMenuGroup(name="NAAC", items=(
            NavMenuItem(link="plugins:naac_network_reliability:dashboard", name="Dashboard"),
        )),
    )),
)
