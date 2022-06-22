import os

try:
    import config
    DT = config.DISCORD_TOKEN
except ImportError:
    DT = os.getenv("DISCORD_TOKEN")

import src.csvparser

if __name__ == "__main__":
    src.main(DT, src.csvparser.CsvParser("Losungen.csv"))
