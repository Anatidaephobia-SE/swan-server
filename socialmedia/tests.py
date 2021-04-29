from django.test import TestCase, RequestFactory
from rest_framework.test import APIClient, APITestCase
from .models import SocialMedia
from team.models import Team
from users.models import User
from .views import twitter_request_authorize
from users.authenticators import generate_access_token
# Create your tests here.
class SocialMediaModelTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        # Set up non-modified objects used by all test methods
        user = User.objects.create(email="hadi@gmail.com")
        t = Team.objects.create(url="team11", name="hahaha", head=user)
        t2 = Team.objects.create(url="team12", name="hahahaha", head=user)
        t3 = Team.objects.create(url="team13", name="hahah", head=user)
        t4 = Team.objects.create(url="team14", name="haha", head=user)
        
        SocialMedia.objects.create(team=t) #1
        SocialMedia.objects.create(team=t2, twitter_oauth_token="token1") #2
        SocialMedia.objects.create(team=t3, twitter_oauth_token="token1", twitter_oauth_token_secret="token1-secret") #3
        SocialMedia.objects.create(team=t4, twitter_oauth_token="token1", twitter_oauth_token_secret="token1-secret", twitter_name="account_name", twitter_user_id="2314") #4


    def test_Null_twitter_oauth_token_field(self):
        social_media = SocialMedia.objects.get(id=1)
        self.assertEqual(social_media.twitter_oauth_token, None)
    def test_twitter_oauth_token_field(self):
        social_media = SocialMedia.objects.get(id=2)
        self.assertEqual(social_media.twitter_oauth_token, "token1")
    def test_Null_twitter_oauth_token_secret_field(self):
        social_media = SocialMedia.objects.get(id=3)
        self.assertEqual(social_media.twitter_oauth_token, "token1")
        self.assertEqual(social_media.twitter_oauth_token_secret, "token1-secret")
    def test_full_model(self):
        social_media = SocialMedia.objects.get(id=4)
        self.assertEqual(social_media.twitter_oauth_token, "token1")
        self.assertEqual(social_media.twitter_oauth_token_secret, "token1-secret")
        self.assertEqual(social_media.twitter_name, "account_name")
        self.assertEqual(social_media.twitter_user_id, "2314")

class TwitterRequestAuthorizeTest(APITestCase):
    @classmethod
    def setUp(self):
        user = User.objects.create(email="hadi@gmail.com")
        user2 = User.objects.create(email="had234i@gmail.com")
        self.team1 = Team.objects.create(url="team11", name="hahaha", head=user)
        self.team2 = Team.objects.create(url="team12", name="hahaha", head=user2)
        client = APIClient()
        client.post('/api/users/signup/', data = {'email' : 'hadi@gmail.com', 'password' : '123456', 'confirm_password' : '123456'})
        user = User.objects.get(email = 'hadi@gmail.com')
        user.verified = True
        user.save(update_fields = ['verified'])
        self.token = generate_access_token(user)
    def test_request_authorize(self):
        client = APIClient()
        response = client.post(
            "/api/v1.0.0/socialmedia/twitter/authorize/request", 
            data={"team_id" : self.team1.id}, 
            **{'HTTP_Authorization' : 'bear ' + self.token}
        )
        self.assertEqual(response.status_code, 200)
    def test_request_authorize_failure(self):
        client = APIClient()
        response = client.post(
            "/api/v1.0.0/socialmedia/twitter/authorize/request", 
            data={"team_id" : 45126}, 
            **{'HTTP_Authorization' : 'bear ' + self.token}
        )
        self.assertEqual(response.status_code, 404)
    def test_request_authorize_permission_denied(self):
        client = APIClient()
        response = client.post(
            "/api/v1.0.0/socialmedia/twitter/authorize/request", 
            data={"team_id" : self.team2.id}, 
            **{'HTTP_Authorization' : 'bear ' + self.token}
        )
        self.assertEqual(response.status_code, 403)

class TwitterGetUserTest(APITestCase):
    @classmethod
    def setUp(self):
        user = User.objects.create(email="hadi@gmail.com")
        self.team = Team.objects.create(url="team11", name="hahaha", head=user)
        self.team2 = Team.objects.create(url="team22", name="hahaha", head=user)
        self.team3 = Team.objects.create(url="team33", name="hahaha", head=user)
        SocialMedia.objects.create(team=self.team, twitter_oauth_token="token1", twitter_oauth_token_secret="token1-secret", twitter_name="account_name", twitter_user_id="1371442090245304321")
        SocialMedia.objects.create(team=self.team3)
        self.token = generate_access_token(user)
    def test_get_user(self):
        client = APIClient()
        response = client.get(
            "/api/v1.0.0/socialmedia/twitter/accounts", 
            data={"team_id" : self.team.id}, 
            **{'HTTP_Authorization' : 'bearer ' + self.token}
        )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data['screen_name'], "Dev23080567")
    def test_request_get_user_failure(self):
        client = APIClient()
        response = client.get(
            "/api/v1.0.0/socialmedia/twitter/accounts", 
            data={"team_id" : 567}, 
            **{'HTTP_Authorization' : 'bearer ' + self.token}
        )
        self.assertEqual(response.status_code, 404)
    def test_request_get_user_without_social_media(self):
        client = APIClient()
        response = client.get(
            "/api/v1.0.0/socialmedia/twitter/accounts", 
            data={"team_id" : self.team2.id}, 
            **{'HTTP_Authorization' : 'bearer ' + self.token}
        )
        self.assertEqual(response.status_code, 404)
    def test_request_get_user_without_twitter(self):
        client = APIClient()
        response = client.get(
            "/api/v1.0.0/socialmedia/twitter/accounts", 
            data={"team_id" : self.team3.id}, 
            **{'HTTP_Authorization' : 'bearer ' + self.token}
        )
        self.assertEqual(response.status_code, 403)