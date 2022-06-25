import os
import src.csvparser
from src import db

DT = None
try:
    if "DISCORD_TOKEN" in os.environ:
        raise ImportError
    import config

    DT = config.DISCORD_TOKEN
except ImportError:
    try:
        config = None
        if "DISCORD_TOKEN" not in os.environ:
            raise OSError
        DT = os.getenv("DISCORD_TOKEN")
    except OSError:
        print("Keine Konfiguration gefunden.")
        print("Gehen sie zu https://github.com/mainquestministries/mq_bot/wiki/How-to-run#create-a-configpy "
              "und wiederholen sie die dort genannten Schritte.")

        exit(1)

db_session = db.create_sqlite_engine()

if __name__ == "__main__":
    src.main(DT, db_session, src.csvparser.CsvParser("Losungen.csv"))
