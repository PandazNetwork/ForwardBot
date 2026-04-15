# -*- coding: utf-8 -*-
# Bot Message Strings
# All message texts for the Telegram Forward Bot

# ==================== START MESSAGES ====================

WELCOME_TEXT = """🤖 **Welcome to Forward Bot!**

I can forward documents, videos, photos, and animations (GIFs).

📋 **How to use:**
• Forward a message from your source channel to this bot
• If the source channel is forward-restricted, send the last message link

📝 **Available Commands:**
`/id` - Get Chat/User ID
`/skip` - Set number of messages to skip
`/set` - Set target channel
`/caption` - Set custom file caption
`/settings` - View current configuration
`/reset` - Clear your settings
`/help` - Show this help message

💡 **Caption Formats:**
`{file_name}` - File name
`{file_size}` - File size
`{caption}` - Default file caption

⚠️ **Note:** This bot doesn't use a database. Your details are not saved permanently. If the bot restarts, your forwarding will stop and settings will be cleared."""

START_GREETING = "👋 Hello {mention},\n\n{text}"

# ==================== HELP MESSAGES ====================

HELP_TEXT = """📚 **Help & Commands**

**Basic Commands:**
`/start` - Start the bot
`/help` - Show this help message

**Configuration Commands:**
`/set <channel_id>` - Set target channel
`/skip <number>` - Set messages to skip
`/caption <text>` - Set custom caption

**Utility Commands:**
`/id` - Get Chat/User ID
`/settings` - View current configuration
`/reset` - Clear all your settings

**How to Forward:**
1. Set your target channel using `/set`
2. Forward a message from source channel OR send the last message link
3. Confirm forwarding when prompted

**Caption Variables:**
`{file_name}` - Original file name
`{file_size}` - File size
`{caption}` - Original caption"""

# ==================== SETTINGS MESSAGES ====================

SETTINGS_TEXT = """⚙️ **Current Settings**

🎯 **Target Channel:** `{target}`
⏭️ **Skip Messages:** `{skip}`
📝 **Custom Caption:** `{caption}`

Use commands below to update settings:"""

SETTINGS_RESET_SUCCESS = "✅ **All settings have been cleared!**\n\nUse `/set`, `/skip`, and `/caption` to configure again."

SETTINGS_RESET_ALERT = "✅ Settings reset successfully!"

# ==================== STATUS MESSAGES ====================

STATUS_FORWARDING = "🔄 **Status:** Forwarding in progress..."

STATUS_IDLE = "✅ **Status:** Idle - No active forwarding"

# ==================== FORWARD MESSAGES ====================

FORWARD_CONFIRMATION = """📋 **Forward Confirmation**

📥 **Source Channel:** {source}
📤 **Target Channel:** {target}
⏭️ **Skip Messages:** `{skip}`
📊 **Total Messages:** `{total}`
📝 **File Caption:** `{caption}`

Do you want to start forwarding?"""

FORWARD_STARTING = "🚀 Starting Forwarding..."

FORWARD_CANCELLING = "🛑 Cancelling forwarding..."

FORWARD_CANCELLED = "🛑 **Forwarding Cancelled!**"

FORWARD_COMPLETED = """✅ **Forward Completed!**

📊 **Progress:** `{percentage}%`
📬 **Total Messages:** `{total}`
✅ **Completed:** `{completed} / {total}`
📥 **Fetched Messages:** `{fetched}`
📤 **Total Forwarded:** `{forwarded}`
🗑️ **Deleted Skipped:** `{deleted}`
⚠️ **Unsupported Skipped:** `{unsupported}`"""

FORWARD_FAILED = "❌ **Forwarding Failed!**\n\nError: `{error}`"

FORWARD_PROCESSING = """🔄 **Forward Processing...**

📊 **Progress:** `{percentage}%`
📬 **Total Messages:** `{total}`
✅ **Completed:** `{completed} / {total}`
📤 **Forwarded Files:** `{forwarded}`
🗑️ **Deleted Skipped:** `{deleted}`
⚠️ **Unsupported Skipped:** `{unsupported}`"""

# ==================== COMMAND RESPONSES ====================

ID_PRIVATE = "★ First Name: {first}\n★ Last Name: {last}\n★ Username: {username}\n★ User ID: <code>{user_id}</code>"

ID_GROUP = "★ Chat ID: <code>{chat_id}</code>"

ID_GROUP_WITH_REPLY = """★ Chat ID: <code>{chat_id}</code>
★ User ID: <code>{user_id}</code>
★ Replied User ID: <code>{replied_user_id}</code>"""

ID_GROUP_WITH_FILE = """★ Chat ID: <code>{chat_id}</code>
★ User ID: <code>{user_id}</code>
★ {message_type}: <code>{file_id}</code>"""

ID_CHANNEL = "ID: <code>{chat_id}</code>"

SKIP_SET_SUCCESS = "✅ Successfully set skip number to `{skip}`."

SKIP_MISSING_NUMBER = "❌ Please provide a skip number.\n\nExample: `/skip 10`"

SKIP_INVALID_NUMBER = "❌ Only numbers are supported."

SKIP_NEGATIVE_NUMBER = "❌ Skip number must be 0 or greater."

TARGET_SET_SUCCESS = "✅ Successfully set `{title}` as target channel."

TARGET_MISSING_ID = "❌ Please provide a target channel ID.\n\nExample: `/set -1001234567890`"

TARGET_INVALID_ID = "❌ Please provide a valid channel ID."

TARGET_NOT_CHANNEL = "❌ I can only set channels as target."

TARGET_NOT_ADMIN = "❌ Error: {error}\n\nMake sure the bot is an admin in your target channel."

CAPTION_SET_SUCCESS = "✅ Successfully set file caption.\n\n`{caption}`"

CAPTION_MISSING_TEXT = "❌ Please provide a caption.\n\nExample: `/caption {{file_name}} - My Channel`"

# ==================== ERROR MESSAGES ====================

ERROR_INVALID_LINK = "❌ Invalid link for forwarding!"

ERROR_GET_CHAT = "❌ Error: {error}"

ERROR_ONLY_CHANNELS = "❌ I can only forward from channels."

ERROR_TARGET_NOT_SET = "❌ Target channel not set.\n\nUse `/set <channel_id>` command to add target channel."

ERROR_WAIT_PROCESS = "⏳ Please wait until the previous process completes."

ERROR_CLOSED = "✅ Closed!"

# ==================== ACCESS DENIED ====================

ACCESS_DENIED = """🚫 **Access Denied**

This is a private bot. You cannot access it.

Create your own bot to use this service."""

# ==================== BUTTON TEXT ====================

BUTTON_UPDATES = "📢 Updates"
BUTTON_SUPPORT = "💬 Support"
BUTTON_SETTINGS = "⚙️ Settings"
BUTTON_HELP = "❓ Help"
BUTTON_CONTACT = "👨‍💻 Contact"
BUTTON_YES_FORWARD = "✅ Yes, Forward"
BUTTON_CLOSE = "❌ Close"
BUTTON_CANCEL = "🛑 Cancel"
BUTTON_RESET_ALL = "🔄 Reset All"

# ==================== BOT RESTART ====================

BOT_RESTARTED = "🤖 Bot Restarted Successfully!"

# ==================== ID COMMAND HELPERS ====================

def get_id_text(chat_type, **kwargs):
    """Generate ID text based on chat type"""
    if chat_type == "private":
        return ID_PRIVATE.format(**kwargs)
    elif chat_type == "group":
        if kwargs.get("has_reply"):
            if kwargs.get("has_file"):
                return ID_GROUP_WITH_FILE.format(**kwargs)
            return ID_GROUP_WITH_REPLY.format(**kwargs)
        else:
            if kwargs.get("has_file"):
                return ID_GROUP_WITH_FILE.format(**kwargs)
            return ID_GROUP.format(**kwargs)
    elif chat_type == "channel":
        return ID_CHANNEL.format(**kwargs)
    return ""
