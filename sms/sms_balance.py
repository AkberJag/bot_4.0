import http.client
from bot_modules.config import msg_auth_key

def get_sms_balance():
    conn = http.client.HTTPSConnection("api.msg91.com")

    conn.request("GET", f"/api/balance.php?authkey={msg_auth_key}&type=4")

    res = conn.getresponse()
    data = res.read()

    return data.decode("utf-8")+'\n\n' if 'error' not in data.decode("utf-8") else 'Not available\n\n'

