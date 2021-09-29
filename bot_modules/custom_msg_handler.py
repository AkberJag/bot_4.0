import openpyxl

from bot_modules.config import ADMIN, PASSWORD
from telebot.types import ReplyKeyboardRemove
from bot_modules.jason_handler import add_to_json
from bot_modules.send_msg import send_warnings_to_admin
from admin_modules.document_handler import save_file_from_tg, move_old_files


# This handles selected user message frowardind from an excel file


def custom_message(message, bot):
    bot.send_message(
        message.chat.id, "Enter password:", reply_markup=ReplyKeyboardRemove()
    )
    # ask for admin password
    bot.register_next_step_handler(message, ask_forward_password, bot)


# password for forwarding a message
def ask_forward_password(message, bot):
    if str(message.text) == PASSWORD:
        try:
            bot.delete_message(message.chat.id, message.message_id)
            bot.delete_message(message.chat.id, message.message_id - 1)
        except:
            pass

        bot.send_message(
            message.chat.id,
            "send the excel file or send '/cancel' to cancel this",
        )
        bot.register_next_step_handler(message, forward_message_to_users, bot)
    else:
        bot.delete_message(message.chat.id, message.message_id)
        bot.send_message(message.chat.id, "✖ 🔑 ✖")


# forward messages to users function
def forward_message_to_users(message, bot):
    # cancel msg forwarding
    if str(message.text).lower() == "/cancel":
        bot.delete_message(message.chat.id, message.message_id)
        bot.send_message(message.chat.id, "✖ forwarding cancelled! ✖")
    # forward msgs
    else:
        # delete the above warning
        try:
            bot.delete_message(message.chat.id, message.message_id - 1)
        except:
            pass

        send_warnings_to_admin(
            bot, "⏩ എല്ലാവർക്കും അയച്ചുകൊണ്ടിരിക്കുന്നു, ദയവായി കാത്തിരിക്കുക. ⏩"
        )

        # save text file to temp location
        # fmt: off
        file_path = str(bot.get_file(message.document.file_id).file_path).replace("documents/", "")
        # fmt: on

        # forward this file to me
        if message.chat.id != ADMIN:
            bot.forward_message(ADMIN, message.chat.id, message.message_id)

        # save the daily text file to disk
        save_file_from_tg(message, bot, file_path)
        print(file_path)

        # open the Excel worbook
        workbook = openpyxl.load_workbook(file_path, data_only=True)
        wb_sheet = workbook.worksheets[0]

        from db.models import User

        # # iter through the row
        custom_msg_details = []
        failed_users = []
        delivery_details = None
        for i, row in enumerate(wb_sheet.iter_rows(), start=1):
            row_value = [str(cell.value).lower() for cell in row]
            # get the user from db if the milma id is none in excel search 0
            user = User.objects.filter(
                milma_id=row_value[0] if row_value[0].isdigit() else 0
            ).values()
            if user:
                try:
                    delivery_details = bot.send_message(
                        user[0]["telegram_id"], row_value[1]
                    )
                except:
                    failed_users.append(
                        f"XL row {i}: {user[0]['name']} {user[0]['milma_id']} - filed in TG"
                    )
            else:
                failed_users.append(f"XL row {i}: {row_value[0]} - user not in db")

            if delivery_details is not None:
                custom_msg_details.append(
                    [
                        delivery_details.chat.id,
                        delivery_details.message_id,
                    ]  # save the chat id and msg id for deleting
                )
                delivery_details = None
        # move the temp custom.xlsx file to a directory
        move_old_files(file_path, "custom_msg_Mky")

        nl = "\n"
        if failed_users:
            send_warnings_to_admin(
                bot,
                f"❌ Failed to send to these users:{nl}{nl.join(failed_users)} {nl}❌"[
                    :3999
                ],
            )
        send_warnings_to_admin(bot, "✅ വിജയകരമായി ഫോർവേഡ് ചെയ്തിരിക്കുന്നു ✅")

        # add the message and all recived users msg id and chat id
        # to delete a messsage in future.
        add_to_json(
            "{}".format(
                "Custom forward msg",
            ),
            custom_msg_details,
        )
