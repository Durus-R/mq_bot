import config
import src.csvparser

if __name__ == "__main__":
    src.main(config.Discord_Token, src.csvparser.CsvParser("Losungen.csv"))
