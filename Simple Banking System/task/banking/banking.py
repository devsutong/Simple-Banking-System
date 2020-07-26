# Write your code here
import sqlite3
import random
conn = sqlite3.connect('card.s3db')
cur = conn.cursor()
cur.execute("""CREATE TABLE IF NOT EXISTS card (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    number TEXT NOT NULL,
    pin TEXT NOT NULL,
    balance INTEGER DEFAULT 0
    );""")
conn.commit()


class Account:

    def __init__(self, ano):
        self.pin = str(random.randint(1000, 9999))
        self.acc_no = ano
        params = (self.acc_no, self.pin, 0)
        cur.execute('INSERT INTO card (number, pin, balance) VALUES (?, ?, ?)', params)
        conn.commit()


def gen():
    sum = 0
    numx = "400000" + str(random.randint(100000000, 999999999))
    num_l = [int(x) for x in numx]
    for a in range(len(num_l)):
        if a % 2 == 0:  # is odd since a starts from 0
            x = num_l[a]
            num_l[a] = 2*x
    for a in range(len(num_l)):
        if num_l[a] > 9:
            x = num_l[a]
            num_l[a] = x - 9

    for a in range(len(num_l)):
        sum += num_l[a]
    if sum % 10 == 0:
        add = 0
    else:
        add = 10 - sum % 10
    str1 = ''.join(str(e) for e in num_l)
    numx = numx + str(add)
    return numx


def add_income():
    print("Enter Income:")
    to_add = int(input())
    cur.execute("UPDATE card set balance = balance + ? WHERE number = ?", (to_add, card_no,))
    conn.commit()
    print("Income was added!")


def check_luhn(number):
    addition_luhn = 0
    last = number % 10
    temp = number // 10
    temp2 = str(temp)
    temp3 = [int(x) for x in temp2]
    for i in range(len(temp3)):
        if i % 2 == 0:
            temp3[i] *= 2
    for i in range(len(temp3)):
        if temp3[i] > 9:
            temp3[i] -= 9
    for i in range(len(temp3)):
        addition_luhn += temp3[i]
    if (addition_luhn + last) % 10 == 0:
        return True
    return False


def chk_balance(card_no):
    ls_balance = cur.execute("SELECT * FROM card WHERE number = ?", (card_no,)).fetchone()
    return ls_balance[3]


def transfer():
    print("Enter Card Number:")
    number = int(input())
    okay = check_luhn(number)
    if okay:
        if number == card_no:
            print("You can't transfer money to the same account!")
        else:
            ls_if_any = cur.execute("SELECT * FROM card WHERE number = ?", (number,)).fetchone()  # number is integer or dtring?
            if ls_if_any is None:
                print("Such a card does not exist.")
            else:
                print("Enter how much money you want to transfer:")
                to_transfer = int(input())
                if to_transfer > chk_balance(card_no):
                    print("Not enough money!")
                else:
                    cur.execute("UPDATE card SET balance = balance - ? WHERE number = ?", (to_transfer, card_no,))
                    conn.commit()
                    cur.execute("UPDATE card SET balance = balance + ? WHERE number = ?", (to_transfer, number,))
                    conn.commit()
                    print("Success!")

    else:
        print("Probably you made mistake in the card number. Please try again!")


def close_account(card_no):
    cur.execute("DELETE FROM card WHERE number =?", (card_no,))
    conn.commit()


def logged_in():
    while True:
        print("1. Balance")
        print("2. Add Income")
        print("3. Do Transfer")
        print("4. Close Account")
        print("5. Log Out")
        print("0. Exit")
        ch = int(input())
        if ch == 1:
            bal = chk_balance(card_no)
            print(bal)
        if ch == 2:
            add_income()
        if ch == 3:
            transfer()
        if ch == 4:
            close_account(card_no)
        if ch == 5:
            print("You have successfully logged out!")
            break
        if ch == 0:
            print("Bye!")
            exit()


while True:
    print("1. Create an account")
    print("2. Log into account")
    print("0. Exit")
    num = int(input())
    if num == 1:
        acc = Account(gen())
        print("Your card has been created")
        print("Your card number:")
        print(acc.acc_no)
        print("Your card PIN:")
        print(acc.pin)
    if num == 2:
        print("Enter your card number:")
        card_no = input()
        print("Enter your PIN:")
        pin_no = input()
        ls = cur.execute("SELECT * FROM card WHERE number = ?", (card_no,)).fetchone()
        if ls is None:
            print("Wrong card number or PIN!")
        else:
            if ls[2] == pin_no:
                print("You have successfully logged in!")
                logged_in()
            else:
                print("Wrong card number or PIN!")
    if num == 0:
        print("Bye!")
        conn.close()
        exit()
