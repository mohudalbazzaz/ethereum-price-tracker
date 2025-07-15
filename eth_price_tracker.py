import pandas as pd 
import requests, csv, os
import seaborn as sns
import matplotlib.pyplot as plt
from datetime import datetime
from dotenv import load_dotenv
import logging

logging.basicConfig(
    filename="tracker.log",
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)

logging.info("Starting script")

ticker = "eth"
name = "Ethereum"
currency = "usd"

load_dotenv()
api_key = os.getenv("COINGECKO_API_KEY")

url = f"https://api.coingecko.com/api/v3/simple/price?vs_currencies={currency}&names={name}&symbols={ticker}&include_market_cap=true&include_24hr_vol=true"

headers = {
    "accept": "application/json",
    "x-cg-demo-api-key": api_key
}

try:
    response = requests.get(url, headers=headers)
    response.raise_for_status()
    data = response.json()
    logging.info("Price data fetched successfully.")
except Exception as e:
    logging.error(f"Failed to fetch data: {e}")

data = response.json()
field_names = data["Ethereum"]
field_names["timestamp"] = datetime.now().replace(microsecond=0)
file_name = "eth_prod.csv"

file_exists = os.path.isfile(file_name)

with open(file_name, 'a', newline='') as file:
    writer = csv.DictWriter(file, fieldnames=list(field_names.keys()))
    if not file_exists:
        writer.writeheader()
    writer.writerow(field_names)

df = pd.read_csv(file_name)
df = df.drop_duplicates(subset=["usd_market_cap", "usd_24h_vol"], keep="first").reset_index(drop=True)

df["Price ($)"] = df["usd"]
df["Market Cap (Billions) ($)"] = (df["usd_market_cap"] / 1000000000).round(2)
df["24h Volume (Billions) ($)"] = (df["usd_24h_vol"] / 1000000000).round(2)

df.drop(columns=["usd_market_cap", "usd", "usd_24h_vol"])


sns.set_style("darkgrid")

sns.lineplot(data=df, x="timestamp", y="Price ($)")

plt.gca().axes.get_xaxis().set_visible(False)
plt.title("Ethereum Price")

plt.show()
