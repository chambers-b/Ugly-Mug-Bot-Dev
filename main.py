#Bot install hyperlink
#https://discord.com/api/oauth2/authorize?client_id=803775247026880522&permissions=534723819584&scope=bot%20applications.commands
import discord
import os
import json
import asyncio
from discord.ext import tasks
import time
from datetime import datetime
import threading

import bot_actions
import command_handler
import torn_api  #used?
import mongo_db  #not used
import mongo_connector
import glob



class MyClient(discord.Client):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        #Object variables (properties)
        self.faction_list = []
        self.stored_mark = {}
        self.pending_messages = []
        self.counter = 0
        self.last_time = ""
        # start the task to run in the background
        print("Start Tasks")
        self.core_loop_60.start()
        self.core_loop_1.start()
        

        #self.main.start()


##TASK LOOP GOES BELOW (MUST BE INDENTED TO MyClient)_____________________

    @tasks.loop(seconds=60)
    async def core_loop_1(self):
        f = open('config.json')
        glob.al = json.load(f)
        mongo = mongo_connector.MongoDBConnection()
        with mongo:
            #Loop through factions and write/update user info + time into collection
            #bot_actions.update_marks
            print("1 minute task")

            t1 = threading.Thread(target=bot_actions.get_marks,
                                  args=(glob.faction_list[0:25], mongo, client))
            t2 = threading.Thread(target=bot_actions.get_marks,
                                  args=(self.faction_list[26:50], mongo, client))
            t3 = threading.Thread(target=bot_actions.get_marks,
                                  args=(self.faction_list[51:75], mongo, client))
            t4 = threading.Thread(target=bot_actions.get_marks,
                                  args=(self.faction_list[76:100], mongo, client))
            t5 = threading.Thread(target=bot_actions.get_marks,
                                  args=(self.faction_list[101:125], mongo, client))
            t6 = threading.Thread(target=bot_actions.get_marks, 
                                  args=(self.faction_list[126:150],mongo, client))
            t7 = threading.Thread(target=bot_actions.get_marks, 
                                  args=(self.faction_list[151:175],mongo, client))
            t8 = threading.Thread(target=bot_actions.get_marks, 
                                  args=(self.faction_list[176:200],mongo, client))
            t9 = threading.Thread(target=bot_actions.get_marks, 
                                  args=(self.faction_list[201:225],mongo, client))
            t10 = threading.Thread(target=bot_actions.get_marks, 
                                  args=(self.faction_list[226:250],mongo, client))
            # bot_actions.get_marks(self.faction_list[0:50], mongo)
            t1.start()
            # t2.start()
            # t3.start()
            # t4.start()
            # t5.start()
            # t6.start()
            # t7.start()
            # t8.start()
            # t9.start()
            # t10.start()
            t1.join()
            # t2.join()
            # t3.join()
            # t4.join()
            # t5.join()
            # t6.join()
            # t7.join()
            # t8.join()
            # t9.join()
            # t10.join()
            #Add a mongo query looking for soonish landings
            while len(client.pending_messages) > 0:
                parameters = client.pending_messages.pop(0)
                await bot_actions.embed_channel(parameters[0], parameters[1], client)
            #await bot_actions.message_channel("Testing Messages", channel_list["admin_notifications"], client)
        #mongo_db.get_api()

    #Runs before the above begins repeating - not currently used
    @core_loop_1.before_loop
    async def before_my_task(self):
        #Need a boot process to retrieve keys
        await self.wait_until_ready()  # wait until the bot logs in
        print("core_loop_1 setup function")

        #Not sure if setup tasks should go here or in on_ready() Maybe cannot use object variables if below?
    @tasks.loop(minutes=60)
    async def core_loop_60(self):
        mongo = mongo_connector.MongoDBConnection()
        with mongo:
            print("Retrieving faction list")
            glob.faction_list = torn_api.get_faction_list(mongo)[1]
            #Smaller list of factions to demo
            #self.faction_list = [8989, 9055, 11581, 11747, 27312, 2013]

        #Loop through factions and write/update user info + time into collection
        #bot_actions.update_marks

client = MyClient(
    intents=discord.Intents.all())  #Uses message intents and presence intents


@client.event
async def on_ready():
    print(f'{client.user} has connected to Discord!')
    await client.change_presence(activity=discord.Activity(
        type=discord.ActivityType.watching, name="for !"))

    #!#Task setup goes here
    #api_list = mongo_db.get_api_list() #How often should this refresh? Every hour?
    #faction_list = bot_actions.get_faction_list()


@client.event
async def on_message(message):
    if message.author == client.user:
        print("Self Message")
        return
    if message.author.bot:
        print("Bot Message")
        return
    if message.content.startswith('!'):
        await command_handler.main(message, client)

        #await message.reply("Attempting Import")
        #await message.reply(functions.bulk_import(message))


#client = MyClient() #This is done at the top

#LAST ROW IS RUN
print("Rate Limit in effect: " + str(client.is_ws_ratelimited()))
response = client.run(os.getenv('TOKEN'))
print(response)  #MugBot#3740 has connected to Discord!
