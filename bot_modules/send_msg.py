from bot_modules import config
from telebot.types import ReplyKeyboardRemove


def send_warnings_to_admin(bot, message_to_admin):

    for admin in config.ADMINS:
        try:
            bot.send_message(
                admin,
                message_to_admin,
                parse_mode="HTML",
                reply_markup=ReplyKeyboardRemove(),
            )
        except Exception as e:
            print(e)


def send_messages(bot, message, user, reply_mrk=None):
    try:
        return {
            "reply": bot.send_message(
                user, message, parse_mode="HTML", reply_markup=reply_mrk
            ),
            "error": None,
        }
    except Exception as e:
        return {"reply": None, "error": e}


# send a image with mesage as caption
def send_to_usrs_img(bot, message, user_id):
    try:
        return bot.send_photo(
            user_id,
            config.CASH_IMAGE,
            caption=message,
            parse_mode="HTML",
        )
    except Exception as e:
        print(f"Exception {user_id}: {e}")
