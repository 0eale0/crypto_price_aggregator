from coinbase.wallet.client import Client

coinbase_API_key = '2310924'
coinbase_API_secret = '49645645049'
client = Client(coinbase_API_key, coinbase_API_secret)
currency_code = 'EUR'

print(client.get_exchange_rates())
