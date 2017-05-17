#!/usr/bin/python3
# -*- coding: utf-8 -*-
import discord
import os
import re
from wow import *


DISCORD_BOT_TOKEN = str(os.environ.get('DISCORD_BOT_TOKEN'))
client = discord.Client()


@client.event
async def on_message(message):
    """Listens for specific user messages."""

    # If the author is the bot do nothing.
    if message.author == client.user:
        return

    # If it's not the bot and the message starts with '!armory' process it.
    if message.content.startswith('!armory'):
        # Splits up the message, requires the user to type their message as '!wow Jimo burning-legion'.
        # Sends the second word (name) and third word (realm) to the characterInfo function to build a character sheet.
        split = message.content.split(" ")
        info = characterInfo(split[1], split[2])

        # If the returned data is an empty string send a message saying the player/realm couldn't be found.
        if info == '':
            msg = 'Could not find a player with that name/realm combination.'.format(message)
            await client.send_message(message.channel, msg)
        # Otherwise respond with an incredibly long string of data holding all of the info.
        else:
            msg = discord.Embed(title="%s" % (info['name']), colour=discord.Colour(info['class_colour']), url="%s" % (info['armory']), description="%s" % (info['class_type']))

            msg.set_thumbnail(url="https://render-%s.worldofwarcraft.com/character/%s" % (WOW_REGION, info['thumb']))
            msg.set_footer(text="Feedback: https://github.com/JamesIves/discord-wow-armory-bot/issues", icon_url="https://github.com/JamesIves/discord-wow-armory-bot/blob/master/assets/icon.png?raw=true")

            msg.add_field(name="Character", value="**`Name`:** `%s`\n**`Realm`:** `%s`\n**`Battlegroup`:** `%s`\n**`Item Level`:** `%s`" % (info['name'], info['realm'], info['battlegroup'], info['ilvl']), inline=True)
            msg.add_field(name="Keystone Achievements", value="**`Master`:** `%s`\n**`Conqueror`:** `%s`" % (info['keystone_master'], info['keystone_conqueror']), inline=True)
            msg.add_field(name="Emerald Nightmare", value="**`Normal`:** `%s/%s`\n**`Heroic`:** `%s/%s`\n**`Mythic`:** `%s/%s`\n**`AOTC`:** `%s`" % (info['emerald_nightmare']['normal'], \
             info['emerald_nightmare']['bosses'], info['emerald_nightmare']['heroic'], info['emerald_nightmare']['bosses'], info['emerald_nightmare']['mythic'], \
             info['emerald_nightmare']['bosses'], info['aotc_en']), inline=True)
            msg.add_field(name="Trial of Valor", value="**`Normal`:** `%s/%s`\n**`Heroic`:** `%s/%s`\n**`Mythic`:** `%s/%s`\n**`AOTC`:** `%s`" % (info['trial_of_valor']['normal'], \
             info['trial_of_valor']['bosses'], info['trial_of_valor']['heroic'], info['trial_of_valor']['bosses'], info['trial_of_valor']['mythic'], \
             info['trial_of_valor']['bosses'], info['aotc_tov']), inline=True)
            msg.add_field(name="The Nighthold", value="**`Normal`:** `%s/%s`\n**`Heroic`:** `%s/%s`\n**`Mythic`:** `%s/%s`\n**`AOTC`:** `%s`" % (info['the_nighthold']['normal'], \
             info['the_nighthold']['bosses'], info['the_nighthold']['heroic'], info['the_nighthold']['bosses'], info['the_nighthold']['mythic'], \
             info['the_nighthold']['bosses'], info['aotc_nh']), inline=True)

            await client.send_message(message.channel, embed=msg)


client.run(DISCORD_BOT_TOKEN)
