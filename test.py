from TransactionWatchdog import Watchdog
from os import getenv

ledger_key = getenv('sooza_ledger_key')
sheet_name = getenv('sooza_venmo_name')

w = Watchdog()
w.wait_for_new_file()