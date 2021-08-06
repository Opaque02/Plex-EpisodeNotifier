## install discord.py
## py -3 -m pip install -U discord.py

## install plexapi
## py -3 -m pip install -U plexapi

import plexapi
import discord
import requests

from plexapi.server import PlexServer
from discord.ext import commands
from discord.ext.commands import UserConverter

#############################
## ENTER YOUR DETAILS HERE ##
#############################

botChannel =  ## ID CHANNEL OF THE CHANNEL FOR THE BOT TO LISTEN TO ##
notificationChannel =  ## ID CHANNEL OF THE CHANNEL FOR THE NOTIFICATIONS TO BE SENT TO ##
tvLibrary = "" ## TV SHOW LIBRARY IN PLEX - i.e. "TV Shows" ##
PersonalLabel = "" ## PERSONAL LABEL IN PLEX - OPTIONAL ##
TOKEN = "BOT_TOKEN" ## DISCORD BOT SECRET ##

baseurl = 'http://localhost:32400'
PlexToken = 'Plex_Token'
plex = PlexServer(baseurl, PlexToken)

#############################
#############################
#############################

print("Connected to Plex!")

def updateShows():
    shows = plex.library.section(tvLibrary).search(filters={"label!":PersonalLabel})
    showList=[]
    for video in shows:
        showList.append(video.title)
    return showList

def listShows():
    message=""
    for i in range(len(showList)):
        message=message+showList[i]+'\n'
    return message.strip()

def validShow(Show):
    for i in range(len(showList)):
        if Show==showList[i]:
            return True
    return False

def addShow(user,Show):
    userCheck(user)
    userSettings = open("Settings.txt",mode='r')
    currentInfo = userSettings.readlines()
    userSettings.close()
    newInfo=[]
    for i in range(len(currentInfo)):
        currentLine=currentInfo[i]
        if user in currentLine.strip():
            if Show in currentLine.strip():
                newInfo.append(currentInfo[i])
                outputMessage = "You are already tracking "+Show+"!"
            else:
                newInfo.append(currentInfo[i].strip()+"|"+Show+"\n")
                outputMessage = "You are now tracking "+Show+" and will be messaged when new episodes are ready to watch!"
        else:
            newInfo.append(currentInfo[i])
    userSettings = open("Settings.txt",mode='w')
    for line in newInfo:
        userSettings.write(line)
    userSettings.close()
    return(outputMessage)

def removeShow(user,Show):
    userCheck(user)
    userSettings = open("Settings.txt",mode='r')
    currentInfo = userSettings.readlines()
    userSettings.close()
    newInfo=[]
    for i in range(len(currentInfo)):
        currentLine=currentInfo[i]
        if user in currentLine.strip():
            if Show in currentLine.strip():
                splitData=currentLine.strip().split("|")
                splitData.remove(Show)
                newInfo.append("|".join(splitData)+"\n")
                outputMessage = "You have untracked "+Show+" and will no longer get notifications!"
            else:
                newInfo.append(currentInfo[i])
                outputMessage = "You weren't tracking "+Show
        else:
            newInfo.append(currentInfo[i])
    userSettings = open("Settings.txt",mode='w')
    for line in newInfo:
        userSettings.write(line)
    userSettings.close()
    return(outputMessage)    

def userCheck(user):
    userSettings = open("Settings.txt",mode='r')
    currentInfo = userSettings.readlines()
    userSettings.close()
    newInfo=[]
    newUser=0
    if len(currentInfo)==0:
        currentInfo.append(user+"\n")
    else:
        for i in range(len(currentInfo)):
            if currentInfo[i].split("|")[0].strip()==user:
                newUser=1
        if newUser==0:
            currentInfo.append(user+"\n")
    userSettings = open("Settings.txt",mode='w')
    for line in currentInfo:
        userSettings.write(line)
    userSettings.close()

def checkUserShows(Show):
    userSettings = open("Settings.txt",mode='r')
    currentInfo = userSettings.readlines()
    userSettings.close()
    users=[]
    for i in range(len(currentInfo)):
        currentLine=currentInfo[i]
        if Show in currentLine.strip():
            users.append(currentLine.strip().split("|")[0])
    return users

def seeShows(user, Show="all"):
    userSettings = open("Settings.txt",mode='r')
    currentInfo = userSettings.readlines()
    userSettings.close()
    shows=[]
    userShows=[]
    for i in range(len(currentInfo)):
        currentLine=currentInfo[i].split("|")[0]
        if currentLine==user:
            userShows=currentInfo[i][:-1]
    if userShows!=[]:
        userShows=userShows.split("|")[1:]
    if len(userShows)==0:
        return "No shows tracked"
    else:
        userShowList=""
        if Show=="all":
            for i in range(len(userShows)):
                userShowList=userShowList+userShows[i]+", "
            userShowList=userShowList[:-2]
        else:
            print(userShows)
            if Show in userShows:
                return "You are tracking "+str(Show)
            else:
                return "You are not tracking "+str(Show)
                
        return "You are tracking " + userShowList

showList=updateShows()
numShows = len(showList)

intents = discord.Intents.all()
intents.members = True

client = discord.Client(intents=intents)

print("starting Discord...")
client = discord.Client()
prefix = "$"
bot=commands.Bot(command_prefix=prefix)

## BOT VERSION ##

@bot.event
async def on_ready():
    print('We have logged in as {0.user}'.format(bot))
    print("------------------------------------------------")

@bot.event
async def on_message(message):
    if message.author == bot.user:
        return
    channelID=message.channel.id

    users=[]
    if channelID==notificationChannel:
        show=message.content.split("\n")[1]
        show=show.split("|")[0]
        users=checkUserShows(show)
    if users!=[]:
        for i in range(len(users)):
            user = await bot.fetch_user(users[i])
            await user.send("A new episode of "+show+" is available to watch!")
    
    await bot.process_commands(message)

@bot.event
async def on_raw_reaction_add(reaction):
    userID = str(reaction.user_id)
    if int(userID)!=bot.user.id:
        channel = bot.get_channel(reaction.channel_id)
        message=await channel.fetch_message(reaction.message_id)
        show=message.content
        output = addShow(userID,str(show))
        user = await bot.fetch_user(userID)
        await user.send(output)

@bot.event
async def on_raw_reaction_remove(reaction):
    userID = str(reaction.user_id)
    if int(userID)!=bot.user.id:
        channel = bot.get_channel(reaction.channel_id)
        message=await channel.fetch_message(reaction.message_id)
        show=message.content
        output = removeShow(userID,str(show))
        user = await bot.fetch_user(userID)
        await user.send(output)

@bot.command(
        help = "Use this command to check what TV shows you are currently tracking. You will be sent a DM letting you know.",
        brief = "Use this to see what shows you're tracking"
    )

async def check(ctx):
    def not_pinned(message):
            return not message.pinned
    showList=updateShows()
    userID=str(ctx.message.author.id)
    channelID=ctx.message.channel.id
    if botChannel==channelID:
        message = seeShows(userID,"all")
        await ctx.message.channel.purge(check=not_pinned)
        user = await bot.fetch_user(userID)
        await user.send(message)
    else:
        print("Wrong channel!")

@bot.command(
        help = "If you add new TV shows, you can use this to update the list in Discord. Note, it won't delete old messages of TV shows, in case people have reacted and are following, so once you update, your list of TV shows may not be alphabetical",
        brief = "Use this to update your list of TV shows"
    )

async def update(ctx):
    def not_pinned(message):
            return not message.pinned
    showList=updateShows()
    channelID=ctx.message.channel.id
    if botChannel==channelID:
        await ctx.message.channel.purge(check=not_pinned)
        messages=[]
        messageList = await ctx.channel.history(limit=200).flatten()
        for i in range(len(messageList)):
            messages.append(messageList[i].content)
        newShows=[x for x in showList if x not in messages]
        for i in range(len(newShows)): #len(newShows) instead of 3
            message = await ctx.channel.send(newShows[i]+"\n")
            await message.add_reaction("⬇")
            await message.pin()
        await ctx.message.channel.purge(check=not_pinned)
        print("Update complete")
    else:
        print("Wrong channel!")

bot.run(TOKEN)
