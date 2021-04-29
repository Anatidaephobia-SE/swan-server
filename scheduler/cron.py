
import requests
from datetime import datetime
from .models import Tasks, TaskState
import pika
def Queue_jobs():
    print(f"[{datetime.now()}]")
    ready_to_queue = Tasks.objects.filter(scheduled_date__lte=datetime.now(), state=int(TaskState.Active))
    print(f"Found {len(ready_to_queue)} tasks to be queued.")
    try:
        print("Connecting to rabbitMQ ...")
        connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
        channel = connection.channel()
        channel.queue_declare(queue='task_queue', durable=True)
        print("Successfully Connected.")
    except:
        print("Failed to connect to rabbitMQ.")
        return
    for item in list(ready_to_queue):
        print(f"pushing job id {item.id} to the queue")
        channel.basic_publish(
            exchange='',
            routing_key="task_queue",
            body=item.body,
            properties=pika.BasicProperties(
                delivery_mode = 2, # make message persistent
            )
        )
        item.state = int(TaskState.Queued)
        item.save()
    connection.close()
    print("Diconnected.")
def Dequeue_Jobs():
    print(f"Dequeue {datetime.now()}") 