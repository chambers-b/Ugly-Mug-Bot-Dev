#---Remove Message
#---Removes messages as they are posted, will not work in private interactions with bot.
async def rm_message(message):
    if message.guild:
        await message.delete()