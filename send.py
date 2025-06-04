import discord
from medium import discord_dm
from medium import discord_group

async def deploy_message(bot, discord_message, options):
    text_message = discord_message.content
    attachments = discord_message.attachments
    info = ""

    files = []
    for attachment in attachments:
        files.append(await attachment.to_file())

    people = ["bigmangohead"]

    info = await discord_group.send([bot.guilds[0]], text_message, files, info)
    for person in people:
        info = await discord_dm.send(bot.guilds[0], text_message, files, person, person, info)

    return info
