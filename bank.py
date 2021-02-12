import random
import sqlite3
from db_execute import *

# MAIN CLASS FOR ACCOUNTS

class BankAccount:

    def __init__(self):
        self.pin = None
        self.card_number = None
        self.balance = None
        self.authorization = False
        self.main_menu()  # Init main menu

    # CREATING ACC USING RANDOM

    def create_account(self):
        self.pin = ''.join([str(random.randint(0, 9)) for _ in range(4)])
        while True:
            self.luhn_creator()
            if self.card_number not in [number[1] for number in database_info]:
                break
            print('copy')
        cur.execute(f"INSERT INTO card (number, pin) VALUES ('{self.card_number}', '{self.pin}');")
        conn.commit()
        print(f'Your card number:\n{self.card_number}')
        print(f'Your card PIN:\n{self.pin}')

        """
        Good tech. for random

        print("%04d" % random.randrange(0000, 9999))
        print('{:04d}'.format(random.randrange(0000, 9999)))
        haha = random.randrange(0000, 9999)
        print(f'{haha:04d}')

        """

    # LOGIN - IF CORRECT ASSIGN VALUES TO SELF.

    def check_authorization(self):
        current_card = input("Enter your card number: ")
        current_pin = input("Enter your PIN: ")
        cur.execute(f"SELECT * FROM card WHERE number={current_card};")
        current_account_info = cur.fetchone()
        if current_account_info != None and current_account_info[2] == current_pin:  # Technique to use get for nested dict
            self.authorization = True
            self.card_number = current_card
            self.pin = current_pin
            self.balance = current_account_info[3]
            print("You have successfully logged in!")
        else:
            print("Wrong card number or PIN!")

    # BALANCE - TO DEVELOP

    def check_balance(self):
        print(self.balance)

    # ADD_INCOME - ADDING MONEY TO BANK_ACCOUNT

    def add_income(self):
        self.balance += int(input('Enter income: '))
        cur.execute(f'''UPDATE card SET balance={self.balance} WHERE number={self.card_number};''')
        conn.commit()
        print('Success!')

    # CLOSING CURRENT ACCOUNT (DELETING ROW FROM DATABASE)

    def close_account(self):
        cur.execute(f'DELETE FROM card WHERE number={self.card_number};')
        conn.commit()
        print('The account has been closed!')

    # TRANSFER MONEY

    def transfer_money(self):
        print('Transfer')
        print('Enter card number:')
        transfer_number = input()
        cur.execute(f'''SELECT * FROM card WHERE number={transfer_number};''')
        transfer_info = cur.fetchone()
        if transfer_number == self.card_number:
            print("You can't transfer money to the same account!")
        elif not self.luhn_verify(transfer_number):
            print('Probably you made a mistake in the card number. Please try again!')
        elif transfer_info == None:
            print('Such a card does not exist.')
        else:
            print('Enter how much money you want to transfer:')
            transfer_money = int(input())
            if transfer_money > self.balance:
                print("Not enough money!")
            else:
                print('Success!')
                self.balance -= transfer_money
                cur.execute(f'UPDATE card SET balance={self.balance} WHERE number={self.card_number};')
                conn.commit()
                cur.execute(f'UPDATE card SET balance={transfer_info[3] + transfer_money} WHERE number={transfer_number};')
                conn.commit()

    # ALGORITHM FOR CHECKING CARDS NUMBERS

    def luhn_creator(self):

        self.card_number = [4, 0, 0, 0, 0, 0] + [random.randint(0, 9) for _ in range(9)]
        luhn_support_list = self.card_number.copy()  # Second list for all operations from Luhn Algo
        for i in range(0, 15):
            if i % 2 == 0:
                luhn_support_list[i] *= 2
            if luhn_support_list[i] > 9:
                luhn_support_list[i] -= 9
        if sum(luhn_support_list) % 10 == 0:
            self.card_number.append(0)
        else:
            self.card_number.append(10 - sum(luhn_support_list) % 10)
        # Transition from int[] to int
        self.card_number = ''.join([str(i) for i in self.card_number])

    def luhn_verify(self, number):
        number = list(map(int, number))
        luhn_support_list = number.copy()
        for i in range(0, len(luhn_support_list) - 1):
            if i % 2 == 0:
                luhn_support_list[i] *= 2
            if luhn_support_list[i] > 9:
                luhn_support_list[i] -= 9
        if sum(luhn_support_list) % 10 == 0:
            return True
        else:
            return False

    # MAIN MENU

    def main_menu(self):
        while True:
            if self.authorization == False:
                print("1. Create an account\n2. Log into account\n0. Exit")
                option = input()
                if option == '1':
                    self.create_account()
                elif option == '2':
                    self.check_authorization()
                else:
                    break
            else:
                print("1. Balance\n2. Add income\n3. Do transfer\n4. Close account\n5. Log out\n0. Exit")
                option = input()
                if option == '1':
                    self.check_balance()
                elif option == '2':
                    self.add_income()
                elif option == '3':
                    self.transfer_money()
                elif option == '4':
                    self.close_account()
                elif option == '5':
                    self.authorization = False
                    print("You have successfully logged out!")
                else:
                    break
        print('Bye!')

bank = BankAccount()
conn.close()
