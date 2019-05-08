import pika, json

credentials = pika.PlainCredentials('guest', 'guest')
connection = pika.BlockingConnection(pika.ConnectionParameters(
    '127.0.0.1', 5672, '/', credentials))
channel = connection.channel()
# 声明queue
channel.queue_declare(queue='balance')
data = {
    "func_name": "emergency_remind_test",
    "emergency_id": 2,
    "user_id": 102

}
body = json.dumps(data)
# n RabbitMQ a message can never be sent directly to the queue, it always needs to go through an exchange.
channel.basic_publish(exchange='',
                      routing_key='balance',
                      body=body)

connection.close()
