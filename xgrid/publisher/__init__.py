import logging
import logging.config
from core import pycore


class Publisher(object):
    """The  publisher code should  be  able   to  generate  any  packet  with  a  specific  IP. It will send the packet to the database"""

    def __init__(self, name, hub, session):
        """Constructor

        Arguments:
            name {[str]} -- [Name for the node]
            hub {[HubNode]} -- [Hubnode of which the nodes will be connceted]
            session {[Session]} -- [Session of pycore network]
        """
        logging.config.fileConfig('logging.conf')
        super(Publisher, self).__init__()
        self.name = name
        self.hub = hub
        self.session = session
        self.node = self.session.addobj(cls=pycore.nodes.CoreNode, name=name)
        self.node.newnetif(self.hub, ["10.0.0.2/24"])
        logging.info("Publisher instance created")
