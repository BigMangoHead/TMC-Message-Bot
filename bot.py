import discord
from discord.ext import commands
from discord import app_commands
from send import deploy_message

intents = discord.Intents.default()
intents.message_content = True
intents.members = True

bot = commands.Bot(command_prefix='!', intents=intents)

# Parse guilds
guildids = []
try: 
    with open("data/guilds") as file:
        guildids = file.read().split("\n")
except Exception as e:
    print("Problem reading \"data/guilds\" file.")
    print("Proceeding without syncronizing any guilds on load. This means that commands may not load for some time.")

guilds =[]
for guild in guildids:
    try:
        guilds.append(discord.Object(id=int(guild)))
    except:
        continue

# Events once loaded
@bot.event
async def on_ready():
    try: 
        for guild in guilds:
            synced = await bot.tree.sync(guild=guild)
            print(f"Synced {len(synced)} commands to guild {guild.id}")
    except Exception as e:
        print(f"Error syncing commands: {e}")

    print("Bot started successfully.")

@bot.tree.command(name="message", description="Forwards last sent message to given list of people", guilds=guilds)
async def send_message(interaction: discord.Interaction, subject: str, send_email: bool=True, send_text: bool=True):
    options = {
        "subject": subject,
        "send_email": send_email,
        "send_text": send_text
    }

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
            log = await deploy_message(bot, last_message, options)
        except Exception as e:
            await webhook.send(f"The following error was met while running. \n{e}")
            raise e
        if log == "":
            await webhook.send("Message sent successfully.", ephemeral=True)
        else: await webhook.send("Message sent successfully.\n\nLog:\n" + log, ephemeral=True)


with open("data/bot-token") as file:
    token = file.read()

bot.run(token)
