import rpyc
import logging
import logging.config
from core import pycore
from rpyc.utils.server import ThreadedServer
from scapy.all import *


class MyPublisherService(rpyc.Service):
    """MyPublisherService has the rpyc implmentation so send the data to the database"""

    def exposed_check_database_connection(self, hostname_, port_):
        logging.info("Initializing database service")
        database_conn = rpyc.connect(hostname_, port_)
        logging.info(database_conn.root.check_connection())
        database_conn.close()

    def exposed_send_one_packet(self, ip, hostname_, port_):
        packet = IP(src=ip, dst="10.0.0.3")
        logging.info("Packet summary: "+packet.summary())
        logging.info(packet[0].getlayer(IP).src)

    def exposed_send_multiple_packets(self, count, hostname_, port_):
        packets = []
        for i in range(0, count):
            ip = '{}.{}.{}.{}'.format(
                *__import__('random').sample(range(0, 255), 4))
            packets.append(IP(src=ip, dst="10.0.0.1"))
        database_conn = rpyc.connect(hostname_, port_)
        result=database_conn.root.check_multiple_packets(packets)
        database_conn.close()

    def exposed_get_packet_count(self, hostname_, port_):
        database_conn = rpyc.connect(hostname_, port_)
        result=database_conn.root.get_count_list()
        database_conn.close()
        return result


class Publisher(object):
    """The  publisher code should  be  able   to  generate  any  packet  with  a  specific  IP. It will send the packet to the database"""

    def __init__(self, name, hub, session, addr):
        """Constructor

        Arguments:
            name {[str]} -- [Name for the node]
            hub {[HubNode]} -- [Hubnode of which the nodes will be connceted]
            session {[Session]} -- [Session of pycore network]
            addr{[]} -- [Addr of the node]
        """
        logging.config.fileConfig('logging.conf')
        super(Publisher, self).__init__()
        self.name = name
        self.hub = hub
        self.session = session
        self.node = self.session.addobj(cls=pycore.nodes.CoreNode, name=name)
        self.node.newnetif(self.hub, [addr])
        logging.info("Publisher instance created")

    def startServer(self, hostname_, port_):
        """It starts the rpyc server for the publisher

        Arguments:
            hostname_ {[str]} -- [ip addr]
            port_ {[int]} -- [port for the rpyc]
        """

        self.t = ThreadedServer(
            MyPublisherService, hostname=hostname_, port=port_)
        self.t.start()
        logging.info("Server ended")

    def init_database_connection(self, hostname_, port_):
        logging.info("Initializing database service")
        self.c = rpyc.connect(hostname_, port_)
        logging.info(self.c.root.check_connection())
        # self.c.close()
