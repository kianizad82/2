from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import (
    Application, CommandHandler, CallbackQueryHandler, MessageHandler, filters, ContextTypes
)
from telegram.request import HTTPXRequest

TOKEN = "8911024888:AAFwQA3xp_uVWZjItENra0CykfvGnohTZU8"  


def main_menu() -> InlineKeyboardMarkup:
    keyboard = [
        [InlineKeyboardButton("درباره ما", callback_data="about"),
         InlineKeyboardButton("تماس", callback_data="contact")],
        [InlineKeyboardButton("وب‌سایت", url="https://example.com")],
    ]
    return InlineKeyboardMarkup(keyboard)

def main():
    proxy = "http://127.0.0.1:10809"
    app= (
        Application.builder()
        .token(TOKEN)
        .request(HTTOXRequest(proxy=proxy, connect_timeout=30, read_timeout=30))
        .get_updates_request(HTTOXRequest(proxy=proxy, connect_timeout=30, read_timeout=30))
        .build()
        )
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CallbackQueryHandler(button_handler))
    app.add_handler(MessageHandler(filters.UpdateType.BUSINESS_MESSAGE, business_reply))
    app.run_polling(allowed_updates=Update.ALL_TYPES)

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("سلام! یکی از گزینه‌ها رو انتخاب کن:", reply_markup=main_menu())


async def button_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer() 

    if query.data == "about":
        text = "این یه ربات تستیه."
    elif query.data == "contact":
        text = "با ما تماس بگیر: ..."
    else:
        text = "گزینه نامعتبر"

    back = InlineKeyboardMarkup([[InlineKeyboardButton("بازگشت", callback_data="back")]])
    if query.data == "back":
        await query.edit_message_text("یکی از گزینه‌ها رو انتخاب کن:", reply_markup=main_menu())
    else:
        await query.edit_message_text(text, reply_markup=back)


# پاسخ خودکار در حالت منشی (Business Mode)
async def business_reply(update: Update, context: ContextTypes.DEFAULT_TYPE):
    msg = update.business_message
    if msg and msg.text:
        await context.bot.send_message(
            chat_id=msg.chat.id,
            text="سلام! پیامت رسید، به‌زودی جواب می‌دم.",
            business_connection_id=msg.business_connection_id,
        )


def main():
    app = Application.builder().token(TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CallbackQueryHandler(button_handler))
    app.add_handler(MessageHandler(filters.UpdateType.BUSINESS_MESSAGE, business_reply))
    # business_connection و business_message باید در allowed_updates باشن
    app.run_polling(allowed_updates=Update.ALL_TYPES)


if __name__ == "__main__":
    main()
