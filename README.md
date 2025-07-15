# Ethereum Price Tracker

A Python script that fetches Ethereum price data from the CoinGecko API, processes it, and saves the results. Includes logging and supports secure API key management using environment variables.

## Features

- Fetches current ETH price, market cap, and 24-hour volume
- Saves data to CSV (`eth_prod.csv`)
- Logs activities and errors to `tracker.log`
- Uses a `.env` file to securely store API keys

## Requirements

Install the dependencies using:

```bash
pip install -r requirements.txt