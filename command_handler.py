#Related to responding to commands
import bot_actions
import torn_api
import mongo_db
import glob

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
    else:
        pass

#---Help Text
async def help(message, client):
   await message.reply("```\nHelp!\n\n!api [public api key] [rate_limit]\nRegisters or updates a public API key in the database. Rate limit controls the number of calls per minute and defaults to " + str(def_rate) + ".\n\n!remove\nRemoves the users saved API info.\n```")
  
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
        response = mongo_db.add_api(verified[1], api, verified[2], rate_limit)
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
    print(message)
    filter = {}
    filter['discord_id'] = str(message.author.id)
    response = mongo_db.rm_api(filter)
    await message.reply(response)
        

      
  
    