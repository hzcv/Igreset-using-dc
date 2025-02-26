import discord
import uuid
import random
import requests
import json
from discord.ext import commands

# Configuration
DISCORD_TOKEN = 'YOUR_DISCORD_BOT_TOKEN'
INSTAGRAM_URL = 'https://i.instagram.com/api/v1/accounts/send_password_reset/'
USER_AGENT = "Instagram 113.0.0.39.122 Android (24/5.0; 515dpi; 1440x2416; 'huawei/google; Nexus 6P; angler; angler; en_US)"

# Create a new bot instance
intents = discord.Intents.all()
bot = commands.Bot(command_prefix='/', intents=intents, case_insensitive=True, self_bot=True)


@bot.event
async def on_ready():
    """Event triggered when the bot is ready."""
    print(f'Logged in as {bot.user.name}')


@bot.command()
async def reset(ctx, user):
    """Send a password reset link to an Instagram user."""
    guid = str(uuid.uuid4())
    header = {
        "user-agent": USER_AGENT,
        "Content-Type": "application/x-www-form-urlencoded"
    }

    if "@" in user:
        payload = f"_csrftoken=QsH54d5BufeHPDczQuauI3Qt7G0M8ixs&user_email={user}&guid={guid}&device_id={guid}"
    else:
        payload = f"_csrftoken=QsH54d5BufeHPDczQuauI3Qt7G0M8ixs&username={user}&guid={guid}&device_id={guid}"

    try:
        response = requests.post(INSTAGRAM_URL, verify=False, headers=header, data=payload).text
        print(response)

        if "obfuscated_email" in response:
            embed = discord.Embed(
                colour=discord.Colour.dark_green(),
                title="Sent Password Reset To"
            )
            embed.set_author(name=user)
            embed.add_field(name="", value=response)
            await ctx.reply(embed=embed)
        elif "Sorry, we can't send you a link to reset your password" in response:
            error = discord.Embed(
                colour=discord.Colour.dark_red(),
                title="Sorry, there was a problem. Please contact Instagram."
            )
            error.set_author(name=user)
            await ctx.reply(embed=error)
        elif "The link you followed may be broken, or the page may have been removed." in response:
            error1 = discord.Embed(
                colour=discord.Colour.dark_red(),
                title="User Not Found."
            )
            error1.set_author(name=user)
            await ctx.reply(embed=error1)
        else:
            error2 = discord.Embed(
                colour=discord.Colour.dark_red(),
                title="Rate Limit. Please try after some time."
            )
            error2.set_author(name=user)
            await ctx.reply(embed=error2)
    except requests.exceptions.RequestException as e:
        error3 = discord.Embed(
            colour=discord.Colour.dark_red(),
            title="An error occurred while sending the request."
        )
        error3.set_author(name=user)
        error3.add_field(name="Error", value=str(e))
        await ctx.reply(embed=error3)


bot.run(DISCORD_TOKEN)
