import json, os, traceback
from datetime import datetime, timedelta
from bot_modules.config import json_file_path


def add_to_json(file_type, json_data):

    current_time = (datetime.now() + timedelta(hours=5, minutes=30)).strftime(
        "%I:%M:%S %p %d/%m/%Y"
    )

    # check the json exist or not if not create.
    if not os.path.exists(json_file_path):
        os.makedirs(os.path.dirname(json_file_path), exist_ok=True)
        # save the data as a json file
        with open(json_file_path, "w") as json_output_file:
            json.dump(
                {
                    0: {
                        "message": file_type,
                        "time": current_time,
                        "users": json_data,
                        "is_deleted": False,
                    }
                },
                json_output_file,
            )

    # goes here if file already exists.
    else:
        with open(json_file_path) as json_file:
            json_file_data = json.load(json_file)

        # keys in json file
        json_keys = list(json_file_data.keys())
        json_keys = [int(key) for key in json_keys]
        json_keys.sort(reverse=True)

        # add new message details to the existing json
        try:
            json_file_data.update(
                {
                    int(
                        json_keys[0]
                    )  # increment current bigguest key to save next data
                    + 1: {
                        "message": file_type,
                        "time": current_time,
                        "users": json_data,
                        "is_deleted": False,
                    }
                }
            )
        except:
            print(traceback.format_exc())

        # save the updated json
        with open(json_file_path, "w") as json_output_file:
            json.dump(json_file_data, json_output_file)


def read_from_json():
    # check for the json file
    if not os.path.exists(json_file_path):
        return None
    else:
        with open(json_file_path) as json_file:
            json_file_data = json.load(json_file)
            # keys in json file
            json_keys = list(json_file_data.keys())
            json_keys = [int(key) for key in json_keys]
            json_keys.sort(reverse=True)
            delete_message = ""

            # get last 5 msg keys
            for key in json_keys[:5]:
                key = str(key)
                # if the msg is already deleted exclude it.
                if json_file_data[key]["is_deleted"] != True:
                    delete_message += f"🔴 <b>{key}</b>:\nMessage: <b>{json_file_data[key]['message']}</b>\nSend time: <b>{json_file_data[key]['time']}</b>\nNo of users: {len(json_file_data[key]['users'])}\n\n\n"

            # true - when all mesasges/no mesages to delete.
            if delete_message == "":
                return {"message": "no message to delete", "keys": None}
            else:
                json_keys = [str(key) for key in json_keys]
                return {"message": delete_message, "keys": json_keys}
