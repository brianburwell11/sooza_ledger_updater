import gspread
from oauth2client.service_account import ServiceAccountCredentials
from os import getenv

from Transaction import Transaction

# client_id = getenv('sooza_client_id')
# client_secret = getenv('sooza_client_secret')

scope = ['https://spreadsheets.google.com/feeds',
         'https://www.googleapis.com/auth/drive']
creds = ServiceAccountCredentials.from_json_keyfile_name('client_secret.json', scope)
client = gspread.authorize(creds)

class GoogleSheetEditor():
    def __init__(self, sheets_key, sheet_name):
        self.sheet = client.open_by_key(sheets_key).worksheet(sheet_name)

    def get_transaction_ids(self):
        return self.sheet.col_values(2)[1:]

    def find_first_empty_row(self):
        for row_num,entry in enumerate( self.sheet.get_all_values() ):
            if not entry[0]:
                return row_num + 1

    def add_transaction(self, row_num, transaction):
        '''
        Date, ID, Note, Debit, To, Credit, From
        '''
        self.sheet.update_cell(row_num, 1, transaction.date)
        self.sheet.update_cell(row_num, 2, transaction.id)
        self.sheet.update_cell(row_num, 3, transaction.note)
        
        if transaction.credit:
            self.sheet.update_cell(row_num, 6, transaction.amount)
            self.sheet.update_cell(row_num, 7, transaction.to_from)
        else:
            self.sheet.update_cell(row_num, 4, transaction.amount)
            self.sheet.update_cell(row_num, 5, transaction.to_from)

        print(f'Added transaction with ID {transaction.id} to ledger')
        print(f'\t{transaction}')

    def update_ledger(self, list_of_transactions_to_add):
        for transaction in list_of_transactions_to_add:
            self.add_transaction( self.find_first_empty_row(), transaction )



# ledger_key  = "1A3m50Z7fiz2zurrdYOZ2qAbMpp2ak3YgT0Um1254W5k"
# venmo_name  = "Venmo Transactions"
# square_name = "Square Transactions"


# g = GoogleSheetEditor(ledger_key, venmo_name)
# print( g.get_transaction_ids() )