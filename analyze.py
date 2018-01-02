"""Process newly discovered hosts

"""
import logging
import configparser as ConfigParser
import sys
import os
from inventory import Inventory
from datetime import datetime
__version__ = '0.1'

def main():
    """Main.

    """
    config = ConfigParser.ConfigParser()
    base = os.path.basename(__file__)
    root = os.path.splitext(base)[0]

    config.read('inventory.ini')
    logging.basicConfig(filename=config.get('logging', 'dir')+ root + '.log',
                        format='%(asctime)s:%(levelname)s:%(message)s',
                        level=logging.DEBUG)
 
    inv = Inventory(config, root)
 
 

if __name__ == "__main__":
    if not sys.version_info[:2] >= (3, 5):
        print('Python 3.5 or greater required')
        sys.exit(2)
    main()
