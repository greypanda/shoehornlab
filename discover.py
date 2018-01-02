"""Run nmap and parse into the database.

"""

import logging
import configparser as ConfigParser
from libnmap.parser import NmapParser
import sys
import os
from nmap_scan import nmapscan
from inventory import Inventory
from datetime import datetime
__version__ = '0.1'
def parse(host,inv):
    
    # is host ip in database?
    
    test_ip = inv.query_host(host)
    # host is not in database
    if not test_ip:
        logging.debug("Host not in database: " + host.address)
        # discovered host is up
        if host.is_up():
            logging.debug("Host is up:" + host.address)
            # nmap may not return hostname
            if len(host.hostnames) > 0:
                temphost = host.hostnames[0]
            else:
                temphost = None
                logging.debug("Host has no hostname:" + host.address)
            # get shost, telnet, nrpe status ( if standard ports are used)
            sshactive = False
            telnetactive = False
            nrpeactive = False
            osfound = ""
            for s in host.services:
                if s.port == 22:
                    sshactive = True
                if s.port == 23:
                    telnetactive = True
                if s.port == 5666:
                    nrpeactive = True
                # get OS
            if host.os_fingerprinted:
                
                if len(host.os.osmatches) > 0:
                    osfound = host.os.osmatches[0].name

            new_host = inv.hostdb(host=temphost,
                                  ip = host.address,
                                  mac = host.mac,
                                  vendor = host.vendor,
                                  host_up = True,
                                  ssh_enabled = sshactive,
                                  telnet_enabled = telnetactive,
                                  nrpe_enabled = nrpeactive,
                                  os_found = osfound,
                                  source = inv.source,
                                  date_last_discovered = datetime.utcnow(),
                                  discovered_host_up = True,
                                  status=u'discovered',
                                  subnet=u'production',
                                  )
            logging.info('Adding new host:' + host.address)
            inv.add_host(new_host)
        # discovered host is down
        else:
            logging.debug("Host is down:" + host.address)
            # don't pollute db with undiscovered hosts
            pass
    # host in database
    else:
        logging.debug("Updating existing host:" + host.address)
        test_ip.discovered_host_up = host.is_up()
        test_ip.date_last_discovered = datetime.utcnow()
        inv.update_host(test_ip)
     
    logging.info("Inventory update complete")
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
    # nmap execution can be turned off with a config entry
    # if nmap = False, we just use the existing xml file
    if config.getboolean('options','nmap'):
        if nmapscan(config):
            print('OK')
    inv = Inventory(config, root)
    rep = NmapParser.parse_fromfile(config.get('nmap','xml'))
        # for each host
    for host in rep.hosts:
        parse(host,inv)
if __name__ == "__main__":
    if not sys.version_info[:2] >= (3, 5):
        print('Python 3.5 or greater required')
        sys.exit(2)
    main()
