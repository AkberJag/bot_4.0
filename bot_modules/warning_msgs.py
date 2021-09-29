from bot_modules.config import MILMA_NAME

bot_start = "🤖 bot started!"
user_already_exist_msg = "<b><u>വീണ്ടും സ്വാഗതം</u></b>\n\nഈ സേവനത്തിൽ നിങ്ങൾ ഇതിനുമുൻപെ രജിസ്റ്റർ ചെയ്തിട്ടുണ്ട് ✅\n\n({milma_id}) {name} - {phone} "
new_user_reg_msg = "<b>നമസ്കാരം</b>\nഈ സേവനം തുടങ്ങുന്നതിനായി ദയവായി താങ്കളുടെ ഫോൺ നമ്പർ ✅ ബട്ടൺ അമർത്തി അയക്കുക"
ph_no_btn_msg = "✅ ഫോൺ നമ്പർ അയക്കാൻ ഇവിടെ അമർത്തുക ✅"
less_than_digit_phone_no = f"⚠ <b>താങ്കളുടെ നമ്പർ ഇപ്പോൾ രജിസ്റ്റർ ചെയ്യാൻ സാധ്യമല്ല.. </b>⚠\n\nകൂടുതൽ സഹായങ്ങൾക്കായി {MILMA_NAME} സന്ദർശിക്കുക."
less_than_digit_phone_no_admin = (
    "⚠ 10 അക്കം ഇല്ലാത്ത ഒരു പുതിയ നമ്പർ രജിസ്റ്റർ ചെയ്യാൻ ശ്രമിച്ചിരിക്കുന്നു .⚠\n\n{}"
)
number_not_in_excel = f"❌ <b>ഈ ഫോൺ നമ്പർ എൻ്റെ പക്കൽ ഇല്ല, </b>❌\n\nകൂടുതൽ സഹായങ്ങൾക്കായി {MILMA_NAME} സന്ദർശിക്കുക."
number_not_in_excel_admin = (
    "❌ ഈ നമ്പർ എക്സൽ ഫയലിൽ ഇല്ല<a href='tg://user?id={}'>.</a> ❌\n\n{phone}"
)
ask_user_password_msg = "ദയവായി പാസ്സ്‌വേർഡ് നൽകുക"
usr_pw_success = (
    "✅ <b><u>പാസ്സ്‌വേർഡ് ശരിയാണ്</u></b> ✅\n\n🎉 <b>രെജിസ്ട്രേഷൻ പൂർത്തിയായി</b> 🎉\n\n❕ നമസ്കാരം <b>{}</b>,\nതാങ്കളുടെ അക്കൗണ്ട് നമ്പർ <b>{}</b> അല്ല എങ്കിൽ ദയവായി "
    + MILMA_NAME
    + " സന്ദർശിക്കുക. ❕"
)

wrong_pw_warning = "⚠ പാസ്സ്‌വേർഡ് തെറ്റ്, വീണ്ടും ശ്രമിക്കുക ({}) ⚠"
wrong_pw_last = (
    f"❌ പാസ്സ്‌വേർഡ് തെറ്റ്, കൂടുതൽ സഹായങ്ങൾക്കായി {MILMA_NAME} സന്ദർശിക്കുക. ❌"
)

help_msg_user = f"<b>ഇവിടെ നിങ്ങൾക്ക് ലഭ്യമാകുന്ന വിവരങ്ങൾ:</b>\n\n\n➡ എല്ലാ ദിവസത്തെയും ബില്ല്\n\n➡ മിൽമയിൽ നിന്നും ഉള്ള അറിയിപ്പുകൾ\n\n➡ വീക്കിലി പേമൻറ്റ് റിപ്പോർട്ട്\n\n➡ കാലിത്തീറ്റയുടെയും മറ്റും വിലവിവരം\n\n\n<b>കൂടുതൽ വിവരങ്ങൾക്കായി {MILMA_NAME} സന്ദർശിക്കുക.</b>"
help_msg_admin = "❗ YOU ARE AN ADMIN ❗\n\n1. You can send the daily messages by uploading the text file to this chat. (password not required)\n\n2. You can update the contact excel file by sending the file to this chat. ⚠ file name should be contacts.xlsx ⚠ (password not required)\n\n3. You can forward any type of files to all registered users, for that use the command:-\n\n        1️⃣ /forward\n\n        2️⃣ Enter your password\n\n        3️⃣ Upload or forward the file to this chat. (one message at a time)\n\n\n4. Use command /status to know about the bot's usage stats and running state etc.\n\n5. Use command /downloadXL to download the contacts excel file \n▪ <code>delete_msg</code>\n▪ <code>add</code>\n▪ /custom \n\n❗ YOU ARE AN ADMIN ❗"
daily_bill_upload = "📤 <b>ബില്ല് അയച്ചുകൊണ്ടിരിക്കുന്നു.</b> 📤\nദയവായി കാത്തിരിക്കുക.\n\n\n{} ൽ പാൽ അളന്ന ആളുകളുടെ എണ്ണം: <b>{}</b>"
daily_bill_success = "✅ <b>{} പേർക്ക് ബില്ല് വിജയകരമായി അയച്ചിരിക്കുന്നു.!</b> ✅"

weekly_pad_upload = "📤 <b>വീക്കിലി പേമൻറ്റ് റിപ്പോർട്ട് അയച്ചുകൊണ്ടിരിക്കുന്നു...</b> 📤\nദയവായി കാത്തിരിക്കുക.\n\nആഴ്ച: {}\n\n\nഎക്സൽ ഫയലിൽ ഉള്ള ആളുകളുടെ എണ്ണം: <b>{}</b>"
weekly_pad_success = (
    "✅ <b>{} പേർക്ക് വീക്കിലി പേമൻറ്റ് റിപ്പോർട്ട് വിജയകരമായി അയച്ചിരിക്കുന്നു.!</b> ✅"
)
weekly_msg_pad = f"<b><u>{MILMA_NAME}</u></b>\n<b>Weekly Payment Report</b>\n"

daily_bill = (
    f"<b><u>{MILMA_NAME}</u></b>\n\n"
    + "<b>MILK BILL</b>\n{date}\n\n{name}, {id}\n\nQty: <b>{qty} ലിറ്റർ </b>\n\nCLR: {clr}\nFAT: {fat}\nSNF: {snf}\n\nRs: <b>₹ {rs}</b>\nTotal: <b>₹ {total}</b>"
)

add_user_msg = "ഈ ഫോർമാറ്റ് ഉപയോഗിക്കുക:\n<b>മെമ്പർ ഐഡി, പേര്, ഫോൺ നമ്പർ, പാസ്സ്‌വേർഡ്\n\nഉദാ: 999, Tojin, 9876543210, 1234</b>\n\n/cancel to cancel this"
