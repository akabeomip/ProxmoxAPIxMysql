import getVMs, postAuthentication, getNodes, getPools, getStorage, getCluster
import _mysql, _save, _compare
from datetime import datetime


proxmox_clusters_api_url = [
    'https://10.1.9.76:8006/api2/json', 
    'https://10.1.9.133:8006/api2/json'
    ]

# Thực hiện xác thực với Proxmox API (nếu cần)
username = 'root@pam'
password = 'proxmox'
proxmox_ticket = None
csrf_token = None
poolinfo = None
now = round(datetime.now().timestamp())
for cluster in proxmox_clusters_api_url:
    proxmox_ticket, csrf_token = postAuthentication.authenticate(cluster, username, password)

    clusterInfo = getCluster.getClusterInfo(cluster, proxmox_ticket, csrf_token)

    #lấy bản VMs
    nodes = []
    nodes = getNodes.getnode(cluster, proxmox_ticket, csrf_token)
    nodeInfo = []
    disk = []
    diskInfoTheoVMID = []
    for node in nodes:
        #Bảng Node
        vmid = getVMs.getvmid(cluster, proxmox_ticket, csrf_token, node)
        #Bảng Storage
        StorageInfo = getStorage.getStoragePerNode(cluster, proxmox_ticket, csrf_token, node)
        nodeInfo.append({
            'NodeID': node,
            'CountVMs': len(vmid),
            'CountStorages': len(StorageInfo),
            'ClusterID': clusterInfo['ClusterID'],
            'Status': getNodes.getNodeInfomation(cluster, proxmox_ticket, csrf_token, node)
        })
        VMs = {}
        numbersOfVMs = 0
        for id in vmid:
            #Bảng VM
            VMs[numbersOfVMs] = {
                "VMID": int(id),
                "PoolID": getVMs.getpool(cluster, proxmox_ticket, csrf_token, id),
                "NodeID": f"{node}",
                "Hostname": getVMs.gethostname(cluster, proxmox_ticket, csrf_token, node, id),
                "IP": getVMs.getip(cluster, proxmox_ticket, csrf_token, node, id),
                "NumberOfDisks": getVMs.getdisk(cluster, proxmox_ticket, csrf_token, node, id),
            }
            VMs[numbersOfVMs].update(getVMs.getosinfo(cluster, proxmox_ticket, csrf_token, node, id))
            VMs[numbersOfVMs].update(getVMs.getstatus(cluster, proxmox_ticket, csrf_token, node, id))
            #Bảng DISK
            diskInfoTheoVMID.append(getStorage.getdisk(cluster, proxmox_ticket, csrf_token, node, id))
            numbersOfVMs+=1
        #get Node infomations
        #nodeInfo[len(nodeInfo) - 1].update(getNodes.getNodeInfomation(cluster, proxmox_ticket, csrf_token, node))
        
    # lấy bảng Pools 
    Pool = getPools.getPoolsinfo(cluster, proxmox_ticket, csrf_token)
    Pools = {}
    i = 0
    #Storage = getStorage.getStorage(proxmox_api_url, proxmox_ticket, csrf_token)
    for p in Pool:
        Pools[i] = {
            "PoolID": p,
        }
        Pools[i].update(getPools.getNumberOfPlugins(cluster, proxmox_ticket, csrf_token, p))
        #Pools[i].update(getStorage.getStorageInPool(cluster, proxmox_ticket, csrf_token, p))
        i+=1

    # with open('U:\MWG\\api\\clusters.json', 'w') as f:
    #     json.dump(clusterInfo, f)
    # with open('U:\MWG\\api\\pools.json', 'w') as f:
    #     json.dump(Pools, f)
    # with open('U:\MWG\\api\\nodes.json', 'w') as f:
    #     json.dump(nodeInfo, f)
    # with open('U:\MWG\\api\\storages.json', 'w') as f:
    #     json.dump(StorageInfo, f)
    # with open('U:\MWG\\api\\vms.json', 'w') as f:
    #     json.dump(VMs, f)
    # with open('U:\MWG\\api\\disks.json', 'w') as f:
    #     json.dump(diskInfoTheoVMID, f)

    OLD = {
        'host': '10.1.9.200',
        'user': 'lechidai',
        'password': 'Admin@123',
        'database': 'proxmoxapi'
    }

    NEW = {
        'host': '10.1.9.200',
        'user': 'lechidai',
        'password': 'Admin@123',
        'database': 'proxmoxapinew'
    }

    _compare.compare_databases(NEW, OLD)
    
    _save.jsonSave('clusters', clusterInfo, now)
    _save.jsonSave('pools', Pools, now)
    _save.jsonSave('nodes', nodeInfo, now)
    _save.jsonSave('storages', StorageInfo, now)
    _save.jsonSave('vms', VMs, now)
    _save.jsonSave('disks', diskInfoTheoVMID, now)

    print(clusterInfo, end='\n\n')
    _mysql.Clusters(clusterInfo)

    for j in range(i):
        print(Pools[j], end='\n\n')
        _mysql.Pools(Pools[j])

    for node in nodeInfo:
        print(node, end='\n\n')
        _mysql.Nodes(node)
    
    for Storage in StorageInfo:
        print(Storage, end='\n\n')
        _mysql.Storages(Storage)

    for VM in VMs:
        print(VMs[VM], end='\n\n')
        _mysql.VMs(VMs[VM])
    
    for j in diskInfoTheoVMID:
        for k in j:
            print(k, end='\n\n')
            _mysql.Disks(k)

