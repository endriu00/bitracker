import argparse

def parse_arguments():
    parser = argparse.ArgumentParser(prog='bitracker', description='bitracker ' 
    + 'reports the current value of a crypto in as many currencies as you want')

    subparsers = parser.add_subparsers(dest='subparser')

    init_parser = subparsers.add_parser('init')
    init_parser.add_argument('--cmc-key', '-ck', type=str, help='Specify the coinmarketcap key.')

    addkey_parser = subparsers.add_parser('addkey')
    addkey_parser.add_argument('--cmc-key', '-ck', type=str, help='Specify the '
    +'coinmarketcap key.')

    price_parser = subparsers.add_parser('price')
    price_parser.add_argument('crypto_name', type=str, help='Name of crypto whose price you want to know')
    price_parser.add_argument('--currency','-c', type=str, help='Return currency', default='USD')
    
    return parser.parse_args()
    