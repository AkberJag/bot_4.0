##########################
# Django specific settings
##########################
import os 
from user_modules.old_bills_handler import get_old_bills

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "settings")
import django

django.setup()
from db.models import User

#####################
# django settings end
#####################

import telebot
import traceback
import pprint
import requests

from time import sleep
from django.db.models import Q
from admin_modules import document_handler
from telebot.types import ReplyKeyboardRemove
from bot_modules.warning_msgs import bot_start
from bot_modules import warning_msgs, send_msg, config
from bot_modules.forward_handler import forward_message
from bot_modules.custom_msg_handler import custom_message
from admin_modules.user_operations_handler import user_operations
from bot_modules.bot_keyboards import add_contect_reqst_keyboard, add_help_keyboard
from sms.sms_balance import get_sms_balance

from bot_modules.config import (
    ADMINS,
    TOKEN,
    ADMIN,
    update_date,
    MILMA_NAME,
    MILMA_SEC,
    bot_version,
    msg_auth_key,
)

# start bot instance
bot = telebot.TeleBot(TOKEN)

# delete any active webhook
bot.delete_webhook()

# to keep track of the current users using the bot.
current_users = dict()
is_deleting = False

################################
# start: Start and register user
################################
@bot.message_handler(commands=["start", "Start"])
def send_welcome(message):
    global current_users

    # if existing user used start
    user_details_from_db = User.objects.filter(
        telegram_id=str(message.chat.id)
    ).values()

    if user_details_from_db:
        bot.send_message(
            message.chat.id,
            warning_msgs.user_already_exist_msg.format(
                name=user_details_from_db[0]["name"],
                milma_id=user_details_from_db[0]["milma_id"],
                phone=user_details_from_db[0]["phone"],
            ),
            parse_mode="HTML",
            reply_markup=ReplyKeyboardRemove(),
        )
        # delete /start.
        bot.delete_message(message.chat.id, message.message_id)

    # if sender is admin
    elif message.chat.id in ADMINS:
        bot.send_message(
            message.chat.id,
            "🤖 <b>BOT IS ALIVE!</b> 🤖",
            reply_markup=ReplyKeyboardRemove(),
            parse_mode="HTML",
        )

    else:
        # check if this user new add them to the list
        if not current_users.get(message.chat.id):
            current_users[message.chat.id] = {
                "phone_number": "",
                "number_of_tries": 3,
            }

        # add a inline keyboard to ask user's contact
        add_contect_reqst_keyboard(bot, message)
        bot.register_next_step_handler(message, validate_contact, bot)


# check the contact file sent by user.
def validate_contact(message, bot):
    if message.content_type == "contact":
        phone_number = str(message.contact.phone_number).replace("+", "")[-10:]

        # check the phone number has 10 digits.
        # if it is lesser or greater than 10 -->
        if len(phone_number) != 10:
            bot.send_message(
                message.chat.id,
                warning_msgs.less_than_digit_phone_no,
                parse_mode="HTML",
                reply_markup=ReplyKeyboardRemove(),
            )

            # send this warning to admin
            send_msg.send_warnings_to_admin(
                bot,
                message=warning_msgs.less_than_digit_phone_no_admin.format(
                    phone_number
                ),
            )

        # if phone number has 10 digits
        else:
            # check this phone number is non registered users list.
            # only non registered users will get to here, reg users will be warned before and they wont reach here

            # save the phone number send by the user to cuncurrent list
            current_users[message.from_user.id]["phone_number"] = phone_number

            # get the user with the phone number from DB
            search_for_user = User.objects.filter(phone=phone_number).values()

            # if the phone number is found on db:
            # ask for password and proceed further.
            if search_for_user:
                current_users[message.from_user.id]["user_data_from_db"] = list(
                    search_for_user
                )

                bot.send_message(
                    message.chat.id,
                    warning_msgs.ask_user_password_msg,
                    reply_markup=ReplyKeyboardRemove(),
                )
                bot.register_next_step_handler(message, ask_user_password, bot)

            # if user not in the db
            else:
                try:
                    bot.delete_message(message.chat.id, message.message_id - 1)
                    bot.delete_message(message.chat.id, message.message_id)
                except:
                    pass
                bot.send_message(
                    message.chat.id,
                    warning_msgs.number_not_in_excel,
                    parse_mode="HTML",
                    reply_markup=ReplyKeyboardRemove(),
                )
                # send this warning to admin
                message_to_admin = warning_msgs.number_not_in_excel_admin.format(
                    message.chat.id, phone=phone_number
                )
                send_msg.send_warnings_to_admin(
                    bot,
                    message_to_admin,
                )

                # remove the user from current users list whose registration is successful
                try:
                    current_users.pop(message.from_user.id)
                except:
                    pass

    # if the file sent by the user is not a contact file
    # ask them the send the contact again. recursively 🔥
    else:
        try:
            bot.delete_message(message.chat.id, message.message_id)
            bot.delete_message(message.chat.id, message.message_id - 1)
        except:
            pass
        bot.send_message(message.chat.id, "വീണ്ടും ശ്രമിക്കുക")
        sleep(2)

        # add keyboard button
        add_contect_reqst_keyboard(bot, message)
        # ask for the contact, again!

        bot.register_next_step_handler(message, validate_contact, bot)


def ask_user_password(message, bot):
    global current_users
    # check password from user and match it with the password in db
    # if matched register userid to excel file.
    if current_users[message.chat.id]["user_data_from_db"][0]["pword"] == str(
        message.text
    ):
        # delete previous messages:
        # shared contact
        # asking contact
        # plz send pw
        # password
        try:
            bot.delete_message(message.chat.id, message.message_id)
            bot.delete_message(message.chat.id, message.message_id - 1)
            bot.delete_message(message.chat.id, message.message_id - 2)
            bot.delete_message(message.chat.id, message.message_id - 3)
        except:
            pass

        # send success message to the user.
        bot.send_message(
            message.chat.id,
            warning_msgs.usr_pw_success.format(
                current_users[message.chat.id]["user_data_from_db"][0]["name"],
                current_users[message.chat.id]["user_data_from_db"][0]["milma_id"],
            ),
            parse_mode="HTML",
        )

        # send user registration confirmation to the admins
        send_msg.send_warnings_to_admin(
            bot,
            f"<b>പുതിയ രജിസ്ട്രേഷൻ:\n{current_users[message.chat.id]['user_data_from_db'][0]['name']} ({current_users[message.chat.id]['user_data_from_db'][0]['milma_id']}) <a href='tg://user?id={message.chat.id}'>-</a> {current_users[message.chat.id]['user_data_from_db'][0]['phone']}</b>",
        )
        User.objects.filter(
            phone=current_users[message.chat.id]["user_data_from_db"][0]["phone"]
        ).update(telegram_id=message.from_user.id)

        # remove the user from current users list whose registration is successful
        try:
            current_users.pop(message.from_user.id)
        except:
            pass

    # if password is wrong
    else:
        if current_users[message.chat.id]["number_of_tries"] > 0:

            bot.delete_message(message.chat.id, message.message_id)
            # send warning to user
            bot.send_message(
                message.chat.id,
                warning_msgs.wrong_pw_warning.format(
                    current_users[message.chat.id]["number_of_tries"] - 1
                ),
            )

            # call this fn recursivly until i = 0
            bot.register_next_step_handler(message, ask_user_password, bot)
            current_users[message.chat.id]["number_of_tries"] -= 1

        # all try is finished.
        elif current_users[message.chat.id]["number_of_tries"] == 0:
            bot.send_message(message.chat.id, warning_msgs.wrong_pw_last)
            current_users[message.chat.id]["number_of_tries"] = 3


# help message
@bot.message_handler(commands=["help", "Help"])
def help_message(message):
    if message.chat.id in ADMINS:
        add_help_keyboard(message, bot)
    else:
        bot.delete_message(message.chat.id, message.message_id)
        bot.send_message(message.chat.id, warning_msgs.help_msg_user, parse_mode="HTML")


# old bills
@bot.message_handler(commands=["my_bills", "My_bills"])
def old_bills(message):
    bot.delete_message(message.chat.id, message.message_id)
    get_old_bills(message, bot)


##############################
# end: Start and register user
##############################


###############################
# start: admin functions
###############################

# document handler
@bot.message_handler(content_types=["document"])
def identify_documents_and_act(message):
    if message.chat.id in ADMINS:
        document_handler.document_from_telegram(message, bot)
    else:
        # delete send msg by the regular users
        bot.delete_message(message.chat.id, message.message_id)


# command /downloadXL
# download the contact excel file from server
# 🛠 More 🛠
@bot.message_handler(func=lambda message: str(message.text) == "🛠 More 🛠")
def downloadxl_message(message):
    if message.chat.id in ADMINS:
        from admin_modules.advanced_functions import more_options

        bot.delete_message(message.chat.id, message.message_id)
        more_options(bot, message)

    else:
        # delete send documents by the regular users
        bot.delete_message(message.chat.id, message.message_id)


# command: /forward
# forward to all users
@bot.message_handler(
    func=lambda message: str(message.text) == "⏩ Forward to all users ⏩"
)
@bot.message_handler(commands=["forward", "Forward"])
def forwardText(message):
    # if admins used this command continue, else do nothing
    if message.from_user.id in ADMINS:
        bot.delete_message(message.chat.id, message.message_id)
        forward_message(message, bot)
    else:
        # delete send msg by the regular users
        bot.delete_message(message.chat.id, message.message_id)


# forward to selected users
@bot.message_handler(
    func=lambda message: str(message.text) == "👥 Forward to selected users 👥"
)
@bot.message_handler(commands=["custom", "Custom"])
def message_to_selected_users(message):
    # if admins used this command continue, else do nothing
    if message.from_user.id in ADMINS:
        bot.delete_message(message.chat.id, message.message_id)
        bot.send_message(message.chat.id, "XL File format\n[milma id][Message]")
        custom_message(message, bot)
    else:
        # delete send msg by the regular users
        bot.delete_message(message.chat.id, message.message_id)


# this leads the user operations like add remove etc
@bot.message_handler(func=lambda message: str(message.text) == "👧 Members 🧔")
def member_operation_functions(message):
    # get_user_details()
    bot.delete_message(message.chat.id, message.message_id)
    user_operations(bot, message)


###############################
# end: admin functions
###############################


@bot.message_handler(commands=["status", "Status"])
def status_message(message):
    global current_users
    if message.from_user.id in ADMINS:
        sms_balance = get_sms_balance()
        bot.send_message(
            message.chat.id,
            f"🤖 <b>BOT IS ALIVE!</b> 🤖\n{pprint.pformat(current_users) if current_users and message.from_user.id == ADMIN else ''}\nRegistered users: {User.objects.filter(~Q(telegram_id=0)).count()}\nNon registered users: {User.objects.filter(telegram_id=0).count()}\n\n{'SMS balance: {}'.format(sms_balance) if sms_balance and msg_auth_key else ''}v {bot_version} - {MILMA_NAME}",
            parse_mode="HTML",
        )


############################################
# Custom exception area
############################################
class Error(Exception):
    """Base class for other exceptions"""

    pass


class ManualBotStopError(Error):
    """Raised when mannualy the bot is stopped"""

    pass


# Stop bot from telegram
@bot.message_handler(commands=["stop_me_baby."])
def stop_bot(message):
    if message.from_user.id == ADMIN:
        bot.send_message(ADMIN, "Good bye🤖😢")
        # raise an exception to stop the bot on command
        raise ManualBotStopError

    else:
        try:
            bot.delete_message(message.chat.id, message.message_id)
            bot.send_message(message.chat.id, "What was that? 🙄😨")
            sleep(2)
            bot.delete_message(message.chat.id, message.message_id)
        except:
            pass


# send file id, if someone sends a photo
@bot.message_handler(content_types=["photo"])
def identify_documents_and_act(message):
    if message.chat.id in ADMINS:
        bot.delete_message(message.chat.id, message.message_id)
        bot.send_message(message.chat.id, message.photo[0].file_id)


@bot.message_handler(commands=["me"])
def send_senders_details(message):
    if message.chat.id in ADMINS:
        import pprint

        bot.send_message(
            message.chat.id,
            f"{message.from_user.first_name}\n{message.chat.id}",
        )


# main function
def main():
    # send bot start warning to admin
    bot.send_message(ADMIN, bot_start, reply_markup=ReplyKeyboardRemove())

    bot.polling(none_stop=True)


if __name__ == "__main__":
    while True:
        try:
            main()

        except KeyboardInterrupt:
            break

        except ManualBotStopError:
            bot.send_message(
                MILMA_SEC,
                "⚠ Bot stopped for maintenance ⚠\nUse /start to get bot status",
            )
            break
        except requests.exceptions.ConnectionError:
            sleep(600)

        except Exception as e:
            exception = str(traceback.format_exc())
            for i in range(0, len(exception), 3999):
                bot.send_message(ADMIN, f"{exception[i : i + 3999]}")
            bot.send_message(ADMIN, f"❌Bot stopped ❌")
            bot.send_message(
                MILMA_SEC,
                "⚠ Bot stopped because of some error ⚠\nUse /status to get bot status\n\nBot will try to restart soon.",
            )
            print(traceback.format_exc())
            if e.__class__.__name__ == "FileNotFoundError":
                break

        current_users = dict()
        sleep(6)
