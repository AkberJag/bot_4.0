import http.client, json

from bot_modules.config import msg_auth_key, daily_flow_id


def daily_sms(data, name, phone, date):

    conn = http.client.HTTPSConnection("api.msg91.com")

    payload = '"flow_id": "{dfi}",  "mobiles": "91{mobile}",  "date": "{bill_date}",  "user": "{user}",  "qty": "{qty}",  "clr": "{clr}",  "fat": "{fat}",  "snf": "{snf}",  "rs": "{rs}",  "tot": "{tot}",  "test": ""'.format(
        mobile=phone,
        user=name,
        dfi=daily_flow_id,
        bill_date=date,
        qty=data[2],
        clr=data[4],
        fat=data[3],
        snf=data[5],
        rs=data[6],
        tot=data[7],
    )

    headers = {
        "authkey": msg_auth_key,
        "content-type": "application/JSON",
    }

    try:
        conn.request("POST", "/api/v5/flow/", "{" + f"{payload}" + "}", headers)

        res = conn.getresponse()
        data = res.read().decode("utf-8")

        return {"reply": json.loads(data).get('type'),"error": None}
    
    except Exception as e:
        return {"reply": None, "error": e}


# todo here.
# get the response from msg9 and if it is not success send admin the details
