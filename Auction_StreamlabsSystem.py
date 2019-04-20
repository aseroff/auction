import os
import sys
import json
import codecs
import time
import threading
from threading import Timer,Thread,Event

ScriptName = "Auction"
Website = "https://github.com/aseroff/auction/"
Description = "Hold auctions with bidding in your Streamlabs currency"
Creator = "rvaen17"
Version = "1.0.0"

configFile = "config.json"
settings = {}
currency_name = ""
auction = ""
bid = 0
user = 0
username = ""
time_elapsed = -1

def ScriptToggled(state):
	return

def Init():
	global configFile, settings, currency_name
	
	currency_name = Parent.GetCurrencyName()

	path = os.path.dirname(__file__)
	try:
		with codecs.open(os.path.join(path, configFile), encoding='utf-8-sig', mode='r') as file:
			settings = json.load(file, encoding='utf-8-sig')
	except:
		settings = {
			"liveOnly": False,
			"secondsToWin": 30,
			"minIncrement": 1,
			"openingBid": 0,
			"firstWarning": 10,
			"secondWarning": 5,
			"openingMessage": "/me Bidding for $auction has opened at $bid $currency. You can bid on this auction by using !bid and then the amount you want to bid. Bids must be $increment higher than the previous bid.",
			"auctionInProgressMessage": "There is an auction for $auction already in progress!",
			"newBidMessage": "/me @$user has the high bid at $bid $currency. Do I hear $min?",
			"insufficientFundsMessage": "Sorry @$user, you can't afford that bid. NotLikeThis",
			"invalidBidMessage": "Invalid bid! Minimum bid is $min $currency.",
			"firstWarningMessage": "/me Going once to @$user for $bid $currency!",
			"secondWarningMessage": "/me Going twice to @$user for $bid $currency!",
			"winningMessage": "/me $auction has sold to @$user for $bid $currency!",
			"noBidsMessage": "/me The auction for $auction has ended with no bids!"
		}

def Execute(data):
	global time_elapsed, user, username, bid, auction
	if ((settings["liveOnly"] and Parent.IsLive()) or (not settings["liveOnly"])) and data.IsChatMessage():
		if (data.Message.strip().split(" ")[0] == "!auction" and Parent.HasPermission(data.User,"mod",data.UserName)):
			if (time_elapsed == -1):
				auction = data.Message.strip().replace("!auction ", "")
                                time_elapsed = 0
                                Parent.SendStreamMessage(settings["openingMessage"].replace("$auction", auction).replace("$currency", currency_name).replace("$bid", str(settings["openingBid"])).replace("$increment", str(settings["minIncrement"])))
                                timer = threading.Timer(1.0, timing)
                                if not timer.is_alive():
                                        timer.start()
			else:
				Parent.SendStreamMessage((settings["auctionInProgressMessage"].replace("$auction", auction)))
		elif (data.Message.strip().split(" ")[0] == "!bid" and data.Message.strip().split(" ")[1].isdigit() and time_elapsed != -1):
			newbid = int(data.Message.strip().split(" ")[1])
                        min = bid + int(settings["minIncrement"])
			if ((newbid == bid and username == "") or (newbid >= min)):
				if ((Parent.GetPoints(data.UserName)) >= newbid):
					user = data.User
					username = data.UserName
					bid = int(newbid)
					time_elapsed = 0
					Parent.SendStreamMessage(settings["newBidMessage"].replace("$currency", currency_name).replace("$user", username).replace("$bid", str(bid)).replace("$min", str(bid + int(settings["minIncrement"]))))
				else:
					Parent.SendStreamMessage(settings["insufficientFundsMessage"].replace("$user", data.UserName))
			else:
				Parent.SendStreamMessage(settings["invalidBidMessage"].replace("$currency", currency_name).replace("$min", str(min)))
	return

def timing():
        global time_elapsed, user, username, bid, auction
        while ((time_elapsed != -1) and (time_elapsed < int(settings["secondsToWin"]))):
                time_elapsed += 1
		if (time_elapsed == (int(settings["secondsToWin"]) - int(settings["firstWarning"])) and int(bid) != settings["openingBid"]):
			Parent.SendStreamMessage(settings["firstWarningMessage"].replace("$user", username).replace("$bid", str(bid)).replace("$currency", currency_name))
		elif (time_elapsed == (int(settings["secondsToWin"]) - int(settings["secondWarning"])) and int(bid) != settings["openingBid"]):
			Parent.SendStreamMessage(settings["secondWarningMessage"].replace("$user", username).replace("$bid", str(bid)).replace("$currency", currency_name))
		elif (time_elapsed == int(settings["secondsToWin"])):
			if (username != ""):
				Parent.SendStreamMessage(settings["winningMessage"].replace("$user", username).replace("$auction", auction).replace("$bid", str(bid)).replace("$currency", currency_name))
				Parent.RemovePoints(user,username,bid)
			else: 
				Parent.SendStreamMessage(settings["noBidsMessage"].replace("$auction", auction))
			time_elapsed = -1
			user = 0
			username = ""
			bid = 0
                time.sleep(1)

def ReloadSettings(jsonData):
        Init()
	return

def OpenReadMe():
	location = os.path.join(os.path.dirname(__file__), "README.txt")
	os.startfile(location)
	return

def Tick():
	return
