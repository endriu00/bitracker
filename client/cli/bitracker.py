from requests import api
from client.api.get_price import get_price

from client.cli.config_parser import read_config, write_config
def bitracker():
    # parse CLI args
    
    # read the config file
    s = read_config()
    api_key = s['coinmarketcap']['api_key']
    
    # issue the request
    price = get_price('bitcoin', api_key, 'EUR')
    print(price)