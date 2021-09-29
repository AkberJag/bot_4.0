from bot_modules.config import PASSWORD
from django.db.models import Q
from telebot.types import ReplyKeyboardRemove
from bot_modules.send_msg import send_warnings_to_admin
from bot_modules.jason_handler import add_to_json
from time import sleep

# from jason_handler import add_to_json


def frwrd_msg_to_users(bot, user_id, chat_id, msg_id):
    try:
        return bot.forward_message(user_id, chat_id, msg_id)
    except:
        pass


def forward_message(message, bot):
    bot.send_message(
        message.chat.id, "Enter password:", reply_markup=ReplyKeyboardRemove()
    )
    # ask for admin password
    bot.register_next_step_handler(message, ask_forward_password, bot)


# password for forwarding a message
def ask_forward_password(message, bot):
    if str(message.text) == PASSWORD:
        try:
            bot.delete_message(message.chat.id, message.message_id - 3)
            bot.delete_message(message.chat.id, message.message_id - 2)
            bot.delete_message(message.chat.id, message.message_id - 1)
            bot.delete_message(message.chat.id, message.message_id)
        except:
            pass

        bot.send_message(
            message.chat.id,
            "send a message to forward or send '/cancel' to cancel this",
        )
        bot.register_next_step_handler(message, forward_message_to_users, bot)
    else:
        bot.delete_message(message.chat.id, message.message_id)
        bot.send_message(message.chat.id, "✖ 🔑 ✖")


# forward messages to users function
def forward_message_to_users(message, bot):
    frwrd_msg_details = []
    # cancel msg forwarding
    if str(message.text).lower() == "/cancel":
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
        from db.models import User

        # select all registered users from db
        for user in User.objects.filter(~Q(telegram_id=0)).values():
            sleep(0.001)
            # forward the message
            delivery_details = frwrd_msg_to_users(
                bot, int(user["telegram_id"]), message.chat.id, message.message_id
            )

            if delivery_details is not None:
                frwrd_msg_details.append(
                    [
                        delivery_details.chat.id,
                        delivery_details.message_id,
                    ]  # save the chat id and msg id for deleting
                )
        send_warnings_to_admin(bot, "✅ വിജയകരമായി ഫോർവേഡ് ചെയ്തിരിക്കുന്നു ✅")

    # add the message and all recived users msg id and chat id
    # to delete a messsage in future.

    if message.document == None:
        if message.photo != None:
            if message.caption == None:
                add_to_json(
                    f"Forwarded message\nType: Photo\n",
                    frwrd_msg_details,
                )
            else:
                add_to_json(
                    f"Forwarded message\nType: Photo\nContent: {message.caption[:100]}...\n",
                    frwrd_msg_details,
                )
        else:
            add_to_json(
                f"Forwarded message\nContent: {message.text[:100]}...\n",
                frwrd_msg_details,
            )

    elif message.document:
        add_to_json(
            f"Forward message\nFile Name: {message.document.file_name}\n",
            frwrd_msg_details,
        )
    else:
        add_to_json(
            f"Forward message\nUnknown file type\n",
            frwrd_msg_details,
        )
