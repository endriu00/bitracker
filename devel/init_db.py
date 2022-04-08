import boto3

DYNAMODB_URL = 'http://localhost:8000'

def create_crypto_table(dynamodb=None) -> bool :
    '''
    `create_crypto_table` creates the table containing the cryptocurrency
    prices in relation to the time.

    ### Parameters:
    - dynamodb: the dynamodb resource.

    ### Returns:
    - a boolean indicating whether the table has been created or not.
    '''

    table_name = 'CryptoTable'
    crypto_name = 'name'
    crypto_timestamp = 'timestamp'

    # Initialize the dynamodb variable if it has not been initialized yet.
    if dynamodb is None:
        dynamodb = boto3.client('dynamodb', endpoint_url=DYNAMODB_URL)

    # Return in case the table already exists.
    if table_name in dynamodb.list_tables()['TableNames']:
        return False

    table = dynamodb.create_table(
        TableName=table_name,
        KeySchema=[
            {
                'AttributeName': crypto_name,
                'KeyType': 'HASH',  # Partition key
            },
            {
                'AttributeName': crypto_timestamp,
                'KeyType': 'RANGE',  # Sort key
            },
        ],
        AttributeDefinitions=[
            {
                'AttributeName': crypto_name,
                'AttributeType': 'S',

            },
            {
                'AttributeName': crypto_timestamp,
                'AttributeType': 'S',
            },
        ],

        ProvisionedThroughput={
            'ReadCapacityUnits': 10,
            'WriteCapacityUnits': 10,
        }
    )

    return True


def insert_sample_crypto():
    '''
    '''


def main():
    if not create_crypto_table():
        print('The table was already created or an error has occurred!')
        exit()

    print('Table created!')


if __name__ == '__main__':
    main()
