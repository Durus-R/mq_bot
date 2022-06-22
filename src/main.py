import contextlib
import os
import importlib
from discord.ext import commands
from csvparser import CsvParser, DateNotFoundError


# Check whether the file "token.txt" exists
def check_token():
    if not os.path.isfile("../token.txt"):
        print("Token datei nicht gefunden. Platzieren sie die Datei in der gleichen Ebene wie dieses Script.")
        print("ABBRUCH")
        exit()

    # Check whether the file "token.txt" is empty
    if not os.path.getsize("../token.txt"):
        print("Token datei ist leer. Bitte fügen Sie einen Token ein.")
        print("ABBRUCH")
        exit()


def get_token():
    """
    Returns the token of the bot.
    """
    with contextlib.suppress(ImportError):
        from config import Discord_Token
        config = importlib.import_module("..config")
        return config.Discord_Token
    if os.path.isfile("/SECRET/token.txt"):
        return open('/SECRET/token.txt', 'r').read()
    check_token()
    return open('../token.txt', 'r').read()


# Main cog
class Losungen(commands.Cog):
    def __init__(self, bot, parser):
        self.bot = bot
        self.parser = parser

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

    @commands.command()
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


# Create a discord bot with discord.ext
def main(token, parser):
    # Check whether the file "Losungen.csv" exists
    bot_ = commands.Bot(command_prefix='!')
    bot_.add_cog(Losungen(bot_, parser))

    @bot_.event
    async def on_ready():
        print("Bot ist bereit.")

    # Run the bot
    bot_.run(token)
