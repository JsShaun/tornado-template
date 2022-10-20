import pika

# 1. 创建一个到RabbitMQ server的连接，如果连接的不是本机，
# 则在pika.ConnectionParameters中传入具体的ip和port即可
auth = pika.PlainCredentials(username="rabbitmq",password="123456")
conn = pika.BlockingConnection(pika.ConnectionParameters(host="localhost",port="5672",credentials=auth))

# 2. 创建一个channel
channel = conn.channel()

# 指定交换机名称和类型
channel.exchange_declare(exchange='direct_logs', exchange_type='direct')


msg = 'Hello world!'

# 4. 发布消息
channel.basic_publish(exchange='direct_logs',routing_key='log',body=msg)

# 5. 关闭连接
conn.close()