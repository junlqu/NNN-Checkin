# import libraries
import discord
from discord.ext import tasks
import os
from dotenv import load_dotenv
import time

# import files
from firebase import *

load_dotenv()

intents = discord.Intents(messages = True, message_content = True, members = True, guilds = True, guild_messages = True)
client = discord.Client(intents=intents)

date = time.localtime()

@client.event
async def on_ready():
    check_date.start()
    print(f'{client.user} is ready!\n')

@client.event
async def on_message(message):
    if message.author == client.user:
        return
    
    if time.localtime().tm_mon != 11:
        await message.channel.send(f'Go ahead and nut... I am always watching...')
        return

    if message.content.lower() == 'present':
        res = update_current_date(message.author.id)
        if res == 0:
            await message.channel.send(f'<@{message.author.id}> checked in!')
        elif res == 1:
            await message.channel.send(f'<@{message.author.id}> already checked in today!')
        elif res == 2:
            await message.channel.send(f'<@{message.author.id}> already failed NNN!\n\nYou lasted {days_lasted(message.author.id)} days.')
        else:
            await message.channel.send(f'Error: Invalid command (System error)')

    elif message.content.lower() == 'nnn remaining':
        users = in_chal()
        if len(users) == 0:
            await message.channel.send('**All contestants failed!**')
        else:
            await message.channel.send(f'**__Remaining contestants:__**\n\n{print_users(users)}')

    elif message.content.lower() == 'nnn failed':
        users = failed_chal()
        if len(users) == 0:
            await message.channel.send('**No one has failed!**')
        else:
            await message.channel.send(f'**__Failures:__**\n\n{print_users(users)}')
    
    elif message.content.lower() == "nnn help":
        await message.channel.send('**__Commands:__**\n\n`present`  to check in daily\n\n`NNN remaining`  to check the remaining contestants\n\n`NNN failed`  to check the contestants that already failed')

@tasks.loop(seconds=12)
async def check_date():
    date = time.localtime()
    await client.wait_until_ready()
    channel = client.get_channel(1037197294606483536) # Channel from ID
    if (date.tm_hour == 0) and (date.tm_min == 0) and (date.tm_sec < 12):
        failed = users_failed()
        if len(failed) == 0:
            await channel.send("Congratulations! All remaining contestants passed!")
        else:
            await channel.send(f"Uh Oh! Somebody couldn't hold the urges...\n\nThe following contestants failed:\n\n{print_users_mention(failed)}")

def print_users(users):
    conc = ""
    for user in users:
        conc += '`' + client.get_user(int(user)).display_name + '`\n\n'
    return conc

def print_users_mention(users):
    conc = ""
    for user in users:
        conc += f"<@{str(user)}>\n"
    return conc

def add_roles(ids, role):
    for id in ids:
        client.get_user(int(id)).add_role(role)

client.run(os.getenv('TOKEN'))