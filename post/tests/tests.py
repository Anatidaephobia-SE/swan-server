from django.test import TestCase
from rest_framework.test import APIClient, APITestCase
from users.models import User
from post.models import Post, Comment
from team.models import Team
from rest_framework import status
from users.authenticators import generate_access_token
from os import path


class PostViewTest(APITestCase):

        def setUp(self):
            client = APIClient()
            client.post('/api/users/signup/', data = {'email' : 'zahra_hosseini99@yahoo.com', 'password' : '123456', 'confirm_password' : '123456'})
            self.user = User.objects.get(email = 'zahra_hosseini99@yahoo.com')
            self.user.verified = True
            self.user.save(update_fields = ['verified'])
            self.token = generate_access_token(self.user)
            create_team_resp = client.post('/api/team/create_team', data = {'name' : 'test_name', 'url' : 'myteam'}, **{'HTTP_Authorization' : 'bear ' + self.token})
            self.test_team = Team.objects.create(url="team11", name="hahaha", head=self.user)
            self.test_post = Post.objects.create(name='test',caption="test caption",status="Drafts",team=self.test_team,owner=self.user)
            self.test_comment = Comment.objects.create(context="testing",author=self.user,post=self.test_post)
            self.second_test_post = Post.objects.create(name='test',caption="test caption",status="Drafts",team=self.test_team,owner=self.user)
            self.second_test_comment = Comment.objects.create(context="testing",author=self.user,post=self.test_post)

        def test_create_post(self):
            client = APIClient()
            files=[]
            abs_path = path.abspath(__file__) 
            dir_path = path.dirname(abs_path) 
            media_file_path = path.join(dir_path,'test_file.jpg')
            with open(media_file_path, 'rb') as fp:
                files.append(fp)
                pk_team = self.test_team.pk
                data = {"name":"big opportunities",
                        "caption":"Over the past decade, the availability and demand for data science skills and data-decision decision making has skyrocketed.",
                        "status":"Drafts",
                        "multimedia[]":files,
                        "team": pk_team
                        }
                self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + self.token)
                response = self.client.post('/api/v1.0.0/post/create_post/', data)
                print(response.__dict__)
                self.assertEqual(response.status_code, status.HTTP_201_CREATED)

                data = {"caption":"Over the past decade, the availability and demand for data science skills and data-decision decision making has skyrocketed.",
                        "status":"Drafts",
                        "multimedia[]":files,
                        "team":pk_team
                        }
                response = self.client.post('/api/v1.0.0/post/create_post/', data)
                self.assertNotEqual(response.status_code, status.HTTP_201_CREATED)

        def test_get_post(self):
            client = APIClient()
            self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + self.token)
            post_id=self.test_post.pk
            response = self.client.get(f'/api/v1.0.0/post/update_post/{post_id}/')
            self.assertEqual(response.status_code, status.HTTP_200_OK)

            client.post('/api/users/signup/', data = {'email' : 'hosseini99_zahra@yahoo.com', 'password' : '123456', 'confirm_password' : '123456'})
            user_test = User.objects.get(email = 'hosseini99_zahra@yahoo.com')
            user_test.verified = True
            user_test.save(update_fields = ['verified'])
            self.token = generate_access_token(user_test)
            self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + self.token)
            response = self.client.get(f'/api/v1.0.0/post/update_post/{post_id}/')
            self.assertNotEqual(response.status_code, status.HTTP_200_OK)

        def test_update_post(self):
            client = APIClient()
            files=[]
            self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + self.token)
            pk_team = self.test_team.pk
            data = {"name":"First Post",
                    "caption":"Over the past decade, the availability and demand for data science skills and data-decision decision making has skyrocketed.",
                    "status":"Drafts",
                    "multimedia[]":files,
                    "team":pk_team
                    }
            post_id=self.test_post.pk
            response = self.client.put(f'/api/v1.0.0/post/update_post/{post_id}/',data)
            self.assertEqual(response.status_code, status.HTTP_200_OK)

            client.post('/api/users/signup/', data = {'email' : 'hosseini99_zahra@yahoo.com', 'password' : '123456', 'confirm_password' : '123456'})
            user_test = User.objects.get(email = 'hosseini99_zahra@yahoo.com')
            user_test.verified = True
            user_test.save(update_fields = ['verified'])
            self.token = generate_access_token(user_test)
            self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + self.token)
            response = self.client.put(f'/api/v1.0.0/post/update_post/{post_id}/')
            self.assertNotEqual(response.status_code, status.HTTP_200_OK)

        def test_get_single_post(self):
            client = APIClient()
            self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + self.token)
            post_id=self.test_post.pk
            response = self.client.get(f'/api/v1.0.0/post/single_post/{post_id}/')
            self.assertEqual(response.status_code, status.HTTP_200_OK)

        def test_get_all_post(self):
            client = APIClient()
            self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + self.token)
            response = self.client.get(f'/api/v1.0.0/post/all_post/')
            self.assertEqual(response.status_code, status.HTTP_200_OK)

        def test_create_comment(self):
            client = APIClient()
            files=[]
            data = {"context":"comment test"}
            self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + self.token)
            post_id=self.test_post.pk
            response = self.client.put(f'/api/v1.0.0/post/create_comment/{post_id}/',data)
            self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        def test_get_all_comment(self):
            client = APIClient()
            self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + self.token)
            post_id=self.test_post.pk
            response = self.client.get(f'/api/v1.0.0/post/all_comment/{post_id}/')
            self.assertEqual(response.status_code, status.HTTP_200_OK)

        def test_delete_comment(self):
            client = APIClient()
            self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + self.token)
            comment_id=self.test_comment.pk
            response = self.client.delete(f'/api/v1.0.0/post/delete_comment/{comment_id}/')
            self.assertEqual(response.status_code, status.HTTP_200_OK)
            
            
            second_comment_id=self.second_test_comment.pk
            client.post('/api/users/signup/', data = {'email' : 'hosseini99_zahra@yahoo.com', 'password' : '123456', 'confirm_password' : '123456'})
            user_test = User.objects.get(email = 'hosseini99_zahra@yahoo.com')
            user_test.verified = True
            user_test.save(update_fields = ['verified'])
            self.token = generate_access_token(user_test)
            self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + self.token)
            response = self.client.delete(f'/api/v1.0.0/post/delete_comment/{second_comment_id}/')
            self.assertNotEqual(response.status_code, status.HTTP_200_OK)
            
        def test_delete_post(self):
            client = APIClient()
            self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + self.token)
            post_id=self.test_post.pk
            response = self.client.delete(f'/api/v1.0.0/post/update_post/{post_id}/')
            self.assertEqual(response.status_code, status.HTTP_200_OK)

            
            post_id=self.second_test_post.pk
            client.post('/api/users/signup/', data = {'email' : 'hosseini99_zahra@yahoo.com', 'password' : '123456', 'confirm_password' : '123456'})
            user_test = User.objects.get(email = 'hosseini99_zahra@yahoo.com')
            user_test.verified = True
            user_test.save(update_fields = ['verified'])
            self.token = generate_access_token(user_test)
            self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + self.token)
            response = self.client.delete(f'/api/v1.0.0/post/update_post/{post_id}/')
            self.assertNotEqual(response.status_code, status.HTTP_200_OK)