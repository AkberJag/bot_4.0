import datetime
from time import sleep
from telebot.types import ReplyKeyboardMarkup, KeyboardButton
from bot_modules import warning_msgs


def add_contect_reqst_keyboard(bot, message):
    # add keyboard button
    keyboard = ReplyKeyboardMarkup(one_time_keyboard=True)
    # this is the button to send contact
    reg_button = KeyboardButton(text=warning_msgs.ph_no_btn_msg, request_contact=True)
    keyboard.add(reg_button)
    # send your phone number msg
    bot.send_message(
        message.chat.id,
        warning_msgs.new_user_reg_msg,
        reply_markup=keyboard,
        parse_mode="HTML",
    )


def add_help_keyboard(message, bot):
    # add keyboard button
    keyboard = ReplyKeyboardMarkup(one_time_keyboard=True, resize_keyboard=True)
    forward_to_all_button = KeyboardButton(text="⏩ Forward to all users ⏩")
    forward_to_selected_button = KeyboardButton(text="👥 Forward to selected users 👥")
    user_op_button = KeyboardButton(text="👧 Members 🧔")
    advance_button = KeyboardButton(text="🛠 More 🛠")

    cancel_button = KeyboardButton(text="✖ Cancel ✖")

    keyboard.add(forward_to_all_button)
    keyboard.add(forward_to_selected_button)
    keyboard.add(advance_button, user_op_button)

    keyboard.add(cancel_button)

    bot.send_message(
        message.chat.id,
        warning_msgs.help_msg_admin,
        parse_mode="HTML",
        reply_markup=keyboard,
    )


def add_user_operations_keyboard(bot, message):
    # add keyboard button
    keyboard = ReplyKeyboardMarkup(one_time_keyboard=True, resize_keyboard=True)

    add_button = KeyboardButton(text="👤 Add user")
    update_button = KeyboardButton(text="👥 Update user")
    delete_button = KeyboardButton(text="❌ delete user ❌")

    search_button1 = KeyboardButton(text="📞 Search with phone number 📞")
    search_button2 = KeyboardButton(text="🆔 Search with milma id 🆔")

    cancel_button = KeyboardButton(text="✖ Cancel ✖")

    keyboard.add(update_button, add_button)
    keyboard.add(search_button2)
    keyboard.add(search_button1)

    keyboard.add(cancel_button)

    keyboard.add(delete_button)

    # add keybooard msg
    bot.send_message(
        message.chat.id,
        "🕺💃",
        reply_markup=keyboard,
        parse_mode="HTML",
    )


def add_user_update_options_keyboard(bot, message):
    keyboard = ReplyKeyboardMarkup(one_time_keyboard=True, resize_keyboard=True)

    # name, telegram_id, milma_id, phone, pword
    name_button = KeyboardButton(text="✒ Update Name ✒")
    phone_button = KeyboardButton(text="📲 Update phone 📲")
    pword_button = KeyboardButton(text="Update password")
    milma_id_button = KeyboardButton(text="Update milma id")
    remove_from_tg_button = KeyboardButton(text="Remove from telegram")

    cancel_button = KeyboardButton(text="✖ Cancel ✖")

    keyboard.add(name_button)
    keyboard.add(phone_button)
    keyboard.add(milma_id_button)
    keyboard.add(remove_from_tg_button, pword_button)

    keyboard.add(cancel_button)

    # add keybooard msg
    bot.send_message(
        message.chat.id,
        "👥",
        reply_markup=keyboard,
        parse_mode="HTML",
    )

    #


def more_options_keyboard(bot, message):
    # add keyboard button
    keyboard = ReplyKeyboardMarkup(one_time_keyboard=True, resize_keyboard=True)

    delete_msgs_button = KeyboardButton(text="💢 Delete Messages 💢")
    download_contacts_XL_button = KeyboardButton(text="📜 Download contacts XL 📜")

    cancel_button = KeyboardButton(text="✖ Cancel ✖")

    keyboard.add(delete_msgs_button)
    keyboard.add(download_contacts_XL_button)

    keyboard.add(cancel_button)

    # more options msg
    bot.send_message(
        message.chat.id,
        "🛠",
        reply_markup=keyboard,
        parse_mode="HTML",
    )


def cancel_keyboard(bot, message, message_to_send="Huh?"):
    # add keyboard button
    keyboard = ReplyKeyboardMarkup(one_time_keyboard=True, resize_keyboard=True)
    # this is the button to send contact
    cancel_button = KeyboardButton(text="✖ Cancel ✖")
    keyboard.add(cancel_button)
    # send your phone number msg
    bot.send_message(
        message.chat.id,
        message_to_send,
        reply_markup=keyboard,
        parse_mode="HTML",
    )


def date_keyboard(bot, message):

    # get today's date and if it is UTC, add 5.30 hrs to it
    current_date = datetime.datetime.now()

    if str(current_date.astimezone().tzinfo) == "India Standard Time":
        current_date = datetime.date.today().strftime("%d-%m-%Y")
    
    elif str(current_date.astimezone().tzinfo) == "UTC":
        current_date = (
            datetime.date.today() + datetime.timedelta(hours=5, minutes=30)
        ).strftime("%d-%m-%Y")


    # add keyboard button
    keyboard = ReplyKeyboardMarkup(one_time_keyboard=True)
    # this is the button to send contact
    date_am_button = KeyboardButton(text=f"\n{current_date} AM\n")
    date_pm_button = KeyboardButton(text=f"\n{current_date} PM\n")
    cancel_button = KeyboardButton(text="❌ Cancel ❌")

    keyboard.add(date_am_button)
    keyboard.add(date_pm_button)
    keyboard.add(cancel_button)

    message_to_send = (
        f"Send date like\n\n{datetime.date.today().strftime('%d-%m-%Y')} AM"
    )

    # Ask for date
    bot.send_message(
        message.chat.id,
        message_to_send,
        reply_markup=keyboard,
        parse_mode="HTML",
    )
