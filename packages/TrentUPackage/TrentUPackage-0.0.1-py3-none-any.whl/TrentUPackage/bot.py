# bot.py
# Skeleton code obtained from realpython.com - see sources
import discord
import os
import random
from dotenv import load_dotenv

#allowing for the bot to read events from messages and guilds(servers)
#do not disbale these for now
intents = discord.Intents.default()
intents.guilds = True
intents.guild_messages = True
intents.message_content = True
intents.members = True

load_dotenv()

#token is not avialable in GIT
TOKEN = os.getenv('DISCORD_TOKEN')

#intents is required for all discord versions past 1.7.3 left 
#defined above
client = discord.Client(intents=intents)

print(TOKEN)

#not seen by users, displays in terminal if the bot loaded
@client.event
async def on_ready():
    print(f'{client.user} Heh....It works...')

#When someone joins the server they get a direct message  
@client.event
async def on_member_join(member):
    await member.create_dm()
    await member.dm_channel.send(
        f'Hi {member.name}, I am your student helper bot \nStarter Commands Here'
    )

@client.event
async def on_message(message):
    #check if the message is fron a bot and if so return
    if message.author == client.user:
        return
    dad_Jokes = [
        # from https://www.countryliving.com/life/a27452412/best-dad-jokes/
        'I\'m afraid for the calendar. Its days are numbered.',
        'My wife said I should do lunges to stay in shape. That would be a big step forward.',
        'Why do fathers take an extra pair of socks when they go golfing?" "In case they get a hole in one!',
        'Singing in the shower is fun until you get soap in your mouth. Then it\'s a soap opera.',
        'What do a tick and the Eiffel Tower have in common?" "They\'re both Paris sites.',
        'What do you call a fish wearing a bowtie?" "Sofishticated."',
    ]
    
    if 'tell me a joke' in message.content.lower():
        response = random.choice(dad_Jokes)
        await message.channel.send(response)


client.run(TOKEN)