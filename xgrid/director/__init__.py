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

    def signal_publisher(self):
        logging.info("Checking connection")
        self.c = rpyc.connect("10.0.0.1", 18800)
        logging.info(self.c.root.check_connection())
