from database import Database
from director import Director
from publisher import Publisher
from core import pycore
import logging
import logging.config

class Xgrid(object):
    """Starting point/ Main of the program"""

    def __init__(self, hub_name):
        logging.config.fileConfig('logging.conf')
        super(Xgrid, self).__init__()
        self.session = pycore.Session(persistent=True)
        self.hub = self.session.addobj(cls=pycore.nodes.HubNode, name=hub_name)
        self.database = Database("database", self.hub, self.session)
        self.director = Director("director", self.hub, self.session)
        self.publisher = Publisher("publisher", self.hub, self.session)

    def destroy_session(self):
        """
        To destroy the pycore session
        """
        self.session.shutdown()
        logging.info("Session destroyed!")


if __name__ == "__main__":
    X = Xgrid("Root")
    X.destroy_session()