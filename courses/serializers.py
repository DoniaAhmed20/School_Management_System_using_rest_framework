from rest_framework import serializers
from .models import Course
from users.serializers import UserRegistrationSerializer

class CourseSerializer(serializers.ModelSerializer):
    enrolled_users = UserRegistrationSerializer(many=True, read_only=True)

    class Meta:
        model = Course
        fields = ['id', 'name', 'start_date', 'end_date', 'active', 'teacher', 'image', 'enrolled_users']