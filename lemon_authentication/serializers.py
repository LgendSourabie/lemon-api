from rest_framework import serializers
from django.contrib.auth.models import User


class UserSerializer(serializers.ModelSerializer):

    id = serializers.IntegerField()
    
    class Meta:
        model = User
        fields = ['id','username', 'email']
        read_only_fields = ['username', 'email']
        extra_kwargs = {
            "id":{'min_value':1},
        }

    def validate_id(self, value):

        try:
            User.objects.get(pk = value)
        except User.DoesNotExist:
            raise serializers.ValidationError({"User not found"})
        return value



