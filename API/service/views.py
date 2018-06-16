# -*- coding=utf-8 -*-

# Implemented by Eduardo Machado

from rest_framework import generics, exceptions, status, views
from rest_framework.response import Response
from django.http import Http404
from django.utils import timezone
from os import system
from time import time
from subprocess import check_output

from .serializers import ServerSerializer, ServerCreateSerializer, ServerGetSerializer, ServerDetailSerializer, ServerListSerializer, DataSerializer, DataGetSerializer
from .models import Server, DataList, Data

class ServerListView(views.APIView):
    """
        order_by = ('name', '-name', 'active', '-active', 'state', '-state')
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

    serializer_class = ServerGetSerializer
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


class ServerDeleteView(views.APIView):
    """
        Server Delete View
    """

    serializer_class = None
    http_method_names = ['delete', 'options']

    def delete(self, request, name=None):
        """
            DELETE
            Delete a new server.
        """

        server = Server.objects.filter(name=name)
        if server:
            server[0].delete()
            return Response(status=status.HTTP_204_NO_CONTENT)

        return Response({'error': 'not found'}, status=status.HTTP_404_NOT_FOUND)


class ServerGetView(views.APIView):
    """
        Server Get View
    """

    serializer_class = ServerGetSerializer
    http_method_names = ['get', 'options']

    def get(self, request):
        """
            GET
            Return a server.
        """

        serializer = self.serializer_class(data=request.GET)

        if serializer.is_valid():
            server = Server.objects.filter(name=serializer.data.get('name'))
            if server:
                return Response(ServerDetailSerializer(server[0]).data, status=status.HTTP_200_OK)

            return Response({'error': 'not found'}, status=status.HTTP_404_NOT_FOUND)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class DataView(generics.ListAPIView):
    """
        attribute = {
            ('r' = Waiting processes),
            ('b' = Sleeping processes),
            ('swpd' = Virtual memory),
            ('free' = Idle memory),
            ('buff' = Memory used as buffers),
            ('cache' = Memory used as cache),
            ('inact' = Inactive memory),
            ('active' = Active memory),
            ('si' = Memory swapped in),
            ('so' = Memory swapped out),
            ('bi' = IO (in)),
            ('bo' = IO (out)),
            ('in' = System interrupts per second),
            ('cs' = Context switches per second),
            ('us' = CPU User time),
            ('sy' = CPU System time),
            ('id' = CPU Idle time),
            ('wa' = CPU IO wait time),
            ('st' = CPU Stolen from a virtual machine time)
        }
    """

    serializer_class = DataGetSerializer
    http_method_names = ['get', 'options']

    def get(self, request):
        """
            GET
            Returna data attribute list
        """

        serializer = self.serializer_class(data=request.GET)

        if serializer.is_valid():

            # Take url parameters
            #try:
            server_name = serializer.data.get('server_name')
            attribute = serializer.data.get('attribute')
            period = serializer.data.get('period', 10)
            spacing = serializer.data.get('spacing', 1)

            data = Data.objects.filter(data_list__server__name=server_name, data_list__attribute=attribute, timestamp__gt = (int(time()) - (period * 60)))

            data_spaced = []
            for i in range(len(data)):
                if i % spacing == 0:
                    data_spaced.append(data[i])

            return Response(DataSerializer(data_spaced, many=True).data, status=status.HTTP_200_OK)
            #except:
            #    return Response({'error': 'not found'}, status=status.HTTP_404_NOT_FOUND)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
