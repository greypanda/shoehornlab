import logging
from nmap_scan import nmapscan
import ConfigParser
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
        print 'OK'
    inv = Inventory(config,root)
    inv.parse()
if __name__ == "__main__":
    main()
