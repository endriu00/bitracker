import requests
import json
import boto3

def handler(event, context):
    '''
    `handler` handles the API Gateway request and returns a response to it.
    '''
    
    # Get path and query parameters from the API Gateway.
    crypto_name = event['pathParameters']['crypto_name']
    cmc_api_key = event['headers']['cmc_api_key'] 
    currency = event['queryStringParameters']['currency']

    price = inspector(crypto_name=crypto_name, cmc_api_key=cmc_api_key, currency=currency)
    return {
        'statusCode': 200,
        'body': json.dumps(price),
        'headers': {
            'Access-Control-Allow-Origin': '*', # Required for CORS support to work
            'Access-Control-Allow-Credentials': True, # Required for cookies, authorization headers with HTTPS
            'Access-Control-Allow-Headers': 'Origin,Content-Type,X-Amz-Date,Authorization,X-Api-Key,X-Amz-Security-Token,locale',
        }
    }


# URL is the Coinmarketcap API endpoint.
URL = "https://pro-api.coinmarketcap.com/v1/cryptocurrency/quotes/latest"

# CMC_API_HEADER is the Coinmarketcap API key header.
CMC_API_HEADER = 'X-CMC_PRO_API_KEY'

# Status codes.
SC_BAD_REQUEST = 400

# Database tables.
CRYPTO_TABLE = 'CryptoTable'

def inspector(crypto_name,  cmc_api_key, currency='EUR'):
    '''
    `inspector` crawls `crypto_name` price data from CoinMarketCap, using 
    cmc_api_key to access it. The returned price refers to its price in
    its `currency` converted value.

    ### Parameters:
    - crypto_name: the name of the crypto.
    - cmc_api_key: the API key used to call the CoinMarketCapi API server.
    - currency: the value of the crypto will refer to this currency.
    
    ### Returns:
    - The price of the crypto in the currency provided.
    '''
    
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

    # Get the timestamp the price was updated at and convert it to a datetime 
    # representation to store more efficiently in the Database.
    last_updated = data['data'][id]['last_updated']

    # TODO separate the data insertion from the inspector!!
    # Create the DynamoDB object and get the table.
    dynamodb = boto3.resource('dynamodb', region_name='us-east-1')
    table = dynamodb.Table(CRYPTO_TABLE)

    # Put the information together to store them in the Database.
    crypto_row = {'name': crypto_name, 'price': str(price), 'timestamp': last_updated}

    # Insert the crypto price at its timestamp in the Database.
    response = table.put_item(
        Item = crypto_row
    )
    
    return price

if __name__ == '__main__':
    inspector('bitcoin', 'b32ecd6a-fb6a-4426-87e9-f9f1651e96bf')