import rpyc
import logging
import logging.config
from core import pycore
from rpyc.utils.server import ThreadedServer


class MyPublisherService(rpyc.Service):
    """MyPublisherService has the rpyc implmentation so send the data to the database"""

    def exposed_check_connection(self):
        return "CONNECTED"


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

    def startServer(self):
        self.t = ThreadedServer(
            MyPublisherService, hostname="10.0.0.1", port=18800)
        self.t.start()
        logging.info("Server ended")
