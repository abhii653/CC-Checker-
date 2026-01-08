# main.py
from telegram.ext import ApplicationBuilder
from bot import setup_handlers, BOT_TOKEN, ADMIN_ID

def main():
    print("━━━━━━━━━━━━━━━━━━━━━━━━━━━━")
    print("   🚀 BOT STARTING...")
    print("━━━━━━━━━━━━━━━━━━━━━━━━━━━━")

    # Build Application
    application = ApplicationBuilder().token(BOT_TOKEN).build()

    # Setup Handlers from bot.py
    setup_handlers(application)

    print(f"✅ Bot is Live!")
    print(f"👑 Admin: {ADMIN_ID}")
    print("━━━━━━━━━━━━━━━━━━━━━━━━━━━━")

    application.run_polling()

if __name__ == '__main__':
    main()
