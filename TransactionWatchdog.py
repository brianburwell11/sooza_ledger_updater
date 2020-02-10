from datetime import datetime
from os import getenv, rename
from os.path import splitext
# from selenium import webdriver
# from selenium.webdriver.common.keys import Keys
# from selenium.webdriver.common.action_chains import ActionChains as action
from time import sleep
from watchdog.events import FileSystemEventHandler
from watchdog.observers import Observer

from VenmoStatement import VenmoStatement
from GoogleSheetsEditor import GoogleSheetEditor

path_to_chrome_driver = '/Users/brianburwell/Desktop/Personal/Python_Playground/selenium/drivers/chromedriver'
venmo_username = getenv('sooza_venmo_username')
venmo_password = getenv('sooza_venmo_password')

ledger_key = getenv('sooza_ledger_key')
sheet_name = getenv('sooza_venmo_name')

class Watchdog():
    def __init__(self):
        self.w = FileSystemEventHandler()
        self.w.on_created = lambda new_file: self.__rename_file_and_update_ledger(new_file.src_path)

        self.o = Observer()
        self.o.schedule(self.w, './venmo_statements')

    def wait_for_new_file(self):
        self.o.start()
        while True:
            sleep(1)
    
    def __rename_file_and_update_ledger(self, full_filename):
        new_filename = self.__add_current_date_to_filename(full_filename)
        self.__update_venmo_ledger(new_filename, ledger_key, sheet_name)


    def __add_current_date_to_filename(self, full_filename):
        filename, extension = splitext(full_filename)

        todays_date = datetime.now()
        todays_date = todays_date.strftime('%Y%m%d')

        new_filename = f'{filename}-{todays_date}{extension}'
        
        rename(full_filename, new_filename)
        return new_filename

    def __update_venmo_ledger(self, csv_file, sheets_key, sheet_name):
        v = VenmoStatement(csv_file)
        g = GoogleSheetEditor(sheets_key, sheet_name)

        transactions_to_add = v.find_new_transactions( g.get_transaction_ids() )
        g.update_ledger(transactions_to_add)

    # def get_current_venmo_statement(self):
    #     driver = webdriver.Chrome(path_to_chrome_driver)

    #     driver.get('https://venmo.com/account/sign-in')

    #     username_input = driver.find_element_by_name('phoneEmailUsername')
    #     password_input = driver.find_element_by_name('password')
    #     sign_in_btn    = driver.find_element_by_class_name('auth-button')

    #     username_input.send_keys(venmo_username)
    #     password_input.send_keys(venmo_password)
    #     sign_in_btn.click()
        
    #     send_code_btn = driver.find_element_by_tag_name('button')
    #     send_code_btn.click()

    #     validation_code = input('Enter the validation code: ')

    #     # validation_code_input = driver.find_elemetn