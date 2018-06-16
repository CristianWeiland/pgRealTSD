from rest_framework import serializers

from .models import Server, DataList, Data

class DataSerializer(serializers.ModelSerializer):
    class Meta:
        model = Data
        fields = ('timestamp', 'value')


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


class ServerListSerializer(serializers.Serializer):
    """
        Server List Serializer
    """

    order_by = serializers.CharField(required=False)


class ServerCreateSerializer(serializers.Serializer):
    """
        Server Create Serializer
    """

    name = serializers.CharField(required=True)
    user_name = serializers.CharField(required=False)
    password = serializers.CharField(required=False)


class ServerGetSerializer(serializers.Serializer):
    """
        Server get Serializer
    """

    name = serializers.CharField(required=True)


class DataGetSerializer(serializers.Serializer):
    """
        Data get Serializer
    """

    server_name = serializers.CharField(required=True)
    attribute = serializers.CharField(required=True)
    period = serializers.IntegerField(required=False)
    spacing = serializers.IntegerField(required=False)
