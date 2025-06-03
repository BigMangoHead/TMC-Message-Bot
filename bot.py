import discord
from discord.ext import commands
from discord import app_commands
from send import deploy_message

intents = discord.Intents.default()
intents.message_content = True
intents.members = True

bot = commands.Bot(command_prefix='!', intents=intents)

@bot.event
async def on_ready():
    try: 
        guild = discord.Object(id=1170796078598193295)
        synced = await bot.tree.sync(guild=guild)
        print(f'Synced {len(synced)} commands to guild {guild.id}')
    except Exception as e:
        print(f'Error syncing commands: {e}')

    print("Bot started successfully.")

GUILD_ID = discord.Object(id=1170796078598193295)

@bot.tree.command(name="message", description="Forwards last sent message to given list of people", guild=GUILD_ID)
async def send_message(interaction: discord.Interaction):
    channel = bot.get_channel(interaction.channel_id)

    # Last message is not guaranteed to be valid, so we run a few checks
    last_message = channel.last_message

    if (last_message is None):
        await interaction.response.send_message("Message not found, please resend it and try again.", ephemeral=True)
    elif (last_message.author != interaction.user):
        await interaction.response.send_message("The last message was not sent by you. Please resend your message.", ephemeral=True)
    else: 
        webhook = interaction.followup
        await interaction.response.send_message("Message is being sent...", ephemeral=True)
        try:
            await deploy_message(bot, last_message)
        except Exception as e:
            await webhook.send(f"The following error was met while running. \n{e}")
        await webhook.send("Message sent successfully", ephemeral=True)


with open("data/bot-token") as file:
    token = file.read()

bot.run(token)
