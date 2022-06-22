try:
    import config
except ImportError:
    import secret.config as config
import src.csvparser

if __name__ == "__main__":
    src.main(config.Discord_Token, src.csvparser.CsvParser("Losungen.csv"))
