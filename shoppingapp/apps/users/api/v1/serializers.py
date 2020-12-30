from rest_framework import serializers
from apps.users.models import User


class RegistrationSerializer(serializers.ModelSerializer):

    password2 = serializers.CharField(style={'input_type':'password'},write_only=True)
    first_name = serializers.CharField()

    class Meta:
        model = User
        fields = ['email','username','first_name','password','password2']
        extra_kwargs = {
            'password':{'write_only':True}
        }

    def save(self):
        user = User(
            email=self.validated_data['email'],
            username=self.validated_data['username']
        )
        password=self.validated_data['password']
        password2=self.validated_data['password2']
        first_name=self.validated_data['first_name']

        if password != password2:
            raise serializers.ValidationError({'password':'Passwords must match'})
        user.set_password(password)
        user.save()
        return user
        