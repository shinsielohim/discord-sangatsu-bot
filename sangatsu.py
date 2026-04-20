import os
import discord
from discord.ext import commands
from datetime import datetime
from zoneinfo import ZoneInfo

# ========= Bot設定 =========
intents = discord.Intents.default()
intents.message_content = True

bot = commands.Bot(command_prefix="!", intents=intents)

# 反応ワード
TRIGGERS = ["サンガツ", "ｻﾝｶﾞﾂ", "さんがつ"]

# ========= 起動 =========
@bot.event
async def on_ready():
    print(f"Botが起動しました: {bot.user}")

# ========= メッセージ処理 =========
@bot.event
async def on_message(message):
    # Bot自身は無視
    if message.author.bot:
        return

    content = message.content

    # トリガー判定
    if any(word in content for word in TRIGGERS):

        now = datetime.now(ZoneInfo("Asia/Tokyo"))
        current_month = now.month

        # 次の3月1日
        year = now.year
        if now.month >= 3:
            year += 1

        target = datetime(year, 3, 1, 0, 0, 0, tzinfo=ZoneInfo("Asia/Tokyo"))

        delta = target - now
        total_seconds = int(delta.total_seconds())

        days = total_seconds // 86400
        hours = (total_seconds % 86400) // 3600
        minutes = (total_seconds % 3600) // 60
        seconds = total_seconds % 60

        # 3月かどうか
        if now.month == 3:
            await message.channel.send(
                f"{message.author.mention} おめでとう！今は3月だよ！\n"
                f"この3月を思い切り楽しもう！\n"
                f"～3月が終わるまであと{days}日{hours}時間{minutes}分{seconds}秒～"
            )
        else:
            await message.channel.send(
                f"{message.author.mention} ちょっと待って！今はまだ{current_month}月だよ。\n"
                f"～3月まであと{days}日{hours}時間{minutes}分{seconds}秒～"
            )

    # コマンド維持
    await bot.process_commands(message)

# ========= 起動（Render対応） =========
TOKEN = os.getenv("DISCORD_TOKEN")

if not TOKEN:
    print("ERROR: DISCORD_TOKENが設定されていません")
else:
    bot.run(TOKEN)