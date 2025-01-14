import sys
import os
import discord
from discord.ext import commands
from greet_member.greet_member import generate_greeting_card

BOT_TOKEN = 'YOUR_BOT_TOKEN'
CHANNEL_ID = YOUR_CHANNEL_ID
ROLE_ID = YOUR_ROLE_ID
MESSAGE_CONTENT = (
    "Reacted with 🚽 to get *slightly* access to the server ||if you want full access, message <@763017830215319572>||"
)

intents = discord.Intents.default()
intents.messages = True
intents.reactions = True
intents.guilds = True
intents.members = True

bot = commands.Bot(command_prefix="!", intents=intents)

@bot.event
async def on_ready():
    channel = bot.get_channel(CHANNEL_ID)
    if channel:
        try:
            message = await channel.send(MESSAGE_CONTENT)
            await message.add_reaction("🚽")
        except Exception as e:
            print(f"Error sending message: {e}")

@bot.event
async def on_raw_reaction_add(payload):
    if payload.channel_id == CHANNEL_ID and payload.emoji.name == "🚽":
        guild = bot.get_guild(payload.guild_id)
        member = guild.get_member(payload.user_id)
        role = guild.get_role(ROLE_ID)
        if member and role:
            try:
                await member.add_roles(role, reason="Reacted with 🚽 to the message.")
            except Exception as e:
                print(f"Error adding role: {e}")

@bot.event
async def on_raw_reaction_remove(payload):
    if payload.channel_id == CHANNEL_ID and payload.emoji.name == "🚽":
        guild = bot.get_guild(payload.guild_id)
        member = guild.get_member(payload.user_id)
        role = guild.get_role(ROLE_ID)
        if member and role:
            try:
                await member.remove_roles(role, reason="Removed 🚽 reaction from the message.")
            except Exception as e:
                print(f"Error removing role: {e}")

@bot.event
async def on_member_join(member):
    channel = bot.get_channel(CHANNEL_ID)
    if channel:
        try:
            card = generate_greeting_card(
                member.name,
                str(member.discriminator),
                len(member.guild.members),
                os.path.join("greet_member", "image.webp"),
                os.path.join("greet_member", "Roboto-Bold.ttf")
            )
            await channel.send(file=discord.File(card, filename="welcome.png"))
        except Exception as e:
            print(f"Error generating greeting card: {e}")

bot.run(BOT_TOKEN)
