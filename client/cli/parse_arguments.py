import argparse

def parse_arguments():
    parser = argparse.ArgumentParser(prog='bitcracker', description='bitcracker reports the current value of a crypto in as many currencies as you want')
    parser.add_argument('--crypto_name', '-cn', required=True, type=str, help='Name of crypto whose price you want to know')
    parser.add_argument('--currency','-c', type=str, help='Return currency', default='USD')
    return parser.parse_args()
    