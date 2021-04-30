
import requests
from requests_oauthlib import OAuth1
import os
from .models import SocialMedia
import queue
import asyncio
import base64
from scheduler.scheduler import Scheduler
from scheduler.models import TaskType
import datetime
from rest_framework.response import Response
from asgiref.sync import sync_to_async

REQUEST_TOKEN_ADDRESS = "https://api.twitter.com/oauth/request_token"
AUTHORIZE_ADDRESS = "https://api.twitter.com/oauth/authorize"
ACCESS_TOKEN = "https://api.twitter.com/oauth/access_token"
UPDATE_STATUS = "https://api.twitter.com/1.1/statuses/update.json"
USERS_LOOKUP = "https://api.twitter.com/1.1/users/lookup.json"
UPLOAD_MEDIA = "https://upload.twitter.com/1.1/media/upload.json"

def Authorize_Address(team_url, modified):
    consumer_key = os.getenv("TWITTER_CONSUMER_KEY")
    consumer_secret = os.getenv("TWITTER_CONSUMER_SECRET")
    auth = OAuth1(client_key=consumer_key, client_secret=consumer_secret,
                  callback_uri=f"http://localhost:8080/dispatch?team_url={team_url}&modify={modified}")

    response = requests.post(url=REQUEST_TOKEN_ADDRESS,
                             auth=auth, params={'lang': 'en'})
    if(response.status_code == 200):
        address = AUTHORIZE_ADDRESS + "?" + response.text
        return address, 200
    else:
        return response.text, response.status_code


def Get_Access_Token(oauth_token, oauth_verifier):
    params = {
        "oauth_token": oauth_token,
        "oauth_verifier": oauth_verifier,
        'lang': 'en'
    }
    response = requests.post(ACCESS_TOKEN, params=params)
    return response.text, response.status_code

    
def Tweet(post, social_media, schedule_for_async = False):
    consumer_key = os.getenv("TWITTER_CONSUMER_KEY")
    consumer_secret = os.getenv("TWITTER_CONSUMER_SECRET")
    auth = OAuth1(
        client_key=consumer_key, 
        client_secret=consumer_secret, 
        resource_owner_key=social_media.twitter_oauth_token, 
        resource_owner_secret=social_media.twitter_oauth_token_secret)
    
    media_list = post.multimedia.all()
    if schedule_for_async:
        sc = Scheduler()
        sc.schedule(post, social_media, TaskType.Twitter, datetime.datetime.now())
        return Response(data={"msg": "Scheduled for at most 1 minute later."}, status=200)
    else:
        responses = [upload_media(media, auth) for media in media_list]

    
    media_ids = []
    for idx, response in enumerate(responses):
        if(response.status_code != 200):
            print(f"Error uploading media with id {media_list[idx].id} in post {post.id} with error code {response.error_code}.")
        else:
            media_ids.append(response.json()['media_id_string'])
    
    params = {
        'status': post.caption ,
        "media_ids": ','.join(media_ids),
        'lang' : 'en'
    }
    
    response = requests.post(url=UPDATE_STATUS, params=params, auth=auth)
    if(response.status_code == 200):
        print(f"posted tweet with response \"{response.status_code} {response.text}\"")
    else:
        print(f"Error posting post {post.id} in twitter with response \"{response.status_code} {response.text}\".")
    return response

def Get_Twitter_User(user_id):
    consumer_key = os.getenv("TWITTER_CONSUMER_KEY")
    consumer_secret = os.getenv("TWITTER_CONSUMER_SECRET")
    params = {"user_id": user_id}
    auth = OAuth1(client_key=consumer_key, client_secret=consumer_secret)
    response = requests.get(USERS_LOOKUP, params=params, auth=auth)
    return response

def upload_media(media, auth):
    with media.open(mode='rb') as file:
        data = file.read()
        response = requests.post(UPLOAD_MEDIA, files={"media": data}, auth=auth)
        return response
    raise FileNotFoundError(f"Cannot open media file {media}")

#async 
async def asyncronous_upload_media(media_list, auth):
    jobs = []
    for media in media_list:
        job = sync_to_async(upload_media)(media.media, auth)
        jobs.append(job)
    responses = await asyncio.gather(*jobs)
    return responses

#This function cannot be called from django views. should called from crons.
async def tweet_with_async_upload(post, social_media):
    consumer_key = os.getenv("TWITTER_CONSUMER_KEY")
    consumer_secret = os.getenv("TWITTER_CONSUMER_SECRET")
    auth = OAuth1(
        client_key=consumer_key, 
        client_secret=consumer_secret, 
        resource_owner_key=social_media.twitter_oauth_token, 
        resource_owner_secret=social_media.twitter_oauth_token_secret)
    media_list = post.multimedia.all()
    try:
        responses = await asyncronous_upload_media(media_list, auth)
    except Exception as e:
        print("Error on asyncio upload media!", e)
        responses =[]
    media_ids = []
    for idx, response in enumerate(responses):
        if(response.status_code != 200):
            print(f"Error uploading media with id {media_list[idx].id} in post {post.id} with error code {response.error_code}.")
        else:
            media_ids.append(response.json()['media_id_string'])
    params = {
        'status': post.caption ,
        "media_ids": ','.join(media_ids),
        'lang' : 'en'
    }
    response = requests.post(url=UPDATE_STATUS, params=params, auth=auth)
    if(response.status_code == 200):
        print(f"posted tweet with response \"{response.status_code} {response.text}\"")
    else:
        print(f"Error posting post {post.id} in twitter with response \"{response.status_code} {response.text}\".")
    return response
    
