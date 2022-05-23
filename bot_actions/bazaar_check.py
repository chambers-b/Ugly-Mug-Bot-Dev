from ext import *  #Import external package set

import txt_log
import torn_api
import glob
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
            if pct_change < -0.05 and (item['market_price'] - item['price']) > 50000 and item['type'] not in glob.al['excluded_categories'] and item['name'] not in glob.al['excluded_items']:
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
