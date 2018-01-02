# models
from base import Base
from sqlalchemy import Column,Integer,String,Boolean,DateTime,Text
from sqlalchemy_utils import  ChoiceType
from datetime import datetime

__version__ = '0.1'

class Host(Base):
    
            STATUS = [
                (u'discovered',u'Discovered'),
                (u'staging',u'Staging'),
                (u'config',u'Config'),
                (u'testing',u'Testing'),
                (u'production',u'Production'),
                (u'retired',u'Retired'),
                (u'disposed',u'Disposed')
            ]

            TEMPLATE = [
                (u'template',u'Template'),
                (u'vm_image',u'VM Image'),
                (u'container_image',u'Container Image'),
                (u'iso',u'ISO'),
                (u'hardware',u'Hardware'),
                (u'vm',u'VM'),
                (u'container',u'Container')
            ]

            SOURCE = [
                (u'discover',u'Discover'),
                (u'arpwatch',u'Arpwatch'),
                (u'lifecycle',u'Lifecycle'),
                (u'manual',u'Manual')
            ]

            SUBNET = [
                # production subnet -- subject to production monitoring and active DNS
                (u'production',u'Production'),
                # testing subnet -- subject to test monitoring and test DNS
                (u'testing',u'Testing'),
                # staging subnet -- used only for initial installation
                (u'staging',u'Staging'),
                # template subnet -- used mainly for vm images with a fixed IP
                (u'template',u'Template'),

            ]
            __tablename__ = 'hosts'

            id = Column(Integer,primary_key=True)
            status = Column(ChoiceType(STATUS))
            host = Column(String(40))
            domain = Column(String(40))
            ip = Column(String(24))
            subnet = Column(String(32))
            template_type = Column(ChoiceType(TEMPLATE))
            template_file = Column(String(250))
            config_file = Column(String(250))
            mac = Column(String(32))
            vendor = Column(String(64))
            active = Column(Boolean,default=False)
            host_up = Column(Boolean,default=False)
            discovered_host_up = Column(Boolean,default=False)
            retired = Column(Boolean,default=False)
            fact_file = Column(String(250))
            os_type = Column(String(64))

            community_String = Column(String(24))
            snmp_version = Column(String(24))
            ssh_enabled = Column(Boolean,default=False)
            telnet_enabled = Column(Boolean,default=False)
            nrpe_enabled = Column(Boolean,default=False)
            os_found = Column(Text)
            date_first_discovered = Column(DateTime,default=datetime.utcnow)
            date_installed = Column(DateTime)
            date_verified = Column(DateTime)
            date_retired = Column(DateTime)
            date_last_discovered = Column(DateTime)
            date_last_changed = Column(DateTime)
            source = Column(ChoiceType(SOURCE))
            def __repr__(self):
                return "Host: %s, ip: %s, mac: %s" % (self.host, self.ip, self.mac)
