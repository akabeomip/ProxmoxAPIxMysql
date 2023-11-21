import requests

def getPoolsinfo (proxmox_api_url, proxmox_ticket, csrf_token):
    poolListUrl = f"{proxmox_api_url}/pools"
    headers = {
        'CSRFPreventionToken': csrf_token,
        'Cookie': f'PVEAuthCookie={proxmox_ticket}' 
    }
    response = requests.get(poolListUrl, headers=headers, verify=False)
    pools = []
    if response.status_code == 200:
        log_data = response.json()  # Dữ liệu log
        for pool in log_data['data']:
            pools.append(pool['poolid'])
    else:
        print(f"Yêu cầu không thành công tại bước getPoolsinfo. Mã trạng thái: {response.status_code}")
    return pools

def getNumberOfPlugins(proxmox_api_url, proxmox_ticket, csrf_token, pool):
    poolListUrl = f"{proxmox_api_url}/pools"
    poolDetailUrl = poolListUrl + f"/{pool}"
    headers = {
        'CSRFPreventionToken': csrf_token,
        'Cookie': f'PVEAuthCookie={proxmox_ticket}' 
    }
    poolinfo = requests.get(poolDetailUrl, headers=headers, verify=False)
    log_data = poolinfo.json()
    NumberOfVMs = 0
    NumberOfStorages = 0
    #còn thì thêm vào đây
    for member in log_data['data']['members']:
        if member['type'] == 'qemu':
            NumberOfVMs+=1
        else:
            if member['type'] == 'storage':
                NumberOfStorages+=1
    return {
        "NumberOfVMs": NumberOfVMs, 
        "NumberOfStorages": NumberOfStorages
    }


