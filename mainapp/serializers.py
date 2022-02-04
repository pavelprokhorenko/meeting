from django.contrib.auth.models import User

from rest_framework import serializers

from .models import Profile


class UserSerializer(serializers.ModelSerializer):
    confirm_password = serializers.CharField(
        label='Подтвердить пароль', style={'input_type': 'password'}, write_only=True, min_length=6
    )

    class Meta:
        model = User
        fields = ('username', 'email', 'password', 'confirm_password', 'first_name', 'last_name')
        extra_kwargs = {
            'username': {'label': 'Имя пользователя'},
            'email': {'label': 'Email'},
            'password': {'style': {'input_type': 'password'}, 'write_only': True, 'min_length': 6, 'label': 'Пароль'},
            'first_name': {'label': 'Имя'},
            'last_name': {'label': 'Фамилия'}
        }

    def validate(self, data):
        if data['password'] != data['confirm_password']:
            raise serializers.ValidationError('Пароли не совпадают!')
        return data

    def validate_username(self, value):
        if User.objects.filter(username=value).exists():
            raise serializers.ValidationError(f'Пользователь с ником {value} уже существует')
        return value

    def validate_email(self, value):
        if User.objects.filter(email=value).exists():
            raise serializers.ValidationError(f'Пользователь с email {value} уже существует')
        return value


class ProfileSerializer(serializers.ModelSerializer):
    user = UserSerializer(label='Пользователь')

    class Meta:
        model = Profile
        fields = ('user', 'avatar', 'gender')

    def create(self, validated_data):
        user_data = validated_data['user']
        user = User(
            email=user_data['email'],
            username=user_data['username'],
            first_name=user_data['first_name'].title(),
            last_name=user_data['last_name'].title(),
        )
        user.set_password(user_data['password'])
        user.save()
        profile = Profile(
            user=user,
            gender=validated_data['gender'],
            avatar=validated_data['avatar'],
        )
        profile.save()
        return profile
