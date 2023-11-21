import requests

def getClusterInfo(proxmox_api_url, proxmox_ticket, csrf_token):
    poolListUrl = f"{proxmox_api_url}/cluster/status"
    headers = {
        'CSRFPreventionToken': csrf_token,
        'Cookie': f'PVEAuthCookie={proxmox_ticket}' 
    }
    response = requests.get(poolListUrl, headers=headers, verify=False)
    clustersInfo = {}
    if response.status_code == 200:
        log_data = response.json()  # Dữ liệu log
        for info in log_data['data']:
            if info['id'] == 'cluster':
                clustersInfo = {
                    'ClusterID': info['name'],
                    'CountNode': info['nodes']
                }
            #print(clustersInfo)
            return clustersInfo
    else:
        print(f"Yêu cầu không thành công tại bước getPoolsinfo. Mã trạng thái: {response.status_code}")
    return clustersInfo