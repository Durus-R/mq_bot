import os

try:
    if "DISCORD_TOKEN" in os.environ:
        raise ImportError
    import config
    DT = config.DISCORD_TOKEN
except ImportError:
    config = None
    DT = os.getenv("DISCORD_TOKEN")
except ModuleNotFoundError:
    print("Keine Konfiguration gefunden.")
    print("Gehen sie zu https://github.com/mainquestministries/mq_bot/wiki/How-to-run#create-a-configpy "
          "um wiederholen sie die dort genannten Schritte.")

import src.csvparser

if __name__ == "__main__":
    src.main(DT, src.csvparser.CsvParser("Losungen.csv"))
