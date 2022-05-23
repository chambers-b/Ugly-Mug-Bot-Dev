#---Send Message---  Unsure if this works or is necessary
async def message_user(message_text, author):
  await author.send(message_text)