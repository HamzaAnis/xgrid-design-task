class Database(object):
    """ It receives and parse the packets and extract the src 
    IP  from  each  one  and  compare  that  IP  to  the  contents  of  another  file  called  "blacklist_ip_list.txt".  The  file 
    "blacklist_ip_list.txt" will have a list of IPs in it. There will be another file called "count_ip.txt" which maintains the 
    number of packets that are received for each of those blacklist IPs. If the src IP matches one of the blacklist IPs in 
    the file then the count value for that IP in "count_ip.txt" will be incremented."""

    def __init__(self, arg):
        super(Database, self).__init__()
        self.arg = arg
        print("Database",self.arg)
