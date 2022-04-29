import json
import discord

import bot_actions
import torn_api
import txt_log
import glob
import emojis

#Builds the discord embed to use
#type = [buymug, mug, flight, cheap_item]
def build_mug_alert(mark, type, mongo, client, bazaar_obj={'buy_mug_value':0, 'potential_mug_value':0}):
    txt_log.console("  message_builder.build_mug_alert", "debug")
    profile_obj = torn_api.get_profile(mark['_id'], mongo)
    stats_obj = torn_api.get_stats(mark['_id'], mongo)['personalstats']
    #print(mark)
    #print("profile_obj")
    #print(profile_obj)
    #print("stats_obj")
    #print(stats_obj)
    #print("bazaar_obj")
    #print(bazaar_obj)
    #Assigning shit
    
    footer_text = "Age: " + str(profile_obj['age'])
    if stats_obj['xantaken'] > stats_obj['lsdtaken']:
        footer_text += " Xan: " + str(stats_obj['xantaken'])
    else:
        footer_text += " LSD: " + str(stats_obj['lsdtaken'])
    footer_text += " Ref: " + str(stats_obj['refills'])
    footer_text += " Can: " + str(stats_obj['energydrinkused'])
    footer_text += " SE: " + str(stats_obj['statenhancersused'])
    emoji_string = ""
    if str(mark['_id']) == "2040172":
        emoji_string += emojis.jigsarnak
    if "Argentina" in profile_obj['status']['description']:
        emoji_string += emojis.argentina
    if "Canada" in profile_obj['status']['description']:
        emoji_string += emojis.canada
    if "Caymen" in profile_obj['status']['description']:
        emoji_string += emojis.caymen
    if "China" in profile_obj['status']['description']:
        emoji_string += emojis.china
    if "Hawaii" in profile_obj['status']['description']:
        emoji_string += emojis.hawaii
    if "Japan" in profile_obj['status']['description']:
        emoji_string += emojis.japan
    if "Mexico" in profile_obj['status']['description']:
        emoji_string += emojis.mexico
    if "South Africa" in profile_obj['status']['description']:
        emoji_string += emojis.southafrica
    if "Switzerland" in profile_obj['status']['description']:
        emoji_string += emojis.switzerland
    if "UAE" in profile_obj['status']['description']:
        emoji_string += emojis.uae
    if "United Kingdom" in profile_obj['status']['description']:
        emoji_string += emojis.unitedkingdom
    if "Okay" in profile_obj['status']['description']:
        emoji_string += emojis.torn
    if profile_obj['job']['company_type'] == 5:
        emoji_string += emojis.clothingstore

    emb_title = str(profile_obj['name']) + " [" + str(mark['_id']) + "] "  + "\n" + emoji_string    
      
    if "buymug" in type:
        channels = glob.al['ch_mugs']
        emb_name = "Buy Mug Opportunity"
        emb_url = "https://www.torn.com/profiles.php?XID=" + str(mark['_id']) + "#/"
        emb_desc = "    Status: " + mark['status'] + "/" + mark['description']
    elif "flight" in type:
        channels = glob.al['ch_travel']
        emb_name = "Flight Landing Soon"
        emb_url = "https://www.torn.com/profiles.php?XID=" + str(mark['_id']) + "#/"
        emb_desc = "Estimated Landing Time: <t:" + str(mark['landing_time'])[:10] + ":R>"
    elif "cheap_item" in type:
        channels = glob.al['ch_bazaar']
        emb_name = "Underpriced Item "
        emb_url = "https://www.torn.com/bazaar.php?userId=" + str(mark['_id']) + "#/"
        emb_desc = "Item Name/Price/Market will go here"
    #The actual embed
    embed=discord.Embed(\
        title=emb_title, \
        url=emb_url, \
        description=emb_desc, \
        color=0xFF5733)
    embed.set_author(name=emb_name)
    if "landing_cash" in mark.keys():
        embed.add_field(name="Cash On Hand", value=("$" + str("{:,}".format(mark['landing_cash']))), inline=True)
    if "buy_mug_value" in bazaar_obj.keys():
        embed.add_field(name="Buy Mug Value", value=("$" + str("{:,}".format(bazaar_obj['buy_mug_value']))), inline=True)
    if "potential_mug_value" in bazaar_obj.keys():
        embed.add_field(name="Minimum profit (max merits)", value=("$" + str("{:,}".format(int(bazaar_obj['potential_mug_value'])))), inline=True)
    embed.set_footer(text=footer_text)
    txt_log.console("Adding embed to que", "messages")
    
    glob.pending_messages.append([embed, channels])
    
    #Show items to buymug or cash on hand
  
    #await bot_actions.message_channel("Testing", channel_list["admin_notifications"], client)