import requests

def authenticate(proxmox_api_url, username, password):
    #luu bien global
    #global proxmox_ticket, csrf_token
    proxmox_ticket = None
    csrf_token = None
    login_url = f"{proxmox_api_url}/access/ticket"
    data = {
        'username': username,
        'password': password
    }
    response = requests.post(login_url, data=data, verify=False)
    response_json = response.json()
    proxmox_ticket = response_json.get('data', {}).get('ticket')
    csrf_token = response_json.get('data', {}).get('CSRFPreventionToken')
    if not proxmox_ticket or not csrf_token:
        raise Exception('Failed to authenticate with Proxmox API')
    return proxmox_ticket, csrf_token