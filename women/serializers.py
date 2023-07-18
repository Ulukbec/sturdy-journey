from rest_framework import serializers

from .models import *


class WomenSerializer(serializers.ModelSerializer):
    user = serializers.HiddenField(default=serializers.CurrentUserDefault())

    class Meta:
        model = Women
        fields = '__all__'


class WomenDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = Women
        fields = 'id title content time_create time_update is_published cat'.split()


class ImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Image
        fields = '__all__'
