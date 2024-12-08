import time
import pika
from pika.adapters.blocking_connection import BlockingChannel


class Worker:
    def __init__(self):
        self.connection = pika.BlockingConnection(
            pika.ConnectionParameters(host='localhost', port=10002)
        )
        self.channel: BlockingChannel = self.connection.channel()

        self.channel.queue_declare(
            queue='remove_background_queue',
            durable=False
        )

    def start_consuming(self) -> None:
        self.channel.basic_qos(prefetch_count=1)
        self.channel.basic_consume(
            queue='remove_background_queue',
            on_message_callback=self.__process_image)

        self.channel.start_consuming()

    def __process_image(self, channel, method, properties, body) -> None:
        print(f"[x] Received {body.decode()}")
        time.sleep(body.count(b'.'))
        print(" [x] Done")
        channel.basic_ack(delivery_tag=method.delivery_tag)

def main():
    worker = Worker()
    worker.start_consuming()

if __name__ == '__main__':
    main()
