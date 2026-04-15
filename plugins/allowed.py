from pyrogram import Client, filters
from pyrogram.types import Message
from info import PRIVATE_BOT, OWNER, UPDATES_CHANNEL, DEV_LINK
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from script import ACCESS_DENIED, BUTTON_UPDATES, BUTTON_CONTACT


async def owner(_, client, message: Message):
    if PRIVATE_BOT:
        return message.from_user.id != OWNER

allowed_user = filters.create(owner)

@Client.on_message(filters.private & allowed_user & filters.incoming)
async def not_owner(bot, message):
    btn = [[
        InlineKeyboardButton(BUTTON_UPDATES, url=UPDATES_CHANNEL)
    ],[
        InlineKeyboardButton(BUTTON_CONTACT, url=DEV_LINK)
    ]]
    await message.reply(ACCESS_DENIED, reply_markup=InlineKeyboardMarkup(btn))
