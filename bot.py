import discord
import firebase

intents = discord.Intents(messages = True, message_content = True, members = True)

client = discord.Client(intents=intents)

@client.event
async def on_ready():
    print(
        f'{client.user} is ready!\n'
    )

@client.event
async def on_message(message):
    if message.author == client.user:
        return

    if message.content.lower() == 'present':
        await message.channel.send(f'<@{message.author.id}> checked in!')

client.run('NzczNzc0NjI4MDk0MjE0MTU0.GGXRda.6tZ4Srfjvth33j0hKGAjSLb7C7HEpZIKUlsi0g')