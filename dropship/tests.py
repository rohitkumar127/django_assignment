from django.test import TestCase
from dropship.models import *
from django.urls import reverse
from rest_framework import status
from rest_framework.test import RequestsClient


class MemberTest(TestCase):
    """ Test module for Member model """

    def setUp(self):
        self.member_1 = Member.objects.create(first_name="Sanket", last_name="Mistry",
                                              email="sanket@email.com", password="sanket")
        self.member_2 = Member.objects.create(first_name="Harsh", last_name="Shah",
                                              email="harsh@email.com", password="harsh")

    def test_member_profile_created(self):
        response = self.client.post('/member/', {'first_name': 'Piyush',
                                                 'last_name': 'Joshi',
                                                 'email': 'piyush@email.com',
                                                 'password': 'piyush'
                                                 })
        self.assertEqual(response.status_code, 201)
        response_data = response.json()
        self.assertEqual(len(response_data), 4)

    def test_member_retrieve(self):
        response = self.client.get('/member/')
        response_data = response.json()
        self.assertEqual(len(response_data), 4)


class ProjectTest(TestCase):
    """ Test module for Member model """

    def test_project_profile_created(self):

        client = RequestsClient()
        # Obtain a CSRF token.
        response = client.get('/member/')
        self.assertEqual(response.status_code, 200)
        csrftoken = response.cookies['csrftoken']

        # Interact with the API.
        response = client.post('/project/', json={
            'title': 'Project1',
            'description': 'This is Project1',
            'code': 'PR1',
            'creator': 1
        }, headers={'X-CSRFToken': csrftoken})
        self.assertEqual(response.status_code, 200)

    # def setUp(self):
    #     self.member_1 = Member.objects.create(first_name="Sanket", last_name="Mistry",
    #                                           email="sanket@email.com", password="sanket")
    #     self.member_2 = Member.objects.create(first_name="Harsh", last_name="Shah",
    #                                           email="harsh@email.com", password="harsh")

    # def test_project_profile_created(self):

    #     self.user_1 = self.client.login(
    #         username='sanket@email.com', password='sanket')
    # response = self.client.post('/project/', {'title': 'Project1',
    #                                           'description': 'This is Project1',
    #                                           'code': 'PR!',
    #                                           'creator': 1
    #                                           })
    #     self.assertEqual(response.status_code, 201)
    #     response_data = response.json()
    #     self.assertEqual(len(response_data), 1)

    # def test_member_retrieve(self):
    #     response = self.client.get('/member/')
    #     response_data = response.json()
    #     self.assertEqual(len(response_data), 4)
