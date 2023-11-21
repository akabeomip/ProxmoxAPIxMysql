import requests

def getAllStoragesName(proxmox_api_url, proxmox_ticket, csrf_token, Node):
    log_url = f"{proxmox_api_url}/nodes/{Node}/storage/"#
    headers = {
        'CSRFPreventionToken': csrf_token,
        'Cookie': f'PVEAuthCookie={proxmox_ticket}'
    }
    response = requests.get(log_url, headers=headers, verify=False)
    # Kiểm tra mã trạng thái response
    if response.status_code == 200:
        log_data = response.json()  # Dữ liệu log
        storageID = []
        #
        for info in log_data['data']:
            storageID.append(info['storage'])
        return storageID
    else:
        print(f"Yêu cầu không thành công. Mã trạng thái: {response.status_code}")

def getStoragePerNode(proxmox_api_url, proxmox_ticket, csrf_token, Node):
    log_url = f"{proxmox_api_url}/nodes/{Node}/storage/"#
    headers = {
        'CSRFPreventionToken': csrf_token,
        'Cookie': f'PVEAuthCookie={proxmox_ticket}'
    }
    response = requests.get(log_url, headers=headers, verify=False)
    # Kiểm tra mã trạng thái response
    if response.status_code == 200:
        log_data = response.json()  # Dữ liệu log
        storagePerNodeInfo = []
        #
        for info in log_data['data']:
            storagePerNodeInfo.append({
                'StorageID': info['storage'],
                'Storage Capacity (GB)': info['total']/pow(1024, 3),
                'Available Capacity (GB)': info['avail']/pow(1024, 3),
                'Type': info['type'],
                'Status': getStorageStatus(proxmox_api_url, proxmox_ticket, csrf_token, Node, info['storage']),
                'NodeID': Node
            })
        return storagePerNodeInfo
    else:
        print(f"Yêu cầu không thành công. Mã trạng thái: {response.status_code}")

def getStorage(proxmox_api_url, proxmox_ticket, csrf_token):
    log_url = f"{proxmox_api_url}/storage/"
    headers = {
        'CSRFPreventionToken': csrf_token,
        'Cookie': f'PVEAuthCookie={proxmox_ticket}'
    }
    response = requests.get(log_url, headers=headers, verify=False)
    # Kiểm tra mã trạng thái response
    if response.status_code == 200:
        log_data = response.json()  # Dữ liệu log
        storageInfo = []
        #
        for info in log_data['data']:
            storageInfo.append({
                'Digest': info['digest'],
                'Type': info['type'],
                'Storage': info['storage']
            })
        return storageInfo
    else:
        print(f"Yêu cầu không thành công. Mã trạng thái: {response.status_code}")

def getStorageInPool(proxmox_api_url, proxmox_ticket, csrf_token, pool):
    poolListUrl = f"{proxmox_api_url}/pools"
    poolDetailUrl = poolListUrl + f"/{pool}"
    headers = {
        'CSRFPreventionToken': csrf_token,
        'Cookie': f'PVEAuthCookie={proxmox_ticket}' 
    }
    poolinfo = requests.get(poolDetailUrl, headers=headers, verify=False)
    log_data = poolinfo.json()
    allStorage = getStorage(proxmox_api_url, proxmox_ticket, csrf_token)
    storageInfo = []
    for member in log_data['data']['members']:
        if member['type'] == 'storage':
            for storage in allStorage:
                if storage['Storage'] == member['storage']:
                    storageInfo.append(
                        {
                            'Pool': pool,
                            'Storage': member['storage']
                        }
                    )
    return storageInfo

def getdisk(proxmox_api_url, proxmox_ticket, csrf_token, node, id):
    diskType = ["scsi", "ide", "sata", "virtio"]
    log_url = f"{proxmox_api_url}/nodes/{node}/qemu/{id}/config"
    headers = {
        'CSRFPreventionToken': csrf_token,
        'Cookie': f'PVEAuthCookie={proxmox_ticket}' 
    }
    response = requests.get(log_url, headers=headers, verify=False)
    if response.status_code == 200:
        log_data = response.json()  # Dữ liệu log
        diskInfo = []
        for i in log_data['data']:
            for type in diskType:
                if (type in i) and (i != 'scsihw'):
                    if "size" in log_data['data'][i]:
                        startPosition = log_data['data'][i].find("size") + 5 #size=
                        endPosition = log_data['data'][i].find(":")
                        diskInfo.append({
                            'VMID': id,
                            'DiskName' : i,
                            'StorageID': log_data['data'][i][:endPosition],
                            'Capacity': log_data['data'][i][startPosition:],
                            #'Status': getStorageStatus(proxmox_api_url, proxmox_ticket, csrf_token, node, log_data['data'][i][:endPosition])
                        })
    return diskInfo

def getStorageStatus(proxmox_api_url, proxmox_ticket, csrf_token, node, storageID):
    log_url = f"{proxmox_api_url}/nodes/{node}/storage/{storageID}/status"
    headers = {
        'CSRFPreventionToken': csrf_token,
        'Cookie': f'PVEAuthCookie={proxmox_ticket}' 
    }
    response = requests.get(log_url, headers=headers, verify=False)
    if response.status_code == 200:
        log_data = response.json()
        if log_data['data']['active'] == 1:
            return 'Active'
        else:
            return 'Deactive'



#{StorageID}/status
#https://10.1.9.76:8006/api2/json/nodes/n976/storage/database/status