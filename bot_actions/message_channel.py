#---Sends message to a group of channel id's (channel_list.json stores these and they are passed as a dictionary)
#---Currently disabled and prints to console instead  

import txt_log

async def message_channel(message_text, channels, client):
    txt_log.console("bot_actions.message_channel", "debug")
    for channel_id in channels:
        #try:
        if True:
            #Not needed
            #guild = client.get_guild(channel_id)
            channel = client.get_channel(int(channel_id))
            await channel.send(message_text)
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