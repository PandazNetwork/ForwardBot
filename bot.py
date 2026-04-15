import logging
from datetime import datetime

from pyrogram import Client, __version__
from pyrogram.raw.all import layer
from pyrogram.types import BotCommand
from info import API_ID, API_HASH, BOT_TOKEN
from typing import Union, Optional, AsyncGenerator
from pyrogram import types
from info import OWNER
from script import BOT_RESTARTED

class Bot(Client):
    def __init__(self):
        super().__init__(
            name='Forward_Bot',
            api_id=API_ID,
            api_hash=API_HASH,
            bot_token=BOT_TOKEN,
            workers=50,
            plugins={"root": "plugins"},
            sleep_threshold=5
        )
    

    async def start(self):
        await super().start()
        me = await self.get_me()
        restart_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        
        # Log restart with timestamp
        logging.info(f"🤖 @{me.username} Started at {restart_time}!")
        
        # Set bot commands
        commands = [
            BotCommand("start", "Start the bot"),
            BotCommand("help", "Show help message"),
            BotCommand("id", "Get Chat/User ID"),
            BotCommand("set", "Set target channel"),
            BotCommand("skip", "Set messages to skip"),
            BotCommand("caption", "Set custom caption"),
            BotCommand("settings", "View configuration"),
            BotCommand("reset", "Clear all settings"),
            BotCommand("status", "Check forwarding status")
        ]
        try:
            await self.set_bot_commands(commands)
            logging.info("✅ Bot commands set successfully!")
        except Exception as e:
            logging.error(f"❌ Failed to set bot commands: {e}")
        
        # Send detailed restart notification to owner
        restart_msg = f"""{BOT_RESTARTED}

📊 **Bot Details:**
🤖 **Bot Username:** @{me.username}
🆔 **Bot ID:** `{me.id}`
👤 **First Name:** {me.first_name}
📅 **Restart Time:** `{restart_time}`
📚 **Pyrogram Version:** `{__version__}`
🔧 **Layer:** `{layer}`"""
        
        try:
            await self.send_message(OWNER, restart_msg)
            logging.info(f"✅ Restart notification sent to owner: {OWNER}")
        except Exception as e:
            logging.error(f"❌ Failed to send restart notification: {e}")

    async def stop(self, *args):
        await super().stop()
        logging.info("Bot stopped. Bye.")
    
    async def iter_messages(self, chat_id: Union[int, str], limit: int, offset: int = 0) -> Optional[AsyncGenerator["types.Message", None]]:
        """Iterate through a chat sequentially.
        This convenience method does the same as repeatedly calling :meth:`~pyrogram.Client.get_messages` in a loop, thus saving
        you from the hassle of setting up boilerplate code. It is useful for getting the whole chat messages with a
        single call.
        Parameters:
            chat_id (``int`` | ``str``):
                Unique identifier (int) or username (str) of the target chat.
                For your personal cloud (Saved Messages) you can simply use "me" or "self".
                For a contact that exists in your Telegram address book you can use his phone number (str).
                
            limit (``int``):
                Identifier of the last message to be returned.
                
            offset (``int``, *optional*):
                Identifier of the first message to be returned.
                Defaults to 0.
        Returns:
            ``Generator``: A generator yielding :obj:`~pyrogram.types.Message` objects.
        Example:
            .. code-block:: python
                for message in app.iter_messages("pyrogram", 1, 15000):
                    print(message.text)
        """
        current = offset
        while True:
            new_diff = min(200, limit - current)
            if new_diff <= 0:
                return
            messages = await self.get_messages(chat_id, list(range(current, current+new_diff+1)))
            for message in messages:
                yield message
                current += 1



app = Bot()
app.run()
