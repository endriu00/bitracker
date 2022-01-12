import configparser

def read_config():  
    config = configparser.ConfigParser()
    config.read('./bitracker.cfg')
    return config

# TODO
def write_config(key, val):
    config = configparser.ConfigParser()
    config[key] = {}
    config[key]['KEY'] = val
    # TODO change to another config file position
    # in ~/.bitracker/bitracker.cfg
    with open('./bitracker.cfg', 'w') as conf:
        config.write(conf)