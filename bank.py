import random

# MAIN CLASS FOR ACCOUNTS

class BankAccount:
    accounts = {1: {'pin': '1', 'balance': 4}} # First acc for testing

    def __init__(self):
        self.pin = None
        self.card_number = None
        self.balance = 0
        self.authorization = False
        self.main_menu() # Init main menu

    # CREATING ACC USING RANDOM

    def create_account(self):
        self.pin = ''.join([str(random.randint(0, 9)) for _ in range(4)]) # tech. for randomize
        #card_random = [str(random.randint(0, 9)) for _ in range(10)]
        while True:
            # self.card_number = '400000'+ ''.join(card_random) # join need to be separate from '400000'
            self.luhn_algorithm()
            if self.card_number not in BankAccount.accounts.keys():
                break
            print('copy')
        BankAccount.accounts[self.card_number] = {'pin': self.pin, 'balance': 0}
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
        current_card = int(input("Enter your card number:"))
        current_pin = input("Enter your PIN:")
        if BankAccount.accounts.get(current_card, {}).get('pin') == current_pin: # Technique to use get for nested dict
            self.authorization = True
            self.card_number = current_card
            self.pin = current_pin
            self.balance = BankAccount.accounts[self.card_number]['balance']
            print("You have successfully logged in!")
        else:
            print("Wrong card number or PIN!")

    # BALANCE - NOW QUIET USELESS - TO DEVELOP

    def check_balance(self):
        print(self.balance)
        #print(BankAccount.accounts)

    # ALGORITHM FOR CHECKING CARDS NUMBERS

    def luhn_algorithm(self):
        self.card_number = [4, 0, 0, 0, 0, 0] + [random.randint(0, 9) for _ in range(9)]
        luhn_support_list = self.card_number.copy() # Second list for all operations from Luhn Algo
        for i in range(0, 15):
            if i % 2 == 0:
                luhn_support_list[i] *= 2
            if luhn_support_list[i] > 9:
                luhn_support_list[i] -= 9
        self.card_number.append(10 - sum(luhn_support_list) % 10)
        # Transition from int[] to int
        card_support_string = [str(i) for i in self.card_number]
        self.card_number = int(''.join(card_support_string))

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
                print("1. Balance\n2. Log out\n0. Exit")
                option = input()
                if option == '1':
                    self.check_balance()
                elif option == '2':
                    self.authorization = False
                    print("You have successfully logged out!")
                else:
                    break
        print('Bye!')

bank = BankAccount()
