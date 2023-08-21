import sqlite3
import csv

DATABASE: str = "final.db"
cnxn: sqlite3 = sqlite3.connect(DATABASE)
cursor = cnxn.cursor()


def read_user(username, password):
    investor = cursor.execute("select * from Investors where username=?", (username,)).fetchone()
    if investor:
        if password == investor[2]:
            return investor
        else:
            print("wrong password")
    else:
        print("username not found")


def write_user(username, password):
    try:
        cursor.execute("INSERT INTO Investors (username, password) VALUES (?, ?)", (username, password))
        cnxn.commit()
        print("success")
    except Exception as e:
        print("username not available")


def write_stock(active_user):
    # unpacking the active user so we can write the stock to db
    investor_id, ticker, quantity, purchase_price, purchase_date = active_user

    try:
        cursor.execute("INSERT INTO Stocks (investor_id, ticker_symbol, quantity, purchase_price, purchase_date) "
                       "VALUES (?, ?, ?, ?, ?)", (investor_id, ticker, quantity, purchase_price, purchase_date))
        cnxn.commit()
        print("successfully entered stock")
    except Exception as e:
        print(f"{ticker} already in database, try update function instead")


def write_csv(csv_file, active_user):
    with open(csv_file, "r") as f:
        reader = csv.DictReader(f)
        for stock in reader:
            write_stock(active_user=[active_user, stock["SYMBOL"], float(stock["NO_SHARES"]), float(stock["PURCHASE_PRICE"]),
                                                                                       stock["PURCHASE_DATE"]])

