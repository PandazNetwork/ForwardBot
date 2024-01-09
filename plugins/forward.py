import asyncio
import re
import logging
from pyrogram import Client, filters, enums
from pyrogram.errors import FloodWait
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from info import FILE_CAPTION
logger = logging.getLogger(__name__)

@Client.on_callback_query(filters.regex(r'^forward'))
async def forward(bot, query):
    _, ident, chat, lst_msg_id = query.data.split("#")
    if ident == 'yes':
        if FORWARDING.get(query.from_user.id):
            return await query.answer('ᴡᴀɪᴛ ᴜɴᴛɪʟ ᴘʀᴇᴠɪᴏᴜs ᴘʀᴏᴄᴇss ᴄᴏᴍᴘʟᴇᴛᴇ.', show_alert=True)

        msg = query.message
        await msg.edit('ғᴏʀᴡᴀʀᴅɪɴɢ sᴛᴀʀᴛᴇᴅ...')
        try:
            chat = int(chat)
        except:
            chat = chat
        await forward_files(int(lst_msg_id), chat, msg, bot, query.from_user.id)

    elif ident == 'close':
        await query.answer("Okay!")
        await query.message.delete()

    elif ident == 'cancel':
        await query.message.edit("sᴛᴏᴘᴘɪɴɢ ғᴏʀᴡᴀʀᴅ ᴛᴀsᴋ...")
        CANCEL[query.from_user.id] = True


@Client.on_message((filters.forwarded | (filters.regex("(https://)?(t\.me/|telegram\.me/|telegram\.dog/)(c/)?(\d+|[a-zA-Z_0-9]+)/(\d+)$")) & filters.text) & filters.private & filters.incoming)
async def send_for_forward(bot, message):
    if message.text:
        regex = re.compile("(https://)?(t\.me/|telegram\.me/|telegram\.dog/)(c/)?(\d+|[a-zA-Z_0-9]+)/(\d+)$")
        match = regex.match(message.text)
        if not match:
            return await message.reply('ᴘʟᴇᴀsᴇ ᴀᴅᴅ ᴠᴀʟɪᴅ ʟɪɴᴋ ᴛᴏ sᴛᴀʀᴛ ғᴏʀᴡᴀᴅɪɴɢ...')
        chat_id = match.group(4)
        last_msg_id = int(match.group(5))
        if chat_id.isnumeric():
            chat_id  = int(("-100" + chat_id))
    elif message.forward_from_chat.type == enums.ChatType.CHANNEL:
        last_msg_id = message.forward_from_message_id
        chat_id = message.forward_from_chat.username or message.forward_from_chat.id
    else:
        return

    try:
        source_chat = await bot.get_chat(chat_id)
    except Exception as e:
        return await message.reply(f'Error - {e}')

    if source_chat.type != enums.ChatType.CHANNEL:
        return await message.reply("I can forward only channels.")

    target_chat_id = CHANNEL.get(message.from_user.id)
    if not target_chat_id:
        return await message.reply("ᴛᴀʀɢᴇᴛ ᴄʜᴀɴɴᴇʟ ɴᴏᴛ ғᴏᴜɴᴅ.\nᴀᴅᴅ ᴜsɪɴɢ /set_channel ᴄᴏᴍᴍᴀɴᴅ.\nғᴏʀ ᴇxᴀᴍᴘʟᴇ - /set_channel -100xxxxxxxxx")

    try:
        target_chat = await bot.get_chat(target_chat_id)
    except Exception as e:
        return await message.reply(f'Error - {e}')

    skip = CURRENT.get(message.from_user.id)
    if skip:
        skip = skip
    else:
        skip = 0

    caption = CAPTION.get(message.from_user.id)
    if caption:
        caption = caption
    else:
        caption = FILE_CAPTION
    # last_msg_id is same to total messages
    buttons = [[
        InlineKeyboardButton('YES', callback_data=f'forward#yes#{chat_id}#{last_msg_id}')
    ],[
        InlineKeyboardButton('CLOSE', callback_data=f'forward#close#{chat_id}#{last_msg_id}')
    ]]
    await message.reply(f"• sᴏᴜʀᴄᴇ ᴄʜᴀɴɴᴇʟ: {source_chat.title}\n• ᴛᴀʀɢᴇᴛ ᴄʜᴀɴɴᴇʟ: {target_chat.title}\n• sᴋɪᴘ ᴍᴇssᴀɢᴇs: <code>{skip}</code>\n• ᴛᴏᴛᴀʟ ᴍᴇssᴀɢᴇs: <code>{last_msg_id}</code>\n• ғɪʟᴇ ᴄᴀᴘᴛɪᴏɴ: {caption}\n\nᴅᴏ ʏᴏᴜ ᴡᴀɴᴛ ᴛᴏ ғᴏʀᴡᴀʀᴅ?", reply_markup=InlineKeyboardMarkup(buttons))


@Client.on_message(filters.private & filters.command(['set_skip']))
async def set_skip_number(bot, message):
    try:
        _, skip = message.text.split(" ")
    except:
        return await message.reply("/set_skip 4xxx")
    try:
        skip = int(skip)
    except:
        return await message.reply("ᴏɴʟʏ sᴜᴘᴘᴏʀᴛ ɪɴ ɴᴜᴍʙᴇʀs.")
    CURRENT[message.from_user.id] = int(skip)
    await message.reply(f"Successfully set <code>{skip}</code> skip number.")


@Client.on_message(filters.private & filters.command(['set_channel']))
async def set_target_channel(bot, message):
    try:
        _, chat_id = message.text.split(" ")
    except:
        return await message.reply("/set_channel -100xxxxxxxx")
    try:
        chat_id = int(chat_id)
    except:
        return await message.reply("ɪᴅ ɴᴏᴛ ᴠᴀʟɪᴅ")

    try:
        chat = await bot.get_chat(chat_id)
    except:
        return await message.reply("ʙᴏᴛ ɪs ɴᴏᴛ ᴀᴅᴍɪɴ ɪɴ ᴛᴀʀɢᴇᴛ ᴄʜᴀɴɴᴇʟ")
    if chat.type != enums.ChatType.CHANNEL:
        return await message.reply("ᴏɴʟʏ ᴄʜᴀɴɴᴇʟs ᴀʟʟᴏᴡᴇᴅ")
    CHANNEL[message.from_user.id] = int(chat.id)
    await message.reply(f"Successfully set {chat.title} target channel.")


@Client.on_message(filters.private & filters.command(['set_caption']))
async def set_caption(bot, message):
    try:
        caption = message.text.split(" ", 1)[1]
    except:
        return await message.reply("Give me a caption.")
    CAPTION[message.from_user.id] = caption
    await message.reply(f"ғɪʟᴇ ᴄᴀᴘᴛɪᴏɴ ᴜᴘᴅᴀᴛᴇᴅ sᴜᴄᴄᴇssғᴜʟʟʏ.\n\n{caption}")
    
    
    
async def forward_files(lst_msg_id, chat, msg, bot, user_id):
    current = CURRENT.get(user_id) if CURRENT.get(user_id) else 0
    forwarded = 0
    deleted = 0
    unsupported = 0
    fetched = 0
    CANCEL[user_id] = False
    FORWARDING[user_id] = True
    # lst_msg_id is same to total messages

    try:
        async for message in bot.iter_messages(chat, lst_msg_id, CURRENT.get(user_id) if CURRENT.get(user_id) else 0):
            if CANCEL.get(user_id):
                await msg.edit(f"ғᴏʀᴡᴀʀᴅ ᴄᴀɴᴄᴇʟᴇᴅ sᴜᴄᴄᴇssғᴜʟʟʏ...")
                break
            current += 1
            fetched += 1
            if current % 20 == 0:
                btn = [[
                    InlineKeyboardButton('CANCEL', callback_data=f'forward#cancel#{chat}#{lst_msg_id}')
                ]]
                await msg.edit_text(text=f"ғᴏʀᴡᴀʀᴅ ᴜɴᴅᴇʀ ᴘʀᴏᴄᴇss...\n\n• ᴛᴏᴛᴀʟ ᴍᴇssᴀɢᴇs: <code>{lst_msg_id}</code>\n• ᴄᴏᴍᴘʟᴇᴛᴇᴅ ᴍᴇssᴀɢᴇs: <code>{current} / {lst_msg_id}</code>\n• ғᴏʀᴡᴀʀᴅᴇᴅ ғɪʟᴇs: <code>{forwarded}</code>\n• ᴅᴇʟᴇᴛᴇᴅ ᴍᴇssᴀɢᴇs sᴋɪᴘᴘᴇᴅ: <code>{deleted}</code>\n• ᴜɴsᴜᴘᴘᴏʀᴛᴇᴅ ғɪʟᴇs sᴋɪᴘᴘᴇᴅ: <code>{unsupported}</code>", reply_markup=InlineKeyboardMarkup(btn))
            if message.empty:
                deleted += 1
                continue
            elif not message.media:
                unsupported += 1
                continue
            elif message.media not in [enums.MessageMediaType.DOCUMENT, enums.MessageMediaType.VIDEO]:  # Non documents and videos files skipping
                unsupported += 1
                continue
            media = getattr(message, message.media.value, None)
            if not media:
                unsupported += 1
                continue
            elif media.mime_type not in ['video/mp4', 'video/x-matroska']:  # Non mp4 and mkv files types skipping
                unsupported += 1
                continue
            try:
                await bot.send_cached_media(
                    chat_id=CHANNEL.get(user_id),
                    file_id=media.file_id,
                    caption=CAPTION.get(user_id).format(file_name=media.file_name, file_size=get_size(media.file_size), caption=message.caption) if CAPTION.get(user_id) else FILE_CAPTION.format(file_name=media.file_name, file_size=get_size(media.file_size), caption=message.caption)
                )
            except FloodWait as e:
                await asyncio.sleep(e.value)  # Wait "value" seconds before continuing
                await bot.send_cached_media(
                    chat_id=CHANNEL.get(user_id),
                    file_id=media.file_id,
                    caption=CAPTION.get(user_id).format(file_name=media.file_name, file_size=get_size(media.file_size), caption=message.caption) if CAPTION.get(user_id) else FILE_CAPTION.format(file_name=media.file_name, file_size=get_size(media.file_size), caption=message.caption)
                )
            forwarded += 1
            await asyncio.sleep(1)
    except Exception as e:
        logger.exception(e)
        await msg.reply(f"ғᴏʀᴡᴀʀᴅ ᴄᴀɴᴄᴇʟᴇᴅ!\n\n⚠️ Error - {e}")
    else:
        await msg.edit(f'ғᴏʀᴡᴀʀᴅ ᴄᴏᴍᴘʟᴇᴛᴇᴅ!\n\n• ᴛᴏᴛᴀʟ ᴍᴇssᴀɢᴇs: <code>{lst_msg_id}</code>\n• ᴄᴏᴍᴘʟᴇᴛᴇᴅ ᴍᴇssᴀɢᴇs: <code>{current} / {lst_msg_id}</code>\n• ғᴇᴛᴄʜᴇᴅ ᴍᴇssᴀɢᴇs: <code>{fetched}</code>\n• ᴛᴏᴛᴀʟ ғᴏʀᴡᴀʀᴅᴇᴅ ғɪʟᴇs: <code>{forwarded}</code>\n• ᴅᴇʟᴇᴛᴇᴅ ᴍᴇssᴀɢᴇs sᴋɪᴘᴘᴇᴅ: <code>{deleted}</code>\n• ᴜɴsᴜᴘᴘᴏʀᴛᴇᴅ ғɪʟᴇs sᴋɪᴘᴘᴇᴅ: <code>{unsupported}</code>')
        FORWARDING[user_id] = False


def get_size(size):
    units = ["Bytes", "KB", "MB", "GB", "TB", "PB", "EB"]
    size = float(size)
    i = 0
    while size >= 1024.0 and i < len(units):
        i += 1
        size /= 1024.0
    return "%.2f %s" % (size, units[i])
