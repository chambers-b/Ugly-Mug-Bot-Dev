#buy mug mark:{'_id': '2034640', 'name': 'lightnemesis', 'last_update': 1651854592.0, 'faction': 27223, 'status': 'Offline', 'description': 'Okay', 'state': 'Okay'} 
#travel mark:{'_id': '2731392', 'name': 'Andeafdod', 'last_update': 1651856448.0, 'faction': 25025, 'status': 'Online', 'description': 'Returning to Torn from Switzerland', 'state': 'Traveling', 'landing_time': 1651863915.0, 'depart_cash': 3100750, 'landing_cash': 2465000}
import txt_log
import glob

async def send_embed(embed, channel_type, mark, client):
    txt_log.console("bot_actions.embed_channel", "debug")
    channel_responses = []
    for channel_id in glob.al[channel_type]:
        #try:
        if True:
            #Not needed
            #guild = client.get_guild(652594486119235622)
            channel = client.get_channel(channel_id)
            txt_log.console("~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~", 'messages')
            txt_log.console(str(channel) + ": Launching Embed", 'messages')
            
            txt_log.console("~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~", 'messages')
            #TEST
            message_response = await channel.send(embed=embed)
            channel_responses.append(message_response.id)
            return channel_responses
        else:
        #except:
            txt_log.log("Failed to send in " + str(channel_id))
            print("Failed to send in " + str(channel_id))
            return False