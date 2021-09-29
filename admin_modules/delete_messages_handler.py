import json
import os

from telebot.types import ReplyKeyboardRemove

from milk_bot import is_deleting
from bot_modules.jason_handler import read_from_json
from bot_modules.config import ADMINS, json_file_path
from bot_modules.send_msg import send_warnings_to_admin


def delete_messages(bot, message):
    global is_deleting
    bot.delete_message(message.chat.id, message.message_id)
    if message.chat.id in ADMINS:
        if is_deleting == False:
            is_deleting == True
            json_data = read_from_json()
            # wait for the msg nuber and delete that section msg
            if json_data is not None:
                # keys are none is no message is there to delete.
                if json_data["keys"] is not None:
                    bot.send_message(
                        message.chat.id, json_data["message"], parse_mode="HTML"
                    )
                    bot.register_next_step_handler(
                        message, delete_message_and_json, bot, json_data["keys"][:5]
                    )
                else:
                    for admin in ADMINS:
                        bot.send_message(
                            admin,
                            "❗ ഡിലീറ്റ് ചെയ്യാൻ ഒന്നും ബാക്കി ഇല്ല ❗",
                            reply_markup=ReplyKeyboardRemove(),
                        )

            # json file is missing
            else:
                for admin in ADMINS:
                    bot.send_message(
                        admin,
                        "❗ <b>മെസ്സേജുകൾ ഒന്നും ഡിലീറ്റ് ചെയ്യാൻ ഇപ്പോൾ സാധ്യമല്ല\nഅൽപ്പ സമയത്തിനു ശേഷം ശ്രമിക്കുക</b> ❗\njson missing",
                        reply_markup=ReplyKeyboardRemove(),
                        parse_mode="HTML",
                    )

            is_deleting = False

        else:
            # if the bot is sending msg
            # ask admin to wait
            bot.send_message(
                message.chat.id,
                "❗ അൽപ്പ സമയത്തിനു ശേഷം ശ്രമിക്കുക ❗",
                reply_markup=ReplyKeyboardRemove(),
            )


def delete_message_and_json(message, bot, json_keys):
    # check the selected key (sended as msg) is in the json (json_keys)
    # if yes continue.
    if str(message.text) in json_keys:
        if not os.path.exists(json_file_path):
            return None
        else:
            with open(json_file_path) as json_file:
                json_file_data = json.load(json_file)

                # delete the options msg and
                # the option selected.
                try:
                    bot.delete_message(message.chat.id, message.message_id)
                    bot.delete_message(message.chat.id, message.message_id - 1)
                except:
                    pass

                # send confirmation to the admin
                for admin in ADMINS:
                    bot.send_message(
                        admin,
                        f"deleting\n❌ <b>{json_file_data[str(message.text)]['message']}\nsend time: {json_file_data[str(message.text)]['time']}</b> ❌",
                        parse_mode="HTML",
                    )

                for user in json_file_data[str(message.text)]["users"]:
                    try:
                        bot.delete_message(
                            user[0],  # user id
                            user[1],  # msg id
                        )
                    except:
                        pass

                # set the is deleted feild to true
                # then update the json
                json_file_data[str(message.text)]["is_deleted"] = True
                with open(json_file_path, "w") as outfile:
                    json.dump(json_file_data, outfile)

                # warn admin after deleting msg
                send_warnings_to_admin(bot, "✅ വിജയകരമായി ഡിലീറ്റ് ചെയ്തിരിക്കുന്നു ✅")

    # if the selected key is not available to delete
    # send a warning
    else:
        # delete the options msg and
        # the option selected.
        try:
            bot.delete_message(message.chat.id, message.message_id)
            bot.delete_message(message.chat.id, message.message_id - 1)
        except:
            pass

        # send warning to admin
        bot.send_message(
            message.chat.id,
            "⚠<b>ആ മെസ്സേജ് ഡിലീറ്റ് ചെയുവാൻ സാധ്യമല്ല, വീണ്ടും ശ്രമിക്കു</b>⚠",
            reply_markup=ReplyKeyboardRemove(),
            parse_mode="HTML",
        )
