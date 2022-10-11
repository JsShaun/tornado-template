import time
from datetime import datetime


localtime = lambda:datetime.now()
timestamp = lambda:int(time.time())


class Web:
    HOST = "0.0.0.0"
    PORT = 5016

class UDP:
    HOST = "0.0.0.0"
    PORT = 5016