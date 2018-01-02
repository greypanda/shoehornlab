#! /usr/bin/env python
"""
    Packages up all the database functions for the system inventory

    Create database

    Add entries to database

    Search for entries

    Update entries


"""
import sqlalchemy
from time import sleep
from sqlalchemy import create_engine


from sqlalchemy.orm import sessionmaker
from sqlalchemy import update
from libnmap.process import NmapProcess

from datetime import datetime, timedelta
import logging
import sys
from models import Host
from base import Base
__version__ = '0.1'

class Inventory():



    def __init__(self,config,source):
        # ############# prepare database ####################
        ## Connect
        self.engine = create_engine('mysql://' +
                                config.get('database','user') + ':' +
                                config.get('database','password') + '@' +
                                config.get('database','host') + '/' +
                                config.get('database','db'))
        # map
        
        self.source = source

        

        self.config = config
        if not self.engine.has_table('hosts'):
            Base.metadata.create_all(self.engine)
        Session = sessionmaker(bind=self.engine)
        self.session = Session()
        self.hostdb = Host

        self.HostCopy = Host

    def add_host(self,newhost):
        """Add a host
            newhost is a new record
        """
        self.session.add(newhost)
        self.session.commit()
    
    def update_host(self,host):
        """Update a host
            host is a record that was queried
        """
        self.session.commit()

    def query_host(self,host):
        """Query the db for a host
            returns the host record or none
        """
        return self.session.query(self.hostdb).filter_by(ip = host.address).first()
       
       
