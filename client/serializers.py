from rest_framework import serializers
from django.utils.translation import gettext as _
from .models import User

class RegisterSerializer(serializers.ModelSerializer):
    confirm = serializers.CharField(max_length=50, write_only=True)

    def validate(self, attrs):
        pswrd = attrs.get("password")
        cnfrm = attrs.get("confirm")
        if pswrd != cnfrm:
            raise serializers.ValidationError(_("Please confirm the password correctly!"))
        del attrs['confirm']
        return attrs

    class Meta:
        model = User
        fields = ['email', 'password', 'confirm', 'is_active']
        read_only_fields = ("id",)
        extra_kwargs = {
            'password': {'write_only': True}
        }
    
    def create(self, validated_data):
        user = User(
        email=validated_data['email'],
        is_active=False
        )
        user.set_password(validated_data['password'])
        user.save()
        return user

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = "__all__"