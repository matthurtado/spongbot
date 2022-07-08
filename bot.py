# This example requires the 'members' privileged intents

from base64 import b64decode
from io import BytesIO
import re
from urllib.request import urlopen
import discord
from discord.ext import commands
import spongebobify
import requests
import json

class SpongeFlags(commands.FlagConverter, delimiter=' ', prefix='--'):
    text: str
    imageOverride: str = None
    textXpos: int = None
    textYpos: int = None
    targetWidthRatio: float = None
    spongeTheText: bool = True

description = '''A bot to create SpOnGeBoB images
    /spongeImage --text Test Test --spongeTheText false
    Required Arguments:
        text: The text to sPonGe.
    Optional Arguments:
        imageOverride: URL of an image to use instead of Spongebob.
        textXpos: The x position of the text.
        textYpos: The y position of the text.
        targetWidthRatio: The width of the image to use.
        spongeTheText: Whether to sPonGe the text.'''

intents = discord.Intents.default()
intents.members = True

bot = commands.Bot(command_prefix='/',
                   description=description, intents=intents)

text_file = open("discord_key", "r")
discord_key = text_file.read()

@bot.event
async def on_ready():
    print('Logged in as')
    print(bot.user.name)
    print(bot.user.id)
    print('------')

@bot.command()
async def sponge(ctx, *args):
    """Sponges a string."""
    await ctx.send(spongebobify.spongebobify(' '.join(args)))


@bot.command()
async def spongeImage(ctx, *, flags: SpongeFlags):
    """Generates a spongebob image
    Required Arguments:
        text: The text to sPonGe.
    Optional Arguments:
        imageOverride: URL of an image to use instead of Spongebob.
        textXpos: The x position of the text.
        textYpos: The y position of the text.
        targetWidthRatio: The width of the image to use.
        spongeTheText: Whether to sPonGe the text.
    """

    url = "https://spongbobify.herokuapp.com/spongebobify"

    payload = json.dumps({
        "textToSponge": flags.text,
        "imageOverride": flags.imageOverride,
        "textXPos": flags.textXpos,
        "textYPos": flags.textYpos,
        "targetWidthRatio": flags.targetWidthRatio,
        "spongeTheText": flags.spongeTheText
    })
    headers = {
        'Content-Type': 'application/json'
    }

    response = requests.request("POST", url, headers=headers, data=payload)
    image = BytesIO(
        b64decode(re.sub("data:image/jpeg;base64", '', response.text)))
    await ctx.send(file=discord.File(fp=image, filename='image.png'))

@spongeImage.error
async def info_error(ctx, error):
    if isinstance(error, commands.MissingRequiredFlag):
        await ctx.send(error)

bot.run(discord_key)
