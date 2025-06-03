import discord

async def deploy_message(bot, discord_message):
    text_message = discord_message.content

    user = discord.utils.get(bot.guilds[0].members, name="bigmangohead")
    if user:
        await user.send(text_message)
