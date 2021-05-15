
import requests
from datetime import datetime
from .models import Tasks, TaskState
import pika
from .consumer import process_jobs
import asyncio
import json
import time
import os
from .logger import printlog
QUEUE_JOBS_LOG_FILE = "/swan/scheduler/logs/queue_jobs_printlog.log"
DEQUEUE_JOBS_LOG_FILE = "/swan/scheduler/logs/queue_jobs_printlog.log"
def Queue_jobs():
    print(f"[{datetime.now()}]")
    printlog(QUEUE_JOBS_LOG_FILE, f"[{datetime.now()}]")
    ready_to_queue = Tasks.objects.filter(scheduled_date__lte=datetime.now(), state=int(TaskState.Active))
    print(f"Found {len(ready_to_queue)} tasks to be queued.")
    printlog(QUEUE_JOBS_LOG_FILE, f"Found {len(ready_to_queue)} tasks to be queued.")
    try:
        print("Connecting to rabbitMQ ...")
        printlog(QUEUE_JOBS_LOG_FILE, "Connecting to rabbitMQ ...")
        credentials = pika.PlainCredentials("root", "Swan@2021")
        parameters = pika.ConnectionParameters("stage-rabbitmq",
                                   5672,
                                   '/',
                                   credentials)
        connection = pika.BlockingConnection(parameters)
        channel = connection.channel()
        channel.queue_declare(queue='task_queue', durable=True)
        print("Successfully Connected.")
        printlog(QUEUE_JOBS_LOG_FILE, "Successfully Connected.")
    except:
        print("Failed to connect to rabbitMQ.")
        printlog(QUEUE_JOBS_LOG_FILE, "Failed to connect to rabbitMQ.")
        return
    for item in list(ready_to_queue):
        print(f"pushing job id {item.id} to the queue")
        printlog(QUEUE_JOBS_LOG_FILE, "pushing job id {item.id} to the queue")
        body = json.loads(item.body)
        body["job_id"] = item.id
    
        channel.basic_publish(
            exchange='',
            routing_key="task_queue",
            body=json.dumps(body),
            properties=pika.BasicProperties(
                delivery_mode = 2, # make message persistent
            )
        )
        item.state = int(TaskState.Queued)
        item.save()
    connection.close()
    print("Diconnected.")
    printlog(QUEUE_JOBS_LOG_FILE, "Diconnected.")
def Dequeue_Jobs():
    time.sleep(5)
    MAX_JOBS = 50
    print(f"[{datetime.now()}]")
    try:
        print("Connecting to rabbitMQ ...")
        printlog(DEQUEUE_JOBS_LOG_FILE, "Connecting to rabbitMQ ...")
        credentials = pika.PlainCredentials("root", "Swan@2021")

        parameters = pika.ConnectionParameters("stage-rabbitmq",
                                   5672,
                                   '/',
                                   credentials)
        connection = pika.BlockingConnection(parameters)
        channel = connection.channel()
        channel.queue_declare(queue='task_queue', durable=True)
        print("Successfully Connected.")
        printlog(DEQUEUE_JOBS_LOG_FILE, "Successfully Connected.")
    except Exception as e:
        print("Failed to connect to rabbitMQ. ", e)
        printlog(DEQUEUE_JOBS_LOG_FILE, f"Failed to connect to rabbitMQ. {e}")
        return
    all_jobs = []
    while True:
        if(len(all_jobs) >= MAX_JOBS):
            break
        method, properties, body = channel.basic_get(queue="task_queue")
        if(method is None):
            break
        print(f"Found queued job \"{body.decode()}\"")
        printlog(DEQUEUE_JOBS_LOG_FILE, f"Found queued job \"{body.decode()}\"")
        all_jobs.append(json.loads(body.decode()))
        channel.basic_ack(delivery_tag=method.delivery_tag)
    print(f"Found total {len(all_jobs)} jobs in queue.")
    printlog(DEQUEUE_JOBS_LOG_FILE, f"Found total {len(all_jobs)} jobs in queue.")
    if len(all_jobs) > 0:
        loop = asyncio.get_event_loop()
        future = asyncio.ensure_future(process_jobs(all_jobs))
        results = loop.run_until_complete(future)
    connection.close()
    print("Diconnected.")
    printlog(DEQUEUE_JOBS_LOG_FILE, f"Diconnected.")

