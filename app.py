# -*- coding: utf-8 -*-
"""Unregulated discord module

This module serves a purpose of collecting certain discord server/channel messages 
and storing it in a convinient JSON format, which then can be used for multiple purposes

Prerequisites:
    (logs) directory must be created next to the program file for it to function properly.
    (token) a discord user token must be set in the config.py file.
    (servers) a server name list must be set in the config.py file, keep in mind that
    when the program dumps a server its name is reffered without any special characters.

Example:
    ::python
        $ python app.py

In order to increase the performance and keep the CPU at a steady 2-5% workload
a special JSON library was used (ujson) which guarantees a fast decode/encode
rates for large JSON documents.

Attributes:
    base_dir (str): Represents a base directory of the application program from where it was launched
    and it is used for avoiding the painful path resolving problem python currently has.

    bot (AutoShardedBot): Represents a sharded bot which serves the purpose of an event handler
    and receives the messages from certain channels. sharded bots work a lot faster and get
    split in two if the workload is more than a single bot can take, this doesn't mean that
    the bot authenticates 2 or more times after it is sharded, the workload is just split in two.

.. _Google Python Style Guide:
   http://google.github.io/styleguide/pyguide.html

"""
import datetime
import logging
import os
import re
import sys

import discord
import ujson as json
from discord import ChannelType
from discord.ext import commands

from config import configuration

base_dir = os.path.dirname(os.path.abspath(sys.argv[0]))

logging.basicConfig(filename=f'{base_dir}/logs/{datetime.datetime.now()}.log',level=logging.ERROR)

bot = commands.AutoShardedBot(command_prefix='', self_bot=True)

if os.path.exists(f"{base_dir}/messages"):
    pass
else:
    os.mkdir(f"{base_dir}/messages")

@bot.event
async def on_message(msg):
    """on_message event handler

    This function is fired every single time a bot detects a new message in a server/channel,
    it is triggered for direct messages as well, but later down the code the logic prevents
    direct messages from getting through the parsing logic.

    Attributes:
        discord_server (str): Represents a special characterless version of the server name.

        discord_channel (str): Represents a special characterless version of the channel name.

        attachments (list): Represents a list of attachment links which is sent by users to the channel
        it collects all of the attachments and puts the links (str) into a list which is then converted
        to a more frinedly format (JSON).

        message_structure (dict): Represents a simple message structure which is then written to a JSON
        document, the fields are:
            id (str): Represents the message identification number.
            author (str): Represents the sender of the message.
            authorId (str): Represents the sender identification number of the message.
            createdAt (str): Represents the creation datetime of the message.
            text (str): Represents the content of the sent text message.
            attachments (list): Represents the attachment list, might be an image, a text file, anything else.
        
        data_structure (dict): Represents a simple data structure which is then used to compile the messages
        and the server/channel names together for a convinient data model, which is then written to a json document,
        the fields are:
            discordServer (str): Represents the server name extracted from the message.
            discordChannel (str): Represents the channel name extracted from the message.
            messages (list): Represents a message list which is built using message_structures
            mentioned above.

    Args:
        msg (Message): Message incomming from the discord server/channel
        containing all of the user information needed for message sender identification.
    
    Returns:
        None

    Raises:
        KeyError: most of old versions of discord.py have a strange bug which raises a KeyError for 'id' which was not found
        it is fixed in the github development version of the library.

    """

    if type(msg.channel) is discord.channel.DMChannel:
        pass
    else:
        discord_server = re.sub('[^0-9a-zA-Z]+', '', f"{msg.guild}")
        discord_channel = re.sub('[^0-9a-zA-Z]+', '', f"{msg.channel}")

        if discord_server not in configuration["servers"]:
            return

        attachments = [attachment.url for attachment in msg.attachments if msg.attachments]

        message_structure = {
            "id": f"{msg.id}",
            "author": f"{msg.author}",
            "authorId": f"{msg.author.id}",
            "createdAt": f"{msg.created_at}",
            "text": f"{msg.content}",
            "attachments": attachments
        }

        if not os.path.exists(f"{base_dir}/messages/{discord_server}"):
            os.mkdir(f"{base_dir}/messages/{discord_server}")

        if os.path.exists(f"{base_dir}/messages/{discord_server}/{discord_channel}.json"):
            with open(f"{base_dir}/messages/{discord_server}/{discord_channel}.json", "r") as f:
                data_structure = json.load(f)

            if data_structure.get("messages"):
                data_structure["messages"].append(message_structure)
            else:
                data_structure["messages"] = [message_structure]
            
            with open(f"{base_dir}/messages/{discord_server}/{discord_channel}.json", 'w') as f:
                json.dump(data_structure, f, indent=4)
        else:
            with open(f"{base_dir}/messages/{discord_server}/{discord_channel}.json", "w+") as f:
                data_structure = {
                    "discordServer": f"{discord_server}",
                    "discordChannel": f"{discord_channel}",
                    "messages": []
                }
                
                json.dump(data_structure, f, indent=4)
                
            data_structure["messages"].append(message_structure)
            with open(f"{base_dir}/messages/{discord_server}/{discord_channel}.json", 'w') as f:
                json.dump(data_structure, f, indent=4)


def main():
    """Entrypoint for the module
    bot.run function loads the token from a configuration file (config.py) and
    runs the bot as a non-bot user to signal the discord.py library that we are
    dealing with a self-bot.

    Args:
        None
    
    Returns:
        None

    Raises:
        Every exception which occurs in the discord.py library.

    """
    try:
        bot.run(configuration["token"], bot=False)

    except:
        raise

if __name__ == "__main__":
    main()
