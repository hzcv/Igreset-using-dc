import os
import uuid
import string
import random
import requests
import discord
from discord.ext import commands

# Load Discord bot token from environment variables
DISCORD_TOKEN = os.getenv("DISCORD_TOKEN")

if not DISCORD_TOKEN:
    raise ValueError("Please set the DISCORD_TOKEN environment variable.")

# Initialize the bot
bot = commands.Bot(command_prefix="/", intents=discord.Intents.all())

class InstagramPasswordReset:
    def __init__(self, target):
        self.target = target
        if self.target[0] == "@":
            raise ValueError("Enter the username without '@'.")
        
        if "@" in self.target:
            self.data = {
                "_csrftoken": "".join(random.choices(string.ascii_letters + string.digits, k=32)),
                "user_email": self.target,
                "guid": str(uuid.uuid4()),
                "device_id": str(uuid.uuid4())
            }
        else:
            self.data = {
                "_csrftoken": "".join(random.choices(string.ascii_letters + string.digits, k=32)),
                "username": self.target,
                "guid": str(uuid.uuid4()),
                "device_id": str(uuid.uuid4())
            }

    def send_password_reset(self):
        headers = {
            "user-agent": f"Instagram 150.0.0.0.000 Android (29/10; 300dpi; 720x1440; {''.join(random.choices(string.ascii_lowercase + string.digits, k=16))}/{''.join(random.choices(string.ascii_lowercase + string.digits, k=16))}; {''.join(random.choices(string.ascii_lowercase + string.digits, k=16))}; {''.join(random.choices(string.ascii_lowercase + string.digits, k=16))}; {''.join(random.choices(string.ascii_lowercase + string.digits, k=16))}; en_GB;)"
        }
        response = requests.post(
            "https://i.instagram.com/api/v1/accounts/send_password_reset/",
            headers=headers,
            data=self.data
        )
        return response.text, response.status_code

@bot.event
async def on_ready():
    print(f"Logged in as {bot.user.name}")

@bot.command(name="reset")
async def reset(ctx, target: str):
    try:
        reset_tool = InstagramPasswordReset(target)
        response_text, status_code = reset_tool.send_password_reset()

        if "obfuscated_email" in response_text:
            embed = discord.Embed(
                title="Password Reset Sent",
                description=f"Password reset link sent to `{target}`.",
                color=discord.Color.green()
            )
        else:
            embed = discord.Embed(
                title="Error",
                description=f"Failed to send password reset to `{target}`.\nResponse: {response_text}",
                color=discord.Color.red()
            )

        await ctx.reply(embed=embed)

    except ValueError as e:
        await ctx.reply(f"Error: {str(e)}")
    except Exception as e:
        await ctx.reply(f"An unexpected error occurred: {str(e)}")

# Run the bot
bot.run(DISCORD_TOKEN)
