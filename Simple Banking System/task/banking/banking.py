from random import randint
from math import ceil
import sqlite3


def generate_card_num():
    # code to generate card number
    suffix = '400000'
    customernumber = str(randint(0, 999999999)).zfill(9)
    first15digit = suffix + customernumber
    luhn = []
    for x in range(1, len(first15digit) + 1):
        newdigit = int(first15digit[x - 1])
        if x % 2 != 0:
            newdigit = newdigit * 2
            newdigit = newdigit - 9 if newdigit > 9 else newdigit
        luhn.append(int(newdigit))
    last_digit = int(ceil(sum(luhn) / 10)) * 10 - sum(luhn)
    card_num = first15digit + str(last_digit)
    return customernumber, card_num


class Card:
    def __init__(self):
        self.cus_num, self.card_number = generate_card_num()
        self.pin = str(randint(0, 9999)).zfill(4)
        self.balance = 0
        conn = sqlite3.connect('card.s3db')
        self.insert_card(conn)
        conn.close()

    def insert_card(self, conn):
        cur = conn.cursor()
        cur.execute(' insert into card values (?,?,?,?)', (self.cus_num, self.card_number, self.pin, self.balance))
        conn.commit()


def login(card_num, pin):
    conn = sqlite3.connect('card.s3db')
    cur = conn.cursor()
    sql = 'Select * from card where number = ? and pin = ?'
    args = (card_num, pin)
    cur.execute(sql, args)
    result = cur.fetchone() is not None
    conn.close()
    return result


def get_balance(card_num):
    conn = sqlite3.connect('card.s3db')
    cur = conn.cursor()
    cur.execute('Select balance from card where number = ?', (card_num,))
    balance = cur.fetchone()[0];
    conn.close()
    return balance


def balance_change(card_num, amt):
    conn = sqlite3.connect('card.s3db')
    cur = conn.cursor()
    cur.execute('update card set balance = balance + ? where number = ?', (amt, card_num))
    conn.commit()
    conn.close()



def check_luhn(card_num):
    digits = []
    for i in range(len(card_num)):
        digit = int(card_num[i])
        if (i+1) % 2 != 0:
            digit *= 2
            if digit > 9:
                digit = digit -9
        digits.append(digit)
    sum_digits = sum(digits)
    return sum_digits % 10 == 0

def exist_card(card_num):
    conn = sqlite3.connect('card.s3db')
    cur = conn.cursor()
    cur.execute('Select * from card where number = ?', (card_num,))
    result = cur.fetchone() is not None
    conn.close()
    return result


def close_acc(number):
    conn = sqlite3.connect('card.s3db')
    cur = conn.cursor()
    cur.execute('delete from card where number = ?', (number,))
    conn.commit()
    conn.close()

conn = sqlite3.connect('card.s3db')
cur = conn.cursor()
cur.execute('''CREATE TABLE if not exists card
             (id integer,
             number text,
             pin text,
             balance integer default 0)
             ''')
conn.commit()

choice = 1

while choice != 0:
    choice = int(input("""1. Create an account
2. Log into account
0. Exit"""))

    if choice == 1:
        card = Card()
        print("Your card has been created")
        print("Your card number:\n{}".format(card.card_number))
        print("Your card PIN:\n{}".format(card.pin))
    elif choice == 2:
        number = input("Enter your card number:")
        pin = input("Enter your pin:")

        if not login(number, pin):
            print('Wrong card number or PIN!')
        else:
            print('You have successfully logged in!')
            choice_logged = 1
            while choice_logged != 0:
                choice_logged = int(input("""1. Balance
2. Add income
3. Do transfer
4. Close account
5. Log out
0. Exit"""))
                if choice_logged == 1:
                    print("Balance: {}".format(get_balance(number)))
                elif choice_logged == 2:
                    income = float(input('Enter income:'))
                    balance_change(number, income)
                    print('Income was added!')
                elif choice_logged == 3:
                    print('Transfer')
                    to_card_num = input('Enter card number:')
                    if not check_luhn(to_card_num):
                        print('Probably you made a mistake in the card number. Please try again!')
                    elif not exist_card(to_card_num):
                        print('Such a card does not exist.')
                    else:
                        amt = float(input('Enter how much money you want to transfer:'))
                        if amt > get_balance(number):
                            print('Not enough money!')
                        else:
                            balance_change(number,-amt)
                            balance_change(to_card_num,amt)
                            print('Success!')
                elif choice_logged == 4:
                    close_acc(number)
                    print('The account has been closed!')
                elif choice_logged == 5:
                    print('You have successfully logged out!')
                elif choice_logged == 0:
                    exit()

    elif choice == 0:
        exit()
