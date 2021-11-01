from datetime import datetime, timedelta


def get_old_bills(message, bot):
    from db.models import DailyBill, User

    user = User.objects.filter(telegram_id=message.chat.id).values().first()
    if user:
        import pprint

        # get the bill from db
        bills = DailyBill.objects.filter(
            milma_id=user["milma_id"], Date__gte=datetime.now() - timedelta(days=15)
        ).values()

        # here we make the bills dictionary where date is the key
        # because of this we can get each days value by calling the key date
        bills_formatted = {
            f'{bill["Date"].strftime("%Y-%m-%d")}-{bill["AM_Pm"]}': bill
            for bill in bills
        }

        old_bill_msg = "<b>Date, Qty, Rate, Amount</b>\n\n"
        # get one week dates and match it with the bills_formatted dict
        for i in range(14):
            day = datetime.now().date() - timedelta(days=i)

            # get the AM bill
            if bills_formatted.get(f"{day}-A"):
                print(day.strftime("%d/%m/%y"), bills_formatted.get(f"{day}-A"))
                one_day_bill = bills_formatted.get(f"{day}-A")
                old_bill_msg += f"{day.strftime('%d/%m/%y')} AM: <b>{one_day_bill['Qty']} L, ₹{one_day_bill['Rate']}, ₹{one_day_bill['Amount']}</b>\n"
            else:
                old_bill_msg += f"{day.strftime('%d/%m/%y')} AM: വിവരങ്ങൾ ലഭ്യമല്ല\n"

            # get the PM bill
            if bills_formatted.get(f"{day}-P"):
                one_day_bill = bills_formatted.get(f"{day}-P")
                print(day.strftime("%d/%m/%y"), bills_formatted.get(f"{day}-P"))
                old_bill_msg += f"{day.strftime('%d/%m/%y')} AM: <b>{one_day_bill['Qty']} L, ₹{one_day_bill['Rate']}, ₹{one_day_bill['Amount']}</b>\n\n"
            else:
                old_bill_msg += f"{day.strftime('%d/%m/%y')} PM: വിവരങ്ങൾ ലഭ്യമല്ല\n\n"

        # fale safe for big messages, if the charater count is greater than 4000 split it into two messages
        for i in range(0, len(old_bill_msg), 3999):
            bot.send_message(
                message.chat.id, old_bill_msg[i : i + 3999], parse_mode="HTML"
            )
        old_bill_msg = "<b>Date, Qty, Rate, Amount</b>\n\n"
