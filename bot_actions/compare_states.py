from ext import *  #Import external package set

import mongo_db
import txt_log
import message_builder
import glob
from bot_actions.bazaar_check import bazaar_check
from bot_actions.clear_travel_variables import clear_travel_variables

def compare_states(old, new, mongo):
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
                    message_builder.build_mug_alert(new, ["flight"], mongo, bazaar)
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
            message_builder.build_mug_alert(new, ["buymug"], mongo, bazaar)
        change = True
        pass

      
    #In hospital offline - Take inventory
    if old['status'] == 'Online' and new['status'] == 'Offline' and new['state'] == 'Hospital':
        bazaar = bazaar_check(new, mongo)
        new['depart_cash'] = bazaar['bazaar_value']
        change = True

      
    #In hospital online - clear values
    elif old['status'] == 'Offline' and new['status'] == 'Online' and new['state'] == 'Hospital':
        new, change = clear_travel_variables(new, change)

      
    #Getting out of hosp soon and offline
    elif "In hospital for 2 mins" in new['description'] and new['status'] == 'Offline':
        bazaar = bazaar_check(new, mongo)
        if 'depart_cash' in old.keys():
            new['landing_cash'] = old['depart_cash'] - bazaar['bazaar_value']
        else:
            new['landing_cash'] = 0
        if bazaar is False:
            txt_log.console("bot_actions.bazaar_check returned False in compare_states", "error")
            return False
        txt_log.console(old['name'] + " is now " + new['status'].lower() + " with $" + str("{:,}".format(bazaar['buy_mug_value'])) + " worth of goods for sale.", "mugs")
      
        if bazaar['potential_mug_value'] > glob.al['min_mug_amount'] or new['landing_cash'] > glob.al['min_mug_amount']:
            message_builder.build_mug_alert(new, ["buymug"], mongo, bazaar)
        change = True
        pass

      
    #Okay and in torn
    if new['state'] != "Traveling" and new['state'] != "Abroad" and new['status'] != 'Offline':
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