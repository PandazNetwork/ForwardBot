## 🤖 Simple Telegram Forward Bot

I can forward documents, videos, photos, and animations (GIFs).
Forward your source channel message to this bot. If the source channel is forward-restricted, send the last message link to this bot.

### ✨ Features

- 📤 Forward documents, videos, photos, and GIFs
- 🎬 Support for all video formats (MP4, MKV, AVI, MOV, etc.)
- 🖼️ Support for all image formats (JPG, PNG, WEBP, etc.)
- ⚙️ Customizable file captions
- ⏭️ Skip messages option
- 📊 Real-time progress tracking with percentage
- 🛑 Cancel forwarding anytime
- 📱 Clean and modern UI with buttons
- ⚡ Lightweight and fast

### 📋 Installation
#### Deploy on Heroku
**BEFORE YOU DEPLOY ON HEROKU, YOU SHOULD FORK THE REPO AND CHANGE ITS NAME TO ANYTHING ELSE**<br>
[![Deploy](https://www.herokucdn.com/deploy/button.svg)](https://heroku.com/deploy?template=https://github.com/pandaznetwork/ForwardBot/)</br>

### 🚀 Commands

**Basic Commands:**
```
/start - Start the bot and see welcome message
/help - Show help message with all commands
/id - Get Chat/User ID
```

**Configuration Commands:**
```
/set <channel_id> - Set target channel for forwarding
/skip <number> - Set number of messages to skip
/caption <text> - Set custom file caption
```

**Utility Commands:**
```
/settings - View current configuration
/reset - Clear all your settings
/status - Check if forwarding is active
```

### 💡 How to Use

1. **Set Target Channel:** Use `/set <channel_id>` to set where files will be forwarded
2. **Forward Files:** Forward a message from source channel OR send the last message link
3. **Confirm:** Click "Yes, Forward" to start forwarding
4. **Monitor:** Watch real-time progress with percentage and statistics
5. **Cancel:** Click "Cancel" button anytime to stop forwarding

### 🔧 Environment Variables

| Variable | Description | Default |
|----------|-------------|---------|
| `API_ID` | Your API ID from my.telegram.org | Required |
| `API_HASH` | Your API Hash from my.telegram.org | Required |
| `BOT_TOKEN` | Your bot token from @BotFather | Required |
| `OWNER` | Your Telegram ID | Required |
| `FILE_CAPTION` | Default file caption format | `{file_name}` |
| `PRIVATE_BOT` | Set to True for private bot | False |
| `UPDATES_CHANNEL` | Updates channel link | - |
| `SUPPORT_GROUP` | Support group link | - |
| `DEV_LINK` | Developer contact link | - |

### 📝 Caption Variables

Use these variables in your custom caption:

| Variable | Description |
|----------|-------------|
| `{file_name}` | Original file name |
| `{file_size}` | File size (formatted) |
| `{caption}` | Original file caption |

**Example:** `/caption {file_name} - {file_size} - My Channel`


### 🙏 Credits

- Thanks to [Dan](https://github.com/pyrogram/pyrogram) for the awesome Pyrogram library
- All contributors and support group members

### 📄 License

[![GNU GPLv3 Image](https://www.gnu.org/graphics/gplv3-127x51.png)](http://www.gnu.org/licenses/gpl-3.0.en.html)

You can use, study, share and improve it at your will. Specifically you can redistribute and/or modify it under the terms of the
[GNU General Public License](https://www.gnu.org/licenses/gpl.html) as
published by the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

---

⭐ **Star this repo if you liked it!**
