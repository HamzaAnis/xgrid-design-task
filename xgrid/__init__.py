from database import Database
from director import Director
from publisher import Publisher
from core import pycore
import logging
import logging.config
import threading
import rpyc
from time import sleep
from termcolor import cprint


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
            group=None, target=X.publisher.startServer, name="RpyC publisher server", args=("10.0.0.2", 18800))
        t2 = threading.Thread(
            group=None, target=X.database.startServer, name="RpyC database server", args=("10.0.0.3", 18801))
        t1.start()
        t2.start()
    except Exception as e:
        logging.critical(e)
        raise e

    X.director.init_connections("10.0.0.2", 18800, "10.0.0.3", 18801)
    # Input to terminate the rpyc server
    while(1):
        cprint("\nEnter 1 to generate a packet with specific IP.\n" +
               "Enter 2 to generate a number of packets with random IPs.\n" +
               "Enter 3 to list count_ip.txt.\n" +
               "Enter 4 to exit.", "red")
        choice = input()
        if choice == 1:
            pass
        elif choice == 2:
            print("2 pressed")
        elif choice == 3:
            print("3 pressed")
        else:
            break
    if t1.isAlive():
        try:
            t1._Thread__stop()
            t2._Thread__stop()
            X.director.close_server_connection()
            logging.info("Rpyc server thread Stopped")
        except Exception as e:
            logging.critical(e)
    X.destroy_session()
