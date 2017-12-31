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
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column,Integer,String,Boolean,DateTime,Text
from sqlalchemy.orm import sessionmaker
from sqlalchemy import update
from libnmap.process import NmapProcess
from libnmap.parser import NmapParser
from datetime import datetime, timedelta
import logging
import sys

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
        self.Base = declarative_base()
        self.source = source

        class Host(self.Base):

            __tablename__ = 'hosts'

            id = Column(Integer,primary_key=True)
            host = Column(String(40))
            ip = Column(String(24))
            mac = Column(String(32))
            vendor = Column(String(64))
            active = Column(Boolean,default=False)
            host_up = Column(Boolean,default=False)
            retired = Column(Boolean,default=False)
            discovering = Column(Boolean)
            ansiblefacts = Column(Text)
            community_String = Column(String(24))
            snmp_version = Column(String(24))
            ssh_enabled = Column(Boolean,default=False)
            telnet_enabled = Column(Boolean,default=False)
            nrpe_enabled = Column(Boolean,default=False)
            os_found = Column(Text)
            date_first_discovered = Column(DateTime,default=datetime.utcnow)
            date_verified = Column(DateTime)
            date_retired = Column(DateTime)
            date_last_discovered = Column(DateTime)
            source = Column(String(120))
            def __repr__(self):
                return "Host: %s, ip: %s, mac: %s" % (self.host, self.ip, self.mac)


        self.config = config
        if not self.engine.has_table('hosts'):
            self.Base.metadata.create_all(self.engine)
        Session = sessionmaker(bind=self.engine)
        self.session = Session()
        self.hostdb = Host

        self.HostCopy = Host

    def parse(self):
        # ####### process nmap report ########
        rep = NmapParser.parse_fromfile(self.config.get('nmap','xml'))
        # for each host
        for host in rep.hosts:
            # is host ip in database?
            test_ip = self.session.query(self.HostCopy).filter_by(ip = host.address).first()
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

                    new_host = self.hostdb(host=temphost,
                                    ip = host.address,
                                    mac = host.mac,
                                    vendor = host.vendor,
                                    discovering = True,
                                    host_up = True,
                                    ssh_enabled = sshactive,
                                    telnet_enabled = telnetactive,
                                    nrpe_enabled = nrpeactive,
                                    os_found = osfound,
                                    source = self.source
                                    )
                    logging.info('Adding new host:' + host.address)
                    self.session.add(new_host)
                    self.session.commit()
                # discovered host is down
                else:
                    logging.debug("Host is down:" + host.address)
                    # don't pollute db with undiscovered hosts
                    pass
            # host in database
            else:
                # is discovered host up?
                if host.is_up:
                    # New: up, Old: up -- no change
                    if test_ip.host_up:
                        logging.debug("Status is up, old status was up -- no change for host:" + host.address)
                    # New: up, Old: down -- change db to up
                    else:
                        logging.debug("Status is up, old status was down, changing status for :" + host.address)
                        rslt = update(self.HostCopy).where(self.HostCopy.ip == host.address).values(host_up = True)

                # discovered status is down
                else:
                    # New down, Old up -- change db status to down
                    if test_ip.host_up:
                        logging.debug("Status is down, old status was up, changing status for:" + host.address)
                        rslt = update(self.HostCopy).where(self.HostCopy.ip == host.address).values(host_up = False)
                    # new down, old down, no change
                    else:
                        logging.debug("Status is down, old status was down, no change for host:" + host.address)
        logging.info("Inventory update complete")
