# Plex-EpisodeNotifier - made by Opaquer

Hey guys, and welcome to my Plex/discord episode notifier bot!

So, first thing's first: I'm not a programmer at all. There may be bugs, and I haven't actually tried this on anything other than my Windows PC. I'm more than happy for people to work on it and make better versions as needed. Also, I've never done this before, so I don't know if there's a better way to do this. I'm going to walk through the steps of making the bot, installing all the necessary things, and finally the code to run. I know it's a lot, and I'm sorry, but if there's a better way to do it, I'd love to hear it!

Step 1: you'll want to make a discord bot and a server on discord. There's plenty of guides out there - since I was also trying to make one, I used this [one](https://www.freecodecamp.org/news/create-a-discord-bot-with-python/). Just go until you add the bot to your server. For permissions, I added a bunch of ones you probably won't need for testing purposes, but I think [this](https://i.imgur.com/xUfYkWo.png) is the minimum you'll need (if not, feel free to update me). Basically, it needs to be able to send/read messages, add/read reactions, delete messages and DM users. At some point you'll get a long token for your bot - keep it for step 3

Step 2: Install Python. Google this one, there's lots of guides out there. Once you've installed it, you'll need to install discord.py and plexapi. For windows, you go to cmd and do this:

    py -3 -m pip install -U discord.py
    py -3 -m pip install -U plexapi

Check your operating system on how to install it. Next go to your discord server and make 2 new channels. The way this works is by sending a notification to one channel that a new episode of a TV show is out, and watching the other channel to get inputs from users. The first one I've called the notification channel, and the second one I've called Show tracker. You can mute the notification channel, and make it a private channel for you only - your users don't need to see it.

NOTE: This bot DOES delete messages, so PLEASE make a new channel for the Show tracker channel. While it will work on any channel, it will try to delete every message you have if it can. You've been warned.

Next, you have to install Tautulli. I tried to do it without it, but it's just too much work. If you can get this working without using Tautulli, great! I look forward to hearing about it :)! Once installed, make a new notification agent that's connected to Discord. Make it trigger only on recently added, with the condition of it being in your TV show library. For the text for recently added, make it "{show_name}|S{season_num00}E{episode_num00} added" (see [here](https://i.imgur.com/WUNEppW.png)). Now when you get a new episode added into Plex, Tautulli will send a notification to our muted, private channel in discord saying there's a new episode for a TV show. It also puts the season and episode number in case you want to use it - though I did not.

Step 3: The fun stuff. Download the UserEpisodeNotification.py file. At the top there'll be a section for your details. The botChannel is the channel the bot is going to listen/message - what we called our Show tracker channel. The notification channel is our notification channel we just set up. Copy the ID of those channels (Google how to do that if you haven't got your account set up with the advanced features) and paste them in after the = sign. Do not use any quotes of any type, as this needs to be an integer.

Next is the TV library. This is the name Plex calls your TV library. For me, that's just "TV Shows" - call it what you will for you. The PersonalLabel is in case there's shows you don't share with everyone. For example, I'm the only person that watches The Flash, so I've only got the last season as I watch through it. I make the show have a tag "Personal" in Plex, and restrict my other users from seeing that library. This is then there so that in discord, only the shows everyone has access to is available, but it's optional if everything is for everyone. Next you'll need your discord token for the bot. That was from step 1. 

Lastly, the baseurl and is the IP address for Plex - if you're running this on the same machine and can get away with localhost, great, but if not, just change it as needed. Same with the port. Finally, the Plex Token - just use Google to find how to get that one.

With a bit of luck, if you save it and run it, it'll say that it's connected to Plex, then that it's starting discord, then finally that it's connected! When that's done, go to your Show tracker discord channel and type $update. This will take a sec, but it should add all the TV shows you have in alphabetical order, react with a down arrow to each of them, and then pin each one. Now when you click the down arrow, you'll get a DM from the bot saying you're tracking the TV show! If you ever get more TV shows, you can use $update again, and it'll add the new shows - but not delete the old messages - this is intentional so that the reactions from people doesn't get deleted. Your users can also type $check, and the bot will DM them all the shows they're tracking.

NOTE: I set up the bot command to be $, but you can change it to whatever you want :)

And with that, you should be good to go! Sorry again this was long winded! I hope you enjoy it, and that it works nicely for you! As I said, I'm not a programmer in any fashion, so there may be bugs that I may not be able to fix, but I'm also super happy for whoever to work on it as you see fit! If you make any cool updates, let me know!

If you're curious, the bot will listen to any message received in the notification channel, get the second line (the body of the text from Tautulli, then split that by "|"), and spits out the TV show based on that. It then goes through the saved list of users that are following that TV show (based on the Settings.txt file it makes/updates when users interact with the bot), and DMs each one if the new episode added is one that's followed by that user!
