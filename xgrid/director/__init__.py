class Director(object):
    """The  director  will  send  a  command  to  the  publisher  to  generate  a  packet  with  a  specific  IP  defined  in  the 
    command.  This  process  for  sending  commands  to  remote  machines  is  implemented  using  RPyC.  The 
    publisher  will  send  that  packet to  the  database  which  will  dissect  the  packet """

    def __init__(self):
        super(Director, self).__init__()
