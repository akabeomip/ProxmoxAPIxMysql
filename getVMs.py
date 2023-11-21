import requests
import time
import postAuthentication
import getNodes

def convert_seconds(seconds):
    time_struct = time.gmtime(seconds)
    time_string = time.strftime("%H:%M:%S", time_struct)
    return time_string

# Gửi yêu cầu GET /api2/json/cluster/log
def getvmid(proxmox_api_url, proxmox_ticket, csrf_token, node):
    log_url = f"{proxmox_api_url}/nodes/{node}/qemu"
    headers = {
        'CSRFPreventionToken': csrf_token,
        'Cookie': f'PVEAuthCookie={proxmox_ticket}' 
    }
    response = requests.get(log_url, headers=headers, verify=False)
    if response.status_code == 200:
        vmid = []
        log_data = response.json()  # Dữ liệu log
        for i in log_data['data']:
            vmid.append(i['vmid'])
        return vmid
    else:
        print(f"Yêu cầu không thành công. Mã trạng thái: {response.status_code}")

def gethostname(proxmox_api_url, proxmox_ticket, csrf_token, node, id):
    hostname = ''
    log_url = f"{proxmox_api_url}/nodes/{node}/qemu/{id}/agent/get-host-name"
    headers = {
        'CSRFPreventionToken': csrf_token,
        'Cookie': f'PVEAuthCookie={proxmox_ticket}' 
    }
    response = requests.get(log_url, headers=headers, verify=False)
    if response.status_code == 200:
        log_data = response.json()  # Dữ liệu log
        hostname = log_data['data']['result']['host-name']
        return hostname
    else:
        print(f"Yêu cầu không thành công. Mã trạng thái: {response.status_code}")

def getip(proxmox_api_url, proxmox_ticket, csrf_token, node, id):
    ip = []
    log_url = f"{proxmox_api_url}/nodes/{node}/qemu/{id}/agent/network-get-interfaces"
    headers = {
        'CSRFPreventionToken': csrf_token,
        'Cookie': f'PVEAuthCookie={proxmox_ticket}' 
    }
    response = requests.get(log_url, headers=headers, verify=False)
    if response.status_code == 200:
        log_data = response.json()  # Dữ liệu log
        none = log_data.get('data').get('result')
        for i in none:
            if 'ip-addresses' in i:
                for j in i['ip-addresses']:
                    if (j['ip-address'] != "::1") and (j['ip-address'] != "127.0.0.1"):
                        ip.append(j['ip-address'])
        return ip
    else:
        print(f"Yêu cầu không thành công. Mã trạng thái: {response.status_code}")

def getosinfo(proxmox_api_url, proxmox_ticket, csrf_token, node, id):
    osname= ''
    osversion = ''
    log_url = f"{proxmox_api_url}/nodes/{node}/qemu/{id}/agent/get-osinfo"
    headers = {
        'CSRFPreventionToken': csrf_token,
        'Cookie': f'PVEAuthCookie={proxmox_ticket}' 
    }
    response = requests.get(log_url, headers=headers, verify=False)
    if response.status_code == 200:
        log_data = response.json()  # Dữ liệu log
        osname = log_data['data']['result']['name']
        osversion = log_data['data']['result']['version']
        return {
            "OSName": osname,
            "Version": osversion
        }
    else:
        print(f"Yêu cầu không thành công tại bước getosinfo. ID: {id}. Mã trạng thái: {response.status_code}")
        return {
            "OSName": 'dontknow',
            "Version": 'dontknow'
        }

def getstatus(proxmox_api_url, proxmox_ticket, csrf_token, node, id):
    log_url = f"{proxmox_api_url}/nodes/{node}/qemu/{id}/status/current"
    headers = {
        'CSRFPreventionToken': csrf_token,
        'Cookie': f'PVEAuthCookie={proxmox_ticket}' 
    }
    response = requests.get(log_url, headers=headers, verify=False)
    if response.status_code == 200:
        log_data = response.json()  # Dữ liệu log
        vmStatus = log_data['data']['status']
        cpus = log_data['data']['cpus']
        maxdisk = float(log_data['data']['maxdisk'])/pow(1024, 3)
        maxmem = float(log_data['data']['maxmem'])/pow(1024, 3)
        #uptime = convert_seconds(log_data['data']['uptime'])
        return {
            'Status': vmStatus,
            'CPUs': cpus,
            'DiskMemory(GB)': maxdisk,
            'RAM(GB)': maxmem,
            #'Uptime': uptime,
        }
    else:
        print(f"Yêu cầu không thành công tại bước getstatus. ID: {id}. Mã trạng thái: {response.status_code}")

def getdisk(proxmox_api_url, proxmox_ticket, csrf_token, node, id):
    diskType = ["scsi", "sata", "virtio"]
    #không có ide vì chỉ nêu hard disk
    log_url = f"{proxmox_api_url}/nodes/{node}/qemu/{id}/config"
    headers = {
        'CSRFPreventionToken': csrf_token,
        'Cookie': f'PVEAuthCookie={proxmox_ticket}' 
    }
    count = 0
    response = requests.get(log_url, headers=headers, verify=False)
    if response.status_code == 200:
        log_data = response.json()  # Dữ liệu log
#        disk = log_data['data']['agent']
        for i in log_data['data']:
            for type in diskType:
                if (type in i) and (i != 'scsihw'):
                    if "size" in log_data['data'][i]:
                        count += 1
    return count

def getpool(proxmox_api_url, proxmox_ticket, csrf_token, id=None):
    poolListUrl = f"{proxmox_api_url}/pools"
    id = f"qemu/{id}"
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
        print(f"Yêu cầu không thành công tại bước getpool. Mã trạng thái: {response.status_code}")
    if id == None:
        return pools
    for pool in pools:
        poolDetailUrl = poolListUrl + f"/{pool}"
        poolinfo = requests.get(poolDetailUrl, headers=headers, verify=False)
        log_data = poolinfo.json()
        for member in log_data['data']['members']:
            if member['id'] == id:
                return pool