from rest_framework import serializers

from .models import Server, DataList, Data

class DataSerializer(serializers.ModelSerializer):
    class Meta:
        model = Data
        fields = ('date', 'value')


class ServerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Server
        fields = ('name', 'user_name', 'active', 'state')


class DataListSerializer(serializers.ModelSerializer):

    data = DataSerializer(many=True)
    server = ServerSerializer(many=False)

    class Meta:
        model = DataList
        fields = ('server', 'attribute', 'data')

class DataListMiniSerializer(serializers.ModelSerializer):
    class Meta:
        model = DataList
        fields = ('server', 'attribute')

class ServerDetailSerializer(serializers.ModelSerializer):

    data_list = DataListMiniSerializer(many=True)

    class Meta:
        model = Server
        fields = ('name', 'user_name', 'active', 'state', 'data_list')
