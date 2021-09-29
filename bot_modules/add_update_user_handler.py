from telebot.types import ReplyKeyboardRemove
from bot_modules.send_msg import send_warnings_to_admin

# add new user to the db
def add_user_details(message, bot):
    from db.models import User

    new_user_details = [i for i in str(message.text).split(",") if i]
    bot.delete_message(message.chat.id, message.message_id)

    if message.text == "/cancel":
        bot.send_message(message.chat.id, "Operation cancelled")

    # this handles if the new user data contain all required feilds.
    elif len(new_user_details) == 4:

        # check the phone number inputed has 10 numbers
        if len(str(new_user_details[2]).strip()) == 10:
            # duplicate phone
            d_phone = User.objects.filter(
                phone=str(new_user_details[2]).strip()
            ).values()
            # duplicate milma id
            d_milma_id = User.objects.filter(
                milma_id=str(new_user_details[0]).strip()
            ).values()

            if d_milma_id or d_phone:
                # all users with duplictes
                all_d_users = list()
                all_d_users = [d for d in d_phone]
                all_d_users.extend([d for d in d_milma_id])
                bot.send_message(message.chat.id, "ഈ വിവരങ്ങൾ നിലവിൽ ഉണ്ട്\n")
                user_text = set()
                for user in all_d_users:
                    user_text.add(
                        f"{user['name']}, {user['milma_id']}\n{user['phone']}"
                    )
                print("Duplicate user: ", user_text)
                bot.send_message(
                    message.chat.id,
                    "\n\n".join(user_text),
                    reply_markup=ReplyKeyboardRemove(),
                )
            else:
                try:
                    User.objects.update_or_create(
                        milma_id=new_user_details[0].strip(),
                        name=new_user_details[1].strip().capitalize(),
                        phone=new_user_details[2].strip(),
                        pword=new_user_details[3].strip(),
                        telegram_id=0,
                    )
                    send_warnings_to_admin(
                        bot, f"New user added: {', '.join(new_user_details)}"
                    )

                except:
                    send_warnings_to_admin(
                        bot, f"failed to add new user: {', '.join(new_user_details)}"
                    )
        else:
            bot.send_message(
                message.chat.id,
                f"ഫോൺ നമ്പർ 10 അക്കം ഇല്ല. ({str(new_user_details[2]).strip()})",
            )

    else:
        bot.send_message(message.chat.id, "Data not valid, try again")


def update_user_details(message, bot):
    pass
