import os
from discord.ext import commands
from csvparser import CsvParser, DateNotFoundError


def get_token():
    """
    Returns the token of the bot.
    """
    return open('token.txt', 'r').read()


# Main cog
class Losungen(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="altes")
    async def altes_testament(self, ctx):
        """
        Returns the word of the day from the Altes Testament.
        """
        csv_parser = CsvParser("Losungen.csv")
        try:
            word_of_day = csv_parser()
        except DateNotFoundError:
            await ctx.send("Dieser Tag ist nicht in der Liste.")
            return
        await ctx.send(word_of_day.at_v + ": " + word_of_day.at)

    @commands.command(name="neues")
    async def neues_testament(self, ctx):
        """
        Returns the word of the day from the Altes Testament.
        """
        csv_parser = CsvParser("Losungen.csv")
        try:
            word_of_day = csv_parser()
        except DateNotFoundError:
            await ctx.send("Dieser Tag ist nicht in der Liste.")
            return
        await ctx.send(word_of_day.nt_v + ": " + word_of_day.nt)


# Create a discord bot with discord.ext
Bot = commands.Bot(command_prefix='!')
Bot.add_cog(Losungen(Bot))

# Check whether the file "token.txt" exists
if not os.path.isfile("token.txt"):
    print("Token datei nicht gefunden. Platzieren sie die Datei in der gleichen Ebene wie dieses Script.")
    print("ABBRUCH")
    exit()

# Check whether the file "token.txt" is empty
if not os.path.getsize("token.txt"):
    print("Token datei ist leer. Bitte fügen Sie einen Token ein.")
    print("ABBRUCH")
    exit()

# Check whether the file "Losungen.csv" exists
if not os.path.isfile("Losungen.csv"):
    print("Losungen.csv nicht gefunden. Platzieren sie die Datei in der gleichen Ebene wie dieses Script.")
    print("Bitte laden sie die korrekte Datei hier herunter: https://www.losungen.de/digital/")
    print("ABBRUCH")
    exit()

# Check whether the file "Losungen.csv" is empty
if not os.path.getsize("Losungen.csv"):
    print("Losungen.csv ist leer. Bitte laden sie die korrekte Datei hier herunter: https://www.losungen.de/digital/")
    print("ABBRUCH")
    exit()


# Run the bot
@Bot.event
async def on_ready():
    print("Bot ist bereit.")

if __name__ == '__main__':
    Bot.run(get_token())

