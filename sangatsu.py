import os
import threading
import random
from http.server import HTTPServer, BaseHTTPRequestHandler

import discord
from discord.ext import commands
from datetime import datetime
from zoneinfo import ZoneInfo

# ========= ダミーWebサーバー（Render用） =========
class Handler(BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.end_headers()
        self.wfile.write(b"Bot is running")

def run_server():
    port = int(os.environ.get("PORT", 10000))
    server = HTTPServer(("0.0.0.0", port), Handler)
    server.serve_forever()

threading.Thread(target=run_server, daemon=True).start()

# ========= Bot設定 =========
intents = discord.Intents.default()
intents.message_content = True

bot = commands.Bot(command_prefix="!", intents=intents)

TRIGGERS = ["サンガツ", "ｻﾝｶﾞﾂ", "さんがつ", "sangatu",  "sangatsu"]

FOOTER_LINES = [
    "季節感は大事にしよう。",
    "今はまだその時期じゃない。",
    "カレンダーって知ってる？便利だよ。",
    "3月はまだ準備中らしい。",
    "落ち着いて、気持ちが先走っているよ。",
    "こっちの時空と少しズレているかも。",
    "未来を先取りしすぎているね。",
    "そんなにホワイトデーが楽しみかい？",
    "その3月への執念、少し尊敬する。",
]

# ========= 起動 =========
@bot.event
async def on_ready():
    print(f"Botが起動しました: {bot.user}")

# ========= メッセージ処理 =========
@bot.event
async def on_message(message):
    if message.author.bot:
        return

    content = message.content

    if any(word in content for word in TRIGGERS):

        now = datetime.now(ZoneInfo("Asia/Tokyo"))

        # 次の3月1日
        year = now.year + (1 if now.month >= 3 else 0)
        target = datetime(year, 3, 1, tzinfo=ZoneInfo("Asia/Tokyo"))

        delta = target - now
        total = int(delta.total_seconds())

        days = total // 86400
        hours = (total % 86400) // 3600
        minutes = (total % 3600) // 60
        seconds = total % 60

        countdown = f"～3月まであと{days}日{hours}時間{minutes}分{seconds}秒～"

        roll = random.random()

        # 5%：3月警察
        if roll < 0.02:
            await message.channel.send(
                f"{message.author.mention} ⚠️ﾋﾟﾋﾟｰ‼️3月警察だ‼️👮\n"
                f"3月虚偽親告罪により逮捕する‼️。\n"
                f"{countdown}"
            )

        # 95%：通常
        else:
            footer = random.choice(FOOTER_LINES)

            await message.channel.send(
                f"{message.author.mention} ちょっと待って！今は{now.month}月だよ。\n"
                f"{footer}\n"
                f"{countdown}"
            )

    await bot.process_commands(message)

# ========= 起動 =========
TOKEN = os.getenv("DISCORD_TOKEN")

if not TOKEN:
    print("ERROR: DISCORD_TOKENが設定されていません")
else:
    bot.run(TOKEN)
