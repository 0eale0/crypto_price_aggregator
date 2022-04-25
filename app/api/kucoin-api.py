from kucoin.client import Client

api_key = '456789io'
api_secret = '456y7u8i'
api_passphrase = '23456789io'

client = Client(api_key, api_secret, api_passphrase)
print(client.get_currencies())
