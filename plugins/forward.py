import asyncio
import re
import logging
from pyrogram import Client, filters, enums
from pyrogram.errors import FloodWait
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from info import FILE_CAPTION
logger = logging.getLogger(__name__)

CURRENT = {}
CHANNEL = {}
CANCEL = {}
FORWARDING = {}
CAPTION = {}

@Client.on_callback_query(filters.regex(r'^forward'))
async def forward(bot, query):
    _, ident, chat, lst_msg_id = query.data.split("#")
    if ident == 'yes':
        if FORWARDING.get(query.from_user.id):
            return await query.answer('Wait until previous process complete.', show_alert=True)

        msg = query.message
        await msg.edit('Starting Forwarding...')
        try:
            chat = int(chat)
        except:
            chat = chat
        await forward_files(int(lst_msg_id), chat, msg, bot, query.from_user.id)

    elif ident == 'close':
        await query.answer("Okay!")
        await query.message.delete()

    elif ident == 'cancel':
        await query.message.edit("Trying to cancel forwarding...")
        CANCEL[query.from_user.id] = True


@Client.on_message((filters.forwarded | (filters.regex("(https://)?(t\.me/|telegram\.me/|telegram\.dog/)(c/)?(\d+|[a-zA-Z_0-9]+)/(\d+)$")) & filters.text) & filters.private & filters.incoming)
async def send_for_forward(bot, message):
    if message.text:
        regex = re.compile("(https://)?(t\.me/|telegram\.me/|telegram\.dog/)(c/)?(\d+|[a-zA-Z_0-9]+)/(\d+)$")
        match = regex.match(message.text)
        if not match:
            return await message.reply('Invalid link for forward!')
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
        return await message.reply("You not added target channel.\nAdd using /set_channel command.")

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
    await message.reply(f"Source Channel: {source_chat.title}\nTarget Channel: {target_chat.title}\nSkip messages: <code>{skip}</code>\nTotal Messages: <code>{last_msg_id}</code>\nFile Caption: {caption}\n\nDo you want to forward?", reply_markup=InlineKeyboardMarkup(buttons))


@Client.on_message(filters.private & filters.command(['set_skip']))
async def set_skip_number(bot, message):
    try:
        _, skip = message.text.split(" ")
    except:
        return await message.reply("Give me a skip number.")
    try:
        skip = int(skip)
    except:
        return await message.reply("Only support in numbers.")
    CURRENT[message.from_user.id] = int(skip)
    await message.reply(f"Successfully set <code>{skip}</code> skip number.")


@Client.on_message(filters.private & filters.command(['set_channel']))
async def set_target_channel(bot, message):
    try:
        _, chat_id = message.text.split(" ")
    except:
        return await message.reply("Give me a target channel ID")
    try:
        chat_id = int(chat_id)
    except:
        return await message.reply("Give me a valid ID")

    try:
        chat = await bot.get_chat(chat_id)
    except:
        return await message.reply("Make me a admin in your target channel.")
    if chat.type != enums.ChatType.CHANNEL:
        return await message.reply("I can set channels only.")
    CHANNEL[message.from_user.id] = int(chat.id)
    await message.reply(f"Successfully set {chat.title} target channel.")


@Client.on_message(filters.private & filters.command(['set_caption']))
async def set_caption(bot, message):
    try:
        caption = message.text.split(" ", 1)[1]
    except:
        return await message.reply("Give me a caption.")
    CAPTION[message.from_user.id] = caption
    await message.reply(f"Successfully set file caption.\n\n{caption}")
    
    
    
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
                await msg.edit(f"Successfully Forward Canceled!")
                break
            current += 1
            fetched += 1
            if current % 20 == 0:
                btn = [[
                    InlineKeyboardButton('CANCEL', callback_data=f'forward#cancel#{chat}#{lst_msg_id}')
                ]]
                await msg.edit_text(text=f"Forward Processing...\n\nTotal Messages: <code>{lst_msg_id}</code>\nCompleted Messages: <code>{current} / {lst_msg_id}</code>\nForwarded Files: <code>{forwarded}</code>\nDeleted Messages Skipped: <code>{deleted}</code>\nUnsupported Files Skipped: <code>{unsupported}</code>", reply_markup=InlineKeyboardMarkup(btn))
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
        await msg.reply(f"Forward Canceled!\n\nError - {e}")
    else:
        await msg.edit(f'Forward Completed!\n\nTotal Messages: <code>{lst_msg_id}</code>\nCompleted Messages: <code>{current} / {lst_msg_id}</code>\nFetched Messages: <code>{fetched}</code>\nTotal Forwarded Files: <code>{forwarded}</code>\nDeleted Messages Skipped: <code>{deleted}</code>\nUnsupported Files Skipped: <code>{unsupported}</code>')
        FORWARDING[user_id] = False


def get_size(size):
    units = ["Bytes", "KB", "MB", "GB", "TB", "PB", "EB"]
    size = float(size)
    i = 0
    while size >= 1024.0 and i < len(units):
        i += 1
        size /= 1024.0
    return "%.2f %s" % (size, units[i])
