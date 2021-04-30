
import requests
from datetime import datetime
from .models import Tasks, TaskState
import pika
from .consumer import process_jobs
import asyncio
import json
import time
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
    time.sleep(5)
    MAX_JOBS = 50
    print(f"[{datetime.now()}]")
    ready_to_queue = Tasks.objects.filter(scheduled_date__lte=datetime.now(), state=int(TaskState.Active))
    try:
        print("Connecting to rabbitMQ ...")
        connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
        channel = connection.channel()
        channel.queue_declare(queue='task_queue', durable=True)
        print("Successfully Connected.")
    except:
        print("Failed to connect to rabbitMQ.")
        return
    all_jobs = []
    while True:
        if(len(all_jobs) >= MAX_JOBS):
            break
        method, properties, body = channel.basic_get(queue="task_queue")
        if(method is None):
            break
        print(f"Found queued job \"{body.decode()}\"")
        all_jobs.append(json.loads(body.decode()))
        channel.basic_ack(delivery_tag=method.delivery_tag)
    print(f"Found total {len(all_jobs)} jobs in queue.")
    if len(all_jobs) > 0:
        loop = asyncio.get_event_loop()
        future = asyncio.ensure_future(process_jobs(all_jobs))
        results = loop.run_until_complete(future)
    connection.close()
    print("Diconnected.")

