#on air movies program
from info import AUTH_CHANNEL, AUTH_USERS, CUSTOM_FILE_CAPTION, API_KEY, AUTH_GROUPS, ADMINS
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton, CallbackQuery
from pyrogram import Client, filters
import re
import random
import asyncio
from pyrogram.errors import UserNotParticipant, UserIsBlocked
from utils import get_filter_results, get_file_details, is_subscribed, get_poster
BUTTONS = {}
BOT = {}

RAT = ["🦋", "🫐", "🎡", "🎈", "🥀", "🔖", "🍭", "🍿", ]
RATING = ["5.1/10 🤺ɪᴍᴅʙ", "6.2/10 🤺ɪᴍᴅʙ", "7.3/10 🤺ɪᴍᴅʙ", "8.1/10 🤺ɪᴍᴅʙ", "5.5/10 🤺ɪᴍᴅʙ", "7.8/10 🤺ɪᴍᴅʙ", "6.4/10 🤺ɪᴍᴅʙ", "6.9/10 🤺ɪᴍᴅʙ", ]
GENRES = ["ғᴜɴ🍿 ғᴀᴄᴛ",
         "ᴛʜʀɪʟʟᴇʀ🍿",
         "ᴅʀᴀᴍᴀ🍿 ᴄᴏᴍᴇᴅʏ",
         "ғᴀᴍɪʟʏ🍿 ᴅʀᴀᴍᴀ",
         "ᴀᴅᴠᴇɴᴛᴜʀᴇ🍿",
         "ғɪʟᴍ ɴᴏɪʀ🍿",
         "ᴅᴏᴄᴜᴍᴇɴᴛᴀʀʏ🍿"]
PHOTO = [
    "https://telegra.ph/file/9075ca7cbad944afaa823.jpg",
    "https://telegra.ph/file/9688c892ad2f2cf5c3f68.jpg",
    "https://telegra.ph/file/51683050f583af4c81013.jpg",
]

@Client.on_message(filters.text & filters.private & filters.incoming & filters.user(AUTH_USERS) if AUTH_USERS else filters.text & filters.private & filters.incoming)
async def filter(client, message):
    if message.text.startswith("/"):
        return
    if AUTH_CHANNEL:
        invite_link = await client.create_chat_invite_link(int(AUTH_CHANNEL))
        try:
            user = await client.get_chat_member(int(AUTH_CHANNEL), message.from_user.id)
            if user.status == "kicked":
                await client.send_message(
                    chat_id=message.from_user.id,
                    text="Sorry mowne 💋, You are Banned to use me.",
                    parse_mode="markdown",
                    disable_web_page_preview=True
                )
                return
        except UserNotParticipant:
            await client.send_message(
                chat_id=message.from_user.id,
                text="**Join My 🎪 group 🎪 to use this Bot 😉**",
                reply_markup=InlineKeyboardMarkup(
                    [
                        [
                            InlineKeyboardButton("🎪 Join GROUP 🎪", url=invite_link.invite_link)
                        ]
                    ]
                ),
                parse_mode="markdown"
            )
            return
        except Exception:
            await client.send_message(
                chat_id=message.from_user.id,
                text="Something went Wrong.",
                parse_mode="markdown",
                disable_web_page_preview=True
            )
            return
    if re.findall("((^\/|^,|^!|^\.|^[\U0001F600-\U000E007F]).*)", message.text):
        return
    if 99 < len(message.text) < 100:    
        btn = []
        search = message.text 
        files = await get_filter_results(query=search)
        if files:
            for file in files:
                file_id = file.file_id
                filename = f"{random.choice(RAT)}[{get_size(file.file_size)}] {file.file_name}"
                btn.append(
                    [InlineKeyboardButton(text=f"{filename}",callback_data=f"subinps#{file_id}")]
                    )
        else:
            await client.send_photo(chat_id=message.from_user.id, photo='https://telegra.ph/file/69152843f167e3977e59d.jpg')
            return

        if not btn:
            return

        if len(btn) > 15: 
            btns = list(split_list(btn, 15)) 
            keyword = f"{message.chat.id}-{message.message_id}"
            BUTTONS[keyword] = {
                "total" : len(btns),
                "buttons" : btns
            }
        else:
            buttons = btn
            buttons.append(
                [InlineKeyboardButton("🎪 channel 🎪", url="https://t.me/joinchat/4-Quex2FaFhjMDM1")]
            )
            poster=None
            if API_KEY:
                poster=await get_poster(search)
            if poster:
                await message.reply_photo(photo=poster, caption=f"<b>🎬 ᴍᴏᴠɪᴇ ɴᴀᴍᴇ : {search} ‌‌‌‌‎</b> \n\n  <b>🌀 ᴄʜᴀɴɴᴇʟ : [ᴏɴᴀɪʀᴍᴏᴠɪᴇs](https://t.me/joinchat/4-Quex2FaFhjMDM1) \n⚡️ᴘᴏᴡᴇʀᴇᴅ ʙʏ:[ᴏɴᴀɪʀ_ғɪʟᴛᴇʀᵇᵒᵗ](https://t.me/On_air_Filter_bot)</b>", reply_markup=InlineKeyboardMarkup(buttons))

            else:
                await message.reply_photo(photo=f"{random.choice(PHOTO)}", caption=f"<b>🎬 ᴍᴏᴠɪᴇ ɴᴀᴍᴇ : {search} ‌‌‌‌‎</b> \n\n <b>🌀 ᴄʜᴀɴɴᴇʟ : [ᴏɴᴀɪʀᴍᴏᴠɪᴇs](https://t.me/joinchat/4-Quex2FaFhjMDM1) \n⚡️ᴘᴏᴡᴇʀᴇᴅ ʙʏ:[ᴏɴᴀɪʀ_ғɪʟᴛᴇʀᵇᵒᵗ](https://t.me/On_air_Filter_bot)</b>", reply_markup=InlineKeyboardMarkup(buttons))
            return

        data = BUTTONS[keyword]
        buttons = data['buttons'][0].copy()

        buttons.append(
            [InlineKeyboardButton(text="⇏ɴᴇxᴛ⇏",callback_data=f"next_0_{keyword}")]
        )    
        buttons.append(
            [InlineKeyboardButton(text=f"🎪 Pages 1/{data['total']}🎪",callback_data="pages")]
        )
        poster=None
        if API_KEY:
            poster=await get_poster(search)
        if poster:
            await message.reply_photo(photo=poster, caption=f"<b>🎬 ᴍᴏᴠɪᴇ ɴᴀᴍᴇ : {search} ‌‌‌‌‎</b> \n\n <b>🌀 ᴄʜᴀɴɴᴇʟ :[ᴏɴᴀɪʀᴍᴏᴠɪᴇs](https://t.me/joinchat/4-Quex2FaFhjMDM1) \n⚡️ᴘᴏᴡᴇʀᴇᴅ ʙʏ:[ᴏɴᴀɪʀ_ғɪʟᴛᴇʀᵇᵒᵗ](https://t.me/On_air_Filter_bot)</b>", reply_markup=InlineKeyboardMarkup(buttons))
        else:
            await message.reply_photo(photo=f"{random.choice(PHOTO)}", caption=f"<b>🎬 ᴍᴏᴠɪᴇ ɴᴀᴍᴇ : {search} ‌‌‌‌‎</b> \n\n <b>🌀 ᴄʜᴀɴɴᴇʟ :[ᴏɴᴀɪʀᴍᴏᴠɪᴇs](https://t.me/joinchat/4-Quex2FaFhjMDM1) \n⚡️ᴘᴏᴡᴇʀᴇᴅ ʙʏ:[ᴏɴᴀɪʀ_ғɪʟᴛᴇʀᵇᵒᵗ](https://t.me/On_air_Filter_bot)</b>", reply_markup=InlineKeyboardMarkup(buttons))

@Client.on_message(filters.text & filters.group & filters.incoming & filters.chat(AUTH_GROUPS) if AUTH_GROUPS else filters.text & filters.group & filters.incoming)
async def group(client, message):
    if re.findall("((^\/|^,|^!|^\.|^[\U0001F600-\U000E007F]).*)", message.text):
        return
    if len(message.text) <= 3:
        kk = await message.reply_text(f"{message.from_user.mention},ɪɴᴄʟᴜᴅᴇ ʏᴇᴀʀ ᴏғ ᴛʜᴇ ᴍᴏᴠɪᴇ. \n\n 𝚜𝚎𝚗𝚝👉 ᴍᴏᴠɪᴇ ɴᴀᴍᴇ & yᴇᴀʀ")
        await asyncio.sleep(10)
        await kk.delete()
        await message.delete() 
    elif 3 < len(message.text) < 45:    
        btn = []

        search = message.text
        result_txt = f"**<b>🎬↳ ᴍᴏᴠɪᴇ ɴᴀᴍᴇ : ‌‌‌‌‎</b>** ‌‌‌‌‎<b>{search}‌‌‌‌‎</b>\n\n**‌‌‌‌╔‎/ʀᴀᴛɪɴɢ‌‌‌‌‎ :** {random.choice(RATING)}\n**╠|ɢᴇɴʀᴇ :** {random.choice(GENRES)}\n**╚\[ᴛᴇʟᴇ ɢʀᴀᴍᴀᴍ](https://t.me/+aZIoNNlskWk4ODg1)\n\n**ᵗʰⁱˢ ᵐˢᵍᵉ ✉️ ᵈᵘʳᵃᵗⁱᵒⁿ 3 ᵐⁱⁿᵘᵗᵉ**"
        resul_txt = f"**<b>🎬↳ ᴍᴏᴠɪᴇ ɴᴀᴍᴇ : ‌‌‌‌‎</b>** ‌‌‌‌‎<b>{search}‌‌‌‌‎</b>\n\n**‌‌‌‌‎╔/ʀᴀᴛɪɴɢ‌‌‌‌‎ :** {random.choice(RATING)}\n**╠|ɢᴇɴʀᴇ :** {random.choice(GENRES)}\n**╚\[ᴛᴇʟᴇ ɢʀᴀᴍᴀᴍ](https://t.me/+aZIoNNlskWk4ODg1)\n\n**ⁱᶠ ʸᵒᵘ ᵈᵒⁿ'ᵗ ˢᵉᵉ ᵗʰᵉ ᶠⁱˡᵉˢ ᵒᶠ ᵗʰᵉ ᵐᵒᵛⁱᵉ ʸᵒᵘ ᵃˢᵏᵉᵈ ᶠᵒʳ 👀 ˡᵒᵒᵏ-ᵃᵗ-ⁿᵉˣᵗ-ᵖᵃᵍᵉ**"
        oam = f"{random.choice(RAT)}"
        oamm = f"{random.choice(RAT)}"
        x = search.split()
        hari = "+".join(x)
        sesna = "_".join(x)

        nyva=BOT.get("username")
        if not nyva:
            botusername=await client.get_me()
            nyva=botusername.username
            BOT["username"]=nyva
        files = await get_filter_results(query=search)
        if files:
            for file in files:
                file_id = file.file_id
                sz = get_size(file.file_size)
                fn = file.file_name[0:24]
                filename = f"{fn}{oam}{sz[0:3]} {sz[-2:]}{oamm}"
                btn.append(
                    [InlineKeyboardButton(text=f"{filename}",callback_data=f"saran#{file_id}")]
                )
        else:            
            buttons = btn
            buttons.append(
                [InlineKeyboardButton(text=f"ɢᴏᴏɢʟᴇ 🍿", url=f"https://google.com/search?q={hari}"),InlineKeyboardButton(text=f"ɪᴍᴅʙ 🍿", url=f"https://www.imdb.com/find?q={hari}")]
            )
            a = await message.reply_photo(photo="https://telegra.ph/file/6a0fea5d018525f7d8ed9.jpg", caption=f"{message.from_user.mention},ᴘᴏssɪʙʟᴇ ᴄᴀᴜsᴇs : 👇🤔\n\n𝟭 sᴘᴇʟʟɪɴɢ ᴍɪsᴛᴀᴋᴇ =- sᴇᴀʀᴄʜ ɪɴ ɢᴏᴏɢʟᴇ ғᴏʀ ᴄᴏʀʀᴇᴄᴛ sᴘᴇʟʟɪɴɢ\n [ᴄʟɪᴄᴋ ʜᴇʀᴇ ᴛᴏ sᴇᴀʀᴄʜ ɪɴ ɢᴏᴏɢʟᴇ](https://www.google.com/)  \n𝟮 ɴᴏᴛ ʀᴇʟᴇᴀsᴇᴅ ʏᴇᴛ \n𝟯, . () ᴅᴏɴᴛ ᴜsᴇ ᴛʜɪꜱ ᴛyᴩᴇ sʏᴍʙᴏʟs \n𝟰 ɴᴏᴛ ɪɴ ᴅᴀᴛᴀʙᴀsᴇ [ʳᵉᵖᵒʳᵗ](https://t.me/movie_requesting_group_rules/12) \n\n **𝙲𝚕𝚒𝚌𝚔 & 𝙲𝚑𝚎𝚌𝚔 𝚝𝚑𝚎 𝚜𝚙𝚎𝚕𝚕𝚒𝚗𝚐** 👇👇", reply_markup=InlineKeyboardMarkup(buttons))
            await message.forward("@S1a2r3a4n")
            await asyncio.sleep(30)
            await a.delete()
            await message.delete()
            return
        if not btn:
            return

        if len(btn) > 6: 
            btns = list(split_list(btn, 6)) 
            keyword = f"{message.chat.id}-{message.message_id}"
            BUTTONS[keyword] = {
                "total" : len(btns),
                "buttons" : btns
            }
        else:
            buttons = btn
            buttons.append(
                [InlineKeyboardButton(text="𝚂𝙴𝙰𝚁𝙲𝙷 𝙸𝙽 𝙿𝙼",callback_data=f"myree#{sesna}"), InlineKeyboardButton("💡close💡", callback_data="close")]
            )
            poster=None
            if API_KEY:
                poster=await get_poster(search)
            if poster:
                a = await message.reply_photo(photo=poster, caption=result_txt, reply_markup=InlineKeyboardMarkup(buttons))
                await asyncio.sleep(180) # second il aanu
                await a.delete()
                await message.delete()
            else:
                ab = await message.reply_photo(photo=f"{random.choice(PHOTO)}", caption=result_txt, reply_markup=InlineKeyboardMarkup(buttons))
                await asyncio.sleep(180)
                await ab.delete()
                await message.delete()
            return

        data = BUTTONS[keyword]
        buttons = data['buttons'][0].copy()

        buttons.append(
            [InlineKeyboardButton(text=f"🎪 Pages 1/{data['total']}🎪",callback_data="pages"),InlineKeyboardButton(text="⇏ɴᴇxᴛ⇏",callback_data=f"next_0_{keyword}")]
        )
        buttons.append(
            [InlineKeyboardButton(text="𝚂𝙴𝙰𝚁𝙲𝙷 𝙸𝙽 𝙿𝙼",callback_data=f"myree#{sesna}")]
        )
        poster=None
        if API_KEY:
            poster=await get_poster(search)
        if poster:
            await message.reply_photo(photo=poster, caption=resul_txt, reply_markup=InlineKeyboardMarkup(buttons))
        else:
            await message.reply_photo(photo=f"{random.choice(PHOTO)}", caption=resul_txt, reply_markup=InlineKeyboardMarkup(buttons))

    else:
        await message.delete()

def get_size(size):
    """Get size in readable format"""

    units = ["Bytes", "ᴋʙ", "ᴍʙ", "ɢʙ", "TB", "PB", "EB"]
    size = float(size)
    i = 0
    while size >= 1024.0 and i < len(units):
        i += 1
        size /= 1024.0
    return "%.2f %s" % (size, units[i])

def split_list(l, n):
    for i in range(0, len(l), n):
        yield l[i:i + n]          



@Client.on_callback_query()
async def cb_handler(client: Client, query: CallbackQuery):
    clicked = query.from_user.id
    try:
        typed = query.message.reply_to_message.from_user.id
    except:
        typed = query.from_user.id
        pass
    if query.data.startswith("saran"):
            ident, file_id = query.data.split("#")
            filedetails = await get_file_details(file_id)
            for files in filedetails:
                title = files.file_name[0:-4]
                size=files.file_size
                f_caption=files.caption
                if CUSTOM_FILE_CAPTION:
                    try:
                        f_caption="{title}",
                    except Exception as e:
                        print(e)
                        f_caption=f_caption
                if f_caption is None:
                    f_caption = f"{title}"
                buttons = [
                    [
                        InlineKeyboardButton('🎪 ɢʀᴏᴜᴘ 2', url='https://t.me/+NY-f484oVqE1NmU1'),
                        InlineKeyboardButton(' 🔍 sᴇᴀʀᴄʜ ғɪʟᴇ', switch_inline_query_current_chat='')
                    ]
                    ]
            
            if (clicked == typed):
                try:  
                    await client.send_cached_media(
                    chat_id=query.from_user.id,
                    file_id=file_id,
                    caption=f"<code>" + title + "</code>""\n\n <b>[𝙼𝚘𝚟𝚒𝚎 ʀᴇϙᴜᴇsᴛɪɴɢ 𝚐𝚛𝚘𝚞𝚙](https://t.me/+aZIoNNlskWk4ODg1)</b>",
                    reply_markup=InlineKeyboardMarkup(buttons)
                    )
                except UserIsBlocked:
                    await query.answer(url=f"http://t.me/On_air_Filter_bot?start=subinps_-_-_-_{file_id}")
                else:
                    await query.answer("ᴄʜᴇcᴋ ᴩᴍ 👀 \n\n file🎬 has 𝚂𝚄𝙲𝙲𝙴𝚂𝚂𝙵𝚄𝙻𝙻𝚈✔️ sent to your pm",show_alert=True)
            else:
                await query.answer(url=f"http://t.me/On_air_Filter_bot?start=subinps_-_-_-_{file_id}")           
    
    elif query.data.startswith("myree"):
            ident, file_name = query.data.split("#")
            await query.answer(url=f"http://t.me/On_air_Filter_bot?start=saran=={file_name}")

    elif (clicked == typed):

        if query.data.startswith("next"):
            ident, index, keyword = query.data.split("_")
            try:
                data = BUTTONS[keyword]
            except KeyError:
                await query.answer("⭕️ You are using this for one of my old message, please send the request again ⭕️.",show_alert=True)
                return

            if int(index) == int(data["total"]) - 2:
                buttons = data['buttons'][int(index)+1].copy()

                buttons.append(
                    [InlineKeyboardButton("⇍ʙᴀᴄᴋ⇍", callback_data=f"back_{int(index)+1}_{keyword}"),InlineKeyboardButton(f"🎪 Pages {int(index)+2}/{data['total']}🎪", callback_data="pages")]
                )
                buttons.append(
                    [InlineKeyboardButton(text="𝚂𝙴𝙰𝚁𝙲𝙷 𝙸𝙽 𝙿𝙼",callback_data=f"myree#")]
                )

                await query.edit_message_reply_markup( 
                    reply_markup=InlineKeyboardMarkup(buttons)
                )
                return
            else:
                buttons = data['buttons'][int(index)+1].copy()

                buttons.append(
                    [InlineKeyboardButton("⇍ʙᴀᴄᴋ⇍", callback_data=f"back_{int(index)+1}_{keyword}"),InlineKeyboardButton(f"🎪{int(index)+2}/{data['total']}🎪", callback_data="pages"),InlineKeyboardButton("⇏ɴᴇxᴛ⇏", callback_data=f"next_{int(index)+1}_{keyword}")]
                )
                buttons.append(
                    [InlineKeyboardButton(text="𝚂𝙴𝙰𝚁𝙲𝙷 𝙸𝙽 𝙿𝙼",callback_data=f"myree#")]
                )

                await query.edit_message_reply_markup( 
                    reply_markup=InlineKeyboardMarkup(buttons)
                )
                return


        elif query.data.startswith("back"):
            ident, index, keyword = query.data.split("_")
            try:
                data = BUTTONS[keyword]
            except KeyError:
                await query.answer("You are using this for one of my old message, please send the request again.",show_alert=True)
                return

            if int(index) == 1:
                buttons = data['buttons'][int(index)-1].copy()

                buttons.append(
                    [InlineKeyboardButton(f"🎪 Pages {int(index)}/{data['total']}🎪", callback_data="pages"),InlineKeyboardButton("⇏ɴᴇxᴛ⇏", callback_data=f"next_{int(index)-1}_{keyword}")]                   
                )
                buttons.append(
                    [InlineKeyboardButton(text="𝚂𝙴𝙰𝚁𝙲𝙷 𝙸𝙽 𝙿𝙼",callback_data=f"myree#")]
                )

                await query.edit_message_reply_markup( 
                    reply_markup=InlineKeyboardMarkup(buttons)
                )
                return   
            else:
                buttons = data['buttons'][int(index)-1].copy()

                buttons.append(
                    [InlineKeyboardButton("⇍ʙᴀᴄᴋ⇍", callback_data=f"back_{int(index)-1}_{keyword}"),InlineKeyboardButton(f"🎪{int(index)}/{data['total']}🎪", callback_data="pages"),InlineKeyboardButton("⇏ɴᴇxᴛ⇏", callback_data=f"next_{int(index)-1}_{keyword}")]
                )
                buttons.append(
                    [InlineKeyboardButton(text="𝚂𝙴𝙰𝚁𝙲𝙷 𝙸𝙽 𝙿𝙼",callback_data=f"myree#")]
                )

                await query.edit_message_reply_markup( 
                    reply_markup=InlineKeyboardMarkup(buttons)
                )
                return
        elif query.data.startswith("report"):
            ident, movie = query.data.split("_")
            try:
                await query.message.edit(text=f"<code>" + movie + "</code>""{query.from_user.mention} [{query.from_user.id}] ", disable_web_page_preview=True)
            await query.answer("𝚂𝚄𝙲𝙲𝙴𝚂𝚂𝙵𝚄𝙻𝙻𝚈 Reported to Admins 👮‍♂️",show_alert=True)
                return
                
        elif query.data == "about":
            await query.answer("🤖ɴᴀᴍᴇ: ᴀᴜᴛᴏ ғɪʟᴛᴇʀ v2.7\n🎪ᴄʀᴇᴀᴛᴏʀ: sᴀʀᴀɴ\n📚ʟᴀɴɢᴜᴀɢᴇ: ᴘʏᴛʜᴏɴ3\n🌀 ʟɪʙʀᴀʀʏ : ᴘʏʀᴏɢʀᴀᴍ ᴀsʏɴᴄɪᴏ 1.13.0",show_alert=True)
        elif query.data == "close":
            await query.message.delete()
        
        elif query.data.startswith("checksub"):
            if AUTH_CHANNEL and not await is_subscribed(client, query):
                await query.answer("🎪ഗ്രൂപ്പിൽ join ചെയ്തതിനു ശേഷം ക്ലിക്ക് ചെയ്യൂ 💐",show_alert=True)
                return
            ident, file_id = query.data.split("#")
            filedetails = await get_file_details(file_id)
            for files in filedetails:
                title = files.file_name
                size=files.file_size
                f_caption=files.caption
                if CUSTOM_FILE_CAPTION:
                    try:
                        f_caption="{title}",
                    except Exception as e:
                        print(e)
                        f_caption=f_caption
                if f_caption is None:
                    f_caption = f"{title}"
                buttons = [
                    [
                        InlineKeyboardButton('🎪 ɢʀᴏᴜᴘ', url='https://t.me/+aZIoNNlskWk4ODg1'),
                        InlineKeyboardButton(' 🔍 sᴇᴀʀᴄʜ ғɪʟᴇ', switch_inline_query_current_chat='')
                    ]
                    ]
                
                await query.answer()
                await client.send_cached_media(
                    chat_id=query.from_user.id,
                    file_id=file_id,
                    caption=f"<b>©[ᵒⁿᵃⁱʳᵐᵒᵛⁱᵉˢ](https://t.me/joinchat/4-Quex2FaFhjMDM1) \n 🎬 file name 👉  </b>""<code>" + title + "</code>""\n\n[𝙼𝚘𝚟𝚒𝚎 ʀᴇϙᴜᴇsᴛɪɴɢ 𝚐𝚛𝚘𝚞𝚙](https://t.me/joinchat/q4xMr02fvA9jNzQ1)",
                    reply_markup=InlineKeyboardMarkup(buttons)
                    ) 


        elif query.data == "pages":
            await query.answer()

    else:
        await query.answer("😊Bro, search your own file, Don't click others Requested files🎬",show_alert=True)
