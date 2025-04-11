import os
import random
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes

user_data = {}
referrals = {}

TOKEN = os.getenv("BOT_TOKEN", "YOUR_BOT_TOKEN_HERE")

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    args = context.args

    if user_id not in user_data:
        user_data[user_id] = {"balance": 0.0}

    if args:
        referrer_id = int(args[0])
        if referrer_id != user_id and referrer_id in user_data:
            reward = round(random.uniform(0.05, 0.50), 2)
            user_data[referrer_id]["balance"] += reward
            referrals.setdefault(referrer_id, []).append(user_id)
            await context.bot.send_message(chat_id=referrer_id, text=f"You earned ₹{reward:.2f} for referring someone!")

    referral_link = f"https://t.me/{context.bot.username}?start={user_id}"
    await update.message.reply_text(f"Welcome! Invite others with this link:\n{referral_link}")

async def balance(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    bal = user_data.get(user_id, {}).get("balance", 0.0)
    await update.message.reply_text(f"Your balance is ₹{bal:.2f}")

async def withdraw(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    bal = user_data.get(user_id, {}).get("balance", 0.0)
    if bal >= 100:
        user_data[user_id]["balance"] = 0.0
        await update.message.reply_text("Withdrawal successful! We'll contact you soon.")
    else:
        await update.message.reply_text("You need at least ₹100 to withdraw.")

if __name__ == "__main__":
    app = ApplicationBuilder().token(TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("balance", balance))
    app.add_handler(CommandHandler("withdraw", withdraw))
    print("Bot is running...")
    app.run_polling()
  
