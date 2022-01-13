import configparser

from client.cli.constants import BITRACKER_CONFIG_PATH

# read_config reads the bitracker config file and returns it.
def read_config():  
    config = configparser.ConfigParser()
    config.read(BITRACKER_CONFIG_PATH)
    return config

# write_config writes the bitracker config file.
# key should be a string, representing the first-level element in the [].
# val should be a string or a dictionary, representing the elements under the []. 
def write_config(key, val):
    config = configparser.ConfigParser()
    config[key] = {}
    config[key] = val
    with open(BITRACKER_CONFIG_PATH, 'w') as conf:
        config.write(conf)