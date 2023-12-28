from djoser.serializers import UserCreateSerializer, UserSerializer
from django.contrib.auth import get_user_model
from rest_framework import serializers
from django.utils import timezone
from django.utils.timezone import make_aware

User = get_user_model()

class UserCreateSerializer(UserCreateSerializer):
    user_type = serializers.CharField(default='normal', required=False)  # Add user_type field with default value

    class Meta(UserCreateSerializer.Meta):
        model = User
        fields = ('id', 'email', 'first_name', 'last_name', 'phone', 'password', 'user_type')  # Include user_type in fields

    def validate(self, attrs):
        attrs = super().validate(attrs)

        user_type = attrs.get('user_type')
        if user_type not in ['normal', 'admin']:  # Make sure user_type is either 'normal' or 'admin'
            raise serializers.ValidationError("Invalid user type")

        return attrs


class CustomUserSerializer(UserSerializer):
    last_login = serializers.DateTimeField(format="%Y-%m-%d %H:%M:%S", read_only=True)

    class Meta(UserSerializer.Meta):
        fields = ('id', 'email', 'first_name', 'last_name', 'phone', 'last_login')

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        last_login = representation.get('last_login')

        if last_login:
            if isinstance(last_login, str):
                # If last_login is a string, try to parse it into a datetime object
                last_login = timezone.make_aware(timezone.datetime.fromisoformat(last_login))

            if not timezone.is_aware(last_login):
                # If it's still not aware, assume it's in the default timezone
                last_login = make_aware(last_login, timezone.get_current_timezone())

            formatted_last_login = timezone.localtime(last_login).strftime('%Y-%m-%d %H:%M:%S')
            representation['last_login'] = formatted_last_login

        return representation


class UserAccountSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'email', 'phone')

    def update(self, instance, validated_data):
        # Allow admins to update name and phone without email uniqueness check
        if self.context['request'].user.is_staff:
            instance.first_name = validated_data.get('first_name', instance.first_name)
            instance.last_name = validated_data.get('last_name', instance.last_name)
            instance.phone = validated_data.get('phone', instance.phone)
        else:
            # For regular users, update all fields
            instance.first_name = validated_data.get('first_name', instance.first_name)
            instance.last_name = validated_data.get('last_name', instance.last_name)
            instance.email = validated_data.get('email', instance.email)
            instance.phone = validated_data.get('phone', instance.phone)

        instance.save()
        return instance