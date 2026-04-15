from pyrogram import Client, filters, enums
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from info import UPDATES_CHANNEL, SUPPORT_GROUP, DEV_LINK
from script import (
    WELCOME_TEXT, START_GREETING, HELP_TEXT, SETTINGS_TEXT,
    SETTINGS_RESET_SUCCESS, SETTINGS_RESET_ALERT, BUTTON_UPDATES,
    BUTTON_SUPPORT, BUTTON_SETTINGS, BUTTON_HELP, BUTTON_CONTACT,
    BUTTON_RESET_ALL, BUTTON_CLOSE, get_id_text
)


@Client.on_message(filters.private & filters.command(["start"]) & filters.incoming)
async def start(client, message):
    btn = [[
        InlineKeyboardButton(BUTTON_UPDATES, url=UPDATES_CHANNEL),
        InlineKeyboardButton(BUTTON_SUPPORT, url=SUPPORT_GROUP)
    ],[
        InlineKeyboardButton(BUTTON_SETTINGS, callback_data='settings'),
        InlineKeyboardButton(BUTTON_HELP, callback_data='help')
    ],[
        InlineKeyboardButton(BUTTON_CONTACT, url=DEV_LINK)
    ]]
    text = START_GREETING.format(mention=message.from_user.mention, text=WELCOME_TEXT)
    await message.reply(text, reply_markup=InlineKeyboardMarkup(btn))


@Client.on_callback_query(filters.regex(r'^(settings|help)$'))
async def menu_callbacks(client, query):
    user_id = query.from_user.id
    
    if query.data == 'help':
        await query.message.edit(HELP_TEXT)
    
    elif query.data == 'settings':
        from plugins.forward import CHANNEL, CURRENT, CAPTION
        target = CHANNEL.get(user_id, "Not set")
        skip = CURRENT.get(user_id, 0)
        caption = CAPTION.get(user_id, "Default")
        
        caption_display = f"`{caption[:50]}...`" if len(str(caption)) > 50 else f"`{caption}`"
        settings_text = SETTINGS_TEXT.format(target=target, skip=skip, caption=caption_display)
        
        btn = [[
            InlineKeyboardButton(BUTTON_RESET_ALL, callback_data='reset_settings')
        ],[
            InlineKeyboardButton(BUTTON_CLOSE, callback_data='close_menu')
        ]]
        await query.message.edit(settings_text, reply_markup=InlineKeyboardMarkup(btn))


@Client.on_callback_query(filters.regex(r'^(reset_settings|close_menu)$'))
async def settings_callbacks(client, query):
    user_id = query.from_user.id
    
    if query.data == 'reset_settings':
        from plugins.forward import CHANNEL, CURRENT, CAPTION
        CHANNEL.pop(user_id, None)
        CURRENT.pop(user_id, None)
        CAPTION.pop(user_id, None)
        await query.answer(SETTINGS_RESET_ALERT)
        await query.message.edit(SETTINGS_RESET_SUCCESS)
    
    elif query.data == 'close_menu':
        await query.message.delete()


@Client.on_message(filters.command('help'))
async def help_command(client, message):
    await message.reply(HELP_TEXT)


@Client.on_message(filters.command('id'))
async def showid(client, message):
    chat_type = message.chat.type
    if chat_type == enums.ChatType.PRIVATE:
        user_id = message.chat.id
        first = message.from_user.first_name
        last = message.from_user.last_name or "None"
        username = f"@{message.from_user.username}" or "None"
        await message.reply_text(
            get_id_text("private", user_id=user_id, first=first, last=last, username=username),
            quote=True
        )

    elif chat_type in [enums.ChatType.GROUP, enums.ChatType.SUPERGROUP]:
        kwargs = {
            "chat_id": message.chat.id,
            "user_id": message.from_user.id if message.from_user else 'Anonymous',
            "has_reply": message.reply_to_message is not None,
            "has_file": False
        }
        if message.reply_to_message:
            kwargs["replied_user_id"] = message.reply_to_message.from_user.id if message.reply_to_message.from_user else 'Anonymous'
            file_info = get_file_id(message.reply_to_message)
        else:
            file_info = get_file_id(message)
        
        if file_info:
            kwargs["has_file"] = True
            kwargs["message_type"] = file_info.message_type
            kwargs["file_id"] = file_info.file_id
        
        await message.reply_text(get_id_text("group", **kwargs), quote=True)

    elif chat_type == enums.ChatType.CHANNEL:
        await message.reply_text(get_id_text("channel", chat_id=message.chat.id))
