import getVMs, postAuthentication, getNodes, getPools, getStorage, getCluster
from datetime import datetime
import _compare

proxmox_api_url = 'https://10.1.9.76:8006/api2/json'

# Thực hiện xác thực với Proxmox API (nếu cần)
username = 'root@pam'
password = 'proxmox'
proxmox_ticket = None
csrf_token = None
poolinfo = None

proxmox_ticket, csrf_token = postAuthentication.authenticate(proxmox_api_url, username, password)

#getCluster.getClusterInfo(proxmox_api_url, proxmox_ticket, csrf_token)
# getNodes.getNodeInfomation(proxmox_api_url, proxmox_ticket, csrf_token, 'n976')
# vmid = getVMs.getvmid(proxmox_api_url, proxmox_ticket, csrf_token, 'n976')
# for id in vmid:
#     print(getVMs.getip(proxmox_api_url, proxmox_ticket, csrf_token, 'n976', id))

# print(getVMs.getdisk(proxmox_api_url, proxmox_ticket, csrf_token, 'n976', 100))


connection1 = {
        'host': '10.1.9.200',
        'user': 'lechidai',
        'password': 'Admin@123',
        'database': 'proxmoxapi'
    }

connection2 = {
        'host': '10.1.9.200',
        'user': 'lechidai',
        'password': 'Admin@123',
        'database': 'proxmoxapinew'
    }
#_compare.copy_tables(connection2, connection1, "Clusters", "Clusters")
_compare.compare_databases(connection1, connection2)