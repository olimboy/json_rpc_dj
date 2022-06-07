from django.contrib.auth.models import User
from rest_framework.serializers import ModelSerializer

from api.models import Book


class UserSerializer(ModelSerializer):
    class Meta:
        model = User
        exclude = ['password']


class BookSerializer(ModelSerializer):
    class Meta:
        model = Book
        fields = '__all__'
