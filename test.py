from TransactionWatchdog import update_venmo_ledger
from os import getenv

csv_file = 'venmo_statements/other.csv'
ledger_key = getenv('sooza_ledger_key')
sheet_name = getenv('sooza_venmo_name')


update_venmo_ledger(csv_file, ledger_key, sheet_name)