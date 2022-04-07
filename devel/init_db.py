import boto3

DYNAMODB_URL = 'http://localhost:8000'

def create_crypto_table(dynamodb=None):
    table_name = 'CryptocurrencyPrice'
    crypto_name = 'name'
    crypto_timestamp = 'timestamp'

    # Initialize the dynamodb variable if it has not been initialized yet.
    if dynamodb is None:
        dynamodb = boto3.client('dynamodb', endpoint_url=DYNAMODB_URL)

    # Return in case the table already exists.
    if table_name in dynamodb.list_tables()['TableNames']:
        print('The table was already created!')
        return

    table = dynamodb.create_table(
        TableName=table_name,
        AttributeDefinitions=[
            {
                'AttributeName': crypto_name,
                'AttributeType': 'S',

            },
            {
                'AttributeName': crypto_timestamp,
                'AttributeType': 'N',
            }
        ],
        KeySchema=[
            {
                'AttributeName': crypto_name,
                'KeyType': 'HASH',  # Partition key
            },
            {
                'AttributeName': crypto_timestamp,
                'KeyType': 'RANGE',  # Sort key
            }
        ],
        ProvisionedThroughput={
            'ReadCapacityUnits': 10,
            'WriteCapacityUnits': 10,
        }
    )
    print('Table created!')


if __name__ == '__main__':
    create_crypto_table()
