from rest_framework import serializers
from django.contrib.auth.models import User
from .models import Book, Review

# Сериализатор для модели User (для регистрации)
class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'username', 'email', 'password')
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        # Используем create_user для хеширования пароля
        user = User.objects.create_user(
            username=validated_data['username'], # или validated_data['email'] если username - это email
            email=validated_data['email'],
            password=validated_data['password']
        )
        return user

# Сериализатор для модели Book
class BookSerializer(serializers.ModelSerializer):
    class Meta:
        model = Book
        fields = '__all__' # Включаем все поля

# Сериализатор для модели Review
class ReviewSerializer(serializers.ModelSerializer):
    class Meta:
        model = Review
        fields = '__all__'