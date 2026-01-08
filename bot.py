#bot.py
#Owner:- @Abhinavinaman
#Join :- t.me/navdish_ff_store

import logging
import json
import time
import uuid
import re
import httpx
import asyncio
import random
from datetime import datetime, timedelta

from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, ContextTypes, CallbackQueryHandler, MessageHandler, filters
from telegram.constants import ParseMode
from telegram.error import BadRequest

# --- CONFIGURATION ---
BOT_TOKEN = "8560262173:AAE1cYkTvqpA2EvL255oIdndfYrSpguIsFk" 
ADMIN_ID = 5950016400  
DEV_CHANNEL_URL = "https://t.me/Cardinghell1" 
HYPERLINK_URL = "https://t.me/Cardinghell1" 
USERS_FILE = 'userss.json' 
CODES_FILE = 'codes.json'
FREE_MINUTES = 60 
BOT_NAME = "CC_bot" 
BOT_FONT = "𝘼𝙐𝙏𝙃 𝙂𝘼𝙏𝙀𝙎" 
BOT_PASSWORD = "Cardinghell@#£" # Bot Password

PROXIES = [
    "142.111.48.253:7030:mgrthddv:ip1dn0lb1po2", "198.23.239.134:6540:mgrthddv:ip1dn0lb1po2",
    "45.38.107.97:6014:mgrthddv:ip1dn0lb1po2", "107.172.163.27:6543:mgrthddv:ip1dn0lb1po2",
    "64.137.96.74:6641:mgrthddv:ip1dn0lb1po2", "154.203.43.247:5536:mgrthddv:ip1dn0lb1po2",
    "84.247.60.125:6095:mgrthddv:ip1dn0lb1po2", "216.10.27.159:6837:mgrthddv:ip1dn0lb1po2",
    "142.111.67.146:5611:mgrthddv:ip1dn0lb1po2", "142.147.128.93:6593:mgrthddv:ip1dn0lb1po2",
]

# APIs
BRAINTREE_API = "https://b3-checker-production.up.railway.app/check?card="
STRIPE_V1_API = "https://chkr-api.vercel.app/api/check?cc="
STRIPE_V2_API = "http://fromdeepweb.gamer.gd/api.php?lista="
SHOPIFY_V1_API = "https://autoshopify-dark.sevalla.app/index.php"
SHOPIFY_V2_API = "https://auto-shopify-6cz4.onrender.com/index.php"
BIN_LOOKUP_API = "https://lookup.binlist.net/" 

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)
logger = logging.getLogger(__name__)

# --- DATA HELPERS ---
def load_data(filepath):
    try:
        with open(filepath, 'r') as f: return json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        save_data(filepath, {})
        return {}

def save_data(filepath, data):
    with open(filepath, 'w') as f: json.dump(data, f, indent=4)

def get_user_data(user_id):
    users = load_data(USERS_FILE)
    return users.get(str(user_id), {})

def is_verified(user_id):
    data = get_user_data(user_id)
    return data.get('verified', False)

def is_user_premium(user_id):
    data = get_user_data(user_id)
    if not data or 'expiry' not in data: return False
    expiry = datetime.fromisoformat(data['expiry'])
    if expiry.year == 9999: return True
    return expiry > datetime.now()

def set_user_expiry(user_id, minutes):
    users = load_data(USERS_FILE)
    user_id_str = str(user_id)
    user_info = users.get(user_id_str, {'verified': True})
    
    if minutes == -1:
        new_expiry = datetime(9999, 12, 31, 23, 59, 59)
    else:
        base_time = datetime.now()
        if 'expiry' in user_info:
            current_expiry = datetime.fromisoformat(user_info['expiry'])
            if current_expiry.year == 9999: return current_expiry
            if current_expiry > base_time: base_time = current_expiry
        new_expiry = base_time + timedelta(minutes=minutes)
    
    user_info['expiry'] = new_expiry.isoformat()
    users[user_id_str] = user_info
    save_data(USERS_FILE, users)
    return new_expiry

def hyper(text): return f"[{text}]({HYPERLINK_URL})"

# --- COMMANDS ---
async def start_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    if not is_verified(user_id):
        await update.message.reply_text("🔒 **Bot is Locked!**\n\nPlease enter the password to continue:")
        return

    welcome_text = (
        f"⎔ {hyper(f'𝙒𝙚𝙡𝙘𝙤𝙢𝙚, {update.effective_user.first_name}')} ⎔\n\n"
        f"⎔ {hyper('𝙔𝙤𝙪𝙧 𝙐𝙨𝙚𝙧 𝙄𝘿')}: `{user_id}`\n"
        f"⎔ {hyper('𝙎𝙮𝙨𝙩𝙚𝙢 𝙎𝙩𝙖𝙩𝙪𝙨')}: 🟢 𝙊𝙣𝙡𝙞𝙣𝙚\n\n"
        f"Click below to see the gates."
    )
    keyboard = [
        [InlineKeyboardButton(f"💎 {BOT_FONT} 💎", callback_data='gates_menu')],
        [InlineKeyboardButton("👤 𝙈𝙔 𝙄𝙉𝙁𝙊", callback_data='my_info'), InlineKeyboardButton("🎁 𝙍𝙀𝘿𝙀𝙀𝙈", callback_data='redeem_info')],
        [InlineKeyboardButton("🔗 𝘿𝙀𝙑𝙀𝙇𝙊𝙋𝙀𝙍", url=DEV_CHANNEL_URL)]
    ]
    await update.message.reply_text(text=welcome_text, reply_markup=InlineKeyboardMarkup(keyboard), parse_mode='Markdown', disable_web_page_preview=True)

async def message_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    text = update.message.text

    # Password Verification Logic
    if not is_verified(user_id):
        if text == BOT_PASSWORD:
            users = load_data(USERS_FILE)
            users[str(user_id)] = {'verified': True}
            save_data(USERS_FILE, users)
            set_user_expiry(user_id, FREE_MINUTES)
            await update.message.reply_text(f"✅ Access Granted! You received {FREE_MINUTES}m free trial. Use /start to begin.")
        else:
            await update.message.reply_text("❌ Wrong Password! Try again.")
        return

async def code_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.effective_user.id != ADMIN_ID: return
    try:
        val = context.args[0].lower()
        minutes = -1 if val == "unlimited" else int(val)
        code = f"XEBEC-{uuid.uuid4().hex[:8].upper()}"
        codes = load_data(CODES_FILE)
        codes[code] = {'minutes': minutes, 'used_by': None}
        save_data(CODES_FILE, codes)
        await update.message.reply_text(f"✅ Code: `{code}`\nType: {'Unlimited' if minutes == -1 else f'{minutes}m'}")
    except: await update.message.reply_text("`/code <min>` or `/code unlimited`")

async def redeem_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not is_verified(update.effective_user.id): return
    try:
        code = context.args[0]
        codes = load_data(CODES_FILE)
        if code in codes and codes[code]['used_by'] is None:
            new_exp = set_user_expiry(update.effective_user.id, codes[code]['minutes'])
            codes[code]['used_by'] = update.effective_user.id
            save_data(CODES_FILE, codes)
            msg = "♾️ Lifetime" if codes[code]['minutes'] == -1 else new_exp.strftime('%Y-%m-%d %H:%M:%S')
            await update.message.reply_text(f"✅ Plan Updated! Expires: `{msg}`")
        else: await update.message.reply_text("❌ Invalid/Used Code.")
    except: await update.message.reply_text("`/redeem <code>`")

# --- BUTTON HANDLER ---
async def button_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    user_id = query.from_user.id
    if not is_verified(user_id):
        await query.answer("❌ Verify password first!", show_alert=True)
        return
    await query.answer()

    if query.data == 'my_info':
        users = load_data(USERS_FILE)
        expiry_raw = users.get(str(user_id), {}).get('expiry', 'N/A')
        if "9999" in expiry_raw: expiry_str = "♾️ Unlimited"
        else: expiry_str = expiry_raw
        
        text = f"👤 **INFO**\nID: `{user_id}`\nPlan: `{expiry_str}`"
        await query.edit_message_text(text, reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("⬅️ BACK", callback_data='start_menu')]]), parse_mode='Markdown')
    
    elif query.data == 'start_menu':
        # Return to main menu
        keyboard = [[InlineKeyboardButton(f"💎 {BOT_FONT} 💎", callback_data='gates_menu')]]
        await query.edit_message_text("Main Menu", reply_markup=InlineKeyboardMarkup(keyboard))

    elif query.data == 'gates_menu':
        gates = "💎 **GATES**\nStripe: `/st`\nBraintree: `/b3`\nShopify: `/sh`"
        await query.edit_message_text(gates, reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("⬅️ BACK", callback_data='start_menu')]]), parse_mode='Markdown')

# --- MAIN ---
def main():
    app = Application.builder().token(BOT_TOKEN).build()
    app.add_handler(CommandHandler('start', start_command))
    app.add_handler(CommandHandler('code', code_command))
    app.add_handler(CommandHandler('redeem', redeem_command))
    app.add_handler(CallbackQueryHandler(button_handler))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, message_handler))
    
    print("Bot is running...")
    app.run_polling()

if __name__ == '__main__':
    main()
