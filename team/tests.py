from django.test import TestCase, Client
from django.urls import reverse
from .models import Team
from users.models import User

class TestViews(TestCase):

    def setUp(self):
        self.client = Client()
        self.client.post('/api/users/signup/', data = {'email' : 'amir.j1881@gmail.com', 'password' : '123456', 'confirm_password' : '123456'})
        user = User.objects.get(email = 'amir.j1881@gmail.com')
        user.verified = True
        user.save(update_fields = ['verified'])
        
        login_resp = self.client.post('/api/users/login/', data = {'email' : 'amir.j1881@gmail.com', 'password' : '123456'})
        self.token = login_resp.data.get('token')


    def test_create_team(self):
        
        client_unauth = Client()

        # Unauthorized Request
        unauthorized_resp = client_unauth.post('/api/v1.0.0/team/create_team', data = {'name' : 'test_name', 'url' : 'test_url'})
        self.assertEqual(unauthorized_resp.status_code, 403)
        
        self.setUp()

        create_team_resp = self.client.post('/api/v1.0.0/team/create_team', data = {'name' : 'test_name', 'url' : 'test_url'}, **{'HTTP_Authorization' : 'bear ' + self.token})

        self.assertEqual(create_team_resp.status_code, 200)
        self.assertEqual(create_team_resp.json()['team']['name'], 'test_name')
        self.assertEqual(create_team_resp.json()['team']['url'], 'test_url')

        # Missed Parameter
        create_team_resp = self.client.post('/api/v1.0.0/team/create_team', data = {'url' :'_test_url'}, **{'HTTP_Authorization' : 'bear ' + self.token})
        self.assertEqual(create_team_resp.status_code, 400)

        # Taken URL
        create_team_resp2 = self.client.post('/api/v1.0.0/team/create_team', data = {'name' : 'test_name', 'url' :'test_url'}, **{'HTTP_Authorization' : 'bear ' + self.token})
        self.assertEqual(create_team_resp2.status_code, 400)

    def test_invite_user(self):
        client_unauth = Client()

        # Unauthorized Request
        unauth_resp = client_unauth.post('/api/v1.0.0/team/invite_user', data = {'username' : 'amir.j1883@gmail.com'})
        self.assertEqual(unauth_resp.status_code, 403)

        self.setUp()

        # Team does not exist
        invite_resp = self.client.post('/api/v1.0.0/team/invite_user', data = {'team_id' : 1, 'username' : 'amir.j1882@gmail.com'}, **{'HTTP_Authorization' : 'bear ' + self.token})
        self.assertEqual(invite_resp.status_code, 404)

        # User does not exist
        invite_resp2 = self.client.post('/api/v1.0.0/team/invite_user', data = {'team_id' : 1, 'username' : 'amir.j1882@gmail.com'}, **{'HTTP_Authorization' : 'bear ' + self.token})
        self.assertEqual(invite_resp2.status_code, 404)

        create_team_resp = self.client.post('/api/v1.0.0/team/create_team', data = {'name' : 'test_name', 'url' : 'test_url'}, **{'HTTP_Authorization' : 'bear ' + self.token})

        # Create User        
        self.client.post('/api/users/signup/', data = {'email' : 'amir.j1882@gmail.com', 'password' : '123456', 'confirm_password' : '123456'})
        user = User.objects.get(email = 'amir.j1882@gmail.com')
        user.verified = True
        user.save(update_fields = ['verified'])
        
        invite_resp3 = self.client.post('/api/v1.0.0/team/invite_user', data = {'team_id' : 1, 'username' : 'amir.j1882@gmail.com'}, **{'HTTP_Authorization' : 'bear ' + self.token})
        self.assertEqual(invite_resp3.status_code, 200)
        team = Team.objects.filter(url = 'test_url').first()
        self.assertEqual(team.pending_users.filter(username = 'amir.j1882@gmail.com').exists(), True)

    def test_accept_invite(self):
        
        # Unauthorized Request
        unauth_resp = client_unauth.post('/api/v1.0.0/team/invite_user', data = {'username' : 'amir.j1883@gmail.com'})
        self.assertEqual(unauth_resp.status_code, 403)

        self.setUp()

        # Team does not exist
        resp1 = self.client.post('/api/team/v1.0.0/team/accept_invite', data = {'team_id' : 1}, **{'HTTP_Authorization' : 'bear ' + self.token})
        self.assertEqual(resp1.status_code, 404)

        create_team_resp = self.client.post('/api/v1.0.0/team/create_team', data = {'name' : 'test_name', 'url' : 'test_url'}, **{'HTTP_Authorization' : 'bear ' + self.token})
        
        # Create User        
        self.client.post('/api/users/signup/', data = {'email' : 'amir.j1882@gmail.com', 'password' : '123456', 'confirm_password' : '123456'})
        user = User.objects.get(email = 'amir.j1882@gmail.com')
        user.verified = True
        user.save(update_fields = ['verified'])
        login_resp = self.client.post('/api/users/login/', data = {'email' : 'amir.j1882@gmail.com', 'password' : '123456'})
        token2 = login_resp.data.get('token')

        
        # User is not invited
        resp2 = self.client.post('/api/team/v1.0.0/accept_invite', data = {'team_id' : 1}, **{'HTTP_Authorization' : 'bear ' + token2})
        self.assertEqual(resp2.status_code, 400)

        self.client.post('api/team/v1.0.0/invite_user', data = {'team_id' : 1, 'username' : 'amir.j1882@gmail.com'}, **{'HTTP_Authorization' : 'bear ' + self.token})

        resp3 = self.client.post('api/team/v1.0.0/accept_invite', data = {'team_id' : 1}, **{'HTTP_Authorization' : 'bear ' + token2})
        team = Team.objects.filter(url = 'test_url').first()
        self.assertEqual(resp3.status_code, 200)
        self.assertEqual(team.pending_users.filter(username = 'amir.j1882@gmail.com').exists(), False)
        self.assertEqual(team.members.filter(username = 'amir.j1882@gmail.com').exists(), True)

    def test_reject_invite(self):
        
        # Unauthorized Request
        unauth_resp = client_unauth.post('/api/v1.0.0/team/invite_user', data = {'username' : 'amir.j1883@gmail.com'})
        self.assertEqual(unauth_resp.status_code, 403)

        self.setUp()

        # Team does not exist
        resp1 = self.client.post('/api/team/v1.0.0/team/reject_invite', data = {'team_id' : 1}, **{'HTTP_Authorization' : 'bear ' + self.token})
        self.assertEqual(resp1.status_code, 404)

        create_team_resp = self.client.post('/api/v1.0.0/team/create_team', data = {'name' : 'test_name', 'url' : 'test_url'}, **{'HTTP_Authorization' : 'bear ' + self.token})
        
        # Create User        
        self.client.post('/api/users/signup/', data = {'email' : 'amir.j1882@gmail.com', 'password' : '123456', 'confirm_password' : '123456'})
        user = User.objects.get(email = 'amir.j1882@gmail.com')
        user.verified = True
        user.save(update_fields = ['verified'])
        login_resp = self.client.post('/api/users/login/', data = {'email' : 'amir.j1882@gmail.com', 'password' : '123456'})
        token2 = login_resp.data.get('token')

        
        # User is not invited
        resp2 = self.client.post('/api/team/v1.0.0/reject_invite', data = {'team_id' : 1}, **{'HTTP_Authorization' : 'bear ' + token2})
        self.assertEqual(resp2.status_code, 400)

        self.client.post('api/team/v1.0.0/invite_user', data = {'team_id' : 1, 'username' : 'amir.j1882@gmail.com'}, **{'HTTP_Authorization' : 'bear ' + self.token})

        resp3 = self.client.post('api/team/v1.0.0/reject_invite', data = {'team_id' : 1}, **{'HTTP_Authorization' : 'bear ' + token2})
        team = Team.objects.filter(url = 'test_url').first()
        self.assertEqual(resp3.status_code, 200)
        self.assertEqual(team.pending_users.filter(username = 'amir.j1882@gmail.com').exists(), False)
        self.assertEqual(team.members.filter(username = 'amir.j1882@gmail.com').exists(), False)

    def test_remove_user(self):
        # Unauthorized Request
        unauth_resp = client_unauth.post('/api/v1.0.0/team/remove_user', data = {'username' : 'amir.j1883@gmail.com'})
        self.assertEqual(unauth_resp.status_code, 403)

        self.setUp()

        # Team does not exist
        resp1 = self.client.post('/api/team/v1.0.0/team/remove_user', data = {'team_id' : 1, 'username' : 'amir.j1882@gmail.com'}, **{'HTTP_Authorization' : 'bear ' + self.token})
        self.assertEqual(resp1.status_code, 404)

        create_team_resp = self.client.post('/api/v1.0.0/team/create_team', data = {'name' : 'test_name', 'url' : 'test_url'}, **{'HTTP_Authorization' : 'bear ' + self.token})

        # User does not exist
        resp2 = self.client.post('/api/team/v1.0.0/team/remove_user', data = {'team_id' : 1, 'username' : 'nothing'}, **{'HTTP_Authorization' : 'bear ' + self.token})
        self.assertEqual(resp2.status_code, 404)
        
        # User is not member of team
        resp3 = self.client.post('/api/team/v1.0.0/team/remove_user', data = {'team_id' : 1, 'username' : 'amir.j1882@gmail.com'}, **{'HTTP_Authorization' : 'bear ' + self.token})
        self.assertEqual(resp3.status_code, 400)

        team = Team.objects.filter(url = 'test_url').first()
        user = User.objects.filter(username = 'amir.j1882@gmail.com')
        team.members.add(user)

        # Not head user request
        resp4 = self.client.post('/api/team/v1.0.0/team/remove_user', data = {'team_id' : 1, 'username' : 'amir.j1882@gmail.com'}, **{'HTTP_Authorization' : 'bear ' + self.token2})
        self.assertEqual(resp4.status_code, 403)

        resp5 = self.client.post('/api/team/v1.0.0/team/remove_invite', data = {'team_id' : 1, 'username' : 'amir.j1882@gmail.com'}, **{'HTTP_Authorization' : 'bear ' + self.token})
        self.assertEqual(resp5.status_code, 200)
        self.assertEqual(team.members.filter(username = 'amir.j1882@gmail.com').exists(), False)
    
    def test_leave_team(self):
        # Unauthorized Request
        unauth_resp = client_unauth.post('/api/v1.0.0/team/remove_user', data = {'username' : 'amir.j1883@gmail.com'})
        self.assertEqual(unauth_resp.status_code, 403)

        self.setUp()

        # Team does not exist
        resp1 = self.client.post('/api/team/v1.0.0/team/remove_user', data = {'team_id' : 1, 'username' : 'amir.j1882@gmail.com'}, **{'HTTP_Authorization' : 'bear ' + self.token})
        self.assertEqual(resp1.status_code, 404)

        create_team_resp = self.client.post('/api/v1.0.0/team/create_team', data = {'name' : 'test_name', 'url' : 'test_url'}, **{'HTTP_Authorization' : 'bear ' + self.token})

        # User is not member of team
        resp3 = self.client.post('/api/team/v1.0.0/team/remove_user', data = {'team_id' : 1}, **{'HTTP_Authorization' : 'bear ' + self.token2})
        self.assertEqual(resp3.status_code, 400)

        team = Team.objects.filter(url = 'test_url').first()
        user = User.objects.filter(username = 'amir.j1882@gmail.com')
        team.members.add(user)

        resp4 = self.client.post('/api/team/v1.0.0/team/remove_user', data = {'team_id' : 1}, **{'HTTP_Authorization' : 'bear ' + self.token2})
        self.assertEqual(resp4.status_code, 200)
        self.assertEqual(team.members.filter(username = 'amir.j1882@gmail.com').exists(), False)

    def test_update_team(self):
        # Unauthorized Request
        unauth_resp = client_unauth.post('/api/v1.0.0/team/update_team_info', data = {'team_id' : 1})
        self.assertEqual(unauth_resp.status_code, 403)

        self.setUp()

        # Team does not exist
        resp1 = self.client.post('/api/team/v1.0.0/team/update_team_info', data = {'team_id' : 1}, **{'HTTP_Authorization' : 'bear ' + self.token})
        self.assertEqual(resp1.status_code, 404)

        self.client.post('/api/v1.0.0/team/create_team', data = {'name' : 'test_name', 'url' : 'test_url'}, **{'HTTP_Authorization' : 'bear ' + self.token})

        # User is not head
        resp2 = self.client.post('/api/team/v1.0.0/team/update_team_info', data = {'team_id' : 1}, **{'HTTP_Authorization' : 'bear ' + self.token2})
        self.assertEqual(resp2.status_code, 403)

        resp3 = self.client.post('/api/team/v1.0.0/team/update_team_info', data = {'team_id' : 1, 'name' : 'new_name', 'url' : 'new_url'}, **{'HTTP_Authorization' : 'bear ' + self.token})
        self.assertEqual(resp3.status_code, 200)
        
        team = Team.objects.filter(id = 1).first()
        self.assertEqual(team.name, 'new_name')
        self.assertEqual(team.url, 'new_url')

        self.client.post('/api/v1.0.0/team/create_team', data = {'name' : 'name2', 'url' : 'url2'}, **{'HTTP_Authorization' : 'bear ' + self.token})

        # Url exist
        resp4 = self.client.post('/api/team/v1.0.0/team/update_team_info', data = {'team_id' : 1, 'url' : 'url2'}, **{'HTTP_Authorization' : 'bear ' + self.token})
        self.assertEqual(resp1.status_code, 400)
        self.assertEqual(team.url, 'new_url')

