from os import makedirs

from client.cli.config_parser import write_config
from client.cli.constants import BITRACKER_CONFIG_PATH, BITRACKER_PATH

# init_bitracker initializes the Bitracker directory where important files
# are stored. It initializes its config file if the coinmarketcap key 
# has been provided.
def init_bitracker(cmc_api_key=None):
    try:
        makedirs(BITRACKER_PATH)
        open(BITRACKER_CONFIG_PATH, 'x')
    except OSError:
        exit("\nDirectory already exists!\n")
    finally:
        if cmc_api_key is not None:
            write_config('coinmarketcap', {'cmc_api_key': cmc_api_key})