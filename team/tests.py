from django.test import TestCase, Client
from django.urls import reverse
from .models import Team
from users.models import User

class TestViews(TestCase):

    def setUp(self):
        self.client = Client()
        signup_url = reverse("users-urls:signup")
        login_url = reverse("users-urls:login")
        self.client.post(signup_url, data = {'email' : 'amir.j1881@gmail.com', 'password' : '123456', 'confirm_password' : '123456'})
        user = User.objects.get(email = 'amir.j1881@gmail.com')
        user.verified = True
        user.save(update_fields = ['verified'])
        
        login_resp = self.client.post(login_url, data = {'email' : 'amir.j1881@gmail.com', 'password' : '123456'})
        self.token = login_resp.data.get('token')

    def test_create_team(self):
        
        client_unauth = Client()
        create_team_url = reverse("team-urls:createTeam")
        unauthorized_resp = client_unauth.post(create_team_url, data = {'name' : 'test_name', 'url' : 'test_url'})
        self.assertEqual(unauthorized_resp.status_code, 403)
        
        self.setUp()

        create_team_resp = self.client.post(create_team_url, data = {'name' : 'test_name', 'url' : 'test_url'}, **{'HTTP_Authorization' : 'bear ' + self.token})

        self.assertEqual(create_team_resp.status_code, 200)
        assert 'test_name' == create_team_resp.json()['team']['name']
        assert 'test_url' == create_team_resp.json()['team']['url']

        create_team_resp = self.client.post(create_team_url, data = {'url' :'_test_url'}, **{'HTTP_Authorization' : 'bear ' + self.token})
        self.assertEqual(create_team_resp.status_code, 400)

    def test_invite_user(self):
        client_unauth = Client()
        invite_url = reverse("team-urls:inviteUser")
        unauth_resp = client_unauth.post(invite_url, data = {'username' : 'amir.j1883@gmail.com'})
        self.assertEqual(unauth_resp.status_code, 403)
        create_team_url = reverse("team-urls:createTeam")
        self.setUp()
        signup_url = reverse("users-urls:signup")
        self.client.post(signup_url, data = {'email' : 'amir.j1882@gmail.com', 'password' : '123456', 'confirm_password' : '123456'})
        user = User.objects.get(email = 'amir.j1882@gmail.com')
        user.verified = True
        user.save(update_fields = ['verified'])

        invite_resp = self.client.post(invite_url, data = {'team_id' : '1234', 'username' : 'amir.j1882@gmail.com'}, **{'HTTP_Authorization' : 'bear ' + self.token})
        self.assertEqual(invite_resp.status_code, 404)

        create_team_resp = self.client.post(create_team_url, data = {'name' : 'test_name', 'url' : 'test_url'}, **{'HTTP_Authorization' : 'bear ' + self.token})
        id = create_team_resp.data.get("team").get("id")
        invite_resp2 = self.client.post(invite_url, data = {'team_id' : id, 'username' : 'amir.j1882@gmail.com'}, **{'HTTP_Authorization' : 'bear ' + self.token})

        self.assertEqual(invite_resp2.status_code, 200)

        
        invite_resp3 = self.client.post(invite_url, data = {'team_id' : id, 'username' : 'nothing'}, **{'HTTP_Authorization' : 'bear ' + self.token})
        self.assertEqual(invite_resp3.status_code, 404)
    
