from rest_framework import serializers
from .models import Image, Places, Category


class ImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Image
        fields = '__all__'



class PlacesSerializer(serializers.ModelSerializer):
    class Meta:
        model = Places
        fields = '__all__'


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = '__all__'
