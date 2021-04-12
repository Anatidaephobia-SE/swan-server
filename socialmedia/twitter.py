
import requests
from requests_oauthlib import OAuth1
import os
from .models import SocialMedia
import queue
from asgiref.sync import sync_to_async
import base64

REQUEST_TOKEN_ADDRESS = "https://api.twitter.com/oauth/request_token"
AUTHORIZE_ADDRESS = "https://api.twitter.com/oauth/authorize"
ACCESS_TOKEN = "https://api.twitter.com/oauth/access_token"
UPDATE_STATUS = "https://api.twitter.com/1.1/statuses/update.json"
USERS_LOOKUP = "https://api.twitter.com/1.1/users/lookup.json"
UPLOAD_MEDIA = "https://upload.twitter.com/1.1/media/upload.json"

def Authorize_Address(team_url):
    consumer_key = os.getenv("TWITTER_CONSUMER_KEY")
    consumer_secret = os.getenv("TWITTER_CONSUMER_SECRET")
    auth = OAuth1(client_key=consumer_key, client_secret=consumer_secret,
                  callback_uri=f"http://localhost:8080/workspaces?team_url={team_url}")

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


tweets_queue = queue.Queue()

def Queue_Tweet(post, social_media: SocialMedia):
    try:
        tweets_queue.put((post, social_media), False)
        print(tweets_queue.qsize())
    except queue.Full:
        return "Main queue is full", 403
    return "Successfully queued for tweeting.", 200

def Pop_Tweets():
    try:
        post, social_media = tweets_queue.get(False)
        sync_to_async(Tweet, thread_sensitive=False)(post, social_media)
    except queue.Empty:
        return
    
def Tweet(post, social_media):
    consumer_key = os.getenv("TWITTER_CONSUMER_KEY")
    consumer_secret = os.getenv("TWITTER_CONSUMER_SECRET")
    auth = OAuth1(
        client_key=consumer_key, 
        client_secret=consumer_secret, 
        resource_owner_key=social_media.twitter_oauth_token, 
        resource_owner_secret=social_media.twitter_oauth_token_secret)

    media_ids = []
    for media in post.multimedia.all():
        response = upload_media(media.media, auth)
        if(response.status_code != 200):
            print(response.status_code)
        else:
            media_ids.append(response.json()['media_id_string'])
    
    params = {
        'status': post.caption , #TODO post.text
        "media_ids": ','.join(media_ids),
        'lang' : 'en'
    }
    
    response = requests.post(url=UPDATE_STATUS, params=params, auth=auth)
    print(f"posted tweet with response: {response.status_code} {response.text}")
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

