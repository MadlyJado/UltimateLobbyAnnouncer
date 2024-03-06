import discord
import os
import pickle
from discord.ext import commands, tasks
import datetime

utc = datetime.timezone.utc

time = datetime.time(hour=8, minute=30, tzinfo=utc)


class LevelingSystem(commands.Cog):
    userandExp = {
        
    }
    
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
            if self.userandExp[ctx.author.name] < 200:
                await author.add_roles(discord.Object(discord.utils.get(author.guild.roles, name="Level 1").id))
            elif self.userandExp[ctx.author.name] == 200:
                await author.add_roles(discord.Object(discord.utils.get(author.guild.roles, name="Level 2").id))
            elif self.userandExp[ctx.author.name] == 300:
                await author.add_roles(discord.Object(discord.utils.get(author.guild.roles, name="Level 3").id))
            elif self.userandExp[ctx.author.name] == 400:
                await author.add_roles(discord.Object(discord.utils.get(author.guild.roles, name="Level 4").id))
            elif self.userandExp[ctx.author.name] == 500:
                await author.add_roles(discord.Object(discord.utils.get(author.guild.roles, name="Level 5").id))
            elif self.userandExp[ctx.author.name] > 600:
                await author.add_roles(discord.Object(discord.utils.get(author.guild.roles, name="Hosts").id))
        
    @commands.Cog.listener()
    async def on_message(self, message):
        '''
        This on_message event makes it so that whenever a message is sent, it checks for a variety of variables
        to see if the user is at a particular exp level, in which case it levels up the member.
        '''
        
        author = message.author
        for user in self.userandExp:
            if author.name in user and self.bot.user.name != author.name:
                if self.userandExp[author.name] == 5000:
                    try:
                        await author.remove_roles(discord.Object(discord.utils.get(author.roles, name="Level 1").id))
                        await author.add_roles(discord.Object(discord.utils.get(author.guild.roles, name="Level 2").id))
                        await message.channel.send("You are now level 2!")
                    except Exception as e:
                        print(f"Error: {e}")
                elif self.userandExp[author.name] == 10000:
                    try:
                        await author.remove_roles(discord.Object(discord.utils.get(author.roles, name="Level 2").id))
                        await author.add_roles(discord.Object(discord.utils.get(author.guild.roles, name="Level 3").id))
                        await message.channel.send("You are now level 3!")
                    except Exception as e:
                        print(f"Error: {e}")
                elif self.userandExp[author.name] == 20000:
                    try:
                        await author.remove_roles(discord.Object(discord.utils.get(author.roles, name="Level 3").id))
                        await author.add_roles(discord.Object(discord.utils.get(author.guild.roles, name="Level 4").id))
                        await message.channel.send("You are now level 4!")
                    except Exception as e:
                        print(f"Error: {e}")
                elif self.userandExp[author.name] == 30000:
                    try:
                        await author.remove_roles(discord.Object(discord.utils.get(author.roles, name="Level 4").id))
                        await author.add_roles(discord.Object(discord.utils.get(author.guild.roles, name="Level 5").id))
                        await message.channel.send("You are now level 5!")
                    except Exception as e:
                        print(f"Error: {e}")
                elif self.userandExp[author.name] == 50000:
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
        
        
    