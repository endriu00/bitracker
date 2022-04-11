import math
import json

import boto3
from boto3.dynamodb.conditions import Key


def handler(event, context):
    '''
    `handler` handles the API Gateway request and returns a response to it.
    '''
    
    # Get path and query parameters from the API Gateway.
    crypto_name = event['pathParameters']['crypto_name']
    start = event['queryStringParameters']['start']
    end = event['queryStringParameters']['end']
    spread = event['queryStringParameters']['spread']
    max_results = event['queryStringParameters']['max_results']

    prices = get_historical_price(
        crypto_name=crypto_name, 
        start=start,
        end=end,
        spread=spread,
        max_results=max_results   
    )
    return {
        'statusCode': 200,
        'body': json.dumps(prices),
        'headers': {
            'Access-Control-Allow-Origin': '*', # Required for CORS support to work
            'Access-Control-Allow-Credentials': True, # Required for cookies, authorization headers with HTTPS
            'Access-Control-Allow-Headers': 'Origin,Content-Type,X-Amz-Date,Authorization,X-Api-Key,X-Amz-Security-Token,locale',
        }
    }


# Database tables.
CRYPTO_TABLE = 'CryptoTable'

# Hard limit on the results the API can return.
MAX_ALLOWED_RESULTS = 100

def get_historical_price(crypto_name: str, start: str, end: str, spread: bool = True, max_results: int = 5):
    '''
    `get_historical_price` retrieves the `max_results` values for the crypto
    `crypto_name`, starting at time `start` and finishing at time `end` from 
    the DynamoDB Database. If `max_results` is set and the fetched results are
    higher than the `max_results`, `spread` takes a subset of `max_results`
    values in this list: these results are taken in a equally distributed 
    interval. If `spread` is set to False, the first `max_results` are taken.

    ### Parameters:
    - crypto_name: the name of the crypto.
    - start: starting time for the query.
    - end: end time for the query.
    - spread: if the results must be spread or not.
    - max_results: number of values returned.

    ### Returns:
    - A dictionary containing the latest prices, along with the timestamp. 
    ''' 

    dynamodb = boto3.resource('dynamodb', region_name='us-east-1')
    table = dynamodb.Table(CRYPTO_TABLE)

    # If max_results is higher than the max allowed amount, cap it to it. 
    if max_results > MAX_ALLOWED_RESULTS:
        max_results = MAX_ALLOWED_RESULTS

    # Take the first max_results values from the Database if the spread 
    # parameter has been set to False.
    # Take everything and process it later otherwise.
    if not spread:
        raw_prices = table.query(
            KeyConditionExpression=
                Key('name').eq(crypto_name) & 
                Key('timestamp').between(start, end),
            Limit=max_results
        )
        prices = [{'name': crypto_name, 'price': price['price']} 
                    for price in raw_prices['Items']]
        return prices

    # NOTE: only 1 MB will be returned as for the DynamoDB limitations.
    raw_prices = table.query(
        KeyConditionExpression=
            Key('name').eq(crypto_name) & 
            Key('timestamp').between(start, end)
    )
    prices = [{'name': crypto_name, 'price': price['price'], 'timestamp': price['timestamp']} 
                for price in raw_prices['Items']]

    # Return everything if the items are lower than the desired max number. 
    if len(prices) <= max_results:
        return prices

    # Purge the input if the items are higher than the desired max number 
    # and the returned values must be spread over the dataset. Take only a value
    # every "take" point. "take" is used to take only evenly distributed indices 
    # in the prices list, including the first value and the last value too.
    take = math.ceil((len(prices)-2)/(max_results-2))
    spread_prices = [prices[i] for i in range(len(prices)) if i == 0 or i == len(prices)-1 or i%take == 0] 

    # TODO if max_results is odd and len(prices) is even, take the one 
    # before the last one too.

    return spread_prices