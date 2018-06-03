from core import pycore
import logging
import logging.config


class Database(object):
    """ It receives and parse the packets and extract the src 
    IP  from  each  one  and  compare  that  IP  to  the  contents  of  another  file  called  "blacklist_ip_list.txt".  The  file 
    "blacklist_ip_list.txt" will have a list of IPs in it. There will be another file called "count_ip.txt" which maintains the 
    number of packets that are received for each of those blacklist IPs. If the src IP matches one of the blacklist IPs in 
    the file then the count value for that IP in "count_ip.txt" will be incremented."""

    def print_details(self):
        """To display the self
        """
        print(self.name)
        print(self.hub)

    def __init__(self, name, hub, session):
        """Constructor

        Arguments:
            name {[str]} -- [Name for the node]
            hub {[HubNode]} -- [Hubnode of which the nodes will be connceted]
            session {[Session]} -- [Session of pycore network]
        """
        logging.config.fileConfig('logging.conf')
        super(Database, self).__init__()
        self.name = name
        self.hub = hub
        self.session = session
        self.node = self.session.addobj(cls=pycore.nodes.CoreNode, name=name)
        self.node.newnetif(self.hub, ["10.0.0.3/24"])
        logging.info("Database instance created")
