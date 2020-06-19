# bot.py
import os
import random
import discord

from discord.ext import commands, tasks
from dotenv import load_dotenv
from gg_commands_discord import *

#load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')

#cache these somewhere
the100 = { "StickyZ" : "StickyZ", "Tom" : "Tommy K", "Santi" : "ASantigate", "Dwight" : "Bigwhitedwight", "Devin" : "Devin", "Dylan" : "dtlerch", "Tyler" : "Tyler H", "Seth" : "wanderersonofwarrior", "Steve" : "stephengill5", "Bee " : "Bee", "Ryan O" : "theczarcasticone", "Drew & Luke" : "Drewski"}
bbobw = {"Sticky & Z" : "StickyZ", "Fish + Chips" : "Tommy K", "Steve" : "stephengill5", "Drew & Squirrels" : "Drewski", "Fucking Canadian" : "LukeG", "thēDRÎ₽ćhrøñićłēš" : "Mr. DRÎ₽", "Andy RML duder" : "andyRML", "Brett Loves IDP and Reese's" : "Madness", "Puka Dogs" : "Bee", "BBQ and Pickles" : "username02", "Vanilla Chocolate Swirl" : "ASantigate", "The Driz" : "thedrizzle"}
theflex = {"FlexyZ" : "StickyZ", "I sawed this boat in half and fixed it with Flextape" : "Tyler H", "Steve, but Flex" : "stephengill5", "Funkmaster Flex" : "Drewski", "Flexual Education" : "LukeG", "On Instagram Straight Flexin’" : "Mr. DRÎ₽", "Flex Capacitor" : "Clawless", "Name of Your Flex Tape" : "Madness", "Stop Trying To Make 'Flex' Happen" : "theczarcasticone", "Flexas with a Dollar Sign" : "mpkalina", "NetFlex and Chill" : "ASantigate", "Tyrannosaurus Flex" : "DrewDodson", "Flexual Healing, Feels Good To Me" : "wanderersonofwarrior", "Weird Flex but OK" : "dtlerch" }
cradle = {"Las Vegas Horned Frogs" : "LukeG", "Philly Rocketz" : "StickyZ", "Arizona Gila Monsters - @DrewK" : "Drewski", "Green Bay Badgers" : "Devin", "Denver Buffaloes" : "RedYeti", "Carolina Volunteers" : "Mr. DRÎ₽", "Houston Harvesters" : "Bumbleclot", "Los Angeles Fighting Irish" : "SaintTomorrow", "Nashville Wonderboys" : "billymo13", "Cleveland Golden Flashes" : "Phil S.", "New England Lake Monsters" : "wanderersonofwarrior", "New Orleans Fighting Okra" : "collin14", "Buffalo Seawolves" : "ASantigate", "Pittsburgh Buckeyes (@ShanePHallam)" : "ShanePHallam" }

bot = commands.Bot(command_prefix='!z')

@commands.cooldown(1, 30, commands.BucketType.user)
@bot.command(name='test', help='doestest')
async def test(ctx):
	print (type(ctx.message.channel))
	if ctx.message.channel.name != "general":
		print (ctx.author.roles)
		if 'Admin' == ctx.author.roles[len(ctx.author.roles)-1].name:
			response = "THIS IS A TEST, Admin, {name}, in {channel}".format(name = ctx.author.mention, channel = ctx.message.channel)
		else:
			response = "THIS IS A TEST, {name}, in {channel}".format(name = ctx.author.mention, channel = ctx.message.channel)
	else:
		response = "THIS IS A TEST, {name}, in henreal".format(name = ctx.author.mention, channel = ctx.message.channel)
	await ctx.send(response)


@bot.command(name='giverole', hidden=True)
async def giveRole(ctx, user, role):
	if 'Admins' == ctx.author.roles[len(ctx.author.roles)-1].name:
		user_upper = user.upper()
		print (role)
		list_of_members = ctx.guild.members #cache this at some point?
		found_member = next((x for x in list_of_members if x.name.upper() == user_upper), None)
		if found_member is not None:
				role_to_add = discord.utils.get(found_member.guild.roles, name=role)
				print (role_to_add)
				print (type(role_to_add))
				await found_member.add_roles(role_to_add, reason = "added by StickyBot", atomic = True)
				response = "Added {role} To {user}".format(role = role, user = user)
		else:
			response = "User not found"
		#response = "THIS IS A TEST, Admin, {name}, in {channel}".format(name = ctx.author.mention, channel = ctx.message.channel)
		await ctx.send(response)

@bot.command(name='mfl', help='MFL Bot Options')
async def mfl_discord(ctx):
	leagueId = parseChannel(ctx.message.channel.name)
	response = await mfl(leagueId)
	print (response)
	await ctx.send(response)

#@commands.cooldown(1, 30, commands.BucketType.user)
@bot.command(name='otc', help='Find who is OTC')
async def otc_discord(ctx):
	if 'Admins' == ctx.author.roles[len(ctx.author.roles)-1].name:
		channel = ctx.message.channel.name
		leagueId = parseChannel(channel)
		otc_team = await getOTC(leagueId)
		print (otc_team)
		response = await matchOTC(otc_team, channel)
		print (response)
	else:
		response = "Only Admins have this power for now, use !zdraft"
	await ctx.send(response)

async def matchOTC(otc_team, channel):
	try:
		if channel == '100':
			user = the100[otc_team]
			response = "{name} is OTC".format(name = discord.utils.get(bot.users, name=user).mention)
		elif channel == 'bbobw':
			user = bbobw[otc_team]
			response = "{name} is OTC".format(name = discord.utils.get(bot.users, name=user).mention)
		elif channel == 'the-flexining':
			user = theflex[otc_team]
			response = "{name} is OTC".format(name = discord.utils.get(bot.users, name=user).mention)
		elif channel == 'cradle-to-grave' or channel == 'bot-commands':
			user = cradle[otc_team]
			response = "{name} is OTC".format(name = discord.utils.get(bot.users, name=user).mention)
		else:
			response = "Discord match not found for team: {name}, but they are OTC".format(name=otc_team)
	except Exception as e:
		print (e)
		response = "Discord match not found for team: {name}, but they are OTC".format(name=otc_team)	
	return response

@tasks.loop(hours=1, count=5)
async def otc_loop(leagueId, channel):
	otc_team = await getOTC(leagueId)
	print (otc_team)
	response = await matchOTC(otc_team, channel)	
	print(response)
	channel = discord.utils.get(bot.get_all_channels(), name=channel)
	await channel.send(response)

@bot.command(name='loop_otc', hidden=True)
async def loop_otc(ctx, channel):
	if 'Admins' == ctx.author.roles[len(ctx.author.roles)-1].name:
		leagueId = parseChannel(channel)
		otc_loop.start(leagueId, channel)
		await ctx.send("running")
	
@bot.command(name='draft', help='Find Draft Info')
def draft_discord(ctx):
	leagueId = parseChannel(ctx.message.channel.name)
	response = draft(leagueId)
	print (response)
	ctx.send(response)

@bot.command(name='bylaws', help='Find Bylaw Info')
async def bylaws_discord(ctx):
	leagueId = parseChannel(ctx.message.channel.name)
	response = await bylaws(leagueId)
	print (response)
	await ctx.send(response)

@bot.command(name='4yp', help='Only Available in #4yp', aliases=['yp'], hidden=True)
async def fouryp_discord(ctx):
	if ctx.message.channel.name == "4yp":
		response = await fourYP()
		print (response)
	else:
		response = "Only Available in #4yp"
	await ctx.send(response)
	
@bot.command(name='lineups', help='Show league lineup settings', aliases=['lineup'])
async def lineups_discord(ctx):
	leagueId = parseChannel(ctx.message.channel.name)
	response = await lineups(leagueId)
	print (response)
	await ctx.send(response)

@bot.command(name='scoring', help='Show league live scoring', aliases=['live'])
async def scoring_discord(ctx):
	leagueId = parseChannel(ctx.message.channel.name)
	response = await scoring(leagueId)
	print (response)
	await ctx.send(response)
	
@bot.command(name='standings', help='Show league standings', aliases=['ranks'])
async def standings_discord(ctx):
	leagueId = parseChannel(ctx.message.channel.name)
	response = await standings(leagueId)
	print (response)
	await ctx.send(response)

@bot.command(name='bucks', help='Only Available in #monopoleague', aliases=['faab', 'DLBucks', 'dlBucks', 'dlbucks'], hidden=True)
async def bucks_discord(ctx):
	if ctx.message.channel.name == "monopoleague":
		leagueId = parseChannel(ctx.message.channel.name)
		response = await dlBucks(leagueId)
		print (response)
	else:
		response = "Only Available in #monopoleague"
	await ctx.send(response)

@bot.command(name='dice', help='Only Available in #monopoleague', aliases=['rolls', 'getrolls'], hidden=True)
async def dice_discord(ctx):
	if ctx.message.channel.name == "monopoleague":
		leagueId = parseChannel(ctx.message.channel.name)
		response = await dl3_dice(leagueId)
		print (response)
	else:
		response = "Only Available in #monopoleague"
	await ctx.send(response)

@bot.command(name='dobucks', help='Only Available in #monopoleague', aliases=['DL3', 'dl3'], hidden=True)
async def dobucks_discord(ctx):
	if ctx.message.channel.name == "monopoleague":
		leagueId = parseChannel(ctx.message.channel.name)
		response = "Running Bucks Update"
		print (response)
	else:
		response = "Only Available in #monopoleague"
	await ctx.send(response)
	await dl3_run()

#--------------------------------------------------------------------------
@bot.command(name='wakeup')
async def wakeup(ctx):
	to_send = "Bleeep Bloop.....I'm up! And now I never sleep"
	await ctx.send(to_send)

@bot.command(name='sticky')
async def sticky(ctx):
	to_send = "Sticky is the man, he is a god among men"
	await ctx.send(to_send)

@bot.command(name='keeperinfo', aliases=['keepershit', '4ypshit'], hidden=True)
async def keeperinfo(ctx):
	to_send = to_send = "Players dropped: Top 10 QBs, Top 20 RBs, Top 30 WRs, Top 10 TEs, Top 10 IDLs, Top 20 EDGE, Top 20 LBs, Top 10 CBs, Top 20 S"
	await ctx.send(to_send)

@bot.command(name='goodbot', hidden=True)
async def goodbot(ctx):
	to_send = 'Thank you {name}, you are a good water filled flesh bag...err I mean Human'.format(name = ctx.author.mention)
	await ctx.send(to_send)

@commands.cooldown(1, 10, commands.BucketType.user)
@bot.command(name='random')
async def random_discord(ctx):
	to_send = str(random.randint(1,100))
	await ctx.send(to_send)

@bot.command(name='woat')
async def woat(ctx):
	to_send = 'You are the worst, {name}'.format(name = ctx.author.mention)
	await ctx.send(to_send)

@bot.command(name='days', help='Show days till stuff', aliases=['day'])
async def days_discord(ctx):
	response = await days()
	print (response)
	await ctx.send(response)		

@bot.command(name='goose')
async def goose(ctx):
	to_send = "The Goose is loose"
	await ctx.send(to_send)

@bot.command(name='brent', hidden=True)
async def brent(ctx):
	to_send = ":brett2:"
	await ctx.send(to_send)

@bot.command(name='badbot', hidden=True)
async def badbot(ctx):
	to_send = "I remember"
	await ctx.send(to_send)

@bot.command(name='santi', hidden=True)
async def santi(ctx):
	to_send = "Staten Island Proud"
	await ctx.send(to_send)

@bot.command(name='luke', hidden=True)
async def luke(ctx):
	to_send = "From Canada, With Love."
	await ctx.send(to_send)

@bot.command(name='steve', hidden=True)
async def steve(ctx):
	to_send = "From Canada, With Love."
	await ctx.send(to_send)

@bot.command(name='drew', hidden=True)
async def drew(ctx):
	to_send = "Go Broncos!"
	await ctx.send(to_send)

@commands.cooldown(1, 30, commands.BucketType.user)
@bot.command(name='dylan')
async def dylan(ctx):
	to_send = "Dylan has set a lineup"
	await ctx.send(to_send)

@bot.command(name='knotts', hidden=True)
async def knotts(ctx):
	to_send = "I may be 99% code but I know that Knotts is the real worst"
	await ctx.send(to_send)
	
@bot.command(name='wife', hidden=True)
async def wife(ctx):
	to_send = "No Pants, No Problem"
	await ctx.send(to_send)
	
@bot.command(name='donotpassgo', hidden=True)
async def donotpassgo(ctx):
	to_send = "DO NOT PASS GO, DO NOT COLLECT 200 DOLLARS: https://www.youtube.com/watch?v=Cj1wcs7SZj0"
	await ctx.send(to_send)

@commands.cooldown(1, 30, commands.BucketType.user)
@bot.command(name='rip')
async def rip(ctx):
	to_send = "Rest In Pepperoni"
	await ctx.send(to_send)
	
# @bot.event
# async def on_message(message):
	# if message.author == bot.user:
		# return

	# response = "response"
	# await message.channel.send(response)

# @bot.event
# async def on_typing(channel, user, when):
	# print (channel)
	# add to a list, get the cache, check its list of on typing, if there are 5 instances of same channel and the time is within 5 seconds of now send message?

def parseChannel(channel):
	return {
		'dl-chat': '60278',
		'dreamleague': '60278',
		'nightmare': '47632',
		'monopoleague': '55825',
		'muppets': '26902',
		'bbobw': '31432',
		'the-flexining': '47021',
		'cradle-to-grave': '11444',
		'nobrew': '58445',
		'bot-commands': '11444',
		'100': '16087',
		'just-draft': '64988',
		'just-draft2': '58512',
		'lodba': '24928',
		'owlb': '48312',
		'gms': '20917',
		'unused': '60278',
		'4yp': '1'
	}.get(channel, "Channel Error, Maybe Panic?") 

bot.run(TOKEN)