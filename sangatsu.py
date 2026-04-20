import discord
from discord.ext import commands
from datetime import datetime
from zoneinfo import ZoneInfo

# Botの設定
intents = discord.Intents.default()
intents.message_content = True

bot = commands.Bot(command_prefix="!", intents=intents)

# 反応するワード
TRIGGERS = ["サンガツ", "ｻﾝｶﾞﾂ", "さんがつ"]

@bot.event
async def on_ready():
    print("Botが起動しました")

@bot.event
async def on_message(message):
    # Bot自身のメッセージには反応しない
    if message.author == bot.user:
        return

    # トリガー判定
    if any(word in message.content for word in TRIGGERS):

        # 日本時間取得
        now = datetime.now(ZoneInfo("Asia/Tokyo"))

        # 3月かどうか判定
        if now.month == 3:
            await message.channel.send(
                f"{message.author.mention} おめでとう！なんと今は3月だよ！\n"
                f"この3月を思う存分に楽しもう！\n"
                f"～3月が終わるまであと{days}日{hours}時間{minutes}分{seconds}秒～"
            )
        else:
            current_month = now.month

            # 次の3月1日を設定
            year = now.year
            if now.month >= 3:
                year += 1

            target = datetime(year, 3, 1, 0, 0, 0, tzinfo=ZoneInfo("Asia/Tokyo"))

            # 差分計算
            delta = target - now
            total_seconds = int(delta.total_seconds())

            days = total_seconds // 86400
            hours = (total_seconds % 86400) // 3600
            minutes = (total_seconds % 3600) // 60
            seconds = total_seconds % 60

            # 返信
            await message.channel.send(
                f"{message.author.mention} ちょっと待って！今はまだ{current_month}月だよ。\n"
                f"～3月まであと{days}日{hours}時間{minutes}分{seconds}秒～"
            )

    # コマンド処理維持
    await bot.process_commands(message)

# トークンを入れる
bot.run("TOKEN")