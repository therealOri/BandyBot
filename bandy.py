####################################################################
#                                                                  #
# Credit: therealOri  |  https://github.com/therealOri/BandyBot    #
#                                                                  #
####################################################################

# +++++++++++ Imports and definitions +++++++++++ #
import asyncio
import datetime
import discord
from discord import app_commands
from libs import rnd #rng without needing internet.
import os
import tomllib



#Load our config
with open('config_bandy.toml', 'rb') as fileObj:
    config = tomllib.load(fileObj) #Dictionary/json




token = config["TOKEN"]
server_id = config["server_id"]
band_role = config["band_role_id"]
band_channel = config["band_channel_id"]
bot_logo = config["bot_logo"]
use_embeds = config["use_embeds"]
mention_members = config["mention_members"]
ignore_channels = config["channel_ignore_list"]



MY_GUILD = discord.Object(id=server_id)
author_logo = None
__authors__ = '@therealOri'




# Colors
hex_red=0xFF0000
hex_green=0x0AC700
hex_yellow=0xFFF000 # I also like -> 0xf4c50b

# +++++++++++ Imports and definitions +++++++++++ #






# +++++++++++ Client Setup +++++++++++ #
class Bandy(discord.Client):
    def __init__(self, *, intents: discord.Intents):
        super().__init__(intents=intents)
        self.tree = app_commands.CommandTree(self)

    async def setup_hook(self):
        await self.tree.sync(guild=None) # It will take 2-3hrs for commands to be registerd with discord. (may need to restart the bot after 2-3hrs of being online.)



intents = discord.Intents.default()
intents.messages = True
intents.message_content = True
bandy = Bandy(intents=intents)
# +++++++++++ Client Setup +++++++++++ #






# +++++++++++ Normal Functions +++++++++++ #

def clear():
    os.system("clear||cls")


def random_hex_color():
    hex_digits = '0123456789abcdef'
    hex_digits = rnd.shuffle(hex_digits)
    color_code = ''
    nums = rnd.randint(0, len(hex_digits)-1, 6)
    for _ in nums:
        color_code += hex_digits[_]
    value =  int(f'0x{color_code}', 16)
    return value


# +++++++++++ Normal Functions +++++++++++ #







# +++++++++++ Events +++++++++++ #

@bandy.event
async def on_ready():
    global author_logo
    me = await bandy.fetch_user(254148960510279683) #das me (Or you, it should get the profile picture of whoever that ID belongs to)
    author_logo = me.display_avatar

    clear()
    print(f'Logged in as {bandy.user} (ID: {bandy.user.id})')
    print('--------')





@bandy.event
async def on_message(message):
    if message.author == bandy.user: # Ignores itself
        return

    msg_channel_id = message.channel.id #channel message was sent in.
    if msg_channel_id == band_channel:
        return #We don't want to get messages from the band channel as that is where we should be sending messages.

    if msg_channel_id in ignore_channels:
        return #Don't get messages in these channels. (reserved for private channels for staff, etc.)

    role = message.guild.get_role(band_role)
    if not role in message.author.roles:
        return
    else:
        channel = bandy.get_channel(band_channel)
        msg_content = str(message.content)
        msg_channel_name = message.channel.id

        if mention_members == True:
            #Mentions enabled
            msg_author = message.author.mention
            embed_name = f'{msg_author}'
            attachment_band_msg = f'\u200B\n{msg_author} has sent attachments in Channel: <#{msg_channel_name}>\nAttachments:\n'
            band_msg1 = f'\u200B\n{msg_author} has sent a message!\n-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-\nChannel: <#{msg_channel_name}>\nMessage: {msg_content}\n-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-\u200B\n'
        else:
            #Mentions disabled
            msg_author = message.author
            embed_name=f'@{msg_author}'
            attachment_band_msg = f'\u200B\n@{msg_author} has sent attachments in Channel: <#{msg_channel_name}>\nAttachments:\n'
            band_msg2 = f'\u200B\n@{msg_author} has sent a message!\n-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-\nChannel: <#{msg_channel_name}>\nMessage: {msg_content}\n-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-\u200B\n'

        #Attachments/media/images
        if message.attachments:
            files = []
            for attachment in message.attachments:
                files.append(await attachment.to_file())
            band_msg = attachment_band_msg
            await channel.send(band_msg, files=files)
        else:
            # Messages/text
            # Embeds
            rnd_hex = random_hex_color()
            if use_embeds == True and mention_members == False:
                band_embed = discord.Embed(title='A band member has sent a message!\n-=-=-=-=-=-=-=-=-=-=-=-=-=-\u200B\n', colour=rnd_hex, timestamp=datetime.datetime.now(datetime.timezone.utc))
                band_embed.set_thumbnail(url=bot_logo)
                band_embed.add_field(name=f'\u200B\n', value=f'Member: {embed_name}\nChannel: <#{msg_channel_name}>\nMessage: {msg_content}', inline=False)
                band_embed.add_field(name='\u200B\n', value='-=-=-=-=-=-=-=-=-=-=-=-=-=-')
                band_embed.set_thumbnail(url=message.author.display_avatar)
                band_embed.set_footer(text=__authors__, icon_url=author_logo)
                await channel.send(embed=band_embed)
                return

            if use_embeds == True and mention_members == True:
                band_embed = discord.Embed(title='A band member has sent a message!\n-=-=-=-=-=-=-=-=-=-=-=-=-=-\u200B\n\u200B\n', description=f'Member: {embed_name}\nChannel: <#{msg_channel_name}>\nMessage: {msg_content}', colour=rnd_hex, timestamp=datetime.datetime.now(datetime.timezone.utc))
                band_embed.set_thumbnail(url=bot_logo)
                band_embed.add_field(name='\u200B\n', value='-=-=-=-=-=-=-=-=-=-=-=-=-=-')
                band_embed.set_thumbnail(url=message.author.display_avatar)
                band_embed.set_footer(text=__authors__, icon_url=author_logo)
                await channel.send(embed=band_embed)
                return

            #No Embeds
            if use_embeds == False and mention_members == True:
                band_msg = band_msg1
                await channel.send(band_msg)
                return

            if use_embeds == False and mention_members == False:
                band_msg = band_msg2
                await channel.send(band_msg2)
                return




# +++++++++++ Events +++++++++++ #





# +++++++++++ Commands +++++++++++ #
@bandy.tree.command(description='Shows you what commands you can use.')
async def help(interaction: discord.Interaction):
    rnd_hex = random_hex_color()
    embed = discord.Embed(title='Commands  |  Help\n-=-=-=-=-=-=-=-=-=-=-=-=-=-', colour=rnd_hex, timestamp=datetime.datetime.now(datetime.timezone.utc))
    embed.set_thumbnail(url=bot_logo)
    embed.add_field(name='\u200B\n/help', value="Shows you this help message.", inline=False)
    embed.add_field(name='\u200B\n/ping', value="Checks the bots latency and to see if it is responsive.", inline=False)
    embed.add_field(name='\u200B\n', value="\u200B\n", inline=False)
    embed.set_footer(text=__authors__, icon_url=author_logo)
    await interaction.response.send_message(embed=embed, ephemeral=True) #ephemeral = Only you/the user that ran the command can see the response.



@bandy.tree.command(description='Test to see if the bot is responsive.')
async def ping(interaction: discord.Interaction):
    await interaction.response.send_message(f"⏱️ Pong! ⏱️\nConnection speed is {round(bandy.latency * 1000)}ms", ephemeral=True)


# +++++++++++ Commands +++++++++++ #












# make bot go brrrrrrrrrrrrrrr
if __name__ == '__main__':
    clear()
    bandy.run(token, reconnect=True)
