import logging
from nmap_scan import nmapscan
try:
    import ConfigParser 
except:
    import configparser as ConfigParser
import sys
import os
from inventory import Inventory

def main():
    config = ConfigParser.ConfigParser()
    base =  os.path.basename(__file__)
    root = os.path.splitext(base)[0]

    config.read('../etc/' + root + '.ini')
    logging.basicConfig(filename=config.get('logging','dir')+ root + '.log',format='%(asctime)s:%(levelname)s:%(message)s',level=logging.DEBUG)
    if nmapscan(config):
        print( 'OK')
    inv = Inventory(config,root)
    inv.parse()
if __name__ == "__main__":
    if not sys.version_info[:2] >= (3,5):
        print('Python 3.5 or greater required')
        sys.exit(2)
    main()
