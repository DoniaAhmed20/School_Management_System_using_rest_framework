from rest_framework import serializers
from .models import Enrollment
from users.serializers import UserRegistrationSerializer
from courses.serializers import CourseSerializer
from django.utils import timezone

class EnrollmentSerializer(serializers.ModelSerializer):
    student = UserRegistrationSerializer(read_only=True)
    course = CourseSerializer(read_only=True)

    class Meta:
        model = Enrollment
        fields = ['id', 'student', 'course', 'enrollment_date']

    def validate(self, data):
        course = data['course']
        if not course.active or course.start_date <= timezone.now().date():
            raise serializers.ValidationError("Course is not active or has already started.")
        return data
