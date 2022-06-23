import os

try:
    if "DISCORD_TOKEN" in os.environ:
        raise ImportError
    import config
    DT = config.DISCORD_TOKEN
except ImportError:
    DT = os.getenv("DISCORD_TOKEN")

import src.csvparser

if __name__ == "__main__":
    src.main(DT, src.csvparser.CsvParser("Losungen.csv"))
