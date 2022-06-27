import contextlib
import datetime

from discord.ext import commands, tasks
from sqlalchemy.orm import Session

from .db import *

from .csvparser import CsvParser, DateNotFoundError


# Main cog
class Losungen(commands.Cog):
    def __init__(self, bot, parser, engine):
        self.bot = bot
        self.parser = parser
        self.eng = engine
        self.losung_loop.start()
        self.losung_loop2.start()

    @commands.command()
    async def info(self, ctx):
        """
        Zeigt Informationen über den Bot an.
        """
        await ctx.send(f'{self.bot.user.mention} ist ein Bot, der die Losungen einliest und sie hier schicken kann'
                       f'. \nMehr Info auf der Github-Seite: https://github.com/mainquestministries/mq_bot'
                       "\n Mit freundlicher Genehmigung der Herrnhuter Brüdergemeinde, siehe "
                       "https://www.losungen.de/fileadmin/media-losungen/download/NUTZUNGSBEDINGUNGEN_November_2021.pdf"
                       )

    @commands.command(aliases=["contrib", "github"])
    async def contribute(self, ctx):
        """
        Zeigt den Link zur GitHub-Seite.
        """
        await ctx.send("https://github.com/mainquestministries/mq_bot")

    @commands.command(name="altes")
    async def altes_testament(self, ctx):
        """
        Sendet den heutigen Losungstext.
        """
        csv_parser = self.parser
        try:
            word_of_day = csv_parser()
        except DateNotFoundError:
            await ctx.send("Dieser Tag ist nicht in der Liste. Bitte eröffnen sie ein Ticket auf GitHub.")
            return
        await ctx.send(word_of_day.at_v + ": " + word_of_day.at)

    @commands.command(name="neues")
    async def neues_testament(self, ctx):
        """
        Sendet den heutigen Lehrtext.
        """
        csv_parser = self.parser
        try:
            word_of_day = csv_parser()
        except DateNotFoundError:
            await ctx.send("Dieser Tag ist nicht in der Liste. Bitte eröffnen sie ein Ticket auf GitHub.")
            return
        await ctx.send(word_of_day.nt_v + ": " + word_of_day.nt)

    @commands.command(name="losung")
    async def losung(self, ctx):
        """
        Sendet die heutige Losung.
        """
        csv_parser = self.parser
        try:
            word_of_day = csv_parser()
        except DateNotFoundError:
            await ctx.send("Dieser Tag ist nicht in der Liste. Bitte eröffnen sie ein Ticket auf GitHub.")
            return
        await ctx.send("Losungstext: " + word_of_day.at_v + ": " + word_of_day.at + "\n" +
                       "Lehrtext: " + word_of_day.nt_v + ": " + word_of_day.nt)

    @tasks.loop(minutes=1)
    async def losung_loop(self):
        if self.bot.is_ready():
            delmsg = 0
            print("Time again...")
            with Session(self.eng) as session:

                for i in session.query(Guild).all():
                    if i.autodel_timeout > 0 and self.bot.get_channel(i.autodel_channel):
                        print("Time for Autodeleting something...")
                        async for message in self.bot.get_channel(i.autodel_channel). \
                                history():
                            if (datetime.datetime.now() - message.created_at).seconds / 3600 > i.autodel_timeout:
                                await message.delete()
                                delmsg += 1
                        print("Deleted {} messages.".format(delmsg))
                    else:
                        print("No History")

    @tasks.loop(hours=1)
    async def losung_loop2(self):
        if self.bot.is_ready():
            print("Time again...")
            with Session(self.eng) as sess:

                for i in sess.query(Guild).all():
                    if i.losung_channel == 0:
                        continue
                    if datetime.datetime.now().hour == i.losung_hour:
                        with contextlib.suppress(DateNotFoundError):
                            word_of_day = self.parser()
                            await self.bot.get_channel(i.losung_channel).send("Losungstext: " + word_of_day.at_v +
                                                                              ": " + word_of_day.at + "\n" +
                                                                              "Lehrtext: " + word_of_day.nt_v + ": "
                                                                              + word_of_day.nt)

    @losung_loop.before_loop
    @losung_loop2.before_loop
    async def before_losung_loop(self):
        await self.bot.wait_until_ready()

    @losung_loop.after_loop
    @losung_loop2.after_loop
    async def after_losung_loop(self):
        await self.bot.wait_until_ready()


class Admin(commands.Cog):
    def __init__(self, bot, engine):
        self.bot = bot
        self.eng = engine

    @commands.command()
    @commands.has_permissions(administrator=True)  # Intern only - Fails if already in database
    async def regen_db(self, ctx, hour):
        with Session(self.eng) as session:
            session.add_all([Guild(name=ctx.guild.name, id=ctx.guild.id, prefix="!", losung_channel=ctx.channel.id,
                                   losung_hour=hour, autodel_channel=0, autodel_timeout=0)])
            session.commit()

    @commands.command()
    async def show_servers(self, ctx):
        with Session(self.eng) as session:
            for guild in session.query(Guild).all():
                await ctx.send(f"{guild.name}")

    @commands.command(pass_context=True)
    @commands.has_permissions(administrator=True)  # ensure that only administrators can use this command
    async def changeprefix(self, ctx, prefix):
        with Session(self.eng) as session:
            guild = session.query(Guild).filter(Guild.id == ctx.guild.id).first()
            guild.prefix = prefix
            session.commit()
        await ctx.send(f"Prefix changed to {prefix}")

    @commands.command(pass_context=True)
    @commands.has_permissions(administrator=True)  # ensure that only administrators can use this command
    async def changehour(self, ctx, hour):
        with Session(self.eng) as session:
            guild = session.query(Guild).filter(Guild.id == ctx.guild.id).first()
            guild.losung_hour = hour
            session.commit()
        await ctx.send(f"Hour changed to {hour}")

    @commands.command(pass_context=True)
    @commands.has_permissions(administrator=True)  # ensure that only administrators can use this command
    async def changeautodel(self, ctx, hour):
        with Session(self.eng) as session:
            guild = session.query(Guild).filter(Guild.id == ctx.guild.id).first()
            guild.autodel_timeout = hour
            guild.autodel_channel = ctx.channel.id
            session.commit()
        await ctx.send(f"Autodeleting after {hour} hours.")


# Create a discord bot with discord.ext
def main(token, engine, parser):
    def get_prefix(client, message):
        try:
            with Session(engine) as session:
                return session.query(Guild).filter(Guild.id == message.guild.id).first().prefix
        except AttributeError:
            return "!"

    # Check whether the file "Losungen.csv" exists
    bot_ = commands.Bot(command_prefix=get_prefix)
    l_cog = Losungen(bot_, parser, engine)
    a_cog = Admin(bot_, engine)
    bot_.add_cog(l_cog)
    bot_.add_cog(a_cog)

    @bot_.event
    async def on_message(message):
        if not message.author.bot:
            if message.content.isupper():
                await message.channel.send("https://c.tenor.com/2wHYojwhV_EAAAAC/keep-calm-cat.gif")
            await bot_.process_commands(message)

    @bot_.event
    async def on_ready():
        print("Bot ist bereit.")

    @bot_.event
    async def on_guild_join(guild):  # when the bot joins the guild
        with Session(engine) as session:
            session.add_all(Guild(name=guild.name, id=guild.id, prefix="!"))

    @bot_.event
    async def on_guild_remove(guild):  # when the bot is removed from the guild
        with Session(engine) as session:
            Session.query(Guild).filter(Guild.id == guild.id).delete()

    # Run the bot
    bot_.run(token)
