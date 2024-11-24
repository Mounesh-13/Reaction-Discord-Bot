import discord
from discord.ext import commands
import random
import aiohttp
import time
from discord.errors import HTTPException
from flask import Flask
from threading import Thread

# Intents and bot setup
intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix="!", intents=intents)

# Animal emojis
animal_emojis = {
    "cat": "😺",
    "dog": "🐶",
    "mouse": "🐭",
    "rabbit": "🐰",
    "fox": "🦊",
    "bear": "🐻",
    "panda": "🐼",
    "koala": "🐨",
    "tiger": "🐯",
    "lion": "🦁",
    "cow": "🐮",
    "pig": "🐷",
    "frog": "🐸",
    "monkey": "🐵",
    "chicken": "🐔",
    "penguin": "🐧",
    "bird": "🐦",
    "snake": "🐍",
    "horse": "🐴",
    "unicorn": "🦄",
    "fish": "🐟",
    "whale": "🐳",
    "dolphin": "🐬",
    "octopus": "🐙",
    "butterfly": "🦋",
    "crab": "🦀",
    "lobster": "🦞",
    "shrimp": "🦐",
    "spider": "🕷️",
    "bee": "🐝",
    "mikey": "💜"
}

# Keep track of reaction limits
last_reaction_time = 0
reaction_cooldown = 5  # 5 seconds cooldown between reactions

# Event: React to messages with animal emojis
@bot.event
async def on_message(message):
    global last_reaction_time

    current_time = time.time()
    if current_time - last_reaction_time < reaction_cooldown:
        return  # Don't react too often

    try:
        reactions_added = 0
        for animal, emoji in animal_emojis.items():
            if animal in message.content.lower() and reactions_added < 20:
                await message.add_reaction(emoji)
                reactions_added += 1

        last_reaction_time = current_time

    except HTTPException as e:
        if e.code == 429:  # Too many requests error
            await message.channel.send("Too many reactions, please wait a moment!")
        else:
            raise  # Re-raise if it's a different HTTP error

    await bot.process_commands(message)

# Command: Send animal GIFs
@bot.command()
async def gif(ctx, keyword="animal"):
    async with aiohttp.ClientSession() as session:
        async with session.get(f"https://g.tenor.com/v1/search?q={keyword}&key=LIVDSRZULELA") as r:
            if r.status == 200:
                data = await r.json()
                gif_url = data['results'][0]['media'][0]['gif']['url']
                await ctx.send(gif_url)
            else:
                await ctx.send("Couldn't fetch a GIF right now. Try again later!")

# Event: Bot is ready
@bot.event
async def on_ready():
    print(f'Logged in as {bot.user}')

# Flask app to keep the bot alive
app = Flask('')

@app.route('/')
def home():
    return "I'm alive!"

def keep_alive():
    Thread(target=lambda: app.run(host='0.0.0.0', port=8080)).start()

# Call keep_alive before bot.run
keep_alive()
bot.run('bot token')  # Replace 'YOUR_BOT_TOKEN' with your bot token
