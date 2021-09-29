import re
from telebot.types import ReplyKeyboardRemove
from bot_modules.warning_msgs import add_user_msg
from bot_modules.add_update_user_handler import add_user_details
from bot_modules.bot_keyboards import (
    add_user_operations_keyboard,
    add_user_update_options_keyboard,
    cancel_keyboard,
)
from bot_modules.send_msg import send_messages, send_warnings_to_admin


def user_operations(bot, message):

    add_user_operations_keyboard(bot, message)
    bot.register_next_step_handler(message, get_user_message, bot)


# find which button is pressed
def get_user_message(message, bot):

    # "👥 Update user" button
    if "Update user" in message.text:
        cancel_keyboard(bot, message, "Enter milma id")
        bot.register_next_step_handler(message, update_user, bot)

    # "🆔 Search with milma id 🆔" button
    elif "id" in message.text:
        bot.delete_message(message.chat.id, message.message_id - 1)
        cancel_keyboard(bot, message, "Enter milma id")
        bot.register_next_step_handler(message, seacrh_db, 0, bot)

    # "📞 Search with phone number 📞" button
    elif "phone" in message.text:
        bot.delete_message(message.chat.id, message.message_id - 1)
        cancel_keyboard(bot, message, "Enter phone number")
        bot.register_next_step_handler(message, seacrh_db, 1, bot)

    # "👤 Add user" button
    elif "Add" in message.text:
        bot.delete_message(message.chat.id, message.message_id - 1)
        send_messages(bot, add_user_msg, message.chat.id)
        bot.register_next_step_handler(message, add_user, bot)

    # "❌ delete user ❌" button
    elif "delete" in message.text:
        bot.delete_message(message.chat.id, message.message_id - 1)
        cancel_keyboard(bot, message, "Enter milma id")
        bot.register_next_step_handler(message, delete_user, bot)

    # cancel button
    elif "Cancel" in message.text:
        bot.delete_message(message.chat.id, message.message_id)
        bot.send_message(message.chat.id, "💥", reply_markup=ReplyKeyboardRemove())

    else:
        bot.delete_message(message.chat.id, message.message_id - 1)
        bot.delete_message(message.chat.id, message.message_id)
        bot.send_message(
            message.chat.id,
            "Operation cancelled!, Try again with a valid option",
            reply_markup=ReplyKeyboardRemove(),
        )


def add_user(message, bot):
    add_user_details(message, bot)


def seacrh_db(message, item, bot):
    if message.text == "✖ Cancel ✖":
        bot.send_message(message.chat.id, "💥", reply_markup=ReplyKeyboardRemove())

    else:
        from db.models import User

        user_details = "Name: {name}\nMilma id: {milma_id}\nPhone: {phone}\nPassword: {pword}\nDB id: {id}\n{reg_stat}<a href='tg://user?id={telegram_id}'>more details.</a>"

        # search with milma id
        if item == 0:
            db_result = None
            # check the input is int or not
            if bool(re.match("^[0-9]+$", message.text)):
                db_result = User.objects.filter(milma_id=message.text).values()

            if db_result:
                for user in db_result:
                    bot.send_message(
                        message.chat.id,
                        user_details.format(
                            name=user["name"],
                            milma_id=user["milma_id"],
                            phone=user["phone"],
                            pword=user["pword"],
                            id=user["id"],
                            telegram_id=user["telegram_id"],
                            reg_stat=""
                            if user["telegram_id"]
                            else "⚠<b>Not yet registered in telegram</b>⚠\n",
                        ),
                        parse_mode="HTML",
                        reply_markup=ReplyKeyboardRemove(),
                    )
                print("search result:", user)
            else:
                bot.send_message(
                    message.chat.id,
                    "No user found!",
                    reply_markup=ReplyKeyboardRemove(),
                )

        # search with phone
        elif item == 1:
            db_result = User.objects.filter(phone=message.text).values()
            if db_result:
                for user in db_result:
                    bot.send_message(
                        message.chat.id,
                        user_details.format(
                            name=user["name"],
                            milma_id=user["milma_id"],
                            phone=user["phone"],
                            pword=user["pword"],
                            id=user["id"],
                            telegram_id=user["telegram_id"],
                            reg_stat=""
                            if user["telegram_id"]
                            else "⚠<b>Not yet registered in telegram</b>⚠\n",
                        ),
                        parse_mode="HTML",
                        reply_markup=ReplyKeyboardRemove(),
                    )
                print("search result:", user)
            else:
                bot.send_message(
                    message.chat.id,
                    "No user found!",
                    reply_markup=ReplyKeyboardRemove(),
                )


def delete_user(message, bot):
    if message.text == "✖ Cancel ✖":
        bot.send_message(message.chat.id, "💥", reply_markup=ReplyKeyboardRemove())
    else:
        from db.models import User

        user_details = "Name: {name}\nMilma id: {milma_id}\nPhone: {phone}\nPassword: {pword}pw\nDB id: {id}\n<a href='tg://user?id={telegram_id}'>more details.</a>"

        db_result = None
        # check the input is int or not
        if bool(re.match("^[0-9]+$", message.text)):
            db_result = User.objects.filter(milma_id=message.text)

        if db_result.values():
            for user in db_result.values():
                send_warnings_to_admin(
                    bot,
                    "deleteing this user:\n"
                    + user_details.format(
                        name=user["name"],
                        milma_id=user["milma_id"],
                        phone=user["phone"],
                        pword=user["pword"],
                        id=user["id"],
                        telegram_id=user["telegram_id"],
                    ),
                )
            print("deleting result:", user)
            db_result.delete()
        else:
            bot.send_message(
                message.chat.id, "No user found!", reply_markup=ReplyKeyboardRemove()
            )


def update_user(message, bot):
    # here we get the user from db and display it
    from db.models import User

    user_details = "Name: {name}\nMilma id: {milma_id}\nPhone: {phone}\nPassword: {pword}\nDB id: {id}\n{reg_stat}<a href='tg://user?id={telegram_id}'>more details.</a>"

    if message.text == "✖ Cancel ✖":
        bot.send_message(message.chat.id, "💥", reply_markup=ReplyKeyboardRemove())
    else:
        db_result = None
        if message.text:
            # check the input is int or not
            if bool(re.match("^[0-9]+$", message.text)):
                db_result = User.objects.filter(milma_id=message.text).values()

            if db_result:
                # then ask get one option line name milma id to update the details
                add_user_update_options_keyboard(bot, message)
                for user in db_result:
                    bot.send_message(
                        message.chat.id,
                        user_details.format(
                            name=user["name"],
                            milma_id=user["milma_id"],
                            phone=user["phone"],
                            pword=user["pword"],
                            id=user["id"],
                            telegram_id=user["telegram_id"],
                            reg_stat=""
                            if user["telegram_id"]
                            else "⚠<b>Not yet registered in telegram</b>⚠\n",
                        ),
                        parse_mode="HTML",
                    )
                print("search result:", user)
                bot.register_next_step_handler(
                    message, get_user_update_options_message, bot, message.text
                )
            else:
                bot.send_message(
                    message.chat.id,
                    "No user found!",
                    reply_markup=ReplyKeyboardRemove(),
                )
        else:
            bot.send_message(message.chat.id, "Please send valid information")


def get_user_update_options_message(message, bot, milma_id):
    # "✒ Update Name ✒"
    if "Update Name" in message.text:
        send_messages(
            bot, "Send <b>New name</b>", message.chat.id, ReplyKeyboardRemove()
        )
        bot.register_next_step_handler(message, update_the_DB, bot, "name", milma_id)

    # "📲 Update phone 📲"
    elif "Update phone" in message.text:
        send_messages(
            bot, "Send <b>New Phone number</b>", message.chat.id, ReplyKeyboardRemove()
        )
        bot.register_next_step_handler(message, update_the_DB, bot, "phone", milma_id)

    # "Update password"
    elif "Update password" in message.text:
        send_messages(
            bot, "Send <b>New password</b>", message.chat.id, ReplyKeyboardRemove()
        )
        bot.register_next_step_handler(message, update_the_DB, bot, "pword", milma_id)

    # "Update milma id"
    elif "Update milma id" in message.text:
        send_messages(
            bot, "Send <b>New milma id</b>", message.chat.id, ReplyKeyboardRemove()
        )
        bot.register_next_step_handler(message, update_the_DB, bot, "id", milma_id)

    # "Remove from telegram"
    elif "Remove from telegram" in message.text:
        from db.models import User

        User.objects.filter(milma_id=milma_id).update(telegram_id=0)
        send_messages(
            bot, "User removed from telegram ✅", message.chat.id, ReplyKeyboardRemove()
        )

    # cancel button
    elif "Cancel" in message.text:
        bot.delete_message(message.chat.id, message.message_id)
        bot.send_message(message.chat.id, "💥", reply_markup=ReplyKeyboardRemove())

    else:
        bot.delete_message(message.chat.id, message.message_id - 1)
        bot.delete_message(message.chat.id, message.message_id)
        bot.send_message(
            message.chat.id,
            "Operation cancelled!, Try again with a valid option",
            reply_markup=ReplyKeyboardRemove(),
        )


def update_the_DB(message, bot, option, milma_id):
    from db.models import User

    if option == "name":
        if bool(re.match("[a-zA-Z\s]+$", message.text)):
            User.objects.filter(milma_id=milma_id).update(name=message.text)
            send_messages(bot, "Name updated ✅", message.chat.id)
        else:
            send_messages(bot, "Not a valid name. Try again!", message.chat.id)

    # check if the phone nuber is existing on the db
    # if not then update the number
    elif option == "phone":
        user = User.objects.filter(phone=message.text).values()
        if not user:
            if len(message.text) == 10 and bool(re.match("^[0-9]+$", message.text)):
                User.objects.filter(milma_id=milma_id).update(phone=message.text)
                send_messages(bot, "Phone number updated ✅", message.chat.id)
            else:
                send_messages(
                    bot, "Not a valid phone number. Try again!", message.chat.id
                )
        else:
            send_messages(
                bot,
                f"This number already exist: {user[0]['name']} {user[0]['milma_id']}. Try again!",
                message.chat.id,
            )

    elif option == "pword":
        User.objects.filter(milma_id=milma_id).update(pword=message.text[:4])
        send_messages(bot, "Password updated ✅", message.chat.id)

    # check for duplicate milma id
    # if no duplicate found update
    elif option == "id":
        user = None
        try:
            user = User.objects.filter(milma_id=message.text).values()
        except:
            pass
        if not user:
            if len(message.text) <= 5 and str(message.text).isnumeric():
                User.objects.filter(milma_id=milma_id).update(milma_id=message.text)
                send_messages(bot, "Milma id updated ✅", message.chat.id)
            else:
                send_messages(bot, "Not a valid milma id. Try again!", message.chat.id)
        else:
            send_messages(
                bot,
                f"This number already exist: {user[0]['name']} {user[0]['milma_id']}. Try again!",
                message.chat.id,
            )
