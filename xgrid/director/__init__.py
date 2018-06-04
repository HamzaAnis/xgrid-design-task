import logging
import logging.config
from core import pycore
import rpyc


class Director(object):
    """The  director  will  send  a  command  to  the  publisher  to  generate  a  packet  with  a  specific  IP  defined  in  the 
    command.  This  process  for  sending  commands  to  remote  machines  is  implemented  using  RPyC.  The 
    publisher  will  send  that  packet to  the  database  which  will  dissect  the  packet """

    def __init__(self, name, hub, session, addr):
        """Constructor

        Arguments:
            name {[str]} -- [Name for the node]
            hub {[HubNode]} -- [Hubnode of which the nodes will be connceted]
            session {[Session]} -- [Session of pycore network]
            addr{[]} -- [Addr of the node]
        """
        logging.config.fileConfig('logging.conf')
        super(Director, self).__init__()
        self.name = name
        self.hub = hub
        self.session = session
        self.node = self.session.addobj(cls=pycore.nodes.CoreNode, name=name)
        self.addr = addr
        self.node.newnetif(self.hub, [self.addr])
        logging.info("Director instance created")

    def init_connections(self, hostname_, port_, hostname_d, port_d):
        logging.info("Initializing publisher service")
        self.publisher_conn = rpyc.connect(hostname_, port_)
        self.port_d = port_d
        self.hostname_d = hostname_d
        logging.info(self.publisher_conn.root.check_database_connection(
            hostname_d, port_d))

    def close_server_connection(self):
        self.publisher_conn.close()

    def send_one(self, ip):
        self.publisher_conn.root.send_one_packet(
            ip, self.hostname_d, self.port_d)

    def send_multiple_packet(self, count):
        self.publisher_conn.root.send_multiple_packets(
            count, self.hostname_d, self.port_d)

    def get_packet_count(self):
        return self.publisher_conn.root.get_packet_count(self.hostname_d, self.port_d)
