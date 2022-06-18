import csv
import datetime
from word_of_day import WordOfDay


class DateNotFoundError(Exception):
    pass


class CsvParser:
    """
    Parse a CSV file. The file must be a CSV file with a header row.
    The values are splitted by tabs.
    """

    def __init__(self, file_name):
        self.file_name = file_name
        self.csv_file = open(file_name, 'r')
        self.csv_reader = csv.reader(self.csv_file, delimiter='\t')
        self.csv_list = list(self.csv_reader)
        self.csv_file.close()

    def get_csv_list(self):
        return self.csv_list

    def get_csv_row(self, row_number):
        return self.csv_list[row_number]

    def get_csv_column(self, column_number):
        return [row[column_number] for row in self.csv_list]

    def get_date(self):
        """
        Returns the current date as a string.
        """
        return datetime.datetime.now().strftime("%d.%m.%Y")

    def get_line_of_today(self):
        """
        Returns the line of the CSV file for the current date.
        """
        today = self.get_date()
        for i in range(len(self.csv_list)):
            if today in self.csv_list[i]:
                return i

    def is_today_in_lines(self):
        """
        Returns True if the current date is in the CSV file.
        """
        today = self.get_date()
        for i in range(len(self.csv_list)):
            if today in self.csv_list[i]:
                return True
        return False

    def __call__(self) -> WordOfDay:
        if not self.is_today_in_lines():
            raise DateNotFoundError
        line = self.get_csv_row(self.get_line_of_today())
        return WordOfDay(line[3], line[4], line[5], line[6], line[0], line[1])
