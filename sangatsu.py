import os
import threading
from http.server import HTTPServer, BaseHTTPRequestHandler

import discord
from discord.ext import commands
from datetime import datetime
from zoneinfo import ZoneInfo

# ========= ダミーWebサーバー =========
class Handler(BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.end_headers()
        self.wfile.write(b"Bot is running")

def run_server():
    port = int(os.environ.get("PORT", 10000))
    server = HTTPServer(("0.0.0.0", port), Handler)
    server.serve_forever()

threading.Thread(target=run_server).start()

# ========= Bot設定 =========
intents = discord.Intents.default()
intents.message_content = True

bot = commands.Bot(command_prefix="!", intents=intents)

TRIGGERS = ["サンガツ", "ｻﾝｶﾞﾂ", "さんがつ"]

@bot.event
async def on_ready():
    print(f"Botが起動しました: {bot.user}")

@bot.event
async def on_message(message):
    if message.author.bot:
        return

    if any(word in message.content for word in TRIGGERS):
        now = datetime.now(ZoneInfo("Asia/Tokyo"))

        year = now.year + (1 if now.month >= 3 else 0)
        target = datetime(year, 3, 1, tzinfo=ZoneInfo("Asia/Tokyo"))

        delta = target - now
        total = int(delta.total_seconds())

        days = total // 86400
        hours = (total % 86400) // 3600
        minutes = (total % 3600) // 60
        seconds = total % 60

        if now.month == 3:
            await message.channel.send(
                f"{message.author.mention} おめでとう！今は3月だよ！\n"
                f"この時間を思う存分楽しもう！\n"
                f"～3月が終わるまであと{days}日{hours}時間{minutes}分{seconds}秒～"
            )
        else:
            await message.channel.send(
                f"{message.author.mention} ちょっと待って！今は{now.month}月だよ。\n"
                f"～3月まであと{days}日{hours}時間{minutes}分{seconds}秒～"
            )

    await bot.process_commands(message)

# ========= 起動 =========
TOKEN = os.getenv("DISCORD_TOKEN")

if not TOKEN:
    print("TOKEN未設定")
else:
    bot.run(TOKEN)
