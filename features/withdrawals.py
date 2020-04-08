from config import *

################# ADDRESS 
en_confirm_markup = types.InlineKeyboardMarkup(row_width=2)
it_confirm_markup = types.InlineKeyboardMarkup()

en_confirm_btn = types.InlineKeyboardButton(text="Confirm", callback_data="confirm_address")
en_modify_btn = types.InlineKeyboardButton(text="Cancel", callback_data="cancel_address")

it_confirm_btn = types.InlineKeyboardButton(text="Confermare", callback_data="confirm_address")
it_modify_btn = types.InlineKeyboardButton(text="Annulla", callback_data="cancel_address")

# en_confirm_markup.keyboard = [[en_confirm_btn], [en_modify_btn]]
# it_confirm_markup.keyboard = [[it_confirm_btn], [it_modify_btn]]

en_confirm_markup.add(en_confirm_btn, en_modify_btn)
it_confirm_markup.add(it_confirm_btn, it_modify_btn)


confirm = {
    "en": en_confirm_markup,
    "it": it_confirm_markup
}

################ ADDRESS ENDS


################ ORDER #########

en_confirm_order_markup = types.InlineKeyboardMarkup(row_width=2)
it_confirm_order_markup = types.InlineKeyboardMarkup()

en_confirm_order_btn = types.InlineKeyboardButton(text="Confirm", callback_data="confirm_order")
en_modify_order_btn = types.InlineKeyboardButton(text="Cancel", callback_data="cancel_address")

it_confirm_order_btn = types.InlineKeyboardButton(text="Confermare", callback_data="confirm_order")
it_modify_order_btn = types.InlineKeyboardButton(text="Annulla", callback_data="cancel_address")

# en_confirm_markup.keyboard = [[en_confirm_btn], [en_modify_btn]]
# it_confirm_markup.keyboard = [[it_confirm_btn], [it_modify_btn]]

en_confirm_order_markup.add(en_confirm_order_btn, en_modify_order_btn)
it_confirm_order_markup.add(it_confirm_order_btn, it_modify_order_btn)


confirm_order = {
    "en": en_confirm_order_markup,
    "it": it_confirm_order_markup
}
##################

# Callback Handlers
@bot.callback_query_handler(func=lambda call: True)
def callback_answer(call):
    chat_id = call.message.chat.id
    # chat_id = message.chat.id
    user_id = call.from_user.id
    fcx_user = db.User.get_user(user_id)
    balance = fcx_user.account_balance
    lang = fcx_user.language


    # user_object = get_user_from_call(call.message)
    # lang = user_object["lang"]
    wallet_address = call.message.text.split('\n')[1]

    if call.data == "confirm_address":
        fcx_user.wallet_address = wallet_address
        
        # data = {
        #     "Withdrawals": {
        #         "wallet_address": wallet_address.split("\n")[1],
        #     }
        # }
        # update_user(user_object["user_id"], data)
        
        confirmation = {
                "en": f"""
Your bitcoin wallet address has been set to : 
<strong>{fcx_user.wallet_address}</strong>

You can now make a <b>withdrawal</b>
                """,
                "it": f"""
Your bitcoin wallet address has been set to (italian) : 
<strong>{fcx_user.wallet_address}</strong>

You can now make a <b>withdrawal</b>
                """
        }
        bot.send_message(chat_id, text=confirmation[lang], parse_mode="html", reply_markup=dashboard[lang])
        # withdrawal(message)


    elif call.data == "cancel_address":
        bot.send_message(chat_id, text="not set", reply_markup=dashboard[lang])
    elif call.data == "confirm_order":
            # data = {
            #         "withdrawal_request_confirmation": "Yes"
            # }
            # user_object.update(data)
            order_set_text = {
                "en": "Your withdrawal order of {amount} would be credited to your account within 72 hours",
                "it": "Il tuo ordine è impostato {amount} verrebbe accreditato sul tuo conto entro 72 ore"
            }
            # update_user(user_object["user_id"], user_object)
            bot.send_message(
                chat_id, 
                text=order_set_text[lang], 
                parse_mode="html",
                reply_markup=dashboard[lang]
                )
    



def wallet_amount_confirmation(message):
    chat_id = message.chat.id
    user_id = message.from_user.id
    fcx_user = db.User.get_user(user_id)
    balance = fcx_user.account_balance
    lang = fcx_user.language



    # user_object = get_user(message)
    # lang = user_object["lang"]
    # chat_id = message.chat.id
    amount = message.text
    try:
        amount = float(amount)
        if amount > balance:
            insufficient_balance_text = {
                "en": "You can't withdrawal a value greater than your account balance try again",
                "it": "Non puoi prelevare un valore superiore al saldo del tuo account"
            }
            bot.send_message(
                chat_id, 
                text=insufficient_balance_text[lang], 
                parse_mode="html",
                reply_to_message_id=message.message_id
                )
            bot.register_next_step_handler(
                message, 
                wallet_amount_confirmation
                )

        else:
            try:
                wallet_address = fcx_user.wallet_address
                if wallet_address is not None:


                # data = {
                #     "Withdrawals": {
                #         "withdrawal_request":  {
                #             "withdrawal_request": amount,
                #             # "date_of_request": datetime.now(),
                #             "status": "unconfirmed"
                #             }
                #     }
                # }
                # update_user(user_object["user_id"], data)

                    address_confirmation = {
                        "en": f"""
Withdrawal Amount: <b>{amount}</b>
Payment Address: <b>{wallet_address}</b>
""",
                        "it": f"""
Importo prelievo: <b>{amount}</b>
indirizzo di pagamento: <b>{wallet_address}</b>
                        """
                    }
                # data = {
                #     "Withdrawals": {
                #         "withdrawal_request":  {
                #             "withdrawal_request": amount,
                #             # "date_of_request": datetime.now(),
                #             "status": "unconfirmed"
                #             }
                #     }
                # }
                # update_user(user_object["user_id"], data)

                            
                    bot.send_message(chat_id, text=address_confirmation[lang], parse_mode="html", reply_markup=confirm_order[lang])
                
                else:
                    bot.send_message(chat_id, text="Set btc address", parse_mode="html")
                    set_wallet_address(message)
                    
            except KeyError:
                bot.send_message(chat_id, text="Invalid wallet address", parse_mode="html")
                set_wallet_address(message)


    except ValueError:
        invalid_amount = {
            "en": "Invalid amount please insert number",
            "it": "Importo non valido inserire il numero"

        }
        bot.send_message(
            chat_id, 
            text=invalid_amount[lang], 
            parse_mode="html",
            reply_to_message_id=message.message_id
            )
        bot.register_next_step_handler(
            message, 
            wallet_amount_confirmation
            )








def wallet_address_confirmation(message):
    chat_id = message.chat.id
    user_id = message.from_user.id
    fcx_user = db.User.get_user(user_id)
    balance = fcx_user.account_balance
    lang = fcx_user.language

    # user_object = get_user(message)
    # lang = user_object["lang"]
    # chat_id = message.chat.id
    wallet_address = message.text

    address_confirmation = {
            "en": f"""
You're about to set your bitcoin wallet address to : 
<strong>{wallet_address}</strong>
            """,
            "it ": f"""
You're about to set you bitcoin wallet address to (italian) : 
<strong>{wallet_address}</strong>
            """
    }
    
    # bot.send_message(chat_id, text=address_confirmation[lang])
    bot.send_message(chat_id, text=address_confirmation[lang], parse_mode="html", reply_markup=confirm[lang])




def set_wallet_address(message):
    regex_filter = '^[13][a-km-zA-HJ-NP-Z1-9]{25,34}$'
    chat_id = message.chat.id
    user_id = message.from_user.id
    fcx_user = db.User.get_user(user_id)
    lang = fcx_user.language

    # user_object = get_user(message)
    # lang = user_object["lang"]
    # chat_id = message.chat.id
    wallet_address = message.text
    text_enter_address = {
        "en": """
<b>Please enter your Bitcoin wallet address:</b>
        """,
        "it": """
<b>Per favore inserire l’indirizzo del Vostro Wallet Bitcoin</b>
        """
    }
    bot.send_message(chat_id,text=text_enter_address[lang], parse_mode="html")
    bot.register_next_step_handler(message, wallet_address_confirmation)






@bot.message_handler(
    func=lambda message: message.content_type == 'text'
    and ( 
        bool(re.search(r'withdrawal$', message.text, re.IGNORECASE)) or 
        bool(re.search(r'Ritiro$', message.text, re.IGNORECASE))
        )
)
def withdrawal(message):
    chat_id = message.chat.id
    user_id = message.from_user.id
    fcx_user = db.User.get_user(user_id)
    balance = fcx_user.account_balance
    lang = fcx_user.language
    # user_object = get_user(message)
    # balance = user_object["investment"]['balance']
    # lang = user_object["lang"]
    withdrawal_minimum_amount = 0.002


    withdrawal_amount_text = {
        "en": """<b>Enter the amount you wish to withdraw</b>""",
        "it": """Enter the amount you wish to withdraw(italian"""
    }
    ################
    text_info = {
        "en": f"""
You can create a payout request any time, depending on your account balance.
Minimum amount to withdraw is 0.002 BTC.
        """,
        "it": f"""
E’ possibile fare una richiesta di pagamento in qualsiasi momento, a seconda del saldo del Vostro conto.
L’importo minimo di prelievo è di 0,002 BTC.
        """
        }
    text_insufficient = {
        "en": """
You don't have enough funds to create a payout request
        """,
        "it": """
Non avete abbastanza fondi per creare una richiesta di pagamento.
        """
    }
 

    if balance < withdrawal_minimum_amount:
        bot.send_message(
            chat_id, text=text_info[lang] + text_insufficient[lang],
            reply_markup=confirm, parse_mode="html"
            )
    else:
        bot.send_message(
            chat_id,  reply_to_message_id=message.message_id,
            text=text_info[lang],
            # reply_markup=force_r, 
            parse_mode="html"
            )

        bot.send_message(
            chat_id, 
            text=withdrawal_amount_text[lang], 
            parse_mode="html",
            reply_markup=force_r
            )
        bot.register_next_step_handler(message, wallet_amount_confirmation)

        
        # bot.send_message(chat_id,text=text_enter_address[lang], parse_mode="html")
        # bot.register_next_step_handler(message, wallet_address_confirmation)



