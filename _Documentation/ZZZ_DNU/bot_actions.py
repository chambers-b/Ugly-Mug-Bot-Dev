#This has been replaced by the folder of the same name

#---Random utility functions related to the bot (sending messages, dealing with channels etc.)

from ext import *  #Import external package set
#from datetime import datetime

import torn_api
import mongo_db
import txt_log
import message_builder
import glob

            
        

#---Sends message to a group of channel id's (channel_list.json stores these and they are passed as a dictionary)
#---Currently disabled and prints to console instead  
def message_channel(message_text, channels, client):
    txt_log.console("bot_actions.message_channel", "debug")
    for channel_id in channels:
        #try:
        if True:
            #Not needed
            #guild = client.get_guild(652594486119235622)
            channel = client.get_channel(channel_id)
            # coro = channel.send(message_text)
            # print("Sending message")
            # fut = asyncio.run_coroutine_threadsafe(coro, client.loop)
            # try:
            #     fut.result()
            # except:
            #     print("Message faild to send")
            #     pass
            # print(str(channel) + ": " + message_text)
            # msg_thread = threading.Thread(target=channel.send,
            #                       args=(str(message_text)))
            # msg_thread.start()
        else:    
        #except:
            print("Failed to send in " + str(channel_id))
          
#buy mug mark:{'_id': '2034640', 'name': 'lightnemesis', 'last_update': 1651854592.0, 'faction': 27223, 'status': 'Offline', 'description': 'Okay', 'state': 'Okay'} 
#travel mark:{'_id': '2731392', 'name': 'Andeafdod', 'last_update': 1651856448.0, 'faction': 25025, 'status': 'Online', 'description': 'Returning to Torn from Switzerland', 'state': 'Traveling', 'landing_time': 1651863915.0, 'depart_cash': 3100750, 'landing_cash': 2465000}
async def embed_channel(embed, channel_type, mark, client):
    txt_log.console("bot_actions.embed_channel", "debug")
    channel_responses = []
    for channel_id in glob.al[channel_type]:
        #try:
        if True:
            #Not needed
            #guild = client.get_guild(652594486119235622)
            channel = client.get_channel(channel_id)
            txt_log.log(str(channel) + ": Launching Embed")
            print("~~~~~~~~~~~~~~~~~~~~~~~")
            print(str(channel) + ": Launching Embed")
            print("~~~~~~~~~~~~~~~~~~~~~~~")
            #TEST
            message_response = await channel.send(embed=embed)
            channel_responses.append(message_response.id)
            return channel_responses
        else:
        #except:
            txt_log.log("Failed to send in " + str(channel_id))
            print("Failed to send in " + str(channel_id))
            return False

#---Remove Message
#---Removes messages as they are posted, will not work in private interactions with bot.
async def rm_message(message):
    if message.guild:
        await message.delete()

#---Send Message---  Unsure if this works or is necessary
async def send(message_text, author):
  await author.send(message_text)




#X---Get Marks (targets) "The Brain"
#The first really complicated function pulls api via faction calls and looks for changes from the database, needs to track the timing of changes, eventually pull bazaar value and estimate a landing time.

def get_marks(faction_list, mongo, client):
    txt_log.console("bot_actions.get_marks", "debug")
    message_channel("Testing", [960573477977460767], client)
    user_count = 0
    ms = datetime.datetime.now()
    start_time = time.mktime(ms.timetuple())
    for faction in faction_list:
        if faction == 0:
            continue
        faction_obj = torn_api.get_members(faction, mongo)
        if faction_obj is False:
            txt_log.console("Escaping get_marks", "error")
            return False
        members = faction_obj['members']
        #print("Faction: " + str(faction) + " " + faction_obj['name'])
        #multi-thread this shit!
        ms = datetime.datetime.now()
        #print(time.mktime(ms.timetuple()))
        for member_id in members:
            user_count += 1
            member_obj = members[member_id]
            #print(member_id)
            mark = {}
            mark['_id'] = member_id
            mark['name'] = member_obj['name']
            mark['last_update'] = time.mktime(ms.timetuple())
            mark['faction'] = faction
            mark['status'] = member_obj['last_action']['status']
            mark['description'] = member_obj['status']['description']
            mark['state'] = member_obj['status']['state']
            if member_id not in glob.player_list.keys():
                #print("Retrieving " + str(member_id))
                glob.player_list[member_id] = mongo_db.get_mark(mark, mongo)
                
              
            if member_id not in glob.player_list.keys() or glob.player_list[member_id] == None: 
                try:
                    print(str(member_obj['name']) + " [" + str(member_id) + "]")
                    print(glob.player_list[member_id])
                except:
                    pass
                print("New: " + str(member_obj['name']) + " [" + str(member_id) + "]")
                mongo_db.update_mark(mark, mongo) 
                glob.player_list[member_id] = mark
            else:
                compare_result = compare_states(glob.player_list[member_id], mark, mongo, client)
                if compare_result is False:
                    txt_log.log("bot_actions.compare_states returned False in get_marks")
                
                    return False
                glob.player_list[member_id] =  compare_result
        mongo_db.update_timestamp(int(faction), mongo)
              
                
            
    ms = datetime.datetime.now()
    #print("Duration: " + str(time.mktime(ms.timetuple()) - start_time) + " seconds for " + str(len(faction_list)) + " factions with " + str(user_count) + " members.")
    mongo.user_count += user_count
    mongo.faction_count += len(faction_list)
    
    

def compare_states(old, new, mongo, client):
    txt_log.console("  bot_actions.compare_states", "debug")
    #print("Old: " + str(old))
    #print("New: " + str(new))
    bazaar = {}
    ms = datetime.datetime.now()
    time_now = time.mktime(ms.timetuple())
    change = False
#Travel Triggers
    #Departing Torn
    if "Traveling to" not in old['description'] and "Traveling to" in new['description']:
        new['depart_time'] = time_now
        bazaar = bazaar_check(new, mongo)
        if bazaar is False:
            txt_log.console("bot_actions.bazaar_check returned False in compare_states", "error")
            return False
        new['depart_cash'] = bazaar['bazaar_value']
        txt_log.console(old['name'] + " is " + new['description'].lower() + " departed @ " + str(new['depart_time']) + " with $" + str("{:,}".format(new['depart_cash'])) + " available in bazaar.", "travel")
        if 'travel_time' in new.keys():
            del new['travel_time']
        change = True
        #Get.bazaar value and check for deals
    #Arriving overseas
    elif "Traveling to" in old['description'] and "Traveling to" not in new['description']:
        try:    
            new['travel_time'] = time_now - old['depart_time'] 
            old['travel_time'] = new['travel_time']
            txt_log.console(old['name'] + " is " + new['description'].lower() + " flight took " + str("{:,}".format(new['travel_time']/60)) + " minutes.", "travel")
            #Use for xx is in xx with COH
            # if 'depart_cash' in old.keys():
            #     bazaar = bazaar_check(new, mongo)
            #     if bazaar is False:
            #         txt_log.log("bot_actions.bazaar_check returned False in compare_states")
            #         return False
            #     new['landing_cash'] = old['depart_cash'] - bazaar['bazaar_value']
        except:
            print("Skipping " + old['name'] + " missed departure.")
        change = True
    #Calculate landing time
    if "Returning" not in old['description'] and "Returning" in new['description']:
        try:
            new['landing_time'] = time_now + old['travel_time']
            txt_log.console(old['name'] + " is " + new['description'].lower() + " landing @ " + time.strftime("%H:%M:%S", time.gmtime(new['landing_time'])), "travel")
            if 'depart_cash' in old.keys():
                bazaar = bazaar_check(new, mongo)
                if bazaar is False:
                    txt_log.console("bot_actions.bazaar_check returned False in compare_states", "error")
                    return False
                new['depart_cash'] = old['depart_cash']
                new['landing_cash'] = old['depart_cash'] - bazaar['bazaar_value']
                txt_log.console("Cash Calc: " + str(new['landing_cash']) + " = " + str(old['depart_cash']) + " - " + str(bazaar['bazaar_value']), "travel")
                txt_log.console(old['name'] + " is landing with $" + str("{:,}".format(new['landing_cash'])) + " on hand.", "travel")
                if new['landing_cash'] > glob.al['min_on_hand']:
                    message_builder.build_mug_alert(new, ["flight"], mongo, client, bazaar)
            if 'travel_time' in new.keys():
                del new['travel_time']
        except:
            txt_log.console("Skipping " + old['name'] + " missed trip duration.", "travel")
        change = True

#Status triggers
    
    #Going offline out of hospital
    if old['status'] == 'Online' and new['status'] == 'Offline' and new['state'] == 'Okay':
        bazaar = bazaar_check(new, mongo)
        if bazaar is False:
            txt_log.console("bot_actions.bazaar_check returned False in compare_states", "error")
            return False
        txt_log.console(old['name'] + " is now " + new['status'].lower() + " with $" + str("{:,}".format(bazaar['buy_mug_value'])) + " worth of goods for sale.", "mugs")
        txt_log.console("Minimum mug is $" + str("{:,}".format(bazaar['potential_mug_value'])), "mugs")
        if bazaar['potential_mug_value'] > glob.al['min_mug_amount']:
            message_builder.build_mug_alert(new, ["buymug"], mongo, client, bazaar)
        change = True
        pass
    #Getting out of hosp soon and offline
    if "In hospital for 2 mins" in new['description'] and new['status'] == 'Offline':
        bazaar = bazaar_check(new, mongo)
        if bazaar is False:
            txt_log.console("bot_actions.bazaar_check returned False in compare_states", "error")
            return False
        txt_log.console(old['name'] + " is now " + new['status'].lower() + " with $" + str("{:,}".format(bazaar['buy_mug_value'])) + " worth of goods for sale.", "mugs")
        if bazaar['potential_mug_value'] > glob.al['min_mug_amount']:
            message_builder.build_mug_alert(new, ["buymug"], mongo, client, bazaar)
        change = True
        pass
    #Okay and in torn
    if new['state'] != "Traveling" and new['state'] != "Abroad":
        new, change = clear_travel_variables(new, change)
        

          
    #The change field tracks if a change was made and updates the database (reduces db calls)
    if change == True:
        #Logging
        status_changes = ""
        status_changes += old['name'] + " [" + str(old['_id']) + "] \n"
        status_changes += "Description: " + old['description'] + " -> " + new['description'] + "\n"
        status_changes += "      State: " + old['state'] + " -> " + new['state'] + "\n"
        status_changes += "     Status: " + old['status'] + " -> " + new['status'] + "\n"
        if 'bazaar_value' in  bazaar.keys():
            status_changes += "     Bazaar: " + str("{:,}".format(bazaar['bazaar_value'])) + "\n"
        if 'buy_mug_value' in  bazaar.keys():
            status_changes += "     Buymug: " + str("{:,}".format(bazaar['buy_mug_value'])) + "\n"
        if 'depart_time' in new.keys():
            status_changes += "Depart Time: " + time.strftime("%H:%M:%S", time.gmtime(new['depart_time'])) + "\n"
        if 'travel_time' in new.keys():
            status_changes += "Travel Time: " + time.strftime("%H:%M:%S", time.gmtime(new['travel_time'])) + "\n"
        if 'landing_time' in new.keys():
            status_changes += "  Land Time: " + time.strftime("%H:%M:%S", time.gmtime(new['landing_time'])) + "\n"
        if 'depart_cash' in new.keys():
            try:
                #This line is occasionally causing an error possibly from bazaar returning False
                status_changes += "Depart Cash: " + str("{:,}".format(new['depart_cash'])) + "\n"
            except:
                txt_log.console("Failed converting value in bot_actions: status_changes += " + str(new['depart_cash']), "error")
        if 'landing_cash' in new.keys():
            try:
                #This line is occasionally causing an error
                status_changes += "  Land Cash: " + str("{:,}".format(new['landing_cash'])) + "\n"
            except:
                txt_log.console("Failed converting value in bot_actions: status_changes += " + str(new['landing_cash']), "error")
            
        txt_log.console(status_changes, "state")
        mongo_db.update_mark(new, mongo)
        return new
    else:
        old['last_update'] = new['last_update']
        return old
#--Bazaar Check
#Handles the logic of checking bazaar for deals/triggers
  
def bazaar_check(member, mongo):
    txt_log.console("    bot_actions.bazaar_check", "debug")
    bazaar = torn_api.get_bazaar(member['_id'], mongo)
    if bazaar is False:
        txt_log.log("torn_api.get_bazaar returned False in bazaar_check")
        return False
    #print(bazaar)
    for item in bazaar['bazaar']:
        if item['price'] > 1 and item['market_price'] > 0:
            pct_change = (item['price'] - item['market_price'])/item['market_price']
            if pct_change < -0.05 and (item['market_price'] - item['price']) > 50000 and item['type'] not in mongo.excluded_categories:
                print("UNDERPRICED ITEM")
                print("Name : " + str(member['name']))
                print("Item : " + str(item['name']))
                print("Price: " + str(item['price']))
                print("Markt: " + str(item['market_price']))
                print("Diff : " + str(item['price'] - item['market_price']))
                print("% Dif: " + str(pct_change))


    
    #     print("  User ID: " + str(member_id))
    #     print("    Value: " + str("{:,}".format(bazaar['bazaar_value'])))
    #     print("BM Value : " + str("{:,}".format(bazaar['buy_mug_value'])))
    return bazaar 
#if db.inventory.find( { status: { $in: [message.author] } } ).limit(1).size() == 1:
#r = requests.get("https://api.torn.com/user/?selections=basic&key=" + db.inventory.find( { status: { $in: [message.author] } } {"api": 1, "_id": 0}).limit(1)

#Clears certain variables when player is in Torn
def clear_travel_variables(new, change):
    if 'depart_time' in new.keys():
        del new['depart_time']
        change = True
    if 'travel_time' in new.keys():
        del new['travel_time']
        change = True
    if 'landing_time' in new.keys():
        del new['landing_time']
        change = True
    if 'depart_cash' in new.keys():
        del new['depart_cash']
        change = True
    if 'landing_cash' in new.keys():
        del new['landing_cash']
        change = True  
    return new, change