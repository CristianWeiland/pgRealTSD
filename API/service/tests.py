from django.test import TestCase
from rest_framework import status
from rest_framework.test import APITestCase, APIClient
import random

from .models import Server, DataList, Data

class RoutesTests(APITestCase):
    def fill_database(self):
        for i in range(10):
            s = Server()
            s.name = 'server' + str(i)
            s.user_name = 'user' + str(i)
            s.save()

            for a in DataList.POSSIBLE_ATTRIBUTES:
                dl = DataList()
                dl.attribute = a[0]
                dl.server = s
                dl.save()

                for j in range(1000):
                    d = Data()
                    d.data_list = dl
                    d.value = random.randint(0,j)*random.randint(0,j)

    def test_get_servers(self):
        self.client = APIClient()
        self.fill_database()

        response = self.client.get('/servers/', format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_get_servers_order(self):
        self.client = APIClient()
        self.fill_database()

        response = self.client.get('/servers/order/name/', format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        response = self.client.get('/servers/order/-name/', format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        response = self.client.get('/servers/order/active/', format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        response = self.client.get('/servers/order/-active/', format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        response = self.client.get('/servers/order/state/', format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        response = self.client.get('/servers/order/-state/', format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_new_server(self):
        self.client = APIClient()
        self.fill_database()

        content = {
            "name": "servertest",
            "user_name": "usertest"
        }

        response = self.client.post('/servers/new', content, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_get_a_server(self):
        self.client = APIClient()
        self.fill_database()

        response = self.client.get('/servers/server1/', format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
