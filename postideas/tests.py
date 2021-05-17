from django.test import TestCase
from rest_framework.test import APIClient, APITestCase
from users.models import User
from team.models import Team
from postideas.models import Card
from rest_framework import status
from users.authenticators import generate_access_token
from os import path
from django.urls import reverse


class CardViewTest(APITestCase):

        def setUp(self):
            client = APIClient()
            signup_url = reverse("users-urls:signup")
            client.post(signup_url, data = {'email' : 'zari@yahoo.com', 'password' : '123456', 'confirm_password' : '123456'})
            self.user = User.objects.get(email = 'zari@yahoo.com')
            self.user.verified = True
            self.user.save(update_fields = ['verified'])
            self.token = generate_access_token(self.user)
            self.test_team = Team.objects.create(url="team11", name="hahaha", head=self.user)
            self.test_card = Card.objects.create(team=self.test_team ,title="test",description="card_description",status="TO DO",assignee=self.user,tag="Low priority")
            self.test_card_second = Card.objects.create(team=self.test_team ,title="second test",description="second_card_description",status="Done",assignee=self.user,tag="High priority")

        def test_create_card(self):
            client = APIClient()
            url = reverse("postideas-urls:createCard")
            data = {
                    "title":"first test",
                    "description":"lalallalalalal",
                    "status":"TO DO",
                    "assignee":self.user.id,
                    "team":self.test_team.id,
                    "tag":"Low priority"
                    }
            self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + self.token)
            response = self.client.post(url, data)
            self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        def test_move_card(self):
            self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + self.token)
            url = reverse("postideas-urls:MoveCard")
            print("**********************************",self.test_card.id)
            card_pk=self.test_card.id
            data1 = {
                    'card_pk':card_pk,
                    'status':'Done'
                    }
            print("**********************************",data1)
            response = self.client.put(url,data=data1)
            print(response.__dict__)
            self.assertEqual(response.status_code, status.HTTP_200_OK)


        def test_get_cards(self):
            url = reverse("postideas-urls:allCard")
            data2 = {
                    'team_pk':self.test_team.id,
                    }
            self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + self.token)
            response = self.client.get(url,data=data2)
            self.assertEqual(response.status_code, status.HTTP_200_OK)

        def test_delete_card(self):  
            url = reverse("postideas-urls:DeleteCard")
            card_pk=self.test_card_second.id
            data3 = {
                    'card_pk':card_pk
                    }
            self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + self.token)
            response = self.client.delete(url,data=data3)
            print(response.__dict__)
            self.assertEqual(response.status_code, status.HTTP_200_OK)
            