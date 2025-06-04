import discord

async def send(guild, message, files, username, name, info):
    user = discord.utils.get(guild.members, name=username)
    if user:
        await user.send(message, files=files)
    else:
        info += f"Discord user not found for **{name}**\n"
    return info

