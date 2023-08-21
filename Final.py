import os
from pathlib import Path
import finalclasses

import finaldbtools

# we cant actually reassign this from local scope so we change value in list (mutable)
ACTIVE_USER: list[any] = []


def signin():
    username: str = input("please enter your username: ")
    password: str = input("please enter your password: ")
    investor = finaldbtools.read_user(username, password)
    if investor:
        ACTIVE_USER.extend(investor)


def create_user():
    username: str = input("please choose a username: ")
    password: str = input("please choose a password: ")
    finaldbtools.write_user(username, password)


def add_stock():
    ticker = input("please enter your ticker: ")
    quantity = float(input("please enter the quantity: "))
    purchase_price: float = float(input("please enter your purchase price: "))
    purchase_date: str = input("please enter purchase date: ")
    stock_to_add_list = (ACTIVE_USER[0], ticker, quantity, purchase_price, purchase_date)
    finaldbtools.write_stock(stock_to_add_list)


def load_csv():
    csv_file = Path(input("please give exact path to csv: "))
    # use os to check for file existence
    print(csv_file.name)
    if os.path.exists(csv_file):
        finaldbtools.write_csv(csv_file.name, active_user=ACTIVE_USER[0])
    else:
        print("file not found!")


def update_stock():
    print("UPDATING STOCK")


def load_viz():
    import visualize  # import here to avoid certain functionality from running
    visualize.vizData()


def main():
    # beginning functionality
    while not ACTIVE_USER:
        functionality = {
            "1": ("sign in", signin),
            "2": ("create account", create_user),
            "3": ("quit", quit)
        }
        print("STOCK APP".center(30, "="))
        print("\nWOULD YOU LIKE TO")
        for key, value in functionality.items():
            print(f"[{key}]. {value[0].upper()}")
        selection: str = input(">>>: ")
        functionality[selection][1]()

    # user has now logged in, functionality changes
    for _ in range(300):  # exit condition not know so we use for loop
        logged_in_functionality = {
            "1": ("add stock", add_stock),
            "2": ("add bond", "PUT SOMETHING HERE"),
            "3": ("load csv", load_csv),
            "4": ("visualize data", load_viz),
            "5": ("quit", quit)
        }
        print("\nWOULD YOU LIKE TO")
        for key, value in logged_in_functionality.items():
            print(f"[{key}]. {value[0].upper()}")
        selection: str = input(">>>: ")
        logged_in_functionality[selection][1]()


if __name__ == '__main__':
    main()