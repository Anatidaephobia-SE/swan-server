from django.test import TestCase, Client
from django.urls import reverse
from .models import Team
from users.models import User

class TestViews(TestCase):

    def setUp(self):
        client = Client()
        client.post('/api/users/signup/', data = {'email' : 'amir.j1881@gmail.com', 'password' : '123456', 'confirm_password' : '123456'})
        user = User.objects.get(email = 'amir.j1881@gmail.com')
        user.verified = True
        user.save(update_fields = ['verified'])
        
        login_resp = client.post('/api/users/login/', data = {'email' : 'amir.j1881@gmail.com', 'password' : '123456'})
        token = login_resp.data.get('token')


    def test_create_team(self):
        
        client_unauth = Client()

        unauthorized_resp = client_unauth.post('/api/team/create_team/', data = {'name' : 'test_name', 'url' : 'test_url'})
        assert unauthorized_resp.status_code == 403
        
        self.setUp()

        create_team_resp = self.client.post('/api/team/create_team/', data = {'name' : 'test_name', 'url' : 'test_url'}, **{'HTTP_Authorization' : 'bear ' + self.token})

        assert create_team_resp.status_code == 200
        assert 'test_name' == create_team_resp.json()['team']['name']
        assert 'test_url' == create_team_resp.json()['team']['url']

        create_team_resp = self.client.post('/api/team/create_team', data = {'url' :'_test_url'})
        assert create_team_resp.status_code == 400

        create_team_resp = self.client.post('/api/team/create_team', data = {'name' : 'test_name', 'url' : 'test_url'})
        assert create_team_resp.status_code == 400

    def test_invite_user(self):
        client_unauth = Client()

        unauth_resp = self.client_unauth.post('/api/team/invite_user/', data = {'username' : 'amir.j1883@gmail.com'})
        assert unauth_resp.status_code == 403

        self.setUp()

        client.post('/api/users/signup/', data = {'email' : 'amir.j1882@gmail.com', 'password' : '123456', 'confirm_password' : '123456'})
        user = User.objects.get(email = 'amir.j1882@gmail.com')
        user.verified = True
        user.save(update_fields = ['verified'])

        invite_resp = self.client.post('/api/team/invite_user/', data = {'team_url' : 'test_url', 'username' : 'amir.j1882@gmail.com'}, **{'HTTP_Authorization' : 'bear ' + self.token})
        assert invite_resp.status_code == 404

        create_team_resp = self.client.post('/api/team/create_team/', data = {'name' : 'test_name', 'url' : 'test_url'}, **{'HTTP_Authorization' : 'bear ' + self.token})

        invite_resp2 = self.client.post('/api/team/invite_user/', data = {'team_url' : 'test_url', 'username' : 'amir.j1882@gmail.com'}, **{'HTTP_Authorization' : 'bear ' + self.token})

        assert invite_resp2.status_code == 200

        
        invite_resp3 = self.client.post('/api/team/invite_user/', data = {'team_url' : 'test_url', 'username' : 'nothing'}, **{'HTTP_Authorization' : 'bear ' + self.token})
        assert invite_resp3.status_code == 404