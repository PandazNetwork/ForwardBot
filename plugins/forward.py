import asyncio
import re
import logging
from pyrogram import Client, filters, enums
from pyrogram.errors import FloodWait
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from info import FILE_CAPTION
from script import (
    FORWARD_CONFIRMATION, FORWARD_STARTING, FORWARD_CANCELLING,
    FORWARD_CANCELLED, FORWARD_COMPLETED, FORWARD_FAILED,
    FORWARD_PROCESSING, BUTTON_YES_FORWARD, BUTTON_SETTINGS,
    BUTTON_CLOSE, BUTTON_CANCEL, BUTTON_RESET_ALL,
    SKIP_SET_SUCCESS, SKIP_MISSING_NUMBER, SKIP_INVALID_NUMBER,
    SKIP_NEGATIVE_NUMBER, TARGET_SET_SUCCESS, TARGET_MISSING_ID,
    TARGET_INVALID_ID, TARGET_NOT_CHANNEL, TARGET_NOT_ADMIN,
    CAPTION_SET_SUCCESS, CAPTION_MISSING_TEXT, ERROR_INVALID_LINK,
    ERROR_GET_CHAT, ERROR_ONLY_CHANNELS, ERROR_TARGET_NOT_SET,
    ERROR_WAIT_PROCESS, ERROR_CLOSED, SETTINGS_TEXT,
    SETTINGS_RESET_SUCCESS, SETTINGS_RESET_ALERT, STATUS_FORWARDING,
    STATUS_IDLE
)
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
            return await query.answer(ERROR_WAIT_PROCESS, show_alert=True)

        msg = query.message
        await msg.edit(FORWARD_STARTING)
        try:
            chat = int(chat)
        except:
            pass
        await forward_files(int(lst_msg_id), chat, msg, bot, query.from_user.id)

    elif ident == 'close':
        await query.answer(ERROR_CLOSED)
        await query.message.delete()

    elif ident == 'cancel':
        await query.message.edit(FORWARD_CANCELLING)
        CANCEL[query.from_user.id] = True


@Client.on_message((filters.forwarded | (filters.regex("(https://)?(t\.me/|telegram\.me/|telegram\.dog/)(c/)?(\d+|[a-zA-Z_0-9]+)/(\d+)$")) & filters.text) & filters.private & filters.incoming)
async def send_for_forward(bot, message):
    if message.text:
        regex = re.compile("(https://)?(t\.me/|telegram\.me/|telegram\.dog/)(c/)?(\d+|[a-zA-Z_0-9]+)/(\d+)$")
        match = regex.match(message.text)
        if not match:
            return await message.reply(ERROR_INVALID_LINK)
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
        return await message.reply(ERROR_GET_CHAT.format(error=e))

    if source_chat.type != enums.ChatType.CHANNEL:
        return await message.reply(ERROR_ONLY_CHANNELS)

    target_chat_id = CHANNEL.get(message.from_user.id)
    if not target_chat_id:
        return await message.reply(ERROR_TARGET_NOT_SET)

    try:
        target_chat = await bot.get_chat(target_chat_id)
    except Exception as e:
        return await message.reply(ERROR_GET_CHAT.format(error=e))

    skip = CURRENT.get(message.from_user.id, 0)
    caption = CAPTION.get(message.from_user.id, FILE_CAPTION)
    
    caption_display = f"`{caption[:50]}...`" if len(str(caption)) > 50 else f"`{caption}`"
    buttons = [[
        InlineKeyboardButton(BUTTON_YES_FORWARD, callback_data=f'forward#yes#{chat_id}#{last_msg_id}'),
        InlineKeyboardButton(BUTTON_SETTINGS, callback_data='settings')
    ],[
        InlineKeyboardButton(BUTTON_CLOSE, callback_data=f'forward#close#{chat_id}#{last_msg_id}')
    ]]
    
    confirm_text = FORWARD_CONFIRMATION.format(
        source=source_chat.title,
        target=target_chat.title,
        skip=skip,
        total=last_msg_id,
        caption=caption_display
    )
    
    await message.reply(confirm_text, reply_markup=InlineKeyboardMarkup(buttons))


@Client.on_message(filters.private & filters.command(['skip']))
async def set_skip_number(bot, message):
    try:
        _, skip = message.text.split(" ", 1)
    except:
        return await message.reply(SKIP_MISSING_NUMBER)
    try:
        skip = int(skip)
        if skip < 0:
            return await message.reply(SKIP_NEGATIVE_NUMBER)
    except:
        return await message.reply(SKIP_INVALID_NUMBER)
    CURRENT[message.from_user.id] = skip
    await message.reply(SKIP_SET_SUCCESS.format(skip=skip))


@Client.on_message(filters.private & filters.command(['set']))
async def set_target_channel(bot, message):
    try:
        _, chat_id = message.text.split(" ", 1)
    except:
        return await message.reply(TARGET_MISSING_ID)
    try:
        chat_id = int(chat_id)
    except:
        return await message.reply(TARGET_INVALID_ID)

    try:
        chat = await bot.get_chat(chat_id)
    except Exception as e:
        return await message.reply(TARGET_NOT_ADMIN.format(error=e))
    if chat.type != enums.ChatType.CHANNEL:
        return await message.reply(TARGET_NOT_CHANNEL)
    CHANNEL[message.from_user.id] = int(chat.id)
    await message.reply(TARGET_SET_SUCCESS.format(title=chat.title))


@Client.on_message(filters.private & filters.command(['caption']))
async def set_caption(bot, message):
    try:
        caption = message.text.split(" ", 1)[1]
    except:
        return await message.reply(CAPTION_MISSING_TEXT)
    CAPTION[message.from_user.id] = caption
    await message.reply(CAPTION_SET_SUCCESS.format(caption=caption))


@Client.on_message(filters.private & filters.command(['settings']))
async def show_settings(bot, message):
    user_id = message.from_user.id
    target = CHANNEL.get(user_id, "Not set")
    skip = CURRENT.get(user_id, 0)
    caption = CAPTION.get(user_id, "Default")
    
    caption_display = f"`{caption[:50]}...`" if len(str(caption)) > 50 else f"`{caption}`"
    settings_text = SETTINGS_TEXT.format(target=target, skip=skip, caption=caption_display)
    
    btn = [[
        InlineKeyboardButton(BUTTON_RESET_ALL, callback_data='reset_settings')
    ]]
    await message.reply(settings_text, reply_markup=InlineKeyboardMarkup(btn))


@Client.on_message(filters.private & filters.command(['reset']))
async def reset_settings(bot, message):
    user_id = message.from_user.id
    CHANNEL.pop(user_id, None)
    CURRENT.pop(user_id, None)
    CAPTION.pop(user_id, None)
    await message.reply(SETTINGS_RESET_SUCCESS)


@Client.on_message(filters.private & filters.command(['status']))
async def show_status(bot, message):
    user_id = message.from_user.id
    is_forwarding = FORWARDING.get(user_id, False)
    
    status_text = STATUS_FORWARDING if is_forwarding else STATUS_IDLE
    
    await message.reply(status_text)
    
    
    
async def forward_files(lst_msg_id, chat, msg, bot, user_id):
    current = CURRENT.get(user_id, 0)
    forwarded = 0
    deleted = 0
    unsupported = 0
    fetched = 0
    CANCEL[user_id] = False
    FORWARDING[user_id] = True

    try:
        async for message in bot.iter_messages(chat, lst_msg_id, CURRENT.get(user_id, 0)):
            if CANCEL.get(user_id):
                await msg.edit(FORWARD_CANCELLED)
                break
            current += 1
            fetched += 1
            if current % 20 == 0:
                percentage = round((current / lst_msg_id) * 100, 1)
                btn = [[
                    InlineKeyboardButton(BUTTON_CANCEL, callback_data=f'forward#cancel#{chat}#{lst_msg_id}')
                ]]
                progress_text = FORWARD_PROCESSING.format(
                    percentage=percentage,
                    total=lst_msg_id,
                    completed=current,
                    forwarded=forwarded,
                    deleted=deleted,
                    unsupported=unsupported
                )
                await msg.edit_text(text=progress_text, reply_markup=InlineKeyboardMarkup(btn))
            if message.empty:
                deleted += 1
                continue
            elif not message.media:
                unsupported += 1
                continue
            elif message.media not in [enums.MessageMediaType.DOCUMENT, enums.MessageMediaType.VIDEO, enums.MessageMediaType.PHOTO, enums.MessageMediaType.ANIMATION]:
                unsupported += 1
                continue
            media = getattr(message, message.media.value, None)
            if not media:
                unsupported += 1
                continue
            # Allow all image formats, all video formats, and documents
            if message.media == enums.MessageMediaType.PHOTO:
                # All photos are allowed
                pass
            elif message.media == enums.MessageMediaType.ANIMATION:
                # All GIFs/animations are allowed
                pass
            elif message.media == enums.MessageMediaType.VIDEO:
                # All video formats are allowed
                pass
            elif message.media == enums.MessageMediaType.DOCUMENT:
                # All documents are allowed
                pass
            else:
                unsupported += 1
                continue
            try:
                caption_text = CAPTION.get(user_id).format(file_name=media.file_name, file_size=get_size(media.file_size), caption=message.caption) if CAPTION.get(user_id) else FILE_CAPTION.format(file_name=media.file_name, file_size=get_size(media.file_size), caption=message.caption)
                await bot.send_cached_media(
                    chat_id=CHANNEL.get(user_id),
                    file_id=media.file_id,
                    caption=caption_text
                )
            except FloodWait as e:
                await asyncio.sleep(e.value)
                caption_text = CAPTION.get(user_id).format(file_name=media.file_name, file_size=get_size(media.file_size), caption=message.caption) if CAPTION.get(user_id) else FILE_CAPTION.format(file_name=media.file_name, file_size=get_size(media.file_size), caption=message.caption)
                await bot.send_cached_media(
                    chat_id=CHANNEL.get(user_id),
                    file_id=media.file_id,
                    caption=caption_text
                )
            forwarded += 1
            await asyncio.sleep(1)
    except Exception as e:
        logger.exception(e)
        await msg.reply(FORWARD_FAILED.format(error=e))
    else:
        percentage = 100.0
        complete_text = FORWARD_COMPLETED.format(
            percentage=percentage,
            total=lst_msg_id,
            completed=current,
            fetched=fetched,
            forwarded=forwarded,
            deleted=deleted,
            unsupported=unsupported
        )
        await msg.edit(complete_text)
        FORWARDING[user_id] = False


def get_size(size):
    units = ["Bytes", "KB", "MB", "GB", "TB", "PB", "EB"]
    size = float(size)
    i = 0
    while size >= 1024.0 and i < len(units):
        i += 1
        size /= 1024.0
    return "%.2f %s" % (size, units[i])
