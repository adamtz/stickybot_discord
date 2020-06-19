# -*- coding: utf-8 -*-
import requests_async as requests
import random
import os
import json
from gg_mfl import *

mflLeagues = ["55825", "31432", "24928", "16087", "60278", "47632", "26902", "58445", "64988", "58512", "48312", "20917", "11444"]

async def mfl(leagueId):
	print (leagueId)
	if leagueId == "1":
		return 'MFL Stuff::\n!otc:See who is OTC\n!draft:Get draft info\n!bylaws:Get Link for Bylaws\n!lineup:Get Lineup Info'
	elif leagueId == "55825":
		return 'MFL Stuff::\n!dlBucks:Get Current DL Bucks\n!bylaws:Get Link for Bylaws\n!lineup:Get Lineup Info\n!scoring:Get Current Scoring\n!standings:Get Current Standings\n!picks:Get Current Picks\n!Survivor:Get Current Survivor'
	else:
		return 'MFL Stuff::\n!otc:See who is OTC\n!draft:Get draft info\n!bylaws:Get Link for Bylaws\n!lineup:Get Lineup Info\n!scoring:Get Current Scoring\n!standings:Get Current Standings\n!picks:Get Current Picks'

async def getOTC(leagueId):
	try:
		otc_info = await getOTCInfo_MFL(leagueId)
		return otc_info
		#match up franchise to discord name
	except Exception as e:
		print ("Error in getting OTC: " + str(e))
		return False
		
async def draft(leagueId):
	to_send = await getDraftInfo_MFL(leagueId)
	return(to_send)

async def bylaws(leagueId):
	if leagueId == "31432":
		to_send = "On the MFL Site"
	elif leagueId == "55825":
		to_send = "https://docs.google.com/document/d/14hFpzUFHm7VFeNXEQ4NydbYqAoSML2gR-PpYHdo-Qh0/view"
	elif leagueId == "1":
		to_send = 'https://docs.google.com/document/d/1kH6CBfGpBkCsiWCzGh5D-iri7cXKwzGIapIXdaMUyNw/edit?usp=sharing'
	else:
		to_send = 'Not Found so check MFL'
	return(to_send)

async def lineups(leagueId):
	if leagueId == "1":
		to_send = '1QB, 2RB, 3WR, 1TE, 1SFLEX, 1FLEX, 2IDL, 3EDGE, 3LB, 3CB, 2S, 1DFLEX'
	elif leagueId in mflLeagues:
		to_send = await getLineupInfo_MFL(leagueId)
	else:
		to_send	= 'lineup info not found'
	return(to_send + ". See !zbylaws For More Info")

async def scoring(leagueId):
	if leagueId in mflLeagues:
		to_send = await getLiveScoring_MFL(leagueId)
	elif leagueId == "1":
		to_send = await do4YP_Scoring()
	else:
		to_send	= 'scoring info not found'
	return(to_send)

async def standings(leagueId):
	if leagueId in mflLeagues:
		to_send = await getStandings_MFL(leagueId)
	elif leagueId == "1":
		to_send = await do4YP_Standings()
	else:
		to_send	= 'standings info not found'
	return(to_send)

async def dlBucks(leagueId):
	to_send = await getDLBucks_MFL(leagueId)
	return(to_send)

async def picks(leagueId):
	if leagueId in mflLeagues:
		to_send = await getPicks_MFL(leagueId)
	else:
		to_send	= 'Picks not found'
	return(to_send)

async def days():
	to_send = await getDays()
	return(to_send)

async def survivor(leagueId):
	if leagueId == "55825":
		to_send = await getSurvivor_MFL(leagueId)
	else:
		to_send	= 'No Survivor'
	return(to_send)

async def bball(leagueId):
	if leagueId == "31432":
		to_send = await doBBall()
	else:
		to_send = "Not in use"
	return(to_send)

async def fourYP():
	to_send = await do4YP()
	return(to_send)

async def dl3_run(leagueId):
	if leagueId == "55825":
		to_send = await doDL3_run()
	else:
		to_send = "Not in use"
	return(to_send)

async def dl3_dice(leagueId):
	if leagueId == "55825":
		to_send = await doDL3_dice()
	else:
		to_send = "Not in use"
	return(to_send)

