import numpy as np
import requests
import pandas as pd
import matplotlib.pyplot as plt
import sqlite3

API_KEY = ""

DATABASE: str = "final.db"
cnxn: sqlite3 = sqlite3.connect(DATABASE)

stocks_df = pd.read_sql_query("SELECT * FROM Stocks", cnxn)

# add columns so concatenate still works but fill with NaN
bonds_df = pd.read_sql_query("SELECT * FROM Bonds", cnxn)

combined_df = pd.concat([stocks_df, bonds_df], ignore_index=True)
combined_df.drop(["stock_id", "bond_id", "investor_id"], inplace=True, axis=1)
combined_df = combined_df[["ticker_symbol", "purchase_price", "quantity", "yield", "coupon"]]
combined_df["current_price"] = np.nan


# here is where we get a current price on a stock so we can add that column to our dataframe
# this will not work without your API key!
for ticker in combined_df["ticker_symbol"].tolist():
    endpoint = f'https://api.twelvedata.com/price?symbol={ticker}&apikey={API_KEY}'
    response = requests.get(endpoint)
    data = response.json()
    if "price" in data:
        combined_df.loc[combined_df["ticker_symbol"] == ticker, "current_price"] = data["price"]
    else:
        print(f"ticker: {ticker} may not exist or may have been changed please update/remove".center(80, "="))
print("\n\n")

combined_df["current_price"] = combined_df["current_price"].astype(np.float64)
combined_df["quantity"] = combined_df["quantity"].astype(np.float64)
combined_df["p/l"] = (combined_df["quantity"] * combined_df["current_price"]) - (combined_df["quantity"] * combined_df["purchase_price"])


def vizData():
    plt.figure(figsize=(10, 6))
    colors = ['red' if x < 0 else 'green' for x in combined_df['p/l']]
    plt.bar(combined_df['ticker_symbol'], combined_df['p/l'], color=colors)
    plt.xlabel('Ticker Symbol')
    plt.ylabel('Profit/Loss')
    plt.title('Stocks Profit/Loss Visualization')
    plt.axhline(0, color='black',linewidth=0.8)  # Add a horizontal line at y=0 for clarity
    plt.grid(axis='y', linestyle='--', linewidth=0.7, alpha=0.7)

    # Display the chart
    plt.tight_layout()
    plt.show()