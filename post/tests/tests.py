from django.test import TestCase
from rest_framework.test import APIClient, APITestCase
from users.models import User
from post.models import Post, Comment
from team.models import Team
from rest_framework import status
from users.authenticators import generate_access_token
from os import path
from django.urls import reverse
from filestorage.models import MediaStorage

class PostViewTest(APITestCase):

        def setUp(self):
            client = APIClient()
            signup_url = reverse("users-urls:signup")
            client.post(signup_url, data = {'email' : 'zahra@yahoo.com', 'password' : '123456', 'confirm_password' : '123456'})
            self.user = User.objects.get(email = 'zahra@yahoo.com')
            self.user.verified = True
            self.user.save(update_fields = ['verified'])
            self.token = generate_access_token(self.user)
            self.test_team = Team.objects.create(url="TESTxzxzvjaTESTxzxz9299y43TEST", name="xzxzvjaTESTxzxz9299y43", head=self.user)
            self.test_post = Post.objects.create(name='test',caption="test caption",status="Drafts",team=self.test_team,owner=self.user)
            self.test_comment = Comment.objects.create(context="testing",author=self.user,post=self.test_post)
            self.second_test_post = Post.objects.create(name='test',caption="test caption",status="Drafts",team=self.test_team,owner=self.user)
            self.second_test_comment = Comment.objects.create(context="testing",author=self.user,post=self.test_post)
            
        def test_create_post(self):
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
                        # "multimedia[]":files,
                        "team": pk_team
                        }
                url = reverse("post-urls:createPost")
                self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + self.token)
                response = self.client.post(url, data)
                post_id=response.data['id']
                post=Post.objects.get(pk=post_id)
                for media in post.multimedia.all():
                    media.delete()
                self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        def test_get_post(self):
            client = APIClient()
            self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + self.token)
            post_id=self.test_post.pk
            url = reverse("post-urls:updatePost",kwargs={'pk': post_id})
            response = self.client.get(url)
            self.assertEqual(response.status_code, status.HTTP_200_OK)
            signup_url = reverse("users-urls:signup")
            client.post(signup_url, data = {'email' : 'hosseini@yahoo.com', 'password' : '123456', 'confirm_password' : '123456'})
            user_test = User.objects.get(email = 'hosseini@yahoo.com')
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
            url = reverse("post-urls:updatePost",kwargs={'pk': post_id})
            response = self.client.put(url,data)
            self.assertEqual(response.status_code, status.HTTP_200_OK)
            signup_url = reverse("users-urls:signup")
            client.post(signup_url, data = {'email' : 'hosseini@yahoo.com', 'password' : '123456', 'confirm_password' : '123456'})
            user_test = User.objects.get(email = 'hosseini@yahoo.com')
            user_test.verified = True
            user_test.save(update_fields = ['verified'])
            self.token = generate_access_token(user_test)
            self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + self.token)
            response = self.client.put(f'/api/v1.0.0/post/update_post/{post_id}/')
            self.assertNotEqual(response.status_code, status.HTTP_200_OK)

        def test_get_single_post(self):
            self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + self.token)
            post_id=self.test_post.pk
            url = reverse("post-urls:singlePost",kwargs={'pk': post_id})
            response = self.client.get(url)
            self.assertEqual(response.status_code, status.HTTP_200_OK)

        def test_get_all_post(self):
            self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + self.token)
            pk_team = self.test_team.pk
            url = reverse("post-urls:allPost",kwargs={'pk': pk_team})
            response = self.client.get(url)
            self.assertEqual(response.status_code, status.HTTP_200_OK)

        def test_create_comment(self):
            data = {"context":"comment test"}
            self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + self.token)
            post_id=self.test_post.pk
            url = reverse("post-urls:createComment",kwargs={'pk': post_id})
            response = self.client.put(url,data)
            self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        def test_get_all_comment(self):
            self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + self.token)
            post_id=self.test_post.pk
            url = reverse("post-urls:allComment",kwargs={'pk': post_id})
            response = self.client.get(url)
            self.assertEqual(response.status_code, status.HTTP_200_OK)

        def test_delete_comment(self):
            client = APIClient()
            self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + self.token)
            comment_id=self.test_comment.pk
            url = reverse("post-urls:deleteComment",kwargs={'pk': comment_id})
            response = self.client.delete(url)
            self.assertEqual(response.status_code, status.HTTP_200_OK)
            
            
            second_comment_id=self.second_test_comment.pk
            signup_url = reverse("users-urls:signup")
            client.post(signup_url, data = {'email' : 'hosseini@yahoo.com', 'password' : '123456', 'confirm_password' : '123456'})
            user_test = User.objects.get(email = 'hosseini@yahoo.com')
            user_test.verified = True
            user_test.save(update_fields = ['verified'])
            self.token = generate_access_token(user_test)
            self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + self.token)
            url2 = reverse("post-urls:deleteComment",kwargs={'pk': second_comment_id})
            response = self.client.delete(url2)
            self.assertNotEqual(response.status_code, status.HTTP_200_OK)
            
        def test_delete_post(self):
            client = APIClient()
            self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + self.token)
            post_id=self.test_post.pk
            url = reverse("post-urls:updatePost",kwargs={'pk': post_id})
            response = self.client.delete(url)
            self.assertEqual(response.status_code, status.HTTP_200_OK)

            
            post_id=self.second_test_post.pk
            signup_url = reverse("users-urls:signup")
            client.post(signup_url, data = {'email' : 'hosseini@yahoo.com', 'password' : '123456', 'confirm_password' : '123456'})
            user_test = User.objects.get(email = 'hosseini@yahoo.com')
            user_test.verified = True
            user_test.save(update_fields = ['verified'])
            self.token = generate_access_token(user_test)
            self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + self.token)
            url = reverse("post-urls:updatePost",kwargs={'pk': post_id})
            response = self.client.delete(url)
            self.assertNotEqual(response.status_code, status.HTTP_200_OK)

        
        #def clear_object_storage(self):
            # pk_team = self.test_team.pk
            # team_media=MediaStorage.objects.filter(pk=pk_team)
            # for media in team_media:
            #     media.delete()
            # self.test_team.pk.delete()
