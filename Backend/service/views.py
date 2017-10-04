# -*- coding=utf-8 -*-

# Implemented by Eduardo Machado

from rest_framework import generics, exceptions, status
from rest_framework.response import Response
from rest_framework.request import Request
from rest_framework.views import APIView
from django.http import Http404
from django.utils import timezone
from os import system
import datetime
import subprocess

from .serializers import ServerSerializer, DataListSerializer, DataSerializer, ServerDetailSerializer
from .models import Server, DataList, Data

class ServerListView(generics.ListAPIView):
    """
    Server List View
    Attributes:
        serializer_class: The serializer used for API's responses.
    """

    serializer_class = ServerSerializer

    def get_queryset(self):
        """
        GET Queryset
        Takes the parameters of the url and builds a response according to.
        """

        # Take url parameters
        try:
            order = self.kwargs['order']
            return Server.objects.all().order_by(order)
        except:
            return Server.objects.all().order_by('name')


class ServerView(APIView):
    """
    Server View
    Attributes:
        serializer_class: The serializer used for API's responses.
    """

    def get_object(self, server_name):
        try:
            return Server.objects.get(name=server_name)
        except Server.DoesNotExist:
            raise Http404

    def get(self, request, server_name, format=None):
        server = self.get_object(server_name)
        serializer = ServerDetailSerializer(server)

        return Response(serializer.data)

    def post(self, request, format=None):
        serializer = ServerSerializer(data=request.data)
        if serializer.is_valid():
            try:
                server = Server.objects.get(name=request.data['name'])
                return Response('Server ' + server.name + ' already exists',
                                status=status.HTTP_422_UNPROCESSABLE_ENTITY)
            except:
                try:
                    request.data['password']
                    bridge_status = subprocess.check_output(['python3', 'create_ssh_bridge.py',
                                                            '-u', request.data['user_name'],
                                                            '-s', request.data['name'],
                                                            '-p', request.data['password']])

                    if bridge_status.decode("utf-8") == 'ok':
                        serializer.save()
                        return Response(serializer.data, status=status.HTTP_201_CREATED)
                    else:
                        return Response(bridge_status.decode("utf-8"), status=status.HTTP_400_BAD_REQUEST)

                except:
                    serializer.save()

                    return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def put(self, request, server_name, format=None):
        server = self.get_object(server_name)
        server.active = not server.active

        if ServerSerializer(server).is_valid:
            if server.active:
                system('python3 collector.py -u ' + server.user_name + ' -s ' + server_name + '&> /dev/null &')

            server.save()

            return Response(ServerSerializer(server).data, status=status.HTTP_202_ACCEPTED)
        else:
            return Response('Error: Bad Request', status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, server_name, format=None):
        server = Server.objects.get(name=server_name)
        server.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class DataView(generics.ListAPIView):
    """
    Data View
    Attributes:
        serializer_class: The serializer used for API's responses.
    """

    serializer_class = DataSerializer

    def get_queryset(self):
        """
        GET Queryset
        Takes the parameters of the url and builds a response according to.
        """

        # Take url parameters
        try:
            server_name = self.kwargs['server_name']
            attribute = self.kwargs['attribute']
            period = int(self.kwargs['period'])

            server = Server.objects.get(name=server_name)
            data_list = DataList.objects.get(server=server, attribute=attribute)
            data = Data.objects.filter(data_list=data_list,
                                       date__gt=(timezone.now() - datetime.timedelta(minutes=period)))

            return data
        except:
            raise exceptions.NotFound
