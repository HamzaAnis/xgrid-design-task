from database import Database
from director import Director
from publisher import Publisher
from core import pycore
import logging
import logging.config
import threading
import rpyc
from time import sleep


class Xgrid(object):
    """Starting point/ Main of the program"""

    def __init__(self, hub_name):
        logging.config.fileConfig('logging.conf')
        super(Xgrid, self).__init__()
        self.session = pycore.Session(persistent=True)
        self.hub = self.session.addobj(cls=pycore.nodes.HubNode, name=hub_name)
        self.database = Database("database", self.hub,
                                 self.session, "10.0.0.3/24")
        self.director = Director("director", self.hub,
                                 self.session, "10.0.0.1/24")
        self.publisher = Publisher(
            "publisher", self.hub, self.session, "10.0.0.2/24")

    def destroy_session(self):
        """
        To destroy the pycore session
        """
        self.session.shutdown()
        logging.info("Session destroyed!")

    def test_ping(self):
        """To check the connection
        """
        # Publisher
        err = self.director.node.icmd(["ping", "-c", "5", "10.0.0.2"])
        if err != 0:
            logging.critical("Publisher not reached!")

        # Database
        err = self.director.node.icmd(["ping", "-c", "5", "10.0.0.3"])
        if err != 0:
            logging.critical("Database not reached!")


if __name__ == "__main__":
    X = Xgrid("Root")
    # X.test_ping()
    try:
        t1 = threading.Thread(
            group=None, target=X.publisher.startServer, name="RpyC server", args=("10.0.0.2", 18800))
        t1.start()
    except Exception as e:
        logging.critical(e)
        raise e

    X.director.signal_publisher("10.0.0.2", 18800)
    # Input to terminate the rpyc server
    while(1):
        if(input() == 1):
            break
    if t1.isAlive():
        try:
            t1._Thread__stop()
            logging.info("Server thread Stopped")
        except:
            print("Yes")
            logging.critical("Not terminated")
    X.destroy_session()
