from core import pycore
import logging
import logging.config
import json
import rpyc
from rpyc.utils.server import ThreadedServer
from scapy.all import *


class DatabaseService(rpyc.Service):
    """DatabaseService has the rpyc implmentation so send the data to the database"""

    def exposed_check_connection(self):
        return "DATABASE SERVICE CONNECTED"

    def to_string(self, json_arr):
        value = "Ip\t\t  Count\n"
        for v in json_arr:
            value = value+v["ip"]+" -----  "+str(v["count"])+"\n"
        return value

    def check_ip_in_database(self,value):
        logging.info("Checking "+str(value))
    def exposed_get_count_list(self):
        try:
            with open("count_ip.json") as file:
                block_ip_packet_count = json.load(file)
        except IOError:
            logging.critical("Error while loading " + packet_count)
            self.block_ip_packet_count = []
        logging.info(block_ip_packet_count)

        return self.to_string(block_ip_packet_count)

    def exposed_check_multiple_packets(self, packets):
        logging.info("Multiple packets inspection")
        logging.info(len(packets))
        for v in packets:
            value=v.summary()
            logging.info(value)
            self.check_ip_in_database(value)

    def exposed_check_single_packets(self, packet):
        logging.info("Singe Packet inspection")
        value=packet.summary()
        logging.info(value)
        self.check_ip_in_database(value)


class Database(object):
    """ It receives and parse the packets and extract the src 
    IP  from  each  one  and  compare  that  IP  to  the  contents  of  another  file  called  "blacklist_ip_list.txt".  The  file 
    "blacklist_ip_list.txt" will have a list of IPs in it. There will be another file called "count_ip.txt" which maintains the 
    number of packets that are received for each of those blacklist IPs. If the src IP matches one of the blacklist IPs in 
    the file then the count value for that IP in "count_ip.txt" will be incremented."""

    def __init__(self, name, hub, session, addr):
        """Constructor
        Arguments:
            name {[str]} -- [Name for the node]
            hub {[HubNode]} -- [Hubnode of which the nodes will be connceted]
            session {[Session]} -- [Session of pycore network]
            addr{[]} -- [Addr of the node]
        """
        logging.config.fileConfig('logging.conf')
        super(Database, self).__init__()
        self.name = name
        self.hub = hub
        self.session = session
        self.node = self.session.addobj(cls=pycore.nodes.CoreNode, name=name)
        self.node.newnetif(self.hub, [addr])
        logging.info("Database instance created")
        self.block_ips = []
        self.block_ip_packet_count = []
        # self.load_files("blacklist_ip_list.json", "count_ip.json")

    def load_files(self, black_list, packet_count):
        """Loads the json files into the database

        Arguments:
            black_list {[str]} -- [File name for the black list IPs]
            packet_count {[str]} -- [File name for the block ip packet counts]
        """

        try:
            with open(black_list) as file:
                self.block_ips = json.load(file)
        except:
            logging.critical("Error while loading " + black_list)
            self.block_ips = []

        try:
            with open(packet_count) as file:
                self.block_ip_packet_count = json.load(file)
        except IOError:
            logging.critical("Error while loading " + packet_count)
            self.block_ip_packet_count = []

        logging.info("File readed into the database")

        logging.info(self.block_ip_packet_count)
        logging.info(self.block_ips)

    def save_file(self, black_list, packet_count):
        """To save the updated values to the files

        Arguments:
            black_list {[str]} -- [name of the file]
            packet_count {[str]} -- [name of the file]
        """

        with open(black_list, 'w') as file:
            json.dump(self.block_ips, file)
        with open(packet_count, 'w') as file:
            json.dump(self.block_ip_packet_count, file)

    def startServer(self, hostname_, port_):
        """It starts the rpyc server for the database

        Arguments:
            hostname_ {[str]} -- [ip addr]
            port_ {[int]} -- [port for the rpyc]
        """

        self.t = ThreadedServer(
            DatabaseService, hostname=hostname_, port=port_, protocol_config={"allow_public_attrs": True, "allow_all_attrs": True, "allow_pickle ": True, "allow_getattr": True})
        self.t.start()
        logging.info("Server ended")
