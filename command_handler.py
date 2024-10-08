#Related to responding to commands
import bot_actions
import torn_api
import mongo_db
import glob
import emojis
import faction_tools

#---api calls-per-minute settings 
#---(move to settings file when necessary)
max_rate = 90
def_rate = 40

#---Processes commands sent to bot via channel or PM
async def main(message, client):
    if message.content.startswith('!help'):
        await help(message, client)
    elif message.content.startswith('!api'):
        await api(message, client)
    elif message.content.startswith('!remove'):
        await rm_user(message, client)
    elif message.content.startswith('!test'):
        string = ''
        string += emojis.argentina
        string += emojis.canada
        string += emojis.caymen
        string += emojis.china
        string += emojis.clothingstore
        string += emojis.hawaii
        string += emojis.japan
        string += emojis.mexico
        string += emojis.southafrica
        string += emojis.switzerland
        string += emojis.torn
        string += emojis.uae
        string += emojis.unitedkingdom
        string += emojis.jigsarnak
            
        await message.reply(string)
    elif message.content.startswith('!msg') and str(message.author.id) in glob.al['admins']:
        await send_message(message.content, client)
    else:
        print(message.content)
        pass

#---Help Text
async def help(message, client):
   await message.reply("```\nHelp!\n\n!api [public api key] [rate_limit]\nRegisters or updates a public API key in the database. Rate limit controls the number of calls per minute and defaults to " + str(def_rate) + ".\n\n!remove\nRemoves the users saved API info.\n\n#flight-alerts - Usually accurate within 2 minutes. \nThis shows bazaar sales between leaving torn and beginning the return flight to torn.  Does not account for money spent overseas and there is a 15 second grace period for the user to store their cash when landing.\n\n#buy-mugs This shows users offline or about to be discharged from the hospital along with the values of fairly priceds goods in their bazaars.\nBe mindful of manipulated prices.\n\nAPI Info - Only a public API is required and it will be securely stored, only available to the developers behind the bot.  I recommend creating a key specifically for this so that you can simply delete the key if you ever leave (this does not happen automatically as I do not pull key owners data at all besides checking if they can revive).\nContact Komir[2392971] with any questions.```")
  
#---Register API
#Main API registration, handles checks and calls utility functions, updates if already present and attempts to delete the message with the key (only works in channels)
async def api(message, client):
    api = message.content.split(" ")[1]
    try:
        rate_limit = int(message.content.split(" ")[2])
        if rate_limit > max_rate: rate_limit = max_rate
    except:
        rate_limit = def_rate
    verified = torn_api.check_if_verified(message, api)
    if verified[0] == True:
        profile_obj = torn_api.get_profile("1000015", False, api)
        revive = False
        if profile_obj['revivable'] == 1:
            revive = True
        response = mongo_db.add_api(verified[1], api, verified[2], rate_limit, revive)
    elif verified[0] == False:
        response = verified[1]
    else:
          response = verified
    await message.reply(response)
    #Will throw an error if you remove the message first 
    #(nothing to reply to)
    await bot_actions.rm_message(message)

#---Remove User
#Removes a users info from "api_keys" collection
#X---Need to add retrieving the key itself and using pull_api(api_key)
async def rm_user(message, client):
    filter = {}
    filter['discord_id'] = str(message.author.id)
    response = mongo_db.rm_api(filter)
    await message.reply(response)
        

async def send_message(message, client):
    msg = message[5:]
    channel_id = []
    channel_id.append(msg[:18])
    msg = msg[19:]
    await bot_actions.message_channel(msg, channel_id, client)
    