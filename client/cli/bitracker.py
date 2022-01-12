from client.cli.parse_arguments import parse_arguments
from client.api.get_price import get_price

def bitracker():
    args = parse_arguments()
    crypto_name = args.crypto_name
    currency = args.currency
    print(get_price(crypto_name, '260bf8e5-a496-4a79-b369-c5ecb3bee523', currency))