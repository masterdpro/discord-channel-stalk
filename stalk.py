from discord.ext import commands
import requests

URL = "Your webhook url"
TOKEN = 'Your account token'
TARGET_CHANNEL = 111111111


bot = commands.Bot(command_prefix='>', self_bot=True)

@bot.event
async def on_ready():
    print(f'User: {bot.user.name}')
    print(f'ID: {bot.user.id}')

@bot.command()
async def ping(ctx):
    await ctx.send('pong')

@bot.event
async def on_message(message):
    await bot.process_commands(message)

    if message.author == bot.user:
        return

    # Check if the message is from the specific channel ID
    if message.channel.id == TARGET_CHANNEL:
        channel = bot.get_channel(TARGET_CHANNEL)
        async for message in channel.history(limit=1):
            data = {
                "content": f'({message.created_at}) {message.author}: {message.content}',
                "username": f'Channel stalking'
            }

            data["embeds"]=[{
                "title": f'({message.created_at}) {message.author}',
                "description": f' {message.content}'
            }]
            result = requests.post(URL, json = data)
            try:
                result.raise_for_status()
            except requests.exceptions.HTTPError as err:
                print(err)
            else:
                print("Payload delivered successfully, code {}.".format(result.status_code))



        

bot.run(TOKEN, bot=False)