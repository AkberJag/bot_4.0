import http.client, json, time

from bot_modules.config import msg_auth_key, daily_flow_id
from bot_modules.config import dlt_te_id_weekly


def daily_sms(data, name, phone, date):
    time.sleep(0.05)
    conn = http.client.HTTPSConnection("api.msg91.com")

    payload = '"flow_id": "{dfi}",  "mobiles": "91{mobile}",  "date": "{bill_date}",  "user": "{user}",  "qty": "{qty}",  "clr": "{clr}",  "fat": "{fat}",  "snf": "{snf}",  "rs": "{rs}",  "tot": "{tot}",  "test": ""'.format(
        mobile=phone,
        user=name[:15].title(),
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

        return {"reply": json.loads(data).get("type"), "error": None}

    except Exception as e:
        return {"reply": None, "error": e}


def weekly_sms(data, user, heading, date):
    time.sleep(0.05)
    text = f"Padamughom APCOS\nWeekly Payment Report\n{date.replace('മുതൽ', 'to').replace('വരെ','')}\n{user[0].get('name').title()} ({user[0].get('milma_id')})\n"

    for enum in range(len(heading[2:])):
        text += f"{str(heading[enum+2]).title()}: "
        text += (
            f"{data[enum+2]:.2f}\n"
            if type(data[enum + 2]) == float
            else f"{data[enum+2]}\n"
        )

    conn = http.client.HTTPConnection("api.msg91.com")

    headers = {
        "authkey": msg_auth_key,
        "content-type": "application/json",
    }
    payload = (
        '{ "sender": "PDMUGM", "route": "4", "DLT_TE_ID": "'
        + dlt_te_id_weekly
        + '","country": "91", "sms": [ { "message": "'
        + text.replace("\n", "\\n")
        .replace("Balance", "BALANCE")
        .replace("Amount", "Amt")
        + '", "to": [ "'
        + f'91{user[0].get("phone").title()}'
        + '"] } ] }'
    )
    # sending the connection request
    conn.request("POST", "/api/v2/sendsms", payload, headers)

    res = conn.getresponse()
    response_status = res.read()

    return {"reply": json.loads(response_status.decode("utf-8")).get("type")}


# todo here.
# get the response from msg9 and if it is not success send admin the details
