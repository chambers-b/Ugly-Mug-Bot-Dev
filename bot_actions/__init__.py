#This imports all of the sub-files when import bot_actions is called.
#When one file uses another within the folder the below must be used to call the right file.
from bot_actions.bazaar_check import bazaar_check
from bot_actions.clear_travel_variables import clear_travel_variables
from bot_actions.compare_states import compare_states
from bot_actions.send_embed import send_embed #Sends embed to channel
from bot_actions.get_marks import get_marks
from bot_actions.message_channel import message_channel
from bot_actions.rm_message import rm_message
from bot_actions.message_user import message_user


# __all__ = [
#         'bazaar_check',
#         'clear_travel_variables',
#         'compare_states',
#         'embed_channel',
#         'get_marks',
#         'message_channel',
#         'rm_message',
#         'send'
#         ]

#Examples:
# relative import 
# from . import africa
# absolute import
# from ext import africa <--- Use this kind of import