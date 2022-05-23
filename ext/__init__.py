# from ext import *  #Import external package set
#Import External pre-built packages
import discord
from discord.ext import tasks
import pymongo
import requests
import os
import sys
import json
import asyncio
import datetime
import time
#from datetime import datetime
import threading
import dns


##### DO NOT INSTALL "BSON" ######
#  It overwrites the pymongo BSON function and 
#  will break any usage of mongo by mangling the '_id'
#
# To fix, uninstall BSON from left package manager
# Delete poetry and tomal lock files
# pip uninstall pymongo
# pip3 install pymongo


#Examples:
# relative import 
# from . import africa
# absolute import
# from ext import africa <--- Use this kind of import