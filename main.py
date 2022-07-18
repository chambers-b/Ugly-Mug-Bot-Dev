#Bot install hyperlink
#https://discord.com/api/oauth2/authorize?client_id=803775247026880522&permissions=534723819584&scope=bot%20applications.commands

from ext import *  #Import external package set
sys.path.append('../') #Allows subfiles to import directly from the top level files


import glob
import bot_actions
import command_handler
import torn_api  #used?
import mongo_db  #not used
import mongo_connector
import txt_log




class MyClient(discord.Client):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        #Object variables (properties)
        self.counter = 0
        self.last_time = ""
        # start the task to run in the background
        print("~~~ Start Task Loops ~~~~~~~~~")
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
            if glob.development_mode is not True:
                t1 = threading.Thread(target=bot_actions.get_marks,
                                      args=(glob.faction_list[0:40], mongo, client))
                t2 = threading.Thread(target=bot_actions.get_marks,
                                      args=(glob.faction_list[41:80], mongo, client))
                t3 = threading.Thread(target=bot_actions.get_marks,
                                      args=(glob.faction_list[81:120], mongo, client))
                t4 = threading.Thread(target=bot_actions.get_marks,
                                      args=(glob.faction_list[121:160], mongo, client))
                t5 = threading.Thread(target=bot_actions.get_marks,
                                      args=(glob.faction_list[160:200], mongo, client))
                t6 = threading.Thread(target=bot_actions.get_marks, 
                                      args=(glob.faction_list[201:240],mongo, client))
                t7 = threading.Thread(target=bot_actions.get_marks, 
                                      args=(glob.faction_list[241:280],mongo, client))
                t8 = threading.Thread(target=bot_actions.get_marks, 
                                      args=(glob.faction_list[281:320],mongo, client))
                t9 = threading.Thread(target=bot_actions.get_marks, 
                                      args=(glob.faction_list[321:],mongo, client))
                # t10 = threading.Thread(target=bot_actions.get_marks, 
                #                       args=(glob.faction_list[226:250],mongo, client))
              
                
                # bot_actions.get_marks(self.faction_list[0:50], mongo)
                t1.start()
                t2.start()
                t3.start()
                t4.start()
                t5.start()
                t6.start()
                t7.start()
                t8.start()
                t9.start()
                # t10.start()
                t1.join()
                t2.join()
                t3.join()
                t4.join()
                t5.join()
                t6.join()
                t7.join()
                t8.join()
                t9.join()
                # t10.join()
            else:
                print('~~~ Dev Mode ~~~~~~~~~~~~~~~~~')
                t_test = threading.Thread(target=bot_actions.get_marks, 
                                  args=(glob.faction_list[226:250],mongo, client))
                t_test.start()
                t_test.join()
            #Add a mongo query looking for soonish landings
            while len(glob.pending_messages) > 0:
                parameters = glob.pending_messages.pop(0)
                #send_embed(embed, channel_type, mark, client)
                result = await bot_actions.send_embed(parameters[0], parameters[1], parameters[2], client)
                #add_message(mark, channel_type, message_list)
                mongo_db.add_message(parameters[2], parameters[1], result, mongo)
                
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
        f = open('config.json')
        glob.al = json.load(f)
        mongo = mongo_connector.SilentConnection()
        with mongo:
            print("Retrieving faction list")
            glob.faction_list = torn_api.get_faction_list(mongo)[1]
            print("Removing old data")
            print(str(mongo_db.rm_old_marks(mongo)) + " records removed.")
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
    if (glob.development_mode is not True and not "dev" in message.content) or "dev" in message.content:
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
glob.player_list = mongo_db.get_mark_collection()
print("Rate Limit in effect: " + str(client.is_ws_ratelimited()))
response = client.run(os.getenv('TOKEN'))
print(response)  #MugBot#3740 has connected to Discord!
