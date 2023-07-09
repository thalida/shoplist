from rest_framework import serializers
from .models import User

class UserSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = [
            "uid",
            "email",
            "first_name",
            "last_name",
            "avatar",
        ]
