import json
import requests

from client.api.constants import URL

# get_price issues a request to the Bitracker API server for 
# the /v1/crypto endpoint.
# It returns the crypto_name price in currency using cmc_api_key as API key.
def get_price(crypto_name, cmc_api_key, currency):
    # prepare the request
    headers = {'cmc_api_key': cmc_api_key}
    params = {'currency': currency}
    url = URL + '/v1/crypto/' + crypto_name

    r = requests.get(url=url, headers=headers, params=params)
    if r.status_code == 500:
        exit("Crypto name or currency is not correct.")
    
    return r.json()