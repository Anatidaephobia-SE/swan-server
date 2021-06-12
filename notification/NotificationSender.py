import asyncio
from asgiref.sync import sync_to_async
from django.core.mail import EmailMessage
class NotificationSender:
    def __init__(self, chunk_size):
        self.chunk_size = chunk_size
    async def send_mail_async(self, title, body, sender, recievers):
        start_idx = 0
        chunked_jobs = []
        while start_idx < len(recievers):
            chunk = recievers[start_idx: start_idx + self.chunk_size]
            start_idx += self.chunk_size
            email = EmailMessage(title, body, sender, chunk, [])
            job = sync_to_async(email.send)(fail_silently=True)
            chunked_jobs.append(job)
        responses = await asyncio.gather(*chunked_jobs)
        print(f"Successfully sent mail {title} to {sum(responses)} out of total {len(recievers)} recievers.")
        return sum(responses)

