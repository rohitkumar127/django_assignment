from django.test import TestCase
from dropship.models import Project,User
from rest_framework.test import APITestCase
# Create your tests here.
class Testprojects(APITestCase):
    def setUp(self):
        user = User.objects.create(username='abc', password='123', email='annc@gmail.com', role='staff')
        self.project_1 = Project.objects.create(title="Amazon",description="lhh",creator=user)
    def test_get_project(self):
        self.setUp()
        response = self.client.get('/jira/projects')
        self.assertEqual(response.status_code, 200)
        # the size should be 2
        response_data = response.json()
        self.assertEqual(len(response_data.get('data')), 2)

    def test_create_new_project(self):
        user=User.objects.create(username='abc',password='123',email='ac@gmail.com',role='staff')
        response = self.client.post('/jira/projects', {'title': 'abcd','description':'efgh','creator':user})
        #the new project should be created
        self.assertEqual(response.status_code, 201)
        response_data = response.json()
        #verify that the details are correct
        self.assertEqual(response_data.get('title'), 'abcd')
        self.assertEqual(response_data.get('description'), 'efgh')

        #now the get api should return 3 people
        response = self.client.get('/jira/projects/')
        response_data = response.json()
        self.assertEqual(len(response_data.get('data')),3)
