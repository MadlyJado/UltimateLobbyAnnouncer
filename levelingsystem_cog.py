import discord
import os
import pickle
from discord.ext import commands, tasks
import datetime

utc = datetime.timezone.utc

time = datetime.time(hour=8, minute=30, tzinfo=utc)


class LevelingSystem(commands.Cog):
    """
    This class creates a Leveling system that helps server owners create a trust system for hosting certain games.

    Example: Let's say a server owner owns a minecraft server, and the server owner whitelists people to join.
    The server owner wishes to only have trusted folks join their server, and possibly have them announce their own servers as well.
    In this case, the server owner adds the UltimateLobbyAnnouncer bot. 
    This bot only grants the lobby announcing command when the user has sent many messages, proving
    to be a trustworthy person. Once they reach level 6, which is at exp lvl 50,000. Every message sent grants the user 100 exp. So in theory, it will take
    500 messages to become a trustworthy individual.
    This can create a heightened level of trust for server owners, who can feel at ease knowing that the people they add as a host for their server, or game 
    lobby/whitelisted member can be a trusted individual.
    """
    userandExp = {
        
    }
    level1Exp = 5000
    level2Exp = 10000
    level3Exp = 20000
    level4Exp = 30000
    level5Exp = 50000

    
    def __init__ (self, bot):
        """
        The initialization function for the LevelingSystem class.
        In this intialization function, the exdict.pkl is automatically loaded to load the exp system from storage.
        If it isn't in storage, it initializes the userandExp dictionary.

        Args:
            bot (Bot): The Bot object for the discord bot
        """
        
        
        self.bot = bot
        if "exdict.pkl" in os.listdir("./"):
            with open("./exdict.pkl", "rb") as f:
                self.userandExp = pickle.load(f)
        elif "exdict.pkl" not in os.listdir("./"):
            for member in bot.get_all_members():
                self.userandExp[member.name] = 0
        self.saveExp.start()
    
    @commands.command()
    async def manualexpsave(self, ctx):
        await ctx.send("Saving exp dictionary!")
        with open("./exdict.pkl", "+wb") as f:
            pickle.dump(self.userandExp, f)
    
    # Automatically save the exp dictionary at 8:30 AM every day.    
    @tasks.loop(time=time)
    async def saveExp(self):
        with open("./exdict.pkl", "+wb") as f:
            pickle.dump(self.userandExp, f)
    
    @commands.command()
    async def checkexp(self, ctx):
        
        if ctx.author.name in self.userandExp:
            embed = discord.Embed(color=discord.colour.Color.blurple(), title="Experience Points Check")
            embed.add_field(name="Member:", value=f"{ctx.author.name}")
            embed.add_field(name="Experience Points:", value=f"{self.userandExp[ctx.author.name]}")
            await ctx.send(ctx.author.mention, embed=embed)
        elif ctx.author not in self.userandExp:
            await ctx.send("user isn't in exp system, adding now...")
            self.userandExp[ctx.author.name] = 0
    
    @commands.command()
    async def refreshlevels(self, ctx):
        """
        This method should be used each time a new guild adds the bot. This automatically refreshes the levels, allowing the server to have the same values
        as the previous one if the member already was in the exp system.
        """
        await ctx.send("Refreshing levels back to their previous levels...")
        author = ctx.author
        if author.name in self.userandExp:
            if self.userandExp[ctx.author.name] < self.level1Exp:
                await author.add_roles(discord.Object(discord.utils.get(author.guild.roles, name="Level 1").id))
            elif self.userandExp[ctx.author.name] == self.level2Exp:
                await author.add_roles(discord.Object(discord.utils.get(author.guild.roles, name="Level 2").id))
            elif self.userandExp[ctx.author.name] == self.level2Exp:
                await author.add_roles(discord.Object(discord.utils.get(author.guild.roles, name="Level 3").id))
            elif self.userandExp[ctx.author.name] == self.level3Exp:
                await author.add_roles(discord.Object(discord.utils.get(author.guild.roles, name="Level 4").id))
            elif self.userandExp[ctx.author.name] == self.level4Exp:
                await author.add_roles(discord.Object(discord.utils.get(author.guild.roles, name="Level 5").id))
            elif self.userandExp[ctx.author.name] > self.level5Exp:
                await author.add_roles(discord.Object(discord.utils.get(author.guild.roles, name="Hosts").id))
    
    @commands.Cog.listener()
    async def on_member_join(self, member):
        await member.send("Checking if you have previous levels from another server which has the UltimateLobbyAnnouncer Bot!")
        if author.name in self.userandExp:
            if self.userandExp[ctx.author.name] < self.level1Exp:
                await author.add_roles(discord.Object(discord.utils.get(author.guild.roles, name="Level 1").id))
            elif self.userandExp[ctx.author.name] == self.level2Exp:
                await author.add_roles(discord.Object(discord.utils.get(author.guild.roles, name="Level 2").id))
            elif self.userandExp[ctx.author.name] == self.level2Exp:
                await author.add_roles(discord.Object(discord.utils.get(author.guild.roles, name="Level 3").id))
            elif self.userandExp[ctx.author.name] == self.level3Exp:
                await author.add_roles(discord.Object(discord.utils.get(author.guild.roles, name="Level 4").id))
            elif self.userandExp[ctx.author.name] == self.level4Exp:
                await author.add_roles(discord.Object(discord.utils.get(author.guild.roles, name="Level 5").id))
            elif self.userandExp[ctx.author.name] > self.level5Exp:
                await author.add_roles(discord.Object(discord.utils.get(author.guild.roles, name="Hosts").id))
        elif author.name not in self.userandExp:
            await member.send("You are not in exp system! adding now...")
            self.userandExp[member.name] = 0

    @commands.Cog.listener()
    async def on_message(self, message):
        '''
        This on_message event makes it so that whenever a message is sent, it checks for a variety of variables
        to see if the user is at a particular exp level, in which case it levels up the member.
        '''
        
        author = message.author
        for user in self.userandExp:
            if author.name in user and self.bot.user.name != author.name:
                if self.userandExp[author.name] == self.level1Exp:
                    try:
                        await author.remove_roles(discord.Object(discord.utils.get(author.roles, name="Level 1").id))
                        await author.add_roles(discord.Object(discord.utils.get(author.guild.roles, name="Level 2").id))
                        await message.channel.send("You are now level 2!")
                    except Exception as e:
                        print(f"Error: {e}")
                elif self.userandExp[author.name] == self.level2Exp:
                    try:
                        await author.remove_roles(discord.Object(discord.utils.get(author.roles, name="Level 2").id))
                        await author.add_roles(discord.Object(discord.utils.get(author.guild.roles, name="Level 3").id))
                        await message.channel.send("You are now level 3!")
                    except Exception as e:
                        print(f"Error: {e}")
                elif self.userandExp[author.name] == self.level3Exp:
                    try:
                        await author.remove_roles(discord.Object(discord.utils.get(author.roles, name="Level 3").id))
                        await author.add_roles(discord.Object(discord.utils.get(author.guild.roles, name="Level 4").id))
                        await message.channel.send("You are now level 4!")
                    except Exception as e:
                        print(f"Error: {e}")
                elif self.userandExp[author.name] == self.level4Exp:
                    try:
                        await author.remove_roles(discord.Object(discord.utils.get(author.roles, name="Level 4").id))
                        await author.add_roles(discord.Object(discord.utils.get(author.guild.roles, name="Level 5").id))
                        await message.channel.send("You are now level 5!")
                    except Exception as e:
                        print(f"Error: {e}")
                elif self.userandExp[author.name] == self.level5Exp:
                    try:
                        await author.remove_roles(discord.Object(discord.utils.get(author.roles, name="Level 5").id))
                        await author.add_roles(discord.Object(discord.utils.get(author.guild.roles, name="Hosts").id))
                        await message.channel.send("You have now finally become a host! Feel free to announce your hosts using the newgame command!")
                    except Exception as e:
                        print(f"Error: {e}")
            elif author.name not in user and self.bot.user.name != author.name:
                await message.channel.send("user isn't in the exp system! Adding now...")
                self.userandExp[author.name] = 0         
    
            # Adding 100 exp to user, will change later, very easy to level up for testing purposes!
            
            self.userandExp[author.name]+=100
        
        
    
