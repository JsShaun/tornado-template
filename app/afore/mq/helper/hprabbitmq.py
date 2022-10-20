import pika



class RabbitMQ:

    def __init__(self,username,password,host,port) -> None:
        auth = pika.PlainCredentials(username=username,password=password)
        self.conn = pika.BlockingConnection(pika.ConnectionParameters(host=host,port=port,credentials=auth))



    @property
    def channel(self):
        return self.conn.channel()


    def __del__(self):
        self.conn.close()





