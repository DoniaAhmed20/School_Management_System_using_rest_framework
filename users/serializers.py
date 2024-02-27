from rest_framework import serializers
from .models import CustomUser
from enrollments.models import Enrollment

class UserRegistrationSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)
    enrollments_as_student = serializers.PrimaryKeyRelatedField(queryset=Enrollment.objects.all(), required=False, many=True)

    class Meta:
        model = CustomUser
        fields = ('username', 'password', 'email', 'user_type', 'gender', 'date_of_birth', 'cv', 'enrollments_as_student')

    def create(self, validated_data):
        enrollments_data = validated_data.pop('enrollments_as_student', [])  
        user = CustomUser.objects.create_user(**validated_data)  
        if enrollments_data:
            user.enrollments_as_student.set(enrollments_data)  
        return user

class LoginSerializer(serializers.Serializer):
    email = serializers.CharField()
    password = serializers.CharField(style={'input_type': 'password'})


class UserProfileUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ['username', 'email', 'user_type', 'gender', 'date_of_birth', 'cv']



class UserImportSerializer(serializers.Serializer):
    file = serializers.FileField()

