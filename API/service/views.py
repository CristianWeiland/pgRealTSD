# -*- coding=utf-8 -*-

# Implemented by Eduardo Machado

from rest_framework import generics, exceptions, status, views
from rest_framework.response import Response
from django.http import Http404
from django.utils import timezone
from os import system
from datetime import timedelta
from subprocess import check_output

from .serializers import ServerSerializer, ServerCreateSerializer, ServerActivationSerializer, DataListSerializer, DataSerializer, ServerDetailSerializer, ServerListSerializer
from .models import Server, DataList, Data

class ServerListView(views.APIView):
    """
        Server List View
    """

    serializer_class = ServerListSerializer
    http_method_names = ['get', 'options']

    def get(self, request):
        """
            GET
            Return a ordened list of all servers.
        """

        # Take url parameters
        serializer = self.serializer_class(data=request.GET)

        if serializer.is_valid():

            if serializer.data.get('order_by', ''):
                order = serializer.data.get('order_by', '')
                return Response(ServerSerializer(Server.objects.all().order_by(order), many=True).data, status=status.HTTP_200_OK)
            else:
                return Response(ServerSerializer(Server.objects.all().order_by('name'), many=True).data, status=status.HTTP_200_OK)
        
        return Response({'error': 'Bad parameter'}, status=status.HTTP_400_BAD_REQUEST)


class ServerCreateView(views.APIView):
    """
        Server Create View
    """

    serializer_class = ServerCreateSerializer
    http_method_names = ['post', 'options']

    def post(self, request):
        """
            POST
            Create a new server.
        """

        serializer = self.serializer_class(data=request.data)

        if serializer.is_valid():

            if Server.objects.filter(name=serializer.data.get('name')):
                return Response('Server ' + serializer.data.get('name') + ' already exists', status = status.HTTP_422_UNPROCESSABLE_ENTITY)

            else:

                if serializer.data.get('password'):
                    bridge_status = check_output(
                        [
                            'python3',
                            'create_ssh_bridge.py',
                            '-u',
                            serializer.data.get('user_name'),
                            '-s',
                            serializer.data.get('name'),
                            '-p',
                            serializer.data.get('password')
                        ]
                    )

                    if bridge_status.decode("utf-8") == 'ok':
                        serverSerializer = ServerSerializer(data=serializer.data)

                        if serverSerializer.is_valid():
                            serverSerializer.save()
                            return Response(serverSerializer.data, status=status.HTTP_201_CREATED)
                        
                        else:
                            return Response(serverSerializer.errors, status=status.HTTP_400_BAD_REQUEST)

                    else:
                        return Response(bridge_status.decode("utf-8"), status=status.HTTP_400_BAD_REQUEST)

                else:
                    serverSerializer = ServerSerializer(data=serializer.data)

                    if serverSerializer.is_valid():
                        serverSerializer.save()
                        return Response(serverSerializer.data, status=status.HTTP_201_CREATED)

                    else:
                        return Response(serverSerializer.errors, status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ServerActivationView(views.APIView):
    """
        Server Activation View
    """

    serializer_class = ServerActivationSerializer
    http_method_names = ['put', 'options']

    def put(self, request):
        """
            PUT
            Activation a new server.
        """

        serializer = self.serializer_class(data=request.data)

        if serializer.is_valid():
            server = Server.objects.filter(name=serializer.data.get('name'))
            if server:
                server[0].active = not server[0].active
                if server[0].active:
                    system('python3 collector.py -u ' + server[0].user_name + ' -s ' + server[0].name + '&> /dev/null &')

                server[0].save()

                return Response(ServerSerializer(server[0]).data, status=status.HTTP_202_ACCEPTED)

            return Response({'error': 'not found'}, status=status.HTTP_404_NOT_FOUND)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class ServerView(views.APIView):
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
            spacing = int(self.kwargs['spacing'])

            server = Server.objects.get(name=server_name)
            data_list = DataList.objects.get(server=server, attribute=attribute)
            data = Data.objects.filter(data_list=data_list,
                                       date__gt=(timezone.now() - timedelta(minutes=period)))

            data_spaced = []

            for i in range(len(data)):
                if i % spacing == 0:
                    data_spaced.append(data[i])

            return data_spaced
        except:
            raise exceptions.NotFound
