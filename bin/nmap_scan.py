#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
    Using libnmap, execute nmap to collect all available hosts.
    Save the xml report in a new file, saving an old one for backup.


"""
from libnmap.process import NmapProcess
import logging

import os

__version__ = "0.1"


def nmapscan(config):
    def mycallback(nmaptask):
        nmaptask = nmap_proc.current_task
        if nmaptask:
            logging.info("Task {0} ({1}):DONE: {2}%".format(nmaptask.name,
                                                            nmaptask.status,
                                                            nmaptask.progress))



    nmap_proc = NmapProcess(targets=config.get('nmap', 'targets'),
                            options=config.get('nmap', 'options'),
                            event_callback=mycallback)
    logging.info("Starting nmap scan")
    nmap_proc.sudo_run()
    logging.info("Ending nmap scan")
    if os.path.isfile(config.get('nmap', 'xml')):
        logging.info("Moving xml to xml-backup")
        os.rename(config.get('nmap', 'xml'), config.get('nmap', 'xml-backup'))
    xml = open(config.get('nmap', 'xml'), 'w')
    xml.write(nmap_proc.stdout)
    xml.close()
    logging.info("nmap scan complete")
    return True
