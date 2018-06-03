import logging
import logging.config
from core import pycore


class Director(object):
    """The  director  will  send  a  command  to  the  publisher  to  generate  a  packet  with  a  specific  IP  defined  in  the 
    command.  This  process  for  sending  commands  to  remote  machines  is  implemented  using  RPyC.  The 
    publisher  will  send  that  packet to  the  database  which  will  dissect  the  packet """

    def __init__(self, name, hub, session,addr):
        logging.config.fileConfig('logging.conf')
        super(Director, self).__init__()
        self.name = name
        self.hub = hub
        self.session = session
        self.node = self.session.addobj(cls=pycore.nodes.CoreNode, name=name)
        self.addr=addr
        self.node.newnetif(self.hub, [self.addr])
        logging.info("Director instance created")
