
# ---------------- Network Parameters -------------------------------------

virtual_switch = [
    ['vSwitch0', 'LAN'],
    ['vSwitch1', 'NFS'],
    ['vSwitch2', 'VMotion'],
    ['vSwitch3', 'DMZ'],
    ['vSwitch4', 'ZAN'],
    ['vSwitch5', 'Dummy'],
    ['vSwitch6', 'CUSTOMERS'],
]

zan_vswitch = 'vSwitch4'

zan_port_group = [
    [zan_vswitch, 'VLAN_OPENVPN_WAN', '9'],
    [zan_vswitch, 'VLAN_WEB_WAN', '10'],
    [zan_vswitch, 'VLAN_TEMP_WAN', '98'],
]
