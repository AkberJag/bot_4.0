from telebot.types import ReplyKeyboardRemove
from bot_modules.send_msg import send_messages
from bot_modules.bot_keyboards import more_options_keyboard
from admin_modules.delete_messages_handler import delete_messages
from admin_modules.document_handler import make_XL_from_db, move_old_files


def more_options(bot, message):
    more_options_keyboard(bot, message)
    bot.register_next_step_handler(message, more_options_choices, bot)


def more_options_choices(message, bot):

    # 💢 Delete Messages 💢
    if "Delete Messages" in message.text:
        delete_messages(bot, message)

    # 📜 Download contacts XL 📜
    elif "Download contacts XL" in message.text:
        make_XL_from_db()
        send_messages(
            bot,
            "❌ ഇതൊരു ചിലവേറിയ ജോലി ആണ്, ദയവായി 'ആഡ് യൂസർ' കമാൻഡ്‌സ് ഉപയോഗിക്കുക. ❌",
            message.chat.id,
            ReplyKeyboardRemove(),
        )
        bot.send_document(message.from_user.id, open("contacts.xlsx", "rb"))
        # move unused file to a directory
        move_old_files("contacts.xlsx", "old_contactsXLDB")
    else:
        bot.delete_message(message.chat.id, message.message_id - 1)
        bot.delete_message(message.chat.id, message.message_id)
        bot.send_message(
            message.chat.id,
            "Operation cancelled!, Try again with a valid option",
            reply_markup=ReplyKeyboardRemove(),
        )
