import asyncio
from calendar import c
from email.mime import application
import os
import random
from datetime import datetime, timedelta
from typing import Dict, List

import discord
from discord.ext import commands
from discord_slash import SlashContext, SlashCommand
from discord_slash.model import ContextMenuType, ButtonStyle, ComponentType
from discord_slash.context import MenuContext
from discord_slash.utils.manage_components import create_button, create_actionrow, ComponentContext, wait_for_component

from bot_constants import *

# a discord slash command bot with a few commands
tartaglia: commands.Bot = commands.Bot(
    command_prefix='!!', intents=discord.Intents.all(), case_insensitive=True)
childe_slash: SlashCommand = SlashCommand(
    tartaglia, sync_commands=True, debug_guild=DEBUG_GUILD)

msg_counter: int = MSG_COUNTER_INITIAL
current_activity: str = ""
ACTIVITIES: Dict[str, discord.BaseActivity] = {
    "normal": discord.Activity(name = "Being Fatui", type = discord.ActivityType.playing, large_image_url = "https://cdn.discordapp.com/attachments/765714136742363136/913526533329678376/genshinIcon.png"),
    "delusional": discord.Activity(name = "Delusion Unleashed", type = discord.ActivityType.playing, large_image_url = "https://cdn.discordapp.com/attachments/765714136742363136/913526532528537630/delusion_tartaglia.png"),
    "superman": discord.Activity(name = "True Foul Legacy", type = discord.ActivityType.playing, large_image_url = "https://cdn.discordapp.com/attachments/765714136742363136/913526533568737311/ultimate_tartaglia.png"),
}


@childe_slash.slash(name='ping', description='Pong!')
async def ping(ctx):
    """
    A simple ping command.
    """
    await ctx.send('Pong!\n' + str(tartaglia.latency * 1000) + 'ms')


@tartaglia.event
async def on_ready():
    """
    What the bot does when it's ready.
    """
    print('Logged in as')
    print(tartaglia.user.name)
    print(tartaglia.user.id)
    print('------')
    await change_nickname("Childe")
    await change_activity(ACTIVITIES["normal"])


@childe_slash.slash(name="delusional", description="delusion childe")
async def delusion(ctx: SlashContext):
    """
    A command that sends delusional childe, and makes the bot delusion mode.
    """
    await ctx.send("https://media.giphy.com/media/Yr1jmHrRMhqjGmGqrE/giphy.gif")
    await change_nickname("Delusional Tartaglia")
    await change_activity(ACTIVITIES["delusional"])


@childe_slash.context_menu(target=ContextMenuType.MESSAGE, name="Your\'re Delusional")
async def delusion_menu(ctx: MenuContext):
    """
    A context menu that sends delusional childe, and makes the bot delusion mode.
    """
    await change_nickname("Delusional Tartaglia")
    await change_activity(ACTIVITIES["delusional"])
    await ctx.send("https://media.giphy.com/media/Yr1jmHrRMhqjGmGqrE/giphy.gif")


@tartaglia.event
async def on_message(message: discord.Message):
    global msg_counter
    msg_counter -= 1
    if message.author == tartaglia.user:
        return
    if msg_counter == 0:
        await message.channel.send(tartaglia_quote())
        msg_counter = MSG_COUNTER_INITIAL
        if current_activity == ACTIVITIES["delusional"].name:
            await change_nickname("Tartaglia | Ultimate Mode")
            await change_activity(ACTIVITIES["superman"])
    if "tar tar taglia" in message.content:
        buttons: List[ComponentType] = [
            create_button(
                style=ButtonStyle.success,
                label="Full Song?",
                custom_id="onmsg_fullsong",
            ),
            create_button(
                style=ButtonStyle.primary,
                label="Full Lyrics?",
                custom_id="onmsg_fulllyrics",
            )
        ]
        action_row : Dict[str, ComponentType] = create_actionrow(*buttons)
        return_msg : discord.Message = await message.channel.send("Lover of Snezhnaya's Queen", components=[action_row])
        while True:
            try:
                button_ctx : ComponentContext = await wait_for_component(
                    tartaglia, components=action_row, timeout=60
                )
                if button_ctx.component_type == 2:  # check if button
                    if button_ctx.custom_id == "onmsg_fullsong":
                        await message.channel.send(
                            "https://www.youtube.com/watch?v=mfV7OwYwJ-Y"
                        )
                        action_row["components"][0]["disabled"] = True
                        await button_ctx.edit_origin(content="Lover of Snezhnaya\'s Queen", components=[action_row])
                    elif button_ctx.custom_id == "onmsg_fulllyrics":
                        await message.channel.send(
                            embed=discord.Embed(
                                name="Lyrics of *Snezhnaya\'s Greatest Love Machine*",
                                description="""There lived a certain man, in snezhnaya long ago, he was big and strong in his eyes a flaming glow, most people looked at him, in terror and fear, but to snezhnayan chicks, he was such a lovely dear. He could preach the bible like a preacher, full of ecstasy and fire, but he also was the kind of teacher, women would desire. Tar-Tar-Taglia lover of snezhnayan queen, there was a cat that really was gone. Tar-Tar-Taglia snezhnaya's famous love machine, it was a shame how he carried on. There lived a certain man, in snezhnaya long ago, he was big and strong, in his eyes a flaming glow, most people looked at him, with terror and fear, but to snezhnayan chicks he was such a lovely dear, he could preach the bible like a preacher, full of ecstasy and fire, but he also was the kind of teacher women would desire. There lived a certain man, in snezhnaya long ago, he was big and strong in his eyes a flaming glow, most people looked at him, in terror and fear, but to snezhnayan chicks, he was such a lovely dear. He could preach the bible like a preacher, full of ecstasy and fire, but he also was the kind of teacher, women would desire. Tar-Tar-Taglia lover of snezhnayan queen, there was a cat that really was gone. Tar-Tar-Taglia snezhnaya's famous love machine, it was a shame how he carried on. There lived a certain man, in snezhnaya long ago, he was big and strong, in his eyes a flaming glow, most people looked at him, with terror and fear, but to snezhnayan chicks he was such a lovely dear, he could preach the bible like a preacher, full of ecstasy and fire, but he also was the kind of teacher women would desire. Now then, I wish you all glorious victory, for snezhnaya, for her majesty, the tsaritsa, and for yourselves. There lived a certain man, in snezhnaya long ago, he was big and strong, in his eyes a flaming glow, most people looked at him, in terror and fear, but to snezhnayan chicks he was such a lovely dear, he could preach the Bible like a preacher, full of ecstasy and fire, but he also was the kind of teacher, women would desire, Tar-Tar-Taglia lover of snezhnayan queen, there was a cat that really was gone, Tar-Tar-Taglia snezhnaya's famous love machine, it was a shame how he carried on. Tar-Tar-Taglia, lover of snezhnayan queen. Tar-Tar-Taglia, lover of snezhnayan queen."""
                            )
                        )
                        action_row["components"][1]["disabled"] = True
                        await button_ctx.edit_origin(content="Lover of Snezhnaya\'s Queen", components=[action_row])
            except asyncio.exceptions.TimeoutError:
                for i in range(2):
                    action_row["components"][i]["disabled"] = True
                await return_msg.edit(content="Timed out.", components=[action_row])
                break

async def change_nickname(nickname: str):
    for guild in tartaglia.guilds:
        await guild.get_member(tartaglia.user.id).edit(nick=nickname)

async def change_activity(activity: discord.BaseActivity):
    global current_activity
    print(f"Changing activity to {activity.name}")
    current_activity = activity.name
    print(current_activity)
    await tartaglia.change_presence(activity=activity)
    start = datetime.now()
    while True:
        if activity != ACTIVITIES["normal"] and datetime.now() - start > timedelta(seconds=30):
            await change_nickname("Childe")
            await tartaglia.change_presence(activity=ACTIVITIES["normal"])
            break
        await asyncio.sleep(1)


def tartaglia_quote():
    """
    Get a random quote by tartaglia from the text file, and send it.
    """
    with open("tartaglia_quotes.txt", "r") as f:
        lines: List[str] = f.readlines()
        mapped_lines: Dict[str, str] = {
            line.split("=")[0]: line.split("=")[1]
            for line in lines
        }
        return mapped_lines[random.choice(list(mapped_lines.keys()))]


tartaglia.run(os.environ["DISCORD_TOKEN"])
