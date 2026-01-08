#main.py


from telegram.ext import ApplicationBuilder
from bot import setup_handlers, BOT_TOKEN, ADMIN_ID

def main():
    """
    Starts the Telegram bot.
    """
    print("Starting bot...")
    
    # Create the Application and pass it your bot's token.
    application = ApplicationBuilder().token(BOT_TOKEN).build()

    # Setup all the handlers (commands, messages, etc.) from bot.py
    setup_handlers(application)

    print(f"Bot started! Admin ID: {ADMIN_ID}")
    print("Polling for updates...")
    
    #Run-Cmds @Abhinavinaman
    application.run_polling()

if __name__ == '__main__':
    main()
