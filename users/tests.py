from rest_framework.test import APITestCase, APIClient
from django.urls import reverse
from users.models import User

# Create your tests here.
class TestViews(APITestCase):

    def setUp(self):
        self.client = APIClient()

    def test_signup(self):
        
        signup_url = reverse("users-urls:signup")
        data = {"email" : "example@example.com", "password" : "12345", "confirm_password": "1234"}
        password_not_match_resp = self.client.post(signup_url, data=data)
        self.assertEqual(password_not_match_resp.status_code, 400)
        
        data = {"email" : "example@example.com", "password" : "12345", "confirm_password": "12345"}
        signup_resp = self.client.post(signup_url, data=data)
        self.assertEqual(signup_resp.status_code, 200)

        data = {"email" : "example@example.com", "password" : "12345", "confirm_password": "12345"}
        signup_resp = self.client.post(signup_url, data=data)
        self.assertEqual(signup_resp.status_code, 400)
    
    def test_login(self):
        signup_url = reverse("users-urls:signup")
        data = {"email" : "example@example.com", "password" : "12345", "confirm_password": "12345"}
        self.client.post(signup_url, data=data)

        login = reverse("users-urls:login")
        login_resp = self.client.post(login, data=None)
        self.assertEqual(login_resp.status_code, 400)
        
        data = {"email" : "example@example.com", "password" : "123"}
        login_resp = self.client.post(login, data=data)
        self.assertEqual(login_resp.status_code, 401)
        
        data = {"email" : "example@example.com", "password" : "12345"}
        login_resp = self.client.post(login, data=data)
        self.assertEqual(login_resp.status_code, 403)

        user = User.objects.get(email = 'example@example.com')
        user.verified = True
        user.save(update_fields = ['verified'])        
        login_resp = self.client.post(login, data=data)
        self.assertEqual(login_resp.status_code, 200)
        self.assertNotEqual(login_resp.json().get('token'), None)

    def test_update_profile(self):
        signup_url = reverse("users-urls:signup")
        data = {"email" : "example@example.com", "password" : "12345", "confirm_password": "12345"}
        self.client.post(signup_url, data=data)
        user = User.objects.get(email = 'example@example.com')
        user.verified = True
        user.save(update_fields = ['verified'])        

        login = reverse("users-urls:login")
        data = {"email" : "example@example.com", "password" : "12345"}
        login_resp = self.client.post(login, data=data)

        token = login_resp.json()['token']
        update_profile_url = reverse("users-urls:updateProfile")
        data = {"first_name": "Example", "last_name": "Example"}
        update_resp = self.client.put(update_profile_url, data=data)
        self.assertEqual(update_resp.status_code, 403)
        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + token)
        update_resp = self.client.put(update_profile_url, data=data)
        self.assertEqual(update_resp.status_code, 200)
        self.assertEqual(update_resp.json()['user']['first_name'], "Example")
        self.assertEqual(update_resp.json()['user']['last_name'], "Example")