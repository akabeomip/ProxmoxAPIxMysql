import requests

def getnode(proxmox_api_url, proxmox_ticket, csrf_token):
    log_url = f"{proxmox_api_url}/nodes/"
    headers = {
        'CSRFPreventionToken': csrf_token,
        'Cookie': f'PVEAuthCookie={proxmox_ticket}'
    }
    response = requests.get(log_url, headers=headers, verify=False)
    # Kiểm tra mã trạng thái response
    if response.status_code == 200:
        log_data = response.json()  # Dữ liệu log
        node = []
        #
        for info in log_data['data']:
            node.append(info['node'])                
        return node
    else:
        print(f"Yêu cầu không thành công. Mã trạng thái: {response.status_code}")

def getNodeInfomation(proxmox_api_url, proxmox_ticket, csrf_token, node):
    log_url = f"{proxmox_api_url}/nodes/"
    headers = {
        'CSRFPreventionToken': csrf_token,
        'Cookie': f'PVEAuthCookie={proxmox_ticket}'
    }
    response = requests.get(log_url, headers=headers, verify=False)
    # Kiểm tra mã trạng thái response
    if response.status_code == 200:
        log_data = response.json()
        for info in log_data['data']:
            if info['node'] == node:
                return info['status']
    #     response = requests.get(qemuInfoURL, headers=headers, verify=False)
    #     log_data = response.json()
    #     numberOfQemu = 0
    #     for qemu in log_data['data']:
    #         numberOfQemu+=1
    # else:
    #     print(f"Yêu cầu không thành công. Mã trạng thái: {response.status_code}")
