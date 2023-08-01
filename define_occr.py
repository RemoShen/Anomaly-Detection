from colorsys import hsv_to_rgb
from xmlrpc.client import ProtocolError


sim_ipv4 = r'\d+.\d+.\d+.\d+(/\d+)?'
sim_ipv6 = r'([a-fA-F0-9]{1,4}(:[a-fA-F0-9]{1,4}){7}|[a-fA-F0-9]{1,4}(:[a-fA-F0-9]{1,4}){0,7}::[a-fA-F0-9]{0,4}(:[a-fA-F0-9]{1,4}){0,7}(/\d+)?)'
port = r'\(?\d{2,7}:\d{1,7}(:\d+)?\)?'
para = ['#', '!', '$']
ot_tfc = ['#', '!', '$', ',', '\n']
setting_name = ['中兴', '华三', '华为', '思科', '烽火']
zx_par = ['!<mim>', '!<system-config>', '!<nsr-config>', '$', '!<tunnel-policy>', '!</mim>']
hs_par = ['display current-configuration', '#']
hw_par =['#']
sk_fh_par = ['!']
other_par = ['#', '!', '$'] 

list_port_after = ['export','import','rd','permit rt','rt','community name','vpn-target','route-distinguisher','apply community']

list_port_before = ['export-extcommunity','import-extcommunity']
list_port_ip4 = ['router-id','ipv4','lsr-id','udp-domain','tunnel-bfd','unicast-server','tunnel-bfd','peer-public-key','peer-ip','host','boot-server','default-gateway','adjacency','prefix-sid']
    # list_port_ip6 = ['rt']
lei_ip = ['net','network-entity','area']
ip_together = ['ip-address','address','neighbor','source-ip','peer','aggregate','network','permit','SmartMAN_SSH_TELNET','network','aggregate-address','route','prefix','server-address','destination']
ip4_ed = ['unicast','interface','point-to-point','default','LoopBack0','end','index','ipv4','prefix-list','loopback0','vrf','ipv6','SmartMAN_NSM_SNMP','SmartMAN_SSH_TELNET','lpuport','loopback1','prefix-name','enable','SSH_WG','ssh','default-ip','for_login','for_snmp','recursive-lookup','SSH','SmartMAN_SSH','SmartMAN_SNMP','default-ip','address','source','snmp-acl','snmp','telnet','server','port','peer','access-list','host','unreachables','Loopback0','changes','unnumbered','huawei','SNMP_ACL']
ip6_ed = ['ip','port','ipv4','node','prefix-list','hold-max-cost','MAR_01','MAR_02','MCR','based','be','rt','udp-domain','all','all-loopback','source','number','MER','hold-max-cost','auto','unnumbered','point-to-point','vpn-instance','any','vrf','MER-M','MER-S','dhcp-alloc','RingISIS1','TJBC-SM-R17','TJBC-SM-R4','TJBCXD-XIAGUA-1','TJBCXD-XIAGUA-2','TJBCXD-XIAGUA-3','ipv6','next-hop','tcp','recursive-lookup','R8-r1','R8-r2','R8-r3','R8-r4','R8-r5','R8-r6','R8-r7','R8-r8','MAR-MER-9','prefix-listSmartMAN_SNMP_IN','advance','inbound','ipv4-prefix','ipv6-prefix','prefix','MAR','MAR_1','MAR_2','MAR_001','MAR_002','MAR_003','MAR_004','MARRing1','MARRing2','MARRing3','acl','MAR-MER-4','MAR-001','MAR-002','MAR-003','MAR-003','basic','rt-trans','RingISIS2','MARRingISIS1','MAR_03','MAR_04','MAR-005','MAR-006','ntp_acl','transport-method','in','changes','address','ISIS1001','ISIS1002','ISIS1003','ISIS1004','ISIS1005','ISIS1006','ISIS1007','ISIS1008','ISIS1009','ISIS1010','MAR_25','IR51AR01','IR51AR02','IR51AR03','IR51AR04','IR51AR05','IR51AR06','IR51AR07','IR51AR08','IR51AR09','IR51AR1','IR51AR10','IR51AR11','IR51AR12','IR51AR16','IR52AR16','RingISIS3','RingISIS4','RingISIS5','RingISIS6','RingISIS7','RingISIS8','RingISIS9','RingISIS3','icmp','DX-IPRAN-V6','udp','MAR_05','MAR_06','MAR_07','MAR_08','MAR_19','DX-IPRAN-ER-V6','MAR-004','ER']
punkt_list = r",.?\"'!()/\\-<>:@#$%^&*~"
ptnum = 'pt.csv'
vfnum = 'vflist.csv'
vsnum = 'vslist.csv'