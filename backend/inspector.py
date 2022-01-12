import requests
import json

def handler(event, context):
    print(event)
    
    price = inspector(event['pathParameters']['crypto_name'], event['headers']['cmc_api_key'], event['queryStringParameters']['currency'])
    return {
        'statusCode': 200,
        'body': json.dumps(price)
    }

# URL is the Coinmarketcap API endpoint.
URL = "https://pro-api.coinmarketcap.com/v1/cryptocurrency/quotes/latest"

# CMC_API_HEADER is the Coinmarketcap API key header.
CMC_API_HEADER = 'X-CMC_PRO_API_KEY'

# Status codes.
SC_BAD_REQUEST = 400

# inspector crawls crypto_name price data from CMC, using cmc_api_key to access it.
# currency is the currency the crypto value is evaluated to.
def inspector(crypto_name,  cmc_api_key, currency):
    # headers represents headers to be sent.
    #   The header X-CMC_PRO_API_KEY represents the API key.
    headers = {CMC_API_HEADER: cmc_api_key}
    
    # params represents the data to be sent.
    #   slug represents the crypto name.
    #   convert represents the convertion currency.
    params = {'slug':crypto_name, 'convert':currency}

    # send the request and save the response.
    r = requests.get(url=URL, headers=headers, params=params)

    # NOTE: CMC API returns a 400: Bad Request when there is no resource.
    if r.status_code == SC_BAD_REQUEST:
        exit('Not found')

    # extract data.
    data = r.json()

    # the API endpoint returns the important data as the value of a numeric key,
    # that is the crypto key as stored in CMC databases. In order to access 
    # the crypto price data, it is necessary to get this ID. 
    # This is is always the first and only value of the dict key data.
    id  = [x for x in data['data'].keys()][0]
    price = data['data'][id]['quote'][currency]['price']
    return price
