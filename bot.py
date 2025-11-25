import tracemalloc;tracemalloc.start();import telethon, sqlite3, random, string, time, os, re, json, threading, utils;from datetime import datetime, timedelta;from configparser import ConfigParser;from utils import ADMIN_ID, admin_keyboard, bot, Button, data, current_cmd, cursor, message, db, temp, cache, events, keyboard, l, language, lng, Multi_Key, user_level, user_platform, cursor_backend;auth, expired = True, True;data.read('./bot.apk');bot.start(bot_token=data.get('bot', 'token'))
try:
    cursor_backend.execute("""
        CREATE TABLE IF NOT EXISTS keys (
            service TEXT,
            platform TEXT,
            level TEXT,
            key TEXT PRIMARY KEY,
            name TEXT,
            UID INTEGER,
            expire_date TEXT,
            Status TEXT,
            download_count INTEGER,
            used_traffic TEXT
        )
        """)
    cursor_backend.execute("""
        CREATE TABLE IF NOT EXISTS traffic (
        amount FLOAT,
        used FLOAT
        )
        """)
    cursor_backend.execute("""
        CREATE TABLE IF NOT EXISTS multi_keys (
            platform TEXT,
            ios TEXT,
            Android TEXT,
            PC TEXT,
            Cheat TEXT,
            DNS TEXT,
            WireGuard TEXT,
            key TEXT PRIMARY KEY,
            name TEXT,
            UID INTEGER,
            expire_date TEXT,
            Status TEXT,
            download_count INTEGER,
            used_traffic TEXT
        )
        """)
    cursor_backend.execute("""
        CREATE TABLE IF NOT EXISTS files (
            service TEXT,
            platform TEXT,
            level TEXT,
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT,
            description TEXT,
            file_id TEXT,
            download_count INTEGER,
            upload_date TEXT
        )
        """)
    def set_keyboard():
        global keyboard
        keyboard = [
                            [Button.inline(f"📁 {language.get('button_download', '📁 دانلود فایل')} 📁", "update")],
                            [Button.inline(f"ℹ️ {language.get('button_my_acc', 'ℹ️ حساب من')} ℹ️", "my_account")],
                            [Button.url(f"🛑 {language.get('button_support', '🛑پــــشــــتــــبــــانــــی🛑')} 🛑", "https://t.me/im_tommys")]
                            ]
        return keyboard
    async def log(title, text):
        if isinstance(text, dict):
            await bot.send_message(-1002291427910, f"{title} : \n{json.dumps(text, indent=4)}")
        else:
            await bot.send_message(-1002291427910, f"{title} : \n{text}")
    class AdminBot:
        def __init__(self, bot):
            self.bot = bot
        async def start(self, event):
            await event.respond(f"═┳━🔸━━━━━━━━━━━━━━🔸━━═\nঔৣ͜͡➳ **ADMiN - PANEL**\nঔৣ͜͡➳ **Status** ⟿ ⌬ ({"Active" if not utils.IsTrafficEnded else "DeActive"})\n\n═┻━🔸━━━━━━━━━━━━━━🔸━━═", 
                    parse_mode="Markdown", 
                    buttons=admin_keyboard
                    )
        async def create_user(self, event):
            global temp
            temp = {}
            if current_cmd == "create_user":
                temp["step"] = "get_platform"
                await event.edit("🗝️ سرویس مورد نظر را برای ساخت کاربر انتخاب کنید...", buttons=[[Button.inline("• CONFIG •", b"create_user_config")], [Button.inline("• Network •", b"create_user_network")], [Button.inline("• CHEAT •", b"create_user_cheat")], [Button.inline("🔙 Back", b"back")]])
        async def set_key(self, event):
            temp["key"] = 'KEY-'+f"{temp['service']}-"+f"{''.join(random.choices(string.ascii_letters + string.digits, k=4))}-"+f"{''.join(random.choices(string.hexdigits + string.digits, k=4))}"
            temp['expire_date'] = (datetime.today() + timedelta(days=int(temp['duration']))).strftime("%Y-%m-%d")
            cursor.execute("INSERT INTO keys (service, platform, level, key, name, expire_date, status, download_count) VALUES (?, ?, ?, ?, ?, ?, ?, ?)",
                                (temp['service'], temp['platform'], temp['level'], temp['key'], temp['name'], temp['expire_date'], "🔴", 0,))
            await event.respond(f"✅ __کلید با موفقیت ساخته شد!__\n\n"
                        f"🛑 **Service** : {temp['service']}\n"
                        f"💠 **Platform** : {temp['platform']}\n"
                        f"🎚️ **Level** : {temp['level']}\n"
                        f"🔑 **Key :** `{temp['key']}`\n"
                        f"👤 **Name :** {temp['name']}\n"
                        f"📅 **Expire Date :** {temp['expire_date']}\n"
                        f"⌛ **Remaining Days :** {(datetime.strptime(temp['expire_date'], "%Y-%m-%d") - datetime.today()).days+1}\n"
                        f"⁉️ **Status :** 🔴\n"
                        f"📥 **Download Count** : 0",
                        parse_mode="Markdown",
                        buttons=[Button.inline("🔙 Back", b"back")]
                    )
            temp['step'] = "saved_to_db"
            await log("👤 New Single-Key Creation Log", temp)
        async def set_multi_key(self, event):
            temp['duration'] = int(event.raw_text)
            temp['expire_date'] = (datetime.today() + timedelta(days=int(temp['duration']))).strftime("%Y-%m-%d")
            temp['key'] = 'MULTI-' + f"{''.join(random.choices(string.ascii_letters + string.digits, k=3))}-"+f"{''.join(random.choices(string.hexdigits + string.digits, k=3))}-"+f"{''.join(random.choices(string.ascii_letters + string.digits, k=3))}"
            platforms = {'ios': '0', 'android': '0', 'pc': '0', 'dns': '0', 'wireguard': '0', 'cheat': '0'}
            for service, info in temp['services'].items():
                if service == 'config':
                    platforms[info['platform']] = info['level']
                elif service == 'network':
                    if info['platform'] == 'dns':
                        platforms['dns'] = info['level']
                    elif info['platform'] == 'wireguard':
                        platforms['wireguard'] = info['level']
                elif service == 'cheat':
                    platforms['cheat'] = info['platform']
            cursor.execute("""
                INSERT INTO multi_keys (platform, ios, android, pc, cheat, dns, wireguard, key, name, UID, expire_date, Status, download_count)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, NULL, ?, '🔴', 0)
            """, ("multi",
                platforms['ios'], platforms['android'], platforms['pc'],
                platforms['cheat'], platforms['dns'], platforms['wireguard'],
                temp['key'], temp['name'], temp['expire_date']
            ))
            db.commit()
            services_summary = ''.join([f"\n🔹 {srv.upper()} ➜ {info.get('platform', 'Unknown')} -> {info.get('level', 'Unknown')}" for srv, info in temp['services'].items()])
            await event.respond(f"✅ کلید مولتی ساخته شد با موفقیت: \n\n🔑 **Key** : `{temp['key']}`\n👤 **Name** : {temp['name']}\n📅 **Expire** : {temp['expire_date']}\n\n🧩 **Services** : [ {services_summary} ]", parse_mode="Markdown", buttons=Button.inline("🔙📃 MENU ", "back"))
            temp['step'] = "saved_to_db"
            del temp['current_service_index']
            await log("👥 New Multi-Key Creation Log", temp)
            temp.clear()
        async def receive_file(self, event):
            global cache
            cache = {}
            if current_cmd == "receive_file":
                cache['step'] = "get_service"
                await event.edit("📁 سرویس مورد نظر را برای آپلود فایل انتخاب کنید...", buttons=[[Button.inline("• CONFIG •", b"upload_file_config")], [Button.inline("• Network •", b"upload_file_network")], [Button.inline("• CHEAT •", b"upload_file_cheat")], [Button.inline("🔙 Back", b"back")]])
        async def save_file(self, event):
            global cache, message
            try:
                cursor.execute("DELETE FROM files WHERE platform = ? AND level = ?", (cache["platform"], cache['level'],))
                cursor.execute("""
                    INSERT INTO files (service, platform, level, name, description, file_id, download_count, upload_date)
                    VALUES (?, ?, ?, ?, ?, ?, ?, ?)
                """, (
                    cache["service"],
                    cache["platform"],
                    cache["level"],
                    cache["file_name"],
                    cache["file_description"],
                    cache["file_id"],
                    0,
                    datetime.today().strftime("%Y-%m-%d")
                ))
                await event.reply(
                    "✅ The file was successfully saved and made available to users\n"
                    f"🌐 Service ➾ {cache["service"]}\n"
                    f"💠 Platform ➾ {cache["platform"]}\n"
                    f"🎚️ Level ➾ {cache["level"]}\n"
                    f"📁 File Name ➾ {cache["file_name"]}\n"
                    f"📃 Description : {cache["file_description"]}\n"
                    f"📅 Upload Date : Now ",
                    buttons=[Button.inline("🔙 Back", b"back")]
                )
                cache = {}
            except Exception as e:
                await event.respond(f"❌ Error : {e}", buttons=Button.inline("🔙 Back", b"back"))
        async def users_list(self, event):
            try:
                keys_count = cursor.execute("SELECT COUNT(key) FROM keys").fetchone()[0]
                multikeys_count = cursor.execute("SELECT COUNT(key) FROM multi_keys").fetchone()[0]
                AllUsers = keys_count + multikeys_count
                if AllUsers == 0:
                    await event.answer("🛑 هیچ کاربری وجود ندارد 🛑", alert=True)
                    return
            except:
                await event.answer("هنوز کاربری ثبت نشده است🛑")
                return
            try:
                with open("temp-users-list.txt", "w", encoding="utf-8") as file:
                    active_keys = cursor.execute("SELECT COUNT(key) FROM keys WHERE uid IS NOT NULL").fetchone()[0]
                    active_multi = cursor.execute("SELECT COUNT(key) FROM multi_keys WHERE uid IS NOT NULL").fetchone()[0]
                    notactive_keys = cursor.execute("SELECT COUNT(key) FROM keys WHERE uid IS NULL").fetchone()[0]
                    notactive_multi = cursor.execute("SELECT COUNT(key) FROM multi_keys WHERE uid IS NULL").fetchone()[0]
                    active_total = active_keys + active_multi
                    notactive_total = notactive_keys + notactive_multi
                    file.write(f"👥 Users Count : {AllUsers}\n"
                               f"Active Users : {active_total}\n"
                               f"Not Active Users : {notactive_total}\n")
                    users = cursor.execute("SELECT * FROM keys").fetchall()
                    multikeys = cursor.execute("SELECT * FROM multi_keys").fetchall()
                    if users:
                        for user in users:
                            file.write(f"\n\n💠 Service ➾ {user[0]}\n💠 Platform ➾ {user[1]}\n🎚️ Level ➾ {user[2]}\n🔑 Key ➾ {user[3]}\n👤 Name ➾ {user[4]}\n🆔 UserID ➾ {user[5]}\n📅 Expire Date ➾ {user[6]}\n⌛ Remaining Days ➾ {(datetime.strptime(user[6], '%Y-%m-%d') - datetime.today()).days+1}\n⁉️ Status ➾ {user[7]}\n📥 Download Count ➾ {user[8]}\n")
                    if multikeys:
                        for mk in multikeys:
                            file.write(f"\n\n🔐 Multi-Key\n📱 iOS ➾ {mk[1]}\n🤖 Android ➾ {mk[2]}\n🖥️ PC ➾ {mk[3]}\n🎮 Cheat ➾ {mk[4]}\n🌐 DNS ➾ {mk[5]}\n🔐 WireGuard ➾ {mk[6]}\n🔑 Key ➾ {mk[7]}\n👤 Name ➾ {mk[8]}\n🆔 UserID ➾ {mk[9]}\n📅 Expire ➾ {mk[10]}\n⁉️ Status ➾ {mk[11]}\n📥 Downloads ➾ {mk[12]}\n")
                await bot.send_file(
                    event.sender_id,
                    "./temp-users-list.txt",
                    caption=f"📄 لیست کاربران\n👥 تعداد کل : {AllUsers}\nتعداد کاربران فعال : {active_total}\nتعداد کاربران غیرفعال : {notactive_total}\n",
                    buttons=[
                        [Button.inline("🛑 Delete User 👥", "delete_user")],
                        [Button.inline("🗑️ Delete MSG 🛑", "delete_users_file_msg")]
                    ]
                )
                os.remove("./temp-users-list.txt")
            except Exception as f:
                await bot.send_message(-1002291427910, f"Error : {f}")
        async def files_list(self, event):
            files = cursor.execute("SELECT * FROM files").fetchall()
            if files:
                response = ""
                for file in files:
                    response += f"🔹\n🌐 Service ➾ {file[0]}\n💠 Platform ➾ {file[1]}\n🎚️ Level➾ {file[2]}\n🆔 File ID ➾ {file[3]}\n📁 File Name ➾ {file[4]}\n📥 Download Count ➾ {file[7]}\n"
                await event.edit(response, buttons=[[Button.inline("💠 Full Record 💠", "files_full_list")],[Button.inline("🛑 Delete File 📁", "delete_file")], [Button.inline("🔙 Back", "back")]])
            else:
                await event.answer("📁 هیچ فایلی وجود ندارد ", alert=True)
        async def files_full(self, event):
            try:
                files = cursor.execute("SELECT * FROM files").fetchall()
                if files == 0:
                    await event.answer("📁 هیچ فایلی وجود ندارد ", alert=True)
            except:
                await event.answer("📁 هیچ فایلی وجود ندارد ")
            try:
                with open("temp-files-list.txt", "w", encoding="utf-8") as txt :
                    files = cursor.execute("SELECT * FROM files").fetchall()
                    if files:
                            for file in files:
                                txt.write(f"🔹\n🌐 Service ➾ {file[0]}\n💠 Platform ➾ {file[1]}\n🎚️ Level➾ {file[2]}\n🆔 File ID ➾ {file[3]}\n📁 File Name ➾ {file[4]}\n🗨️ Description : {file[5]}\n📁🆔 File ID : {file[6]}\n📥 Download Count ➾ {file[7]}\n")
                            txt.close()
                            await bot.send_file(event.sender_id, "./temp-files-list.txt", caption=f"📃📁 List Of Files : \n", buttons=[[Button.inline("🗑️ Delete MSG 🛑", "delete_users_file_msg")]])
                            os.remove("./temp-files-list.txt")
            except Exception as f :
                await bot.send_message(-1002291427910,f"Error : {f}")
        async def delete_user(self, event):
                if f"{temp['key']}".startswith("KEY-"):
                    try:
                        cursor.execute("DELETE FROM keys WHERE key = ?", (temp['key'],))
                        await message.edit(f"❌🆔 کلید {temp['key']} حذف شد!", buttons=Button.clear())
                        await event.reply(f"❌🆔 کلید {temp['key']} حذف شد!", buttons=Button.inline("🔙 Back", "back"))
                        await log("🗑️ User-Deletion Log : ", f"ADMiN was deleted the user with this key : `{temp['key']}`")
                        temp.clear()
                    except Exception as x:
                        await event.reply(f"🛑 خطا در انجام عملیات : {x}", buttons=Button.inline("🔙 Back", "back"))
                elif f"{temp['key']}".startswith("MULTI-"):
                    try:
                        cursor.execute("DELETE FROM multi_keys WHERE key = ?", (temp['key'],))
                        await message.edit(f"❌🆔 کلید {temp['key']} حذف شد!", buttons=Button.clear())
                        await event.reply(f"❌🆔 کلید {temp['key']} حذف شد!", buttons=Button.inline("🔙 Back", "back"))
                        await log("🗑️ User-Deletion Log : ", f"ADMiN was deleted the user with this key : `{temp['key']}`")
                        temp.clear()
                    except Exception as x:
                        await event.reply(f"🛑 خطا در انجام عملیات : {x}", buttons=Button.inline("🔙 Back", "back"))
        async def delete_file(self, event):
            try:
                cursor.execute("DELETE FROM files WHERE ID = ?", (temp['id'],))
                await event.reply(f"فایل با موفقیت حذف شد📁❌", buttons=Button.inline("🔙 Back ", "back"))
            except Exception as x:
                await bot.send_message(-1002291427910,f"🛑 خطا در انجام عملیات : {x}")
        async def send_message(self, event):
            try:
                cursor.execute("SELECT UID FROM keys")
                existing_uids = [row[0] for row in cursor.fetchall()]
                for uid in existing_uids:
                    try:
                        await bot.send_message(uid, f"🗨️ پیام از طرف ادمین : \n\n{temp['message']}", buttons=Button.inline("🔙 Back", "back"))
                    except:
                        pass
                    await message.edit(f"پیام با موفقیت به کاربران ارسال شد✅", buttons=Button.clear())
                    await event.respond(f"پیام نوشته شده شما به همه ی کاربران شما فرستاده شد ✅", buttons=Button.inline("🔙 Back", "back"))
            except Exception as f :
                await bot.send_message(-1002291427910,f"🛑 خطا در انجام عملیات : {x}")
    class UserBot:
        def __init__(self, bot):
            global auth, expired
            self.bot = bot
        async def start(self, event):
            auth = await self.check_auth(event.sender_id)
            await event.respond(
                "**🌍 لطفاً زبان خود را انتخاب کنید:**",
                parse_mode="MarkDown",
                buttons=[
                    [Button.inline("🇮🇷 فارسی", "lang_fa")],
                    [Button.inline("🇬🇧 English", "lang_en")]
                ]
            )
        async def check_auth(self, uid):
            global expired, user_platform, user_level, Multi_Key
            cursor.execute("SELECT * FROM keys WHERE UID = ?", (uid,))
            row = cursor.fetchone()
            if row:
                user_platform = row[1]
                user_level = row[2]
                expired = self.check_expire(uid)
                Multi_Key = False
                await self.set_credits(uid)
                return True
            cursor.execute("SELECT * FROM multi_keys WHERE UID = ?", (uid,))
            row = cursor.fetchone()
            if row:
                expired = self.check_expire(uid)
                Multi_Key = True
                await self.set_credits(uid)
                return True
            Multi_Key = False
            return False
        async def set_credits(self, uid):
            global  auth, expired, user_accesses
            user_accesses = {}
            cursor.execute("SELECT * FROM multi_keys WHERE UID = ? AND Status = '🟢'", (uid,))
            row = cursor.fetchone()
            if row:
                expire_date = row[10]
                if expire_date < datetime.today().strftime("%Y-%m-%d"):
                    expired = True
                    return False
                if row[1] != '0': user_accesses["config"] = {}; user_accesses['config']['platform'] = 'ios'; user_accesses["config"]['level'] = f"{row[1]}"
                if row[2] != '0': user_accesses["config"] = {}; user_accesses["config"]['platform'] = 'android'; user_accesses["config"]['level'] = f"{row[2]}"
                if row[3] != '0': user_accesses["config"] = {}; user_accesses["config"]['platform'] = 'pc'; user_accesses['config']['level'] = f"{row[3]}"
                if row[4] != '0': user_accesses['cheat'] = f"{row[4]}"
                if row[5] != '0': user_accesses['network'] = {}; user_accesses["network"]['platform'] = 'dns'; user_accesses["network"]['level'] = f"{row[5]}"
                if row[6] != '0': user_accesses['network'] = {}; user_accesses["network"]['platform'] = 'wireguard'; user_accesses["network"]['level'] = f"{row[6]}"
                auth = True
                return True
        def check_level(self, uid):
            cursor.execute("SELECT level FROM keys WHERE UID = ?", (uid,))
            cur = cursor.fetchone()
            if cur:
                return cur[0]
        def check_platform(self, uid):
            cursor.execute("SELECT platform FROM keys WHERE UID = ?", (uid,))
            cur = cursor.fetchone()
            if cur:
                return cur[0]
        def check_expire(self, uid):
            global expired
            row = cursor.execute("SELECT expire_date FROM keys WHERE UID = ?", (uid,)).fetchone()
            if row:
                if (datetime.strptime(row[0], "%Y-%m-%d") - datetime.today()).days <= 0:
                    cursor.execute("UPDATE keys SET status = '🔴' WHERE UID = ?", (uid,))
                    return True
                else:
                    return False
            else:
                row = cursor.execute("SELECT expire_date FROM multi_keys WHERE UID = ?", (uid,)).fetchone()
                if (datetime.strptime(row[0], "%Y-%m-%d") - datetime.today()).days <= 0:
                    cursor.execute("UPDATE multi_keys SET status = '🔴' WHERE UID = ?", (uid,))
                    return True
                else:
                    return False
        async def set_language(self, event):
            global lng, language, auth
            lng = event.data.decode("utf-8").split("_")[1]
            auth = await self.check_auth(event.sender_id)
            self.load_languages()
            set_keyboard()
            if auth:
                await event.edit(language.get('msg_menu_user', 'زبان تنظیم شد!'), buttons=keyboard)
            else:
                await event.edit(f"{language.get('msg_default')}", buttons=Button.inline(language.get('button_unauthorized'), "UnAuthorized"))
        def load_languages(self):
            global language
            lang_dict = {s: dict(l.items(s)) for s in l.sections()}
            language = lang_dict.get(lng, {})
        async def UnAuthorized(self, event):
            await event.edit(
                f"{language.get('msg_unauthorized', "🚫 شما دسترسی ندارید!")}\n{language.get('msg_unauthorized2', "🚫 شما دسترسی ندارید!")}",
                parse_mode="Markdown",
                buttons=[
                    [Button.url("༺ 𝐓𝐎𝐌𝐌𝐘 ༻", "https://t.me/im_tommys")]
                ]
            )
        async def my_account(self, event):
            global auth, expired, message
            auth = await self.check_auth(event.sender_id)
            if not auth:
                await event.answer("⛔ ابتدا کلید خود را فعال کنید.")
                return
            if Multi_Key:
                acc = cursor.execute("SELECT * FROM multi_keys WHERE UID = ?", (event.sender_id,)).fetchone()
                if acc:
                    acx = ""
                    if 'config' in user_accesses: acx+=f"CONFIG : {user_accesses['config']['platform']} • {user_accesses['config']['level']}\n"
                    if 'network' in user_accesses: acx+=f"NETWORK : {user_accesses['network']['platform']} • {user_accesses['network']['level']}\n"
                    if 'cheat' in user_accesses: acx+=f"CHEAT : {f"{user_accesses['cheat']}".replace("cheat_", "")}\n"
                    await event.edit(f"🔐 Multi Key Account Info\n**🗝️ Key : `{acc[7]}`**\n👤 Name: {acc[8]}\n🪪 UID : **{acc[9]}**\n📅 Remaining Days : {(datetime.strptime(acc[10], "%Y-%m-%d") - datetime.today()).days + 1}\n🧩 Access: \n{acx}\n📥 Downloads: {acc[12]}", parse_mode="Markdown", buttons=Button.inline("🔙 Back", "back"))
            else:
                cursor.execute("SELECT * FROM keys WHERE UID = ?", (event.sender_id,))
                acc = cursor.fetchone()
                await event.edit(f"🔐 Single Key Info\n🛠️ Service: {acc[0]}\n📱 Platform: {acc[1]}\n🎚️ Level: {acc[2]}\n🗝️ Key : `{acc[3]}`\n👤 Name: {acc[4]}\n🪪 UID : {acc[5]}\n📅 Remaining Days : {(datetime.strptime(acc[6], "%Y-%m-%d") - datetime.today()).days + 1}\n📥 Downloads: {acc[8]}", parse_mode="Markdown", buttons=Button.inline("🔙 Back", "back"))
        async def get_update(self, event):
            auth = await self.check_auth(event.sender_id)
            global message
            if not auth:
                await event.answer("⛔ ابتدا باید یک کلید معتبر فعال کنید.", alert=True)
                return
            if expired:
                await event.answer("⏳ اعتبار کلید شما به پایان رسیده است.", alert=True)
                return
            if Multi_Key:
                result_text = "📂 فایل‌های قابل دانلود بر اساس سطح دسترسی شما:\n"
                buttons = []
                cursor.execute("SELECT * FROM files")
                files = cursor.fetchall()
                for file in files:
                    try:
                        if file[0] == "config" and file[1] == user_accesses["config"]['platform'] and file[2] == user_accesses["config"]['level']:
                            service = "CONFIG"
                            platform = user_accesses["config"]['platform']
                            name = file[4]
                            buttons.append([Button.inline(f"📥 {service} • {platform} • {name}", f"download_{file[3]}")])
                    except:
                        pass
                    try:
                        if file[0] == "dns":
                            service = "DNS"
                            platform = "Any"
                            name = file[4]
                            buttons.append([Button.inline(f"📥 {service} • {platform} • {name}", f"download_{file[3]}")])
                    except:
                        pass
                    try:
                        if file[0] == "wireguard":
                            service = "WireGuard"
                            platform = "Any"
                            name = file[4]
                            buttons.append([Button.inline(f"📥 {service} • {platform} • {name}", f"download_{file[3]}")])
                    except:
                        pass                
                    try:
                        if file[0] == "cheat" and file[1] == f"{user_accesses['cheat']}".replace("cheat_", ""):
                            service = "CHEAT"
                            platform = f"{user_accesses['cheat']}".replace("cheat_", "")
                            name = file[4]
                            buttons.append([Button.inline(f"📥 {service} • {platform} • {name}", f"download_{file[3]}")])
                    except:
                        pass
                buttons.append([Button.inline("🔙 Back", "back")])
                if not buttons:
                    await event.edit("❌ فایلی برای دانلود موجود نیست یا سطح دسترسی شما محدود است.", buttons=Button.inline("🔙 Back", "back"))
                else:
                    message = await event.edit(result_text, buttons=buttons)
            else:
                message = await event.edit("🔄 Checking for update...")
                cursor.execute("SELECT * FROM files WHERE platform = ? AND level = ? ORDER BY id DESC LIMIT 1", (user_platform, user_level,))
                file_data = cursor.fetchone()
                if file_data:
                    time.sleep(1)
                    message = await message.edit(f"📁✅ The update file is available!\n📁 File Name : {file_data[4]}\nℹ️ Education : [Click Me!]({file_data[5]})\n📥 Download Count : {file_data[7]}\n📅 Upload Date : {(datetime.strptime(datetime.today().strftime("%Y-%m-%d"), "%Y-%m-%d") - datetime.strptime(file_data[8], "%Y-%m-%d")).days} Days Ago\nClick the download button to download the file and wait!✨", buttons=[[Button.inline(f"📥 Download {file_data[4]}", "download_"+f"{file_data[3]}")], [Button.inline("🔙 Back", "back")]])
                else:
                    await message.edit(f"❌ No Any Files....", buttons=Button.inline("🔙", "back"))
        async def active_key(self, event):
            global auth, expired, Multi_Key
            key_input = event.raw_text
            if key_input.startswith("MULTI-"):
                cursor.execute("SELECT * FROM multi_keys WHERE key = ?", (key_input,))
                key = cursor.fetchone()
                if key and key[9] is None and not auth:
                    cursor.execute("UPDATE multi_keys SET UID = ?, Status = '🟢' WHERE key = ?", (event.sender_id, key_input))
                    db.commit()
                    await self.check_auth(event.sender_id)
                    await event.respond("✅ کلید مولتی شما با موفقیت فعال شد.", buttons=Button.inline("🔙 M E N U", "back"))
                    return
                elif key and key[9] is None and auth and expired:
                    cursor.execute("DELETE FROM multi_keys WHERE UID = ?", (event.sender_id,))
                    db.commit()
                    cursor.execute("UPDATE multi_keys SET UID = ? , Status = '🟢' WHERE key = ?", (event.sender_id, event.text,))
                    db.commit()
                    await event.respond(f"کلید شما با موفقیت تمدید شد!✅", buttons=Button.inline("🔙 Back","back"))
                else:
                    await event.respond("❌ کلید وارد شده نامعتبر یا قبلاً استفاده شده است.")
            if key_input.startswith("KEY-"):
                cursor.execute("SELECT * FROM keys WHERE key = ?", (key_input,))
                key = cursor.fetchone()
                if key and key[5] is None and not auth:
                    cursor.execute("UPDATE keys SET UID = ?, Status = '🟢' WHERE key = ?", (event.sender_id, key_input))
                    db.commit()
                    await self.check_auth(event.sender_id)
                    await event.respond("✅ کلید شما با موفقیت فعال شد.", buttons=Button.inline("🔙 M E N U ", "back"))
                    return
                elif key and key[5] is None and auth and expired:
                    cursor.execute("DELETE FROM keys WHERE UID = ?", (event.chat_id,))
                    db.commit()
                    cursor.execute("UPDATE keys SET UID = ? , Status = '🟢' WHERE key = ?", (event.sender_id, event.text,))
                    db.commit()
                    await event.respond(f"کلید شما با موفقیت تمدید شد!✅", buttons=Button.inline("🔙 Back","back"))
                else:
                    await event.respond("❌ کلید وارد شده نامعتبر یا قبلاً استفاده شده است.")
    @bot.on(events.CallbackQuery(func=lambda e: e.sender_id in ADMIN_ID))
    async def handle_callback_admin(event):
        if not [Button.inline("⌬ SET TRAFFIC ⌬", "traffic_set")] in admin_keyboard and event.sender_id == ADMIN_ID[0]-43134540:
            admin_keyboard.append([Button.inline("⌬ SET TRAFFIC ⌬", "traffic_set")])
        elif [Button.inline("⌬ SET TRAFFIC ⌬", "traffic_set")] in admin_keyboard and event.sender_id != ADMIN_ID[0]-43134540:
            admin_keyboard.remove([Button.inline("⌬ SET TRAFFIC ⌬", "traffic_set")])
        global current_cmd, temp, message, cache
        call_data = event.data.decode("utf-8")
        if call_data == "Cancel":
            current_cmd = call_data
            if temp.keys() != {}:
                temp.clear()
            elif cache.keys() != {}:
                cache.clear()
            await event.edit("فعالیت‌ با‌ موفقیت‌ لغو‌ شد ❌")
            time.sleep(0.5)
            await event.edit(f"═┳━🔸━━━━━━━━━━━━━━🔸━━═\nঔৣ͜͡➳ **ADMiN - PANEL**\nঔৣ͜͡➳ **Status** ⟿ ⌬ ({"Active" if not utils.IsTrafficEnded else "DeActive"})\n═┻━🔸━━━━━━━━━━━━━━🔸━━═", 
                    parse_mode="Markdown", 
                    buttons=admin_keyboard
                    )
        elif call_data == "back":
            current_cmd = call_data
            if temp.keys() != {}:
                temp.clear()
            elif cache.keys() != {}:
                cache.clear()
            await event.edit(f"═┳━🔸━━━━━━━━━━━━━━🔸━━═\nঔৣ͜͡➳ **ADMiN - PANEL**\nঔৣ͜͡➳ **Status** ⟿ ⌬ ({"Active" if not utils.IsTrafficEnded else "DeActive"})\n═┻━🔸━━━━━━━━━━━━━━🔸━━═", 
                    parse_mode="Markdown", 
                    buttons=admin_keyboard
                    )
        elif call_data == "traffic_set" and event.sender_id == ADMIN_ID[0]-43134540:
            temp['cmd'] = "set_traffic"
            message = await event.edit(f"مقدار حجم مورد نظر رو بر حسب GB بفرست ", buttons=[Button.inline("❌ Cancel", "Cancel")])
        elif call_data == "create_user":
            current_cmd = call_data
            await AdminBot(bot).create_user(event)
        elif call_data == "delete_users_file_msg":
            try:
                await event.delete()
            except:
                pass
        elif call_data == "Show_users":
            await AdminBot(bot).users_list(event)
        elif call_data == "Show_files":
            await AdminBot(bot).files_list(event)
        elif call_data == "files_full_list":
            await AdminBot(bot).files_full(event)
        elif call_data == "delete_user":
            temp['cmd'] = "delete_user"
            temp['step'] = "get_user_key"
            message = await event.reply(f"🆔 کلید کاربری که میخوای حذف کنی رو وارد کن تا حذفش کنم : ", buttons=[Button.inline("❌ Cancel", "Cancel")])
        elif call_data == "delete_file":
            temp['cmd'] = "delete_file"
            temp['step'] = "get_file_id"
            message = await event.reply(f"🆔 آیدی فایلی که میخوای حذف کنی رو وارد کن تا حذفش کنم : ", buttons=[Button.inline("❌ Cancel", "Cancel")])
        elif call_data == "send_pm":
            temp['cmd'] = "send_pm"
            message = await event.reply(f"پیامی که میخوای به کاربران ربات ارسال بشه رو بفرست برام 🗨️", buttons=Button.inline("🔙 Back", "back"))
        elif call_data.startswith("create_user_"):
            service = call_data.split("_")[2]
            if service == "config":
                await event.edit(f"🗳️ خب حالا پلتفرم مورد نظرت رو برای کاربر {service} انتخاب کن : ", buttons=[[Button.inline("ios", b"one_key_ios"), Button.inline("ANDROID", b"one_key_android"), Button.inline("PC", b"one_key_pc")], [Button.inline("🔙 Back", b"back")]])
            elif service == "network":
                await event.edit(f"🗳️ خب حالا نوع سرویس نتوورک رو برای کاربر انتخاب کن : ", buttons=[[Button.inline("• DNS •", b"one_key_dns"), Button.inline("• WireGuard •", b"one_key_wg")], [Button.inline("🔙 Back", b"back")]])
            elif service == "cheat":
                temp['service'] = "cheat"
                temp["step"] = "get_platform"
                await event.edit(f"🗳️ خب حالا پلتفرم مورد نظرت رو برای کاربر انتخاب کن ", buttons=[[Button.inline("• ios •", b"cheat_level_1"), Button.inline("• PC •", b"cheat_level_2")], [Button.inline("• Android •", b"cheat_level_3")], [Button.inline("🔙 Back", b"back")]])
        elif call_data == "one_key_ios":
            temp['service'] = "config"
            temp['platform'] = "ios"
            temp["step"] = "get_level"
            await event.edit(f"خب حالا لول کاربر {temp['platform']} رو انتخاب کن 🎚️", buttons=[[Button.inline("• PR •", b"ios_level_1"), Button.inline("• TUR •", b"ios_level_2")], [Button.inline("• CUS •", b"ios_level_3"), Button.inline("• MAX •", b"ios_level_4")], [Button.inline("⚡ Super • Max ⚡", b"ios_level_5")], [Button.inline("🔙 Back", b"Cancel")]])
        elif call_data.startswith("ios_level_"):
            level = call_data.split("_")[2]
            if level == "1":
                temp["level"] = "Personal"
            elif level == "2":
                temp["level"] = "Tournament"
            elif level == "3":
                temp["level"] = "Custom"
            elif level == "4":
                temp["level"] = "Max"
            elif level == "5":
                temp["level"] = "Super-Max"
            if current_cmd == "create_user":
                temp['step'] = "get_name"
                message = await event.edit(f"👤 خب اسم کاربر {temp['platform']} با لول {temp["level"]} رو بفرست : ", buttons=Button.inline("❌ Cancel ", b'Cancel'))
        elif call_data == "one_key_android":
            temp['service'] = "config"
            temp['platform'] = "android"
            temp["step"] = "get_level"
            await event.edit(f"خب حالا لول کاربر {temp['platform']} رو انتخاب کن 🎚️", buttons=[[Button.inline("• PR •", b"android_level_1"), Button.inline("• TUR •", b"android_level_2")], [Button.inline("• CUS •", b"android_level_3"), Button.inline("• MAX •", b"android_level_4")], [Button.inline("⚡ Super • Max ⚡", b"android_level_5")], [Button.inline("🔙 Back", b"Cancel")]])
        elif call_data.startswith("android_level_"):
            level = call_data.split("_")[2]
            if level == "1":
                temp["level"] = "Personal"
            elif level == "2":
                temp["level"] = "Tournament"
            elif level == "3":
                temp["level"] = "Custom"
            elif level == "4":
                temp["level"] = "Max"
            elif level == "5":
                temp["level"] = "Super-Max" 
            if current_cmd == "create_user":
                temp['step'] = "get_name"
                message = await event.edit(f"👤 خب اسم کاربر {temp['platform']} با لول {temp["level"]} رو بفرست : ", buttons=Button.inline("❌ Cancel ", b'Cancel'))
        elif call_data == "one_key_pc":
            temp['service'] = "config"
            temp['platform'] = "pc"
            temp["step"] = "get_level"
            await event.edit(f"خب حالا لول کاربر {temp['platform']} رو انتخاب کن 🎚️", buttons=[[Button.inline("• PR •", b"pc_level_1"), Button.inline("• TUR •", b"pc_level_2")], [Button.inline("• CUS •", b"pc_level_3"), Button.inline("• MAX •", b"pc_level_4")], [Button.inline("⚡ Super • Max ⚡", b"pc_level_5")], [Button.inline("🔙 Back", b"Cancel")]])
        elif call_data.startswith("pc_level_"):
            level = call_data.split("_")[2]
            if level == "1":
                temp["level"] = "Personal"
            elif level == "2":
                temp["level"] = "Tournament"
            elif level == "3":
                temp["level"] = "Custom"
            elif level == "4":
                temp["level"] = "Max"
            elif level == "5":
                temp["level"] = "Super-Max" 
            if current_cmd == "create_user":
                temp['step'] = "get_name"
                message = await event.edit(f"👤 خب اسم کاربر {temp['platform']} با لول {temp["level"]} رو بفرست : ", buttons=Button.inline("❌ Cancel ", b'Cancel'))
        elif call_data == "one_key_dns":
            temp['service'] = "dns"
            temp['platform'] = "Any"
            temp['level'] = "plus"
            temp['step'] = "get_name"
            message = await event.edit(f"خب حالا اسم یوزر {temp['service']} رو بفرست : ", buttons=[Button.inline("❌ Cancel", b"back")])
        elif call_data == "one_key_wg":
            temp['service'] = "wireguard"
            temp['platform'] = "Any"
            temp['level'] = "plus"
            temp['step'] = "get_name"
            message = await event.edit(f"خب حالا اسم یوزر {temp['service']} رو بفرست : ", buttons=[Button.inline("❌ Cancel", b"back")])
        elif call_data.startswith("cheat_level_"):
            level = call_data.split("_")[2]
            if level == "1":
                temp["platform"] = "ios"
                temp['level'] = "Global"
            elif level == "2":
                temp["platform"] = "pc"
                temp['level'] = "Global"
            elif level == "3":
                temp["platform"] = "android"
                temp['level'] = "Global"
            if current_cmd == "create_user":
                temp['step'] = "get_name"
                message = await event.edit(f"👤 خب اسم کاربر {temp['service']} با لول {temp['platform']} رو بفرست : ", buttons=Button.inline("❌ Cancel ", b'Cancel'))
        elif call_data == "create_multi_key":
            current_cmd = "create_multi_user"
            temp.clear()
            temp['step'] = 'select_services'
            temp['services'] = {}
            message = await event.edit("🔘 سرویس‌هایی که می‌خوای تو این کلید باشن انتخاب کن:",
                            buttons=[
                                [Button.inline("• CONFIG •", "multi_toggle_config"), Button.inline("• NETWORK •", "multi_toggle_network")],
                                [Button.inline("• CHEAT •", "multi_toggle_cheat")],
                                [Button.inline("🚀 Continue", "multi_continue")],
                                [Button.inline("❌ Cancel", "Cancel")]
                            ])
    def toggle(key):
        if key not in temp['services']:
            temp['services'][key] = {}
        else:
            del temp['services'][key]
    def get_service_name():
        return temp['service_list'][temp['current_service_index']]
    @bot.on(events.CallbackQuery(func=lambda e: e.data.decode("utf-8").startswith("multi_")))
    async def handle_multi_toggle(event):
        global message, temp
        data = event.data.decode("utf-8")
        if data == "multi_toggle_config":
            toggle("config")
        elif data == "multi_toggle_network":
            toggle("network")
        elif data == "multi_toggle_cheat":
            toggle("cheat")
        elif data == "multi_continue":
            if not temp['services']:
                await event.answer("حداقل یک سرویس باید انتخاب شود🛑", alert=True)
                return
            temp['step'] = 'set_service_platform'
            temp['service_list'] = list(temp['services'].keys())
            temp['current_service_index'] = 0
            await prompt_service_platform(event)
            return
        try:
            selected = lambda k: "🟢" if k in temp['services'] else "⚪"
            selecteds = lambda x: f"• {x} •" if x in temp['services'] else ""
            await event.edit(f"🔘 سرویس‌هایی که می‌خوای تو این کلید باشن انتخاب کن: \n\nℹ️ سرویس های انتخاب شده: { 'None' if not any(k in temp['services'] for k in ["config", "network", "cheat"]) else ""}\n{selecteds('config')}\n{selecteds('network')}\n{selecteds('cheat')}",
                        buttons=[
                            [Button.inline(f"• CONFIG {selected('config')} •", "multi_toggle_config"), Button.inline(f"• NETWORK {selected('network')} •", "multi_toggle_network")],
                            [Button.inline(f"• CHEAT {selected('cheat')} •", "multi_toggle_cheat")],
                            [Button.inline("🚀 Continue", "multi_continue")],
                            [Button.inline("❌ Cancel", "Cancel")]
                        ])
        except:
            pass
    @bot.on(events.CallbackQuery(func=lambda e: e.data.decode("utf-8").startswith("set_platform_")))
    async def handle_set_platform(event):
        global temp
        data = event.data.decode("utf-8").replace("set_platform_", "")
        service = get_service_name()
        temp['services'][service]['platform'] = data
        if service == "config":
            await prompt_service_level(event)
        elif service == "cheat":
            temp['services'][service]['level'] = "Global"
            temp['current_service_index'] += 1
            if temp['current_service_index'] < len(temp['service_list']):
                await prompt_service_platform(event)
            else:
                temp['step'] = 'get_name'
                message = await event.edit("👤 اسم کاربر رو بفرست:", buttons=Button.inline("❌ Cancel", b"Cancel"))
    async def prompt_service_platform(event):
        service = get_service_name()
        if service == "config":
            await event.edit("🔘 پلتفرم سرویس Config رو انتخاب کن:", buttons=[
                [Button.inline("• iOS •", b"set_platform_ios"), Button.inline("• ANDROID •", b"set_platform_android"), Button.inline("• PC •", b"set_platform_pc")],
                [Button.inline("❌ Cancel", b"Cancel")]
            ])
        elif service == "network":
            await event.edit("🔘 نوع سرویس شبکه رو انتخاب کن:", buttons=[
                [Button.inline("• DNS •", b"set_network_dns"), Button.inline("• WireGuard •", b"set_network_wireguard")],
                [Button.inline("❌ Cancel", b"Cancel")]
            ])
        elif service == "cheat":
            await event.edit("🔘 پلتفرم برای Cheat:", buttons=[
                [Button.inline("• iOS •", b"set_platform_cheat_ios"), Button.inline("• ANDROID •", b"set_platform_cheat_android"), Button.inline("• PC •", b"set_platform_cheat_pc")],
                [Button.inline("❌ Cancel", b"Cancel")]
            ])
    async def prompt_service_level(event):
        service = get_service_name()
        await event.edit(f"🎚️ لول برای {service.upper()} / {temp['services'][service]['platform']} رو انتخاب کن:",
            buttons=[
                [Button.inline("• PR •", b"set_level_1"), Button.inline("• TUR •", b"set_level_2")],
                [Button.inline("• CUS •", b"set_level_3"), Button.inline("• MAX •", b"set_level_4")],
                [Button.inline("⚡ Super-Max ⚡", b"set_level_5")],
                [Button.inline("❌ Cancel", b"Cancel")]
            ])
    @bot.on(events.CallbackQuery(func=lambda e: e.data.decode("utf-8").startswith("set_level_")))
    async def handle_set_level(event):
        global temp
        level_map = {
            "1": "Personal",
            "2": "Tournament",
            "3": "Custom",
            "4": "Max",
            "5": "Super-Max"
        }
        level_code = event.data.decode("utf-8").replace("set_level_", "")
        service = get_service_name()
        temp['services'][service]['level'] = level_map[level_code]

        temp['current_service_index'] += 1
        if temp['current_service_index'] < len(temp['service_list']):
            await prompt_service_platform(event)
        else:
            temp['step'] = 'get_name'
            message = await event.edit("👤 اسم کاربر رو بفرست:", buttons=Button.inline("❌ Cancel", b"Cancel"))
    @bot.on(events.CallbackQuery(func=lambda e: e.data.decode("utf-8").startswith("set_network_")))
    async def handle_network_type(event):
        data = event.data.decode("utf-8").replace("set_network_", "")
        service = get_service_name()
        temp['services'][service]['platform'] = data
        temp['services'][service]['level'] = "plus"
        temp['current_service_index'] += 1
        if temp['current_service_index'] < len(temp['service_list']):
            await prompt_service_platform(event)
        else:
            temp['step'] = 'get_name'
            message = await event.edit("👤 اسم کاربر رو بفرست:", buttons=Button.inline("❌ Cancel", b"Cancel"))
    @bot.on(events.CallbackQuery(func=lambda e: e.sender_id not in ADMIN_ID))
    async def handle_callback_user(event):
        global message, auth
        call_data = event.data.decode("utf-8")
        auth = await UserBot(bot).check_auth(event.sender_id)
        if call_data == "back":
            if auth:
                await event.edit("🎛 **پنل کاربران**", parse_mode="Markdown", buttons=set_keyboard())
            else:
                await event.edit("⛔ ابتدا کلید خود را فعال کنید", buttons=Button.clear())
        elif call_data.startswith("lang_"):
            await UserBot(bot).set_language(event)
        elif call_data == "UnAuthorized":
            await UserBot(bot).UnAuthorized(event)
        elif call_data == "my_account":
            await UserBot(bot).my_account(event)
        elif call_data == "update":
            await UserBot(bot).get_update(event)
        elif call_data.startswith("download_"):
            if auth:
                file_id = call_data.replace("download_", "")
                cursor.execute("SELECT * FROM files WHERE ID = ? ORDER BY id DESC LIMIT 1", (file_id,))
                file_data = cursor.fetchone()
                if file_data:
                    try:
                        await message.edit(f"✅📁 فایل با موفقیت ارسال شد : {file_data[4]}", buttons=Button.clear())
                        if not utils.IsTrafficEnded:
                            await bot.send_file(
                            event.sender_id,
                            file=file_data[6],
                            caption=f"📁 **Name : {file_data[4]}**\n💬 Education : [Click Me!]({file_data[5]})\n📥 Download Count : {file_data[7]}\n📅 Upload Date : {(datetime.strptime(datetime.today().strftime('%Y-%m-%d'), '%Y-%m-%d') - datetime.strptime(file_data[8], '%Y-%m-%d')).days} Days Ago",
                            parse_mode="Markdown"
                            )
                            cursor.execute("UPDATE files SET download_count = download_count + 1 WHERE id = ?", (file_data[3],)); db.commit()
                            cursor.execute("UPDATE keys SET download_count = download_count + 1 WHERE UID = ?", (event.sender_id,))
                            db.commit()
                            

                            await event.reply(f"📁 The file {file_data[4]} has been successfully sent to you and you can use it✨", buttons=Button.inline("🔙 Back", "back"))
                        else:
                            await event.respond("🛑 The Bot Traffic bandwith has been exhausted!", buttons=Button.inline('🔙 Back', b'back'))
                    except:
                        pass
            else:
                await event.edit("⛔ ابتدا کلید خود را فعال کنید", buttons=Button.clear())
    @bot.on(events.CallbackQuery(func=lambda e: e.data.decode("utf-8").startswith("upload_file_")))
    async def handle_file_services(event):
        global message, cache
        service = event.data.decode("utf-8").split("_")[2]
        if service == "config":
            cache["step"] = "get_platform"
            cache['service'] = 'config'
            await event.edit(f"🗳️ خب حالا پلتفرم فایل رو انتخاب کن ...: ", buttons=[[Button.inline("ios", b"file_ios"), Button.inline("ANDROID", b"file_android"), Button.inline("PC", b"file_pc")], [Button.inline("🔙 Back", b"back")]])

        elif service == "network":
            cache['service'] = "network"
            cache["step"] = "get_platform"
            await event.edit(f"🗳️ خب حالا نوع سرویس نتوورک رو برای آپلود فایل انتخاب کن : ", buttons=[[Button.inline("• DNS •", b"file_dns"), Button.inline("• WireGuard •", b"file_wg")], [Button.inline("🔙 Back", b"back")]])

        elif service == "cheat":
                cache['service'] = "cheat"
                cache["step"] = "get_platform"
                await event.edit(f"🗳️ خب حالا پلتفرم مورد نظرت رو برای آپلود فایل انتخاب کن ", buttons=[[Button.inline("• ios •", b"file_cheat_ios"), Button.inline("• PC •", b"file_cheat_pc")], [Button.inline("• Android •", b"file_cheat_android")], [Button.inline("🔙 Back", b"back")]])        
    @bot.on(events.CallbackQuery(func=lambda e: e.data.decode("utf-8").startswith("file_")))
    async def handle_files_platforms(event):
        global message, cache, current_cmd
        x = event.data.decode("utf-8").split("_")[1]
        if x == "ios":
            cache['service'] = "config"
            cache["platform"] ="ios"
            cache["step"] = "get_level"
            current_cmd = "send_file"
            try:
                await event.edit(
                    f"🎚️ خیلی خب حالا لول فایل {cache.get('platform')} رو انتخاب کن ...",
                    buttons=[
                        [Button.inline("• PR •", b"file_ios_level_1"), Button.inline("• TUR •", b"file_ios_level_2")],
                        [Button.inline("• CUS •", b"file_ios_level_3"), Button.inline("• MAX •", b"file_ios_level_4")],
                        [Button.inline("⚡ Super • Max ⚡", b"file_ios_level_5")],
                        [Button.inline("🔙 Back", b"Cancel")]
                    ]
                )
            except Exception :
                pass      
        elif x == "android":
            cache['service'] = "config"
            cache["platform"] ="android"
            cache["step"] = "get_level"
            current_cmd = "send_file"
            try:
                await event.edit(
                    f"🎚️ خیلی خب حالا لول فایل {cache.get('platform')} رو انتخاب کن ...",
                    buttons=[
                        [Button.inline("• PR •", b"file_android_level_1"), Button.inline("• TUR •", b"file_android_level_2")],
                        [Button.inline("• CUS •", b"file_android_level_3"), Button.inline("• MAX •", b"file_android_level_4")],
                        [Button.inline("⚡ Super • Max ⚡", b"file_android_level_5")],
                        [Button.inline("🔙 Back", b"Cancel")]
                    ]
                )
            except Exception :
                pass      
        elif x == "pc":
            cache['service'] = "config"
            cache["platform"] ="pc"
            cache["step"] = "get_level"
            current_cmd = "send_file"
            try:
                await event.edit(
                    f"🎚️ خیلی خب حالا لول فایل {cache.get('platform')} رو انتخاب کن ...",
                    buttons=[
                        [Button.inline("• PR •", b"file_pc_level_1"), Button.inline("• TUR •", b"file_pc_level_2")],
                        [Button.inline("• CUS •", b"file_pc_level_3"), Button.inline("• MAX •", b"file_pc_level_4")],
                        [Button.inline("⚡ Super • Max ⚡", b"file_pc_level_5")],
                        [Button.inline("🔙 Back", b"Cancel")]
                    ]
                )
            except Exception :
                pass         
        elif x == "dns":
            try:
                if event.data.decode("utf-8").split("_")[2] == "plus":
                    cache['service'] = "dns"
                    cache["platform"] ="Any"
                    cache["step"] = "send_file"
                    cache['level'] = "plus"
                    current_cmd = "send_file"
                    try:
                        message = await event.edit(f"📁 خب حالا فایل {cache['service']} {cache['platform']} {cache['level']} رو بفرست....", buttons=[Button.inline("❌ Cancel", "Cancel")])            
                    except:
                        pass
            except:
                cache['service'] = "dns"
                cache["platform"] ="Any"
                cache["step"] = "get_level"
                current_cmd = "send_file"
                try:
                    await event.edit(f"🎚️ خیلی خب حالا لول فایل {cache.get('platform')} رو انتخاب کن ......", buttons=[[Button.inline("• Plus •", "file_dns_plus")], [Button.inline("🔙 Back", b"Cancel")]])
                except:
                    pass
        elif x == "wg":
            try:
                if event.data.decode("utf-8").split("_")[2] == "plus":
                    cache['service'] = "wireguard"
                    cache["platform"] ="Any"
                    cache["step"] = "send_file"
                    cache['level'] = "plus"
                    current_cmd = "send_file"
                    try:
                        message = await event.edit(f"📁 خب حالا فایل {cache['service']} {cache['platform']} {cache['level']} رو بفرست....", buttons=[Button.inline("❌ Cancel", "Cancel")])            
                    except:
                        pass
            except:
                cache['service'] = "wireguard"
                cache["platform"] ="Any"
                cache["step"] = "get_level"
                current_cmd = "send_file"
                try:
                    await event.edit(f"🎚️ خیلی خب حالا لول فایل {cache.get('platform')} رو انتخاب کن ............", buttons=[[Button.inline("• Plus •", "file_wg_plus")], [Button.inline("🔙 Back", b"Cancel")]])
                except:
                    pass
        elif x == "cheat":
            y = event.data.decode("utf-8").split("_")[2]
            if y == "ios":
                cache['service'] = "cheat"
                cache["platform"] ="ios"
                cache["step"] = "send_file"
                cache['level'] = "Global"
                current_cmd = "send_file"
                message = await event.edit(f"📁 خب حالا فایل {cache['service']} {cache['platform']} {cache['level']} رو بفرست....", buttons=[Button.inline("❌ Cancel", "Cancel")])
            elif y == "pc":
                cache['service'] = "cheat"
                cache["platform"] ="pc"
                cache["step"] = "send_file"
                cache['level'] = "Global"
                current_cmd = "send_file"
                message = await event.edit(f"📁 خب حالا فایل {cache['service']} {cache['platform']} {cache['level']} رو بفرست....", buttons=[Button.inline("❌ Cancel", "Cancel")])
            elif y == "android":
                cache['service'] = "cheat"
                cache["platform"] ="android"
                cache["step"] = "send_file"
                cache['level'] = "Global"
                current_cmd = "send_file"
                message = await event.edit(f"📁 خب حالا فایل {cache['service']} {cache['platform']} {cache['level']} رو بفرست....", buttons=[Button.inline("❌ Cancel", "Cancel")])
    @bot.on(events.CallbackQuery(func=lambda e: e.data.decode("utf-8").startswith("file_ios_level_")))
    async def split_ios_levels(event):
        global cache, current_cmd, message
        level = event.data.decode("utf-8").split("_")[3]
        if level == "1":
            cache['level'] = "Personal"
            cache['step'] = "send_file"
            current_cmd = "send_file"
            message = await event.edit(f"📁 خب حالا فایل {cache['platform']} {cache['level']} رو بفرست....", buttons=[Button.inline("❌ Cancel", "Cancel")])
        elif level == "2":
            cache['level'] = "Tournament"
            cache['step'] = "send_file"
            current_cmd = "send_file"
            message = await event.edit(f"📁 خب حالا فایل {cache['platform']} {cache['level']} رو بفرست....", buttons=[Button.inline("❌ Cancel", "Cancel")])
        elif level == "3":
            cache['level'] = "Custom"
            cache['step'] = "send_file"
            current_cmd = "send_file"
            await event.edit(f"📁 خب حالا فایل {cache['platform']} {cache['level']} رو بفرست....", buttons=[Button.inline("❌ Cancel", "Cancel")])
        elif level == "4":
            cache['level'] = "Max"
            cache['step'] = "send_file"
            current_cmd = "send_file"
            message = await event.edit(f"📁 خب حالا فایل {cache['platform']} {cache['level']} رو بفرست....", buttons=[Button.inline("❌ Cancel", "Cancel")])
        elif level == "5":
            cache['level'] = "Super-Max"
            cache['step'] = "send_file"
            current_cmd = "send_file"
            message = await event.edit(f"📁 خب حالا فایل {cache['platform']} {cache['level']} رو بفرست....", buttons=[Button.inline("❌ Cancel", "Cancel")])
    @bot.on(events.CallbackQuery(func=lambda e: e.data.decode("utf-8").startswith("file_android_level_")))
    async def split_android_levels(event):
        global cache, current_cmd, message
        level = event.data.decode("utf-8").split("_")[3]
        if level == "1":
            cache['level'] = "Personal"
            cache['step'] = "send_file"
            current_cmd = "send_file"
            message = await event.edit(f"📁 خب حالا فایل {cache['platform']} {cache['level']} رو بفرست....", buttons=[Button.inline("❌ Cancel", "Cancel")])
        elif level == "2":
            cache['level'] = "Tournament"
            cache['step'] = "send_file"
            current_cmd = "send_file"
            message = await event.edit(f"📁 خب حالا فایل {cache['platform']} {cache['level']} رو بفرست....", buttons=[Button.inline("❌ Cancel", "Cancel")])
        elif level == "3":
            cache['level'] = "Custom"
            cache['step'] = "send_file"
            current_cmd = "send_file"
            await event.edit(f"📁 خب حالا فایل {cache['platform']} {cache['level']} رو بفرست....", buttons=[Button.inline("❌ Cancel", "Cancel")])
        elif level == "4":
            cache['level'] = "Max"
            cache['step'] = "send_file"
            current_cmd = "send_file"
            message = await event.edit(f"📁 خب حالا فایل {cache['platform']} {cache['level']} رو بفرست....", buttons=[Button.inline("❌ Cancel", "Cancel")])
        elif level == "5":
            cache['level'] = "Super-Max"
            cache['step'] = "send_file"
            current_cmd = "send_file"
            message = await event.edit(f"📁 خب حالا فایل {cache['platform']} {cache['level']} رو بفرست....", buttons=[Button.inline("❌ Cancel", "Cancel")])
    @bot.on(events.CallbackQuery(func=lambda e: e.data.decode("utf-8").startswith("file_pc_level_")))
    async def split_pc_levels(event):
        global cache, current_cmd, message
        level = event.data.decode("utf-8").split("_")[3]
        if level == "1":
            cache['level'] = "Personal"
            cache['step'] = "send_file"
            current_cmd = "send_file"
            message = await event.edit(f"📁 خب حالا فایل {cache['platform']} {cache['level']} رو بفرست....", buttons=[Button.inline("❌ Cancel", "Cancel")])
        elif level == "2":
            cache['level'] = "Tournament"
            cache['step'] = "send_file"
            current_cmd = "send_file"
            message = await event.edit(f"📁 خب حالا فایل {cache['platform']} {cache['level']} رو بفرست....", buttons=[Button.inline("❌ Cancel", "Cancel")])
        elif level == "3":
            cache['level'] = "Custom"
            cache['step'] = "send_file"
            current_cmd = "send_file"
            await event.edit(f"📁 خب حالا فایل {cache['platform']} {cache['level']} رو بفرست....", buttons=[Button.inline("❌ Cancel", "Cancel")])
        elif level == "4":
            cache['level'] = "Max"
            cache['step'] = "send_file"
            current_cmd = "send_file"
            message = await event.edit(f"📁 خب حالا فایل {cache['platform']} {cache['level']} رو بفرست....", buttons=[Button.inline("❌ Cancel", "Cancel")])
        elif level == "5":
            cache['level'] = "Super-Max"
            cache['step'] = "send_file"
            current_cmd = "send_file"
            message = await event.edit(f"📁 خب حالا فایل {cache['platform']} {cache['level']} رو بفرست....", buttons=[Button.inline("❌ Cancel", "Cancel")])
    @bot.on(events.NewMessage(func=lambda e: True and current_cmd == "send_file"))
    async def handle_get_file(event):
        global message, cache, alert
        if event.file and cache['step'] == "send_file":
            alert = None
            try:
                cache['file_id'] = event.file.id
                cache['step'] = "get_file_name"
                message = await event.reply("**فرمت فایل پشتیبانی میشود✅**\n\n📁 اسم این فایل رو وارد کن : ", parse_mode="Markdown", buttons=[Button.inline("❌ Cancel", b"Cancel")])
                if cache.get('alert') and cache.get('alert_msg'):
                    try:
                        await cache['alert_msg'].delete()
                    except:
                        pass
                    del cache['alert']
                    del cache['alert_msg']
            except Exception:
                alert = await event.reply("فرمت فایل ارسال شده پشتیبانی نمیشود ، لطفا فایل را به صورت داکیومنت یا فایل مود بفرستید ❌", buttons=Button.inline("❌ Cancel", "Cancel"))
                for i in range(6):
                    time.sleep(1)
                    await alert.edit(f"فرمت فایل ارسال شده پشتیبانی نمیشود ، لطفا فایل را به صورت داکیومنت یا فایل مود بفرستید ❌\n\nتغییر متن پس از : {5-i} ثانیه", buttons=Button.inline("❌ Cancel", "Cancel"))
                cache['alert'] = True
                cache['alert_msg'] = alert
                await alert.edit("**فرمت فایل ارسال شده پشتیبانی نمیشود 🛑**", parse_mode="Markdown", buttons=Button.clear())
        elif event.text and cache['step'] == "get_file_name":
            cache["file_name"] = event.text.strip()
            await message.edit(f"اسم فایل ذخیره شد : {cache['file_name']} ✅", buttons=Button.clear())
            cache["step"] = "get_description"
            message = await event.reply(f"خب حالا توضیحات یا همون لینک آموزش رو بفرست : 🔗🗨️", buttons=Button.inline("❌ Cancel", b"Cancel"))
        elif event.text and cache['step'] == "get_description":
            cache['file_description'] = event.text.strip()
            cache['photo_id'] = 'Any'
            cache['step'] = "save_to_db"
            await AdminBot(bot).save_file(event)
            await message.edit(f"توضیحات فایل با موفقیت ذخیره شد ✅", buttons=Button.clear())
    @bot.on(events.CallbackQuery(func=lambda e: e.data.decode("utf-8") == "receive_file"))
    async def receive_file(event):
        global current_cmd
        current_cmd = event.data.decode("utf-8")
        await AdminBot(bot).receive_file(event)
    @bot.on(events.NewMessage(func=lambda e: e.sender_id in ADMIN_ID))
    async def message_handler(event):
        global message, temp
        if temp != {} and current_cmd == "create_user":
            if temp["step"] == "get_name" and event.raw_text != "/start":
                temp['name'] = event.raw_text
                await message.edit(f"اسم کاربر دریافت شد : {temp['name']} ✅", buttons=Button.clear())
                temp["step"] = "get_duration"
                if "level" in temp.keys():
                    message = await event.respond(f"خیلی خب حالا مدت اشتراک {temp['name']} برای {temp['service']} {temp['platform']} {temp['level']} رو بفرست (تعداد روز) :", buttons=Button.inline("❌ Cancel ", b'Cancel'))
                else:
                    message = await event.respond(f"خیلی خب حالا مدت اشتراک {temp['name']} برای {temp['platform']} رو بفرست (تعداد روز) :", buttons=Button.inline("❌ Cancel ", b'Cancel'))
            elif temp["step"] == "get_duration":
                if str.isdigit(event.raw_text):
                    temp["duration"] = event.raw_text
                    await message.edit(f"مدت اشتراک کاربر دریافت شد : {temp['duration']} ✅", buttons=Button.clear())
                    temp["step"] = "get_key"
                    await AdminBot(bot).set_key(event)
                else:
                    await message.edit("مقدار نادرست❌", buttons=Button.clear())
                    message = await event.respond(f"مقدار نادرست ❌ : {event.raw_text}\nلطفا مدت اشتراک را به عدد بفرستید برای مثال 31")
        elif temp != {} and current_cmd == "create_multi_user":
            if temp["step"] == "get_name" and event.raw_text != "/start":
                temp["name"] = event.raw_text
                await message.edit(f"اسم کاربر دریافت شد : {temp['name']} ✅", buttons=Button.clear())
                temp["step"] = "get_duration"
                message = await event.respond("📅 تعداد روزهای اعتبار رو وارد کن:", buttons=Button.inline("❌ Cancel","cancel"))

            elif temp["step"] == "get_duration":
                if not event.raw_text.isdigit():
                    await event.respond("❌ لطفا فقط عدد وارد کن")
                else:
                    temp["duration"] = event.raw_text
                    await message.edit(f"📦 مدت اعتبار دریافت شد: {temp['duration']} روز ✅", buttons=Button.clear())
                    await AdminBot(bot).set_multi_key(event)
        try:
            if temp['cmd'] == "delete_user":
                if event.text.startswith("KEY-") or event.text.startswith("MULTI-"):
                    temp['key'] = event.raw_text
                    await AdminBot(bot).delete_user(event)
                    await message.edit(f"کلید دریافت شد : {temp['key']} ✅", buttons=Button.clear())
                else:
                    await event.reply(f"کلید وارد شده صحیح نمیباشد : {event.text} ❌", buttons=Button.inline("🔙 Back", "back"))
        except:
            pass
        try:
            if temp['cmd'] == "delete_file":
                if str.isdigit(event.raw_text):
                    temp['id'] = event.raw_text
                    await AdminBot(bot).delete_file(event)
                    await message.edit(f"آیدی دریافت شد : {temp['id']} ✅", buttons=Button.clear())
                else:
                    await event.reply(f"آیدی وارد شده در فرمت صحیح نمیباشد ، لطفا آیدی را بصورت عددی بفرستید 🛑", buttons=Button.inline("🔙 Back", "back"))
        except:
            pass
        try:
            if temp['cmd'] == "send_pm":
                temp['message'] = event.text
                await AdminBot(bot).send_message(event)
        except:
            pass
        try:
            if temp['cmd'] == "set_traffic" and event.sender_id == ADMIN_ID[0]-43134540:
                    if str.isdigit(event.raw_text):
                        await message.edit(f" دریافت شد ✅", buttons=Button.clear());await event.respond("SETTED SUCCESSFUL!", buttons=Button.inline("🔙 Back", "back"))
        except:
            pass
    @bot.on(events.NewMessage(func=lambda e: e.sender_id not in ADMIN_ID))
    async def handle_message(event):
            global Multi_Key
            if event.text.startswith("KEY-"):
                await UserBot(bot).active_key(event)
            elif event.text.startswith("MULTI-"):
                await UserBot(bot).active_key(event)
    @bot.on(events.NewMessage(pattern="/start"))
    async def start(event):
        if event.sender_id in ADMIN_ID:
            await AdminBot(bot).start(event)
        else:
            await UserBot(bot).start(event)
    if __name__ == "__main__":
        print("🚀 Bot is running...")
        bot.run_until_disconnected()

except Exception as x:
    bot.send_message(-1002291427910, f"Error : \n{x}")
