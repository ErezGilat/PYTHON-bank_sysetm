# @author Erez Gilat
import random as random
import numpy as np
import re
import pandas as pd
from currency_converter import CurrencyConverter
from datetime import datetime
import os

# Creating an instants of Currency converter object
c = CurrencyConverter()

# All the needed regex patterns for the project
regex_name_pattern = '[A-Za-z]{2,25}( [A-Za-z]{2,25})?'
regex_email_pattern = "(^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$)"
regex_postal_code = "^(([0-9]{5})|([0-9]{7}))(?:-[0-9]{4})?$"
regex_israel_phone_number = "^0?(([23489]{1}\d{7})|[5]{1}\d{8})$"


# This function check's whether the ID number that was giving as an argument is a valid Israeli ID number.
def is_valid_israeli_id(id_num):
    if not id_num.isnumeric():
        return False
    id_num = int(id_num)
    if len(str(id_num)) > 9:
        return False
    array_to_check = np.array([1, 2, 1, 2, 1, 2, 1, 2, 1])
    id_array = np.array([0, 0, 0, 0, 0, 0, 0, 0, 0])
    for i in range(8, 9 - len(str(id_num)) - 1, -1):
        id_array[i] = id_num % 10
        id_num = int(id_num / 10)
    array_to_check = array_to_check * id_array
    for i in range(len(array_to_check)):
        if array_to_check[i] > 9:
            array_to_check[i] = array_to_check[i] % 10 + int(array_to_check[i] / 10) % 10
    if array_to_check.sum() % 10 == 0:
        return True
    else:
        return False


# The following function set's up different id if an invalid id number was entered.
# It iterates only 3 times, if after 3 times the user still
# did not enter a valid id it stops and returns.
def set_id_after_error():
    tries = 3
    id_num = input(
        f"You have entered a wrong Israeli id number, please try again or 0 to exit(you have {tries} "
        f"more tries to go)\n")
    while not (is_valid_israeli_id(id_num) or tries == 1):
        if id_num == 0:
            return 0
        tries -= 1
        id_num = input(f"Enter id number, you have {tries} more tries to go\n")
    if tries == 1 and not (is_valid_israeli_id(id_num)):
        return 0
    return id_num


# Whenever there is a problem in the program that is about invalid string(names,email,etc...)The following function
# comes in and run until the user enters a valid input.
# If after 3 time the user still hasn't entered any valid value the function stops and return 0.
# This function gets a first name, last name and an israeli id and make sure that they are valid.The function creates
# a Person object if everything is alright.
# the function also gives the user an option to change the data if something is incorrect.
# The function gets a regex pattern (string) and str (string) that holds the name of the wrong input
# ("family name","address line",etc...)
def set_str_after_regex_error(pattern, str1):
    tries = 3
    valid_input = input(
        f"You have entered an invalid {str1},\nplease try again or 0 to exit (you have {tries} more tries to go):\n")
    while not (re.fullmatch(pattern, valid_input) or tries == 1):
        if valid_input == '0':
            return '0'
        tries -= 1
        valid_input = input(f"Enter {str1}, you have {tries} more tries to go\n")
    if tries == 1 and not re.fullmatch(pattern, valid_input):
        return '0'
    return valid_input


# In order to make an account you first need to have an instant of the object
# Account, these instants holds the information of the account owner.
# In order to make persons you need to make sure that the first and last name are
# valid and also check if the id is valid by the israeli law of id numbers
def person_creating_validation(first_name, last_name, person_id):
    if not is_valid_israeli_id(person_id):
        person_id = set_id_after_error()
        if person_id == 0:
            return None
    if not (re.fullmatch(regex_name_pattern, first_name)):
        first_name = set_str_after_regex_error(regex_name_pattern, "First Name")
        if first_name == '0':
            return None
    if not (re.fullmatch(regex_name_pattern, last_name)):
        last_name = set_str_after_regex_error(regex_name_pattern, "Last Name")
        if last_name == '0':
            return None
    return Person(first_name, last_name, person_id)


# This function gets address line, city and zip code and returns if they represent a valid address.
# I was able only to validate the zip code with regex, but I didn't find out how to do that.
def address_creation_validation(address_line1, city, zipcode):

    if not (re.fullmatch(regex_postal_code, zipcode)):
        zipcode = set_str_after_regex_error(regex_postal_code, "zip code")
        if zipcode == '0':
            return None
    return Address(address_line1, city, zipcode)


# The following function creates an account with users input info.
# The function also validate the information and let the user change details if something went wrong.
# This function returns an instats of the object Account and a password of the accounts' data.
# If it failed to create account it returns None
def account_creation_validation():
    print("Wellcome!, thank you for choosing our bank")
    first_name = input("Please enter your first name: ")
    last_name = input("Please enter your last name: ")
    person_id = input("Please enter your id number: ")
    person = person_creating_validation(first_name, last_name, person_id)
    if person is None:
        return None
    print("Okay, everything seems alright")
    print("Now lets set up the address")
    address_line1 = input("Please enter the address line(Street and ect. exclude city): ")
    city = input("Please enter the city: ")
    zipcode = input("Please enter zip code: ")
    address = address_creation_validation(address_line1, city, zipcode)
    if address is None:
        return None
    print("Good! The address was entered successfully")
    phone_number = input("Please enter your main phone number: ")
    if not (re.fullmatch(regex_israel_phone_number, phone_number)):
        phone_number = set_str_after_regex_error(regex_israel_phone_number, "phone number")
    if phone_number == '0':
        return None
    email = input("Enter your email please: ")
    if not (re.fullmatch(regex_email_pattern, email)):
        email = set_str_after_regex_error(regex_email_pattern, "email")
    if email == '0':
        return None
    password = input("Please enter you desired password: ")
    tries = 3
    while password != input("Enter the password again to validate") and tries != 1:
        print("The password are not the same, please try again")
        tries -= 1
        password = input("Please enter you desired password, you have {tries} tries left: ")
    if tries == 1:
        print("You tried to many times")
        print("Failed to create account")
        person = None
        address = None
    return Account(person, address, email, phone_number), password


# This function is in charge of log in to the account, with email/account number and password.
# If the user logged in successfully it returns the account object, else it returns None.
def login(bank):
    acc_num = input("Please enter account number, if you don't remember it enter 1 and you will be "
                    "able to try with email")
    if acc_num != '1':
        password = input("Enter accounts password: ")
        if (bank.get_accounts_data()[bank.get_accounts_data().account_number == acc_num].password == password).any():
            print("You have logged in successfully")
            return bank.get_accounts_data()[bank.get_accounts_data().account_number == acc_num]['account'].values[0]
        else:
            email = input("Wrong account number or password, try to enter email address instead or get back to "
                          "menu by entering 0 ")
            password = input("Enter password ")
            if email == '0':
                print("Canceling")
                return None
            if (bank.get_accounts_data()[bank.get_accounts_data().email == email].password == password).any():
                print("You have logged in successfully")
                return bank.get_accounts_data()[bank.get_accounts_data().email == email]['account'].values[0]
    else:
        email = input("Enter email address: ")
        password = input("Enter password: ")
        if email == '0':
            print("Canceling")
            return None
        if (bank.get_accounts_data()[bank.get_accounts_data().email == email].password == password).any():
            print("You have logged in successfully")
            return bank.get_accounts_data()[bank.get_accounts_data().email == email]['account'].values[0]
    print("Account doesn't exist or wrong password")
    return None


# This is the Person class, an instant of this class is the base of every account.
# The following class holds the value of a human, first name, family name and the id of the person.0
class Person:
    def __init__(self, first_name, last_name, person_id):
        self.first_name = first_name
        self.last_name = last_name
        self.person_id = person_id

    # Returning the full name of the person
    def get_full_name(self):
        return f"{self.first_name} {self.last_name}"

    # Returning the first name of the person
    def get_first_name(self):
        return f"{self.first_name}"

    # Returning the last name of the person
    def get_last_name(self):
        return f"{self.last_name}"

    # The function gets the new first name and set the person name to be the new name.
    def set_first_name(self, first_name):
        self.first_name = first_name

    # The function gets the new last name and set the person name to be the new last name.
    def set_last_name(self, last_name):
        self.last_name = last_name


# This class holds all the information of a physical address, address line, city and zip code.
# all the addresses of the account in the bank are in Israel.
class Address:
    def __init__(self, address_line1, city, zip_code):
        self.address_line1 = address_line1
        self.city = city
        self.zip_code = zip_code

    # This function lets the user change his/her address.
    def edit_address(self):
        new_add_line = input("Enter new address line")
        new_city = input("Enter new city")
        new_zip = input("Enter new zip code")
        new_address = address_creation_validation(new_add_line, new_city, new_zip)
        if new_address is None:
            print("address hasn't been change")
            return
        self.address_line1 = new_address.get_address_line()
        self.city = new_address.get_city()
        self.zip_code = new_address.get_zip
        print("Address was changed successfully")

    # This function returns the address line of the address instant.
    def get_address_line(self):
        return self.address_line1

    # The following function returns the city.
    def get_city(self):
        return self.city

    # This function returns the zip code.
    def get_zip(self):
        return self.zip_code

    # The following function returns the full address.
    def full_address(self):
        return f"{self.address_line1}, {self.city}, Israel, {self.zip_code}"


# This is the Account class, an instants of this account holds all the values that are related to a bank account,
# Such as balance, email, phone_number and ect. and it contains functions that help to manage the account.
class Account:
    acc_num_set_bool = False  # This boolean var helps create a single tone design pattern, when it's turn
    # into true, it means That the account number was already set, and you cannot set it again.

    # Constructor
    def __init__(self, person, address, email, phone_number):
        self.person = person
        self.address = address
        self.email = email
        self.phone_number = phone_number
        self.balance = 0
        self.transactions_history = pd.DataFrame(
            columns=['Time', 'type_of_transaction', 'how_much', 'currency', 'how_much_in_ils', 'money_before(ILS)',
                     'money_after(ILS)', 'Description'])
        self.account_num = -1  # We set the account number to be -1 at creation because only when we save the account
        # as a new account in the bank class we are able to know which account number the new account got.

    # This function returns the accounts email.
    def get_email(self):
        return self.email

    # This function returns the accounts balance.
    def get_balance(self):
        return self.balance

    # This function is in charge of making transactions of any kind with the account, Withdraw, deposit and transfer
    # money to others.
    def make_transaction(self):
        k = input("Transaction menu: \n"
                  "1 - To make a deposit\n"
                  "2 - To withdraw\n"
                  "3 - To transfer money\n"
                  "0 - Cancel")
        if k == '1':
            details = {}
            try:
                dep = float(input("How much money do you want to deposit? "))
            except ValueError:
                print("You didn't enter a number, returning to main menu")
                return
            currency = input('Choose one of the currencies, ILS,USD,EUR,GBP: ')
            if dep < 0:
                print("Deposing negative amount of money is not possible, returning to main menu")
                return
            if currency not in ['ILS', 'USD', 'EUR', 'GBP']:
                print('Currency error, returning to main menu')
                return
            details['Time'] = [datetime.now()]
            details['type_of_transaction'] = ['Deposit']
            details['how_much'] = [dep]
            details['currency'] = [currency]
            details['how_much_in_ils'] = [c.convert(dep, currency, 'ILS')]
            details['money_before(ILS)'] = [self.balance]
            self.balance += c.convert(dep, currency, 'ILS')
            details['money_after(ILS)'] = [self.balance]
            details['Description'] = [input('Enter description of transaction')]
            df = pd.DataFrame(details)
            self.transactions_history = pd.concat([self.transactions_history, df])
        if k == '2':
            details = {}
            try:
                wit = float(input("How much money do you want to withdraw? "))
            except ValueError:
                print("You didn't enter a number, returning to main menu")
                return
            currency = input('Choose one of the currencies, ILS,USD,EUR,GBP: ')
            if wit < 0:
                print("Withdraw negative amount of money is not possible, returning to main menu")
                return
            if currency not in ['ILS', 'USD', 'EUR', 'GBP']:
                print('Currency error, returning to main menu')
                return
            details['Time'] = [datetime.now()]
            details['type_of_transaction'] = ['Withdraw']
            details['how_much'] = [wit]
            details['currency'] = [currency]
            details['how_much_in_ils'] = [c.convert(wit, currency, 'ILS')]
            details['money_before(ILS)'] = [self.balance]
            self.balance -= c.convert(wit, currency, 'ILS')
            details['money_after(ILS)'] = [self.balance]
            if details['money_after(ILS)'][0] < 0:
                print("Not enough money in the account, couldn't complete transaction")
                return
            details['Description'] = [input('Enter description of transaction')]
            df = pd.DataFrame(details)
            self.transactions_history = pd.concat([self.transactions_history, df])
        if k == '3':
            details = {}
            try:
                snd = float(input("How much money do you want send? "))
            except ValueError:
                print("You didn't enter a number, returning to main menu")
                return
            currency = input('Choose one of the currencies, ILS,USD,EUR,GBP: ')
            if snd < 0:
                print("sending negative amount of money is not possible, returning to main menu")
                return
            if currency not in ['ILS', 'USD', 'EUR', 'GBP']:
                print('Currency error, returning to main menu')
                return
            details['Time'] = [datetime.now()]
            details['type_of_transaction'] = ['Send']
            details['how_much'] = [snd]
            details['currency'] = [currency]
            details['how_much_in_ils'] = [c.convert(snd, currency, 'ILS')]
            details['money_before(ILS)'] = [self.balance]
            self.balance -= c.convert(snd, currency, 'ILS')
            details['money_after(ILS)'] = [self.balance]
            if details['money_after(ILS)'][0] < 0:
                print("Not enough money in the account, couldn't complete transaction")
                return
            details['Description'] = [input('Enter description of transaction')]
            df = pd.DataFrame(details)
            self.transactions_history = pd.concat([self.transactions_history, df])
        if k == '0':
            print("The activity was canceled")
            return

    # This function returns the last transaction data, the transaction history is a data frame, so the function returns
    # The tail of it.
    def get_last_tr_history(self):
        return self.transactions_history.tail().to_string()

    # This functions returns the data frame of the account activity history.
    def get_df_of_trans(self):
        return self.transactions_history

    # This function changes the acc
    def set_acc_num(self, acc_num):
        if self.acc_num_set_bool:
            print("The account number was already set.")
            return
        self.account_num = acc_num

    # This function returns the account number.
    def get_acc_num(self):
        return self.account_num

    # This function gives basic stats about the accounts activities.
    def get_stats(self):
        print("Statistics:")
        print("Number of transactions: " + str(len(self.transactions_history.index)))
        print("Number of deposits: " +
              str(len(self.transactions_history[self.transactions_history['type_of_transaction'] == 'Deposit'])))
        print("Sum of Deposits(ILS): " + str(self.transactions_history[self.transactions_history['type_of_transaction']
                                                                       == 'Deposit']['how_much_in_ils'].sum()))
        print("Deposit mean(ILS): " + str(self.transactions_history[self.transactions_history['type_of_transaction']
                                                                    == 'Deposit']['how_much_in_ils'].mean()))
        print("Number of withdraws: " +
              str(len(self.transactions_history[self.transactions_history['type_of_transaction'] == 'Withdraw'])))
        print("Sum of withdraws(ILS): " + str(self.transactions_history[self.transactions_history['type_of_transaction']
                                                                        == 'Withdraw']['how_much_in_ils'].sum()))
        print("Withdraw mean(ILS): " + str(self.transactions_history[self.transactions_history['type_of_transaction']
                                                                     == 'Withdraw']['how_much_in_ils'].mean()))

    # This function returns the info of the account.
    def info(self):
        print("Account number: " + str(self.account_num))
        print("Full name: " + self.person.get_full_name())
        print("Email: " + self.email)
        print("Address: " + self.address.full_address())
        print("Balance: " + str(self.balance))
        print("Phone number: " + self.phone_number)


# This is the Bank class, it holds the information about all the accounts in the bank and lets the user create new
# accounts.
class Bank:
    # Constructor
    def __init__(self):
        self.accounts_df = pd.DataFrame(columns=["account_number", "account", "email", "password"])

    # This function calls the function of the account creation and if the other function succeed to create account
    # it gives this account a special bank account number and adds the info to the bank data frame.
    def create_account(self):
        new_account_data = account_creation_validation()
        if new_account_data is None:
            print("Account wasn't added!")
            return
        # If the account creation and validation succeed creating account, it returns the account (Account object)
        # and the password of the account.
        new_account = new_account_data[0]
        new_account_pass = new_account_data[1]
        # Choosing a random number to be tha accounts data
        new_acc_num = str(random.randint(10000, 99999))
        while new_acc_num in self.accounts_df.account_number:
            new_acc_num = str(random.randint(10000, 99999))
        new_account.set_acc_num(new_acc_num)
        # If the new account is the first account we are creating a new data frame for the bank, else we are adding the
        # account to the existing data frame.
        if self.accounts_df.empty:
            self.accounts_df = (pd.DataFrame(
                {"account_number": [new_acc_num], "account": [new_account], "email": [new_account.get_email()],
                 "password": new_account_pass}))
        else:
            self.accounts_df = pd.concat([self.accounts_df, pd.DataFrame(
                {"account_number": [new_acc_num], "account": [new_account], "email": [new_account.get_email()],
                 "password": new_account_pass})])
        print("Your new account number is " + new_acc_num)

    # This function returns the account
    def get_accounts_data(self):
        return self.accounts_df

    # This function sets the bank data frame to be the data frame given as an argument.
    def set_accounts_df(self, df):
        self.accounts_df = df


# This function runs all the bank system, you have an option to use previous data or to open a new bank.
# You can create new accounts, make transactions, save data and ect...
def run():
    bank = Bank()  # Creating a bank
    # You can choose to start with saved data if you already have pkl file of bank data, you can also choose to start
    # a new bank.
    if os.path.exists('bank.pkl'):
        if input("If you want to start a new bank enter 1, else enter any key") != '1':
            bank.set_accounts_df(pd.read_pickle('bank.pkl'))
        else:
            # When we choose to start a new bank we delete all the previous bank data.
            os.remove('bank.pkl')
    print("Hello and welcome to the bank system")
    while True:  # The way to stop the loop is by entering 0, if you enter 0 the loop will break.
        key = input("Main Menu -\n"
                    "1 - Open account\n"
                    "2 - Check balance\n"
                    "3 - Make a transaction\n"
                    "4 - Last transactions\n"
                    "5 - Get the statistic of the account\n"
                    "6 - Save account transactions on disk(csv)\n"
                    "7 - Get accounts information\n"
                    "0 - Exit and save data\n")
        if key == '1':
            bank.create_account()
        if key == '2':
            print("You chose to check balance ")
            acc = login(bank)  # Log in to the account.
            # If it fails the function login returns None and the loop continue, otherwise we get the information we
            # need.
            if acc is None:
                continue
            print("The balance of the account is: " + str(acc.get_balance()))
        if key == '3':
            print("In order to make a transaction you need to login first")
            acc = login(bank)
            if acc is None:
                continue
            acc.make_transaction()
        if key == '4':
            acc = login(bank)
            if acc is None:
                continue
            # Printing the tale of the transaction history data frame which is an attributes of Account.
            print(acc.get_last_tr_history())
        if key == '5':
            print("In order to get statistics of the account you need to login first")
            acc = login(bank)
            if acc is None:
                continue
            # Printing statistics about the account's activity.
            acc.get_stats()
        if key == '6':
            print("In order to save historical transaction data on your disk you need to login first")
            acc = login(bank)
            if acc is None:
                continue
            # If we have logged in successfully we save the accounts' transaction data on a csv file.
            acc.get_df_of_trans().to_csv(path_or_buf=str(acc.get_acc_num()) + ".csv")
        if key == '7':
            print("In order to get account info you need to login first")
            acc = login(bank)
            if acc is None:
                continue
            acc.info()
        if key == '0':
            break
    # After we choose to finish the running of the program by entering '0',
    # the data of the bank will be saved as a pickle.
    bank.get_accounts_data().to_pickle("bank.pkl")


# Starting the program
run()
