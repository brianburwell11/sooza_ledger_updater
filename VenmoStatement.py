from csv import DictReader
from datetime import datetime

from Transaction import Transaction

class VenmoStatement():
    def __init__(self, csv_file):
        self.file = csv_file
        self.data = self.read_file()
    
    def read_file(self):
        data = {}
        with open( self.file ) as f:
            reader = DictReader(f)

            for transaction in reader:
                if transaction["ID"]:
                    date = datetime.strptime( transaction["Datetime"], "%Y-%m-%dT%H:%M:%S")
                    date = date.strftime("%m/%d/%Y")
                    
                    transaction_id  = transaction["ID"]
                    amount          = transaction["Amount (total)"][2:]
                    note            = transaction["Note"]

                    if transaction["Amount (total)"][0] == '+':
                        credit  = True
                        to_from = transaction["From"]
                    else:
                        credit = False
                        to_from = transaction["To"]

                    data[transaction_id] = Transaction(date,transaction_id,credit,amount,to_from,note)

        return data

    def find_new_transactions(self, list_of_other_transaction_ids):
        return [self.data[transaction_id] for transaction_id in self.data.keys() if transaction_id not in list_of_other_transaction_ids]



# a = VenmoStatement('venmo_statements/SAMPLE_venmo_statement.csv')
# b = VenmoStatement('venmo_statements/other.csv')

