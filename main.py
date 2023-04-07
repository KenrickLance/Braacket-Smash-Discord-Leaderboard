import asyncio

from datetime import datetime

import requests
import discord

from bs4 import BeautifulSoup

import elo

from commands import get_leaderboards

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
            timestamp = datetime.now().strftime("%I:%M %p")
            out_str = f'```PHRL ELO Leaderboards\n\n{out_str}\n\nLast updated: {timestamp}```'
            if has_been_sent == False:
                has_been_sent = True
                sent_message = await message.channel.send(out_str)
            else:
                await sent_message.edit(content=out_str)
            await asyncio.sleep(60 * 10)

            leaderboards_loop.setdefault(message.id, {'is_deleted': False})
            if leaderboards_loop[message.id]['is_deleted'] == True:
                break

    if message.content.lower().startswith('!true-leaderboards'):
        has_been_sent = False
        while True:
            out_str = get_leaderboards(rating_type='true')
            timestamp = datetime.now().strftime("%I:%M %p")
            out_str = f'```PHRL ELO Leaderboards\n\n{out_str}\n\nLast updated: {timestamp}```'
            if has_been_sent == False:
                has_been_sent = True
                sent_message = await message.channel.send(out_str)
            else:
                await sent_message.edit(content=out_str)
            await asyncio.sleep(60 * 60)

            leaderboards_loop.setdefault(message.id, {'is_deleted': False})
            if leaderboards_loop[message.id]['is_deleted'] == True:
                break

@client.event
async def on_message_delete(message):
    try:
        leaderboards_loop[message.id]['is_deleted'] = True
    except KeyError:
        pass

client.run('MTA1Mzg4NDg5MzQzNzg5MDU5MQ.GC1RuE.kzLZAyRZbZxYxzfJ4xjhjLav7hMWzBrWS5XhH0')