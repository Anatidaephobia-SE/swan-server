import asyncio
from os import terminal_size
from asgiref.sync import sync_to_async
from django.core.mail import EmailMessage, send_mail
from .reciever_retrieval import recieve_mail_list
class NotificationSender:
    def __init__(self):
        pass
    async def send_mail_async(self, template):
        start_idx = 0
        jobs = []
        recievers = recieve_mail_list(template.reciviers)
        for reciever in recievers:
            job = sync_to_async(send_mail)(template, reciever)
            jobs.append(job)
        responses = await asyncio.gather(*jobs)
        print(f"Successfully sent mail {template.name} to {sum(responses)} out of total {len(recievers)} recievers.")
        return sum(responses)
    def send_mail(self, template, reciever_data):
        body = template.body
        api_vars = reciever_data.keys()
        email = reciever_data['email']
        for var in api_vars:
            if var == "email":
                continue
            body = body.replace(f'%^{var}^%', reciever_data[f'{var}'])
        message = EmailMessage(template.subject, body, template.sender, [email], [])
        return message.send(fail_silently=True)

Instance  = NotificationSender()
