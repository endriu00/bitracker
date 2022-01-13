<<<<<<< HEAD
from client.api.get_price import get_price

from client.cli.config_parser import read_config, write_config
from client.cli.parse_arguments import parse_arguments
from client.cli.init_bitracker import init_bitracker

def bitracker():
    # parse CLI args
    args = parse_arguments()
    command = args.subparser

    if command == 'init':
        cmc_api_key = args.cmc_key
        init_bitracker(cmc_api_key)

    if command == 'addkey':
        cmc_api_key = args.cmc_key
        write_config('coinmarketcap', {'cmc_api_key': cmc_api_key})

    if command == 'price':
        # no subcommand has been issued
        crypto_name = args.crypto_name
        currency = args.currency

        # read the config file
        s = read_config()
        cmc_api_key = s.get('coinmarketcap', 'cmc_api_key')
    
        # issue the request
        price = get_price(crypto_name=crypto_name, cmc_api_key=cmc_api_key, currency=currency)
        print(str(price) + ' ' + currency)
=======
from client.cli.parse_arguments import parse_arguments
from client.api.get_price import get_price

def bitracker():
    args = parse_arguments()
    crypto_name = args.crypto_name
    currency = args.currency
    print(get_price(crypto_name, '260bf8e5-a496-4a79-b369-c5ecb3bee523', currency))
>>>>>>> f20992377c66e660a8e259de01e9ba594966a471
