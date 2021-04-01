
REQUEST_TOKEN_ADDRESS = "https://api.twitter.com/oauth/request_token"
AUTHORIZE_ADDRESS = "https://api.twitter.com/oauth/authorize"
ACCESS_TOKEN = "https://api.twitter.com/oauth/access_token"
import requests
from requests_oauthlib import OAuth1
import os

def Authorize_Address():
    consumer_key = os.getenv("TWITTER_CONSUMER_KEY")
    consumer_secret = os.getenv("TWITTER_CONSUMER_SECRET")
    auth = OAuth1(client_key=consumer_key, client_secret=consumer_secret)
    print(consumer_key)
    response = requests.post(url=REQUEST_TOKEN_ADDRESS, auth=auth, params={'lang': 'en'})
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
    response=requests.post(ACCESS_TOKEN, params=params)
    return response.text, response.status_code


    