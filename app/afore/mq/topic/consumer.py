import pika

auth = pika.PlainCredentials(username="rabbitmq",password="123456")
conn = pika.BlockingConnection(pika.ConnectionParameters(host="localhost",port="5672",credentials=auth))

# 2. 创建一个channel
channel = conn.channel()

# 指定交换机名称和类型

channel.exchange_declare(exchange='topic_logs', exchange_type='topic')

# 使用RabbitMQ给自己生成一个专属于自己的queue
result = channel.queue_declare(queue='', exclusive=True)
queue_name = result.method.queue

binding_key = 'anonymous.*'
channel.queue_bind(exchange='topic_logs', queue=queue_name,routing_key=binding_key)


print(' [*] Waiting for logs. To exit press CTRL+C')

def callback(ch, method, properties, body):
    print("ch: ",ch)
    print("method: ",method)
    print("properties: ",properties)
    print("body: ",body)



channel.basic_consume(queue=queue_name, on_message_callback=callback, auto_ack=True)

channel.start_consuming()