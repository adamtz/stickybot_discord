import requests_async as requests
import json
import os
from datetime import datetime, timedelta, date
from werkzeug.contrib.cache import SimpleCache

cache = SimpleCache()

async def franchiseMatch(franchiseId, leagueId):
	try:
		#attempt to get the list of franchise names from the cache, its not cached go and get it from MFL
		franchise_list = cache.get("franchises_" + str(leagueId))
		if franchise_list is None:
			franchise_list = await getFranchiseInfo_MFL(leagueId)
			cache.set("franchises_" + str(leagueId), franchise_list, 32000)
		for franchise in franchise_list:
			if (str(franchise["id"]) == str(franchiseId)):
				return franchise["name"]
	except Exception as e:
		print ("Error in doing franchise match: " + str(e))

async def getFranchiseInfo_MFL(leagueId):
	mflJar = await loginHELPER("stickyz", "redsreds1")
	try:
		url = "https://api.myfantasyleague.com/2020/export?TYPE=league&L="+ leagueId +"&JSON=1"
		#UPDATE TO CORRECT WEEK AND URL FOR LEAGUE
		response = await requests.get(url,cookies=mflJar)
		if response.status_code == 200:
			data= json.loads(response.text)
			results = data["league"]["franchises"]["franchise"]
			franchise_list = []
			for franchise in results:
				franchise_info = {"id" : franchise["id"], "name" : franchise["name"]}
				franchise_list.append(franchise_info)
			return franchise_list
		else:
			print ("request to mfl failed")
			return None
	except Exception as e:
		print ("Error in getting getting franchise info from mfl: " + str(e))

async def getLineupInfo_MFL(leagueId):
	mflJar = await loginHELPER("stickyz", "redsreds1")
	try:
		url = "https://api.myfantasyleague.com/2020/export?TYPE=league&L=" + leagueId + "&JSON=1"
		response = await requests.get(url,cookies=mflJar)
		if response.status_code == 200:
			data= json.loads(response.text)
			results = results = data["league"]["starters"]
			count = results["count"]
			idp_count = results["idp_starters"]
			starters_list  = results["position"]
			if idp_count is None or idp_count == "" or not idp_count:
				lineup_info = "Total Starters: " + count
			else:
				lineup_info = "Total Starters: " + count + ", IDP Total: " + idp_count
			for position in starters_list:
				lineup_info = lineup_info + ", " + position["limit"] + position["name"]
			return lineup_info
		else:
			print ("request to mfl failed")
	except Exception as e:
		print ("Error in getting getting lineup info: " + str(e))

async def getLiveScoring_MFL(leagueId):
	mflJar = await loginHELPER("stickyz", "redsreds1")
	week = await weekHelper()
	try:
		url = "https://api.myfantasyleague.com/2020/export?TYPE=liveScoring&L=" + leagueId + "&APIKEY=&W="+ week + "&DETAILS=&JSON=1"		#UPDATE TO CORRECT WEEK AND URL FOR LEAGUE
		response = await requests.get(url,cookies=mflJar)
		if response.status_code == 200:
			data= json.loads(response.text)
			if "matchup" in data["liveScoring"].keys():
				franchise_list = await getFranchiseInfo_MFL(leagueId)
				matchups = data["liveScoring"]["matchup"]
				lineup_info = ""
				for matchup in matchups:
					franchises = matchup["franchise"]
					score1 = float(franchises[0]["score"])
					team1 = list(filter(lambda team: team['id'] == franchises[0]["id"], franchise_list))[0]["name"]
					score2 = float(franchises[1]["score"])
					team2 = list(filter(lambda team: team['id'] == franchises[1]["id"], franchise_list))[0]["name"]
					lineup_info= "{}{} vs {} : {} to {}\n".format(lineup_info, team1, team2, score1, score2)
			else:
				lineup_info = "No matchups"
			return lineup_info
		else:
			print ("request to mfl failed")
	except Exception as e:
		print ("Error in getting getting live scoring info: " + str(e))
		return ("Error getting scoring or there is none yet")

async def getStandings_MFL(leagueId):
	mflJar = await loginHELPER("stickyz", "redsreds1")
	week = await weekHelper()
	try:
		url = "https://api.myfantasyleague.com/2020/export?TYPE=leagueStandings&L=" + leagueId + "&APIKEY=&W="+ week + "&DETAILS=&JSON=1"		#UPDATE TO CORRECT WEEK AND URL FOR LEAGUE
		response = await requests.get(url,cookies=mflJar)
		if response.status_code == 200:
			data= json.loads(response.text)
			standings_list = data["leagueStandings"]["franchise"]
			standings_info = "League Standings:\n"
			franchise_list = await getFranchiseInfo_MFL(leagueId)
			for franchise in standings_list:
				teamName = list(filter(lambda team: team['id'] == franchise["id"], franchise_list))[0]["name"]
				wins = franchise["h2hw"]
				losses = franchise["h2hl"]
				pf = franchise["pf"]
				if "pf" in franchise.keys():
					power = franchise["pwr"]
					standings_info = "{}{}: {}-{} PF:{} PWR:{}\n".format(standings_info, teamName, wins, losses, pf, power)
				else:
					standings_info = "{}{}: {}-{} PF:{}\n".format(standings_info, teamName, wins, losses, pf)
			return standings_info
		else:
			print ("request to mfl failed")
	except Exception as e:
		print ("Error in getting getting standings info: " + str(e))
		return ("Error getting standings or there are none yet")

async def getPicks_MFL(leagueId):
	mflJar =  awaitloginHELPER("stickyz", "redsreds1")
	try:
		url = "https://api.myfantasyleague.com/2020/export?TYPE=futureDraftPicks&L=" + leagueId + "&APIKEY=&JSON=1"
		response = await requests.get(url,cookies=mflJar)
		if response.status_code == 200:
			data= json.loads(response.text)
			picks_list = data["futureDraftPicks"]["franchise"]
			picks_info = "League Picks:\n"
			franchise_list = await getFranchiseInfo_MFL(leagueId)
			for franchise in picks_list:
				teamName = list(filter(lambda team: team['id'] == franchise["id"], franchise_list))[0]["name"]
				future_picks_list = franchise["futureDraftPick"]
				future_pick_info = ""
				#handle 1 pick or no picks
				if type(future_picks_list) == list:
					for future_pick in future_picks_list:
						future_pick_info = "{}Rd{},".format(future_pick_info,future_pick["round"])
					future_pick_info = future_pick_info[:-1]
				elif type(future_picks_list) == dict:
						future_pick_info = "{}Rd{},".format(future_pick_info,future_picks_list["round"])
						future_pick_info = future_pick_info[:-1]
				else:
					#no picks
					future_pick_info = "{}:Do Not Pass Go".format(future_pick_info,"0")
				
				picks_info = "{}{}: {}\n".format(picks_info,teamName, future_pick_info)
			return picks_info
		else:
			print ("request to mfl failed")
	except Exception as e:
		print ("Error in getting getting picks info: " + str(e))

async def getDays():
	url = "https://stickypi.herokuapp.com/days"
	try:
		response = await requests.get(url)
		print (response.text)
		return response.text
	except:
		return "Error Getting Days"

async def getSurvivor_MFL(leagueId):
	mflJar = await loginHELPER("stickyz", "redsreds1")
	#week has to be an int here for getting the right week on the array of weeks from mfl
	week = int( await weekHelper())
	print ("week is: " + str(week))
	try:
		url = "https://api.myfantasyleague.com/2020/export?TYPE=survivorPool&L=" + leagueId + "&APIKEY=&JSON=1"
		response = await requests.get(url,cookies=mflJar)
		if response.status_code == 200:
			franchise_list = await getFranchiseInfo_MFL(leagueId)
			data= json.loads(response.text)
			survivor_list = data["survivorPool"]["franchise"]
			survivor_info = ""
			for franchise in survivor_list:
				teamName = list(filter(lambda team: team['id'] == franchise["id"], franchise_list))[0]["name"]
				franchise_info = franchise["week"]
				this_week = franchise_info[week-1]
				if "pick" in this_week.keys() and this_week["pick"] != "" :
					pick = this_week["pick"]
				else:
					pick = "Dead"
				survivor_info = "{}{}: {}\n".format(survivor_info,teamName, pick)
			return survivor_info
		else:
			print ("request to mfl failed")
	except Exception as e:
		print ("Error in getting survivor info: " + str(e))
		return ("No Survivor")

async def getOTCInfo_MFL(leagueId):
	mflJar = await loginHELPER("stickyz", "redsreds1")
	try:
		url = "https://api.myfantasyleague.com/2020/export?TYPE=draftResults&L=" + leagueId + "&JSON=1"
		#UPDATE TO CORRECT WEEK AND URL FOR LEAGUE
		response = await requests.get(url,cookies=mflJar)
		if response.status_code == 200:
			data = json.loads(response.text)
			#get otc info first
			results = data["draftResults"]["draftUnit"]["draftPick"]
			draft_info = next((item for item in results if item["player"] == ""), False)
			print (draft_info)
			if draft_info:
				otc_team = await franchiseMatch(draft_info["franchise"], leagueId)
				return otc_team
			else:
				return "Sorry Bub, Draft Over"
			print ("request to otc mfl failed")
			return None
	except Exception as e:
		print ("Error in getting OTC: " + str(e))
		return ("OTC Not Found For This League")

async def getDraftInfo_MFL(leagueId):
	mflJar = await loginHELPER("stickyz", "redsreds1")
	try:
		url = "https://api.myfantasyleague.com/2020/export?TYPE=draftResults&L=" + leagueId + "&JSON=1"
		#UPDATE TO CORRECT WEEK AND URL FOR LEAGUE
		response = await requests.get(url,cookies=mflJar)
		if response.status_code == 200:
			data = json.loads(response.text)
			#get otc info first
			results = data["draftResults"]["draftUnit"]["draftPick"]
			draft_info = next((item for item in results if item["player"] == ""), False)
			print (draft_info)
			if draft_info:
				otc_team = await franchiseMatch(draft_info["franchise"], leagueId)
				#get current pick and round
				draft_info_str = "Draft is in Round: " + draft_info["round"] + ", Pick: " + draft_info["pick"] + ". Waiting for: " + otc_team
				return draft_info_str
			else:
				return "Sorry Bub, Draft Over"
		else:
			print ("request to draft mfl failed")
			return ("Draft Not Started or This code is broken")
	except Exception as e:
		print ("Error in getting draft info: " + str(e))
		return ("Draft Not Found For This League")

async def getDLBucks_MFL(leagueId):
	mflJar = await loginHELPER("stickyz", "redsreds1")
	try:
		url = "https://api.myfantasyleague.com/2020/export?TYPE=league&L=" + leagueId + "&JSON=1"
		response = await requests.get(url,cookies=mflJar)
		if response.status_code == 200:
			data= json.loads(response.text)
			#loop through teams to get current bb and franchise info
			franchises = data["league"]["franchises"]["franchise"]
			DLBucks_info = ""
			for franchise in franchises:
				DLBucks_info = "{}{} : {}\n".format(DLBucks_info, franchise["name"],franchise["bbidAvailableBalance"])
			return DLBucks_info
		else:
			print ("request to mfl failed")
	except Exception as e:
		print ("Error in getting BB: " + str(e))

async def loginHELPER(username, password):
	response = await requests.get("https://api.myfantasyleague.com/2020/login?USERNAME=" + username + "&PASSWORD=" + password + "&XML=1")
	#data= json.loads(response.text)
	jar = response.cookies
	mfl_id = jar.get("MFL_USER_ID")
	return jar

async def doBBall():
	week = await weekHelper()
	print ("doing the thing for week: " + week)
	url = "https://stickypi.herokuapp.com/run/" + week + "/"
	try:
		response = await requests.get(url, timeout=3)
	except:
		return "Doing the thing, might take us a second"

async def do4YP():
	url = "https://stickypi.herokuapp.com/4yp/vp/"
	try:
		response = await requests.get(url)
		print (response.text)
		return response.text
	except:
		return "Error Getting VP Standings"

async def do4YP_Standings():
	url = "https://stickypi.herokuapp.com/4yp/standings/"
	try:
		response = await requests.get(url)
		print (response.text)
		return response.text
	except:
		return "Error Getting Standings"

async def do4YP_Scoring():
	url = "https://stickypi.herokuapp.com/4yp/scoring/"
	try:
		response = await requests.get(url)
		print (response.text)
		return response.text
	except:
		return "Error Getting Scoring"

async def doDL3_run():
	url = "https://stickypi.herokuapp.com/dl3/run/"
	try:
		response = await requests.get(url)
		print (response.text)
		return response.text
	except:
		return "Error Running Monopoly Update"

async def doDL3_dice():
	url = "https://stickypi.herokuapp.com/dl3/dice/"
	try:
		response = await requests.get(url)
		print (response.text)
		return response.text
	except:
		return "Error Getting Standings"

async def weekHelper():
	d1 = date(2019, 9, 3)
	d2 = date.today()
	wk1tue = (d1 - timedelta(days=d1.weekday()))
	thiswktue = d2 - timedelta(days=(d2.weekday())+1)
	week = ((thiswktue - wk1tue).days / 7)
	today = date.today().weekday()
	#if today is sunday/monday/tuesday/wednesday keep on previous week stuff else do the current week
	if today <= 2:
		week = week + 1
	else:
		week = week + 2
	return str(int(float(week)))
