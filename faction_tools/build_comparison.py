
#Takes a list of factions and builds a csv comparing them
#Can probably be considered an external utility
def build_comparison(faction_list, mongo):
    if glob.al['debug'] is True:
        print("bot_actions.build_comparison")
    message_channel("Testing", [960573477977460767], client)
    for faction in faction_list:
        #print(faction)
        faction_obj = torn_api.get_members(faction, mongo)
        members = faction_obj['members']
        if glob.al['extras'] is True:
            print(members)
        for member_id in members:
            member_obj = torn_api.get_stats(member_id, mongo)['personalstats']   
            csv_line = ""
            csv_line += str(faction_obj['name']) + ", "
            csv_line += str(member_id) + ", "
            csv_line += str(members[member_id]['name']) + ", "
            csv_line += str(members[member_id]['level']) + ", "
            csv_line += str(member_obj['attackswon']) + ", "
            csv_line += str(member_obj['attackslost']) + ", "
            csv_line += str(member_obj['attacksdraw']) + ", "
            csv_line += str(member_obj['energydrinkused']) + ", "
            csv_line += str(member_obj['lsdtaken']) + ", "
            csv_line += str(member_obj['xantaken']) + ", "
            csv_line += str(member_obj['statenhancersused']) + ", "
            csv_line += str(member_obj['elo']) + "\n"
            file_object = open('csv_export.csv', 'a')
            file_object.write(csv_line)
            file_object.close()