
import asyncio
from scheduler.models import TaskType, Tasks, TaskState
from socialmedia.twitter import tweet_with_async_upload
from socialmedia.models import SocialMedia
from post.models import Post
from notification.NotificationSender import Instance as notification_sender
from notification.models import Template
from asgiref.sync import sync_to_async
import os
CHUNK_SIZE = 100
async def process_jobs(bodies):
    jobs = []
    job_ids = []
    try:
        os.environ["DJANGO_ALLOW_ASYNC_UNSAFE"] = "true"
        loop = asyncio.get_event_loop()
        for body in bodies:
            if body['type'] == int(TaskType.Twitter):                
                socialmedia = await sync_to_async(SocialMedia.objects.get)(id=body['social_id'])
                post = await sync_to_async(Post.objects.get)(id=body['post_id'])
                job_id = body['job_id']
                job = tweet_with_async_upload(post, socialmedia)
                jobs.append(job)
                job_ids.append(job_id)
            elif body['type'] == int(TaskType.Email):
                job_id = body['job_id']
                mail_id = body['mail']
                mail = await sync_to_async(Template.objects.get)(id=mail_id)
                job = notification_sender.send_mail_async(mail)
                jobs.append(job)
                job_ids.append(job_id)
        responses = await asyncio.gather(*jobs)
        for idx, response in enumerate(responses):
            job_id = job_ids[idx]
            scheduled_task = await sync_to_async(Tasks.objects.get)(id=job_id)
            posted = (scheduled_task.post is not None and response.status_code == 200)
            notified = (scheduled_task.mail is not None and response >= 0.75 * len(bodies[idx]['recievers']))
            if posted or notified:
                scheduled_task.state = int(TaskState.Done)
                scheduled_task.save()
    except Exception as e:
        print(e)
    return responses


