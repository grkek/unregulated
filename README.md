# Unregulated

Unregulated is a [Discord](https://discordapp.com/) "self" bot, which provides a reliable method of storing messages in a JSON format.

For example: If an user is joined in a server and one of the channels receive a message it will be logged in a server specific folder as a JSON file named after the channel it was received in.

## Warning

**Discord is banning all self-bot users**

[A post on a forum](https://support.discordapp.com/hc/en-us/community/posts/360029279832-Bring-back-our-selfbots-) has a discussion about why self-bots are getting banned, use this code at your own risk !

## Installation

```bash
# Clone the repository
git clone https://github.com/grkek/unregulated.git
cd unregulated
# Create a new environment
python3 -m venv env
# Activate the environment
source env/bin/activate
# Install the Ultra JSON library
pip install ujson
cd ..
# Clone the dependency
git clone https://github.com/Rapptz/discord.py
cd discord.py
# Install the discord.py library
pip install -U .
cd ..
cd unregulated
```

## Usage

**Configuration**

Before you can run the bot you need a token which can be obtained via your web-browsers local storage tab, give it a quick refresh and for a moment the token will show up after getting deleted again.

Open the `config.py` file and edit `YOUR_TOKEN_HERE` with your obtained token, then provide the server names in a such fashion:

```python
configuration = {
    "token": "YOUR_TOKEN_HERE",
    "servers": [
        "MyServerName",
        "JoesServerName"
    ]
}
```

Keep in mind that all of the special characters are replaced by an empty space, for example in case of Jonathan-Mommas-Server you have to enter JonathanMommasServer and in case of Something+Weird you'll have to enter SomethingWeird and so on.

**Running**

You can run this script by:

```bash
python src/app.py
```

**Data collection**

The data which will consist of user details and the message will be stored in a server specific folder as a JSON file named after the channel it was received in.

The files are stored in the `/messages/` directory.
