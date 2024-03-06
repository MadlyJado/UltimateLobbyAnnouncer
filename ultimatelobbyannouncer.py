import discord
import random
from discord.ext import commands, tasks
import datetime
import random
import asyncio
import json
import os
from apikey import api_key
from levelingsystem_cog import LevelingSystem

intent = discord.Intents().all()
client = commands.Bot(command_prefix=".", intents=intent)
emoji2 = "🟦"
    

@client.event
async def on_ready():
    """
    This method prints "bot is ready" when the bot is ready.
    """
    
    print("Bot is Ready")
    

@client.command()
async def setupnotifs(ctx):
    """
    This command sets up the notification message all users react to to notify the members who wish to be notified of hosted
    games.
    """
    guild = ctx.guild
    bluehostmessage = await ctx.send("React with 🟦 to recieve notifactions for a new stellaris game!")
    await bluehostmessage.add_reaction("🟦")
    try:   
        for member in guild.members:
            await member.add_roles(discord.Object(discord.utils.get(ctx.guild.roles, name="Level 1").id))
        for member in guild.members:
            await member.remove_roles(discord.Object(discord.utils.get(ctx.guild.roles, name="Notified for new games").id))
    except Exception:
        await ctx.send("Make sure you have a role for notifications called 'Notified for new games' as well as one called 'Level 1' You'll also need to make 4 more like it Named 'Level 2' through 'Level 5'. As well as a 'Hosts' role")

@client.event
async def on_guild_join(guild):
    """
    This on_guild_join event creates the appropiate roles and channels that the bot requires, to make it easier for end users to use.
    
    """
    await guild.owner.send("Thanks for using ultimatelobbyannouncer! The bot will now add the appropiate channels and roles for you to use our bot!")
    channel1 = await guild.create_text_channel("Notifications")
    channel2 = await guild.create_text_channel("lobbies")
    level1 = await guild.create_role(name="Level 1")
    level2 = await guild.create_role(name="Level 2")
    level3 = await guild.create_role(name="Level 3")
    level4 = await guild.create_role(name="Level 4")
    level5 = await guild.create_role(name="Level 5")
    level6 = await guild.create_role(name="Hosts")
    level7 = await guild.create_role(name="Notified for new games")
    await guild.owner.send("Done! To get your members notified of new games, make sure to setup notifcations by using .setupnotifs in any channel, although we have added a notification channel for you to use if you wish.")   

@client.event
async def on_reaction_add(reaction, member):
    """
    In this on_reaction_add event, it checks if a certain emoji is being used. That emoji being blue square emote, used to add the notification role with the bot.
    """
    if reaction.emoji == emoji2:
        await member.add_roles(discord.Object(discord.utils.get(member.guild.roles, name="Notified for new games").id))


@client.event
async def on_reaction_remove(reaction, member):
    """
    In this on_reaction_remove method, it checks if the blue square emoji is being reacted, if the blue square is used, then it will remove
    the notification role of the server for lobbies.
    """
    if reaction.emoji == emoji2:
        await member.remove_roles(discord.utils.get(member.guild.roles, name="Notified for new games"))

@client.event
async def on_member_join(member):
    """
    In this on_member_join event, adds the "Level 1" role whenever a member joins a server in which the 
    ultimatelobbyannouncer bot is used.
    """
    await member.add_roles(discord.utils.get(member.guild.roles, name="Level 1"))



@client.command(pass_context=True)
async def newgame(ctx, game: str, gameid : str, *, desc: str):
    """
    This command announces a new game lobby, if the person has the required role.
    
    Args:
        game (string): the game that is being hosted
        gameid (string): the lobby's id, this could also be replaced if the server is a minecraft server, with the IP Address 
        of the minecraft server
        desc (string): The description of the lobby.
    """
    author = ctx.author
    hostrole = discord.utils.get(ctx.guild.roles, name="Hosts")
    notificationrole = discord.utils.get(ctx.guild.roles, name="Notified for new games")
    lobbychannel = discord.utils.get(ctx.guild.channels, name="lobbies")
    if(hostrole in author.roles):
        embed = discord.Embed(color = discord.colour.Color.red())
        embed.set_author(name=f"{game} Lobby")
        embed.add_field(name="Host's Name: ", value=author.mention)
        embed.add_field(name="Game ID:", value=gameid)
        embed.add_field(name="Description:", value=desc)
        await lobbychannel.send(notificationrole.mention, embed=embed)
    elif(hostrole not in author.roles):
        await ctx.send("Sorry but you are not a host, keep leveling up to become a host today!")

@client.command()
async def rolldie(ctx, faces: int):
    """
    As can be explained from the title of the command, it rolls a die!
    """
    die = []
    for face in range(faces+1):
        die.append(face)
    await ctx.send(f"Die from d{faces} rolled: {random.choice(die)}")


@client.command()
async def clear(ctx, *, amount : int):
    """
    This command clears a number of messages, which is good when spam or messages you wish to delete are shown, such as spam.
    
    
    Args:
        amount (integer): This parameter takes the amount of messages the admin wishes to remove
    """
    author = ctx.author
    
    if(author.guild_permissions.administrator):
        await ctx.channel.purge(limit=amount)
    elif(author.guild_permissions.administrator == False):
        await author.send("You are not an administrator!")

async def load():
    await client.add_cog(LevelingSystem(client))

async def main():
    await load()
    await client.start(api_key)

asyncio.run(main())
