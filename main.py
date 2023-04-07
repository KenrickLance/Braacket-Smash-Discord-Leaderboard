import json
import asyncio

from datetime import datetime

import requests
import discord
import pytz

from bs4 import BeautifulSoup

import elo

from commands import get_leaderboards

with open('./settings.json', 'r') as f:
    settings = json.load(f)

timezone = pytz.timezone(settings['timezone'])

intents = discord.Intents.default()
intents.message_content = True

client = discord.Client(intents=intents)

leaderboards_loop = {}

@client.event
async def on_message(message):
    if message.author == client.user:
        return

    if message.content.lower().startswith('!leaderboards'):
        has_been_sent = False
        while True:
            out_str = get_leaderboards()
            timestamp = datetime.now(timezone).strftime("%I:%M %p")
            out_str = f'```{settings["leaderboard_name"]}\n\n{out_str}\n\nLast updated: {timestamp}```'
            if has_been_sent == False:
                has_been_sent = True
                sent_message = await message.channel.send(out_str)
            else:
                await sent_message.edit(content=out_str)
            await asyncio.sleep(settings['leaderboard_refresh_rate'])

            leaderboards_loop.setdefault(message.id, {'is_deleted': False})
            if leaderboards_loop[message.id]['is_deleted'] == True:
                break

    if message.content.lower().startswith('!true-leaderboards'):
        has_been_sent = False
        while True:
            out_str = get_leaderboards(rating_type='true')
            timestamp = datetime.now(timezone).strftime("%I:%M %p")
            out_str = f'```{settings["leaderboard_name"]}\n\n{out_str}\n\nLast updated: {timestamp}```'
            if has_been_sent == False:
                has_been_sent = True
                sent_message = await message.channel.send(out_str)
            else:
                await sent_message.edit(content=out_str)
            await asyncio.sleep(settings['true_leaderboard_refresh_rate'])

            leaderboards_loop.setdefault(message.id, {'is_deleted': False})
            if leaderboards_loop[message.id]['is_deleted'] == True:
                break

@client.event
async def on_message_delete(message):
    try:
        leaderboards_loop[message.id]['is_deleted'] = True
    except KeyError:
        pass

client.run(settings['discord_api_token'])