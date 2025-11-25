import telethon, sqlite3, random, string, time, os, re, threading
from telethon import events, TelegramClient, Button
from configparser import ConfigParser
from datetime import datetime

# -- > set source requirements
data = ConfigParser()
data.read('./bot.apk')
l = ConfigParser()
lng = "fa"
language = {}
message = any

# -- > Users Variables
auth = False
expired = False
user_level = str
user_platform = str
Multi_Key=False
IsTrafficEnded = False
traffic_stat = dict
l.read('./languages.ini', "UTF-8")
keyboard = any
current_cmd = str
message = any
temp = {}
cache = {}
edu_links = {
    "ios" : "https://t.me/+FLl7cd2zg545OWVk",
    "android" : "https://t.me/+bQU_Xo9gMaE0YjU0",
    "pc" : "https://t.me/+HFsx-qds5n5hNWQ0",
    "cheat" : "https://t.me/+JH1gIqIAP6Y3ODQ0"
}
db = sqlite3.connect(data.get('bot', 'db'), autocommit=True, check_same_thread=False)
cursor = db.cursor()
cursor_backend = db.cursor()

bot = TelegramClient(
    data.get('bot', 'session'),
    data.getint('bot', 'api_id'),
    data.get('bot', 'api_hash'),
    auto_reconnect=True,
    device_model="Steve",
)
ADMIN_ID = [data.getint('bot', 'admin'), data.getint('bot', 'admin')-43134540]
admin_keyboard = [
                    [Button.inline("🗝️ New Key", "create_user")],
                    [Button.inline("👥🗝️ Multi Key", "create_multi_key")],
                    [Button.inline("📁 Upload File", "receive_file")],
                    [Button.inline("👥 Users", "Show_users"), Button.inline("📂 Files", "Show_files")],
                    [Button.inline("🔔 Send Message To Users", "send_pm")]
                    ]
