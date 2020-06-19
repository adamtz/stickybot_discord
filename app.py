import requests
import time
import os
import json
import datetime
from flask import Flask, request
from gg_commands import *

app = Flask(__name__)

@app.route('/', methods=['POST'])
def webhook():
	data = request.get_json()
	#we don't want to reply to ourselves!
	if data['name'] != os.getenv('BOT_NAME') and "!" in data['text'][0]:
		parseMessage(data)
	return "ok", 200

def parseMessage(message):
	#check if someone is abusing the bot, if they have an entry in the cache then they hit too many times
	status = cache.get(message['name'])
	if status == "used" and message['user_id'] != "27293802":
		print ("banning: " + message['name'])
		#delete from cache first so we can update the timeout via set
		cache.delete(message['name'])
		cache.set(message['name'], "banned", timeout = 30)
		sendText_mention("@" + message['name']+ " ,you are using the bot too much, no bot for you for 30 seconds", message['user_id'], message['name'])
	elif status == "banned":
		print ("ignoring commands from: " + message['name'])
		return None
	else:
		#add all users to this cache so they cant overwhelm the bot
		cache.delete(message['name'])
		cache.set(message['name'], "used", timeout = 6)
		#run the commands
		runCommands(message)

def runCommands(message):
	elif (message['text'] == '!dobucks' or message['text'] == '!DL3'):
		if message['user_id'] == "6739678":
			to_send = "Running Bucks Update"
			sendText(to_send)
			dl3_run()
	elif (message['text'] == '!dothething' or message['text'] == '!bestball'):
		if message['user_id'] == "6739678" or message['user_id'] == "27293802":
			bball()
		else:
			to_send = "No BestBall for you!"
			sendText(to_send)
			to_send = "https://thumbs.gfycat.com/UnknownAdorableBuzzard-size_restricted.gif"
			sendText(to_send)
	elif (message['text'] == '!survivor'):
		today = date.today().weekday()
		print (today)
		if today != 1 and today != 2:
			survivor()
		else:
			to_send = "Check back later in the week"
			sendText(to_send)