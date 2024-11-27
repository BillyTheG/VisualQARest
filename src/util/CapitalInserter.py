import csv


class CapitalInserter:

    def __init__(self, global_cursor):
        self.global_cursor = global_cursor

    def insert_value_into_db(self, row):
        if row is not None:
            result = self.global_cursor.execute('INSERT INTO [dbo].[CustomEntity] (Name,Land,Long, Lat) VALUES(?,?,?,?);',
                                                [row[1], row[0],
                                                 row[3], row[2]])
            print(result.commit())

    def init_capitals(self):
        try:
            with open('../../../Resources/country-list.csv', newline='') as csvfile:
                spam_reader = csv.reader(csvfile, delimiter=',')
                for row in spam_reader:
                    self.insert_value_into_db(row)
        except Exception as e:
            print('Failed to load csv: ' + str(e))
            return False

