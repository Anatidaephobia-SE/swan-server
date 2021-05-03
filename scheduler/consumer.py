
import asyncio
from scheduler.models import TaskType
from socialmedia.twitter import tweet_with_async_upload
from socialmedia.models import SocialMedia
from post.models import Post
from asgiref.sync import sync_to_async
import os
async def process_jobs(bodies):
    jobs = []
    posts = []
    try:
        os.environ["DJANGO_ALLOW_ASYNC_UNSAFE"] = "true"
        loop = asyncio.get_event_loop()
        for body in bodies:
            if body['type'] == int(TaskType.Twitter):                
                socialmedia = await sync_to_async(SocialMedia.objects.get)(id=body['social_id'])
                post = await sync_to_async(Post.objects.get)(id=body['post_id'])
                job = tweet_with_async_upload(post, socialmedia)
                jobs.append(job)
                posts.append(post)
        responses = await asyncio.gather(*jobs)
    except Exception as e:
        print(e)
    return responses


