from kucoin.client import Client

api_key = '456789io'
api_secret = '456y7u8i'
api_passphrase = '23456789io'

client = Client(api_key, api_secret, api_passphrase)
lst_currency_name = []
print(client.get_currencies())
# for i in range(len(client.get_currencies())):
#     lst_currency_name.append(client.get_currencies()[i]['name'])
# print(lst_currency_name)
