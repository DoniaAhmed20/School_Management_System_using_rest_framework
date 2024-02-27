from django.shortcuts import render
from rest_framework import  viewsets
from .models import Enrollment
from .serializers import EnrollmentSerializer
from rest_framework import pagination
from courses.serializers import CourseSerializer
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from courses.models import Course
from django.utils import timezone
from rest_framework.permissions import IsAuthenticated
import datetime

# custom pagination
class CustomPagination(pagination.PageNumberPagination):
    page_size = 2
    page_size_query_param = 'page_size'
    max_page_size = 100



# Retrieve all enrollments with pagination .
class viewsets_Enrollment(viewsets.ModelViewSet):
    queryset = Enrollment.objects.all()
    serializer_class = EnrollmentSerializer
    pagination_class = CustomPagination





# Enroll student into course
class EnrollCourse(APIView):
    def post(self, request, course_id):
        try:
            course = Course.objects.get(pk=course_id)
        except Course.DoesNotExist:
            return Response({'error': 'Course not found'}, status=status.HTTP_404_NOT_FOUND)
        course_start_datetime = datetime.datetime.combine(course.start_date, datetime.time())
        course_start_datetime_aware = timezone.make_aware(course_start_datetime, timezone.get_default_timezone())

        # Check if the course is active and has not started yet
        if course.active and course_start_datetime_aware > timezone.now():
            enrollment = Enrollment(student=request.user, course=course)
            enrollment.save()
            serializer = EnrollmentSerializer(enrollment)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response({'error': 'Course is not active or has already started'}, status=status.HTTP_400_BAD_REQUEST)
        






# student leave courses
class LeaveCourse(APIView):
    def post(self, request, enrollment_id):
        try:
            enrollment = Enrollment.objects.get(pk=enrollment_id)
        except Enrollment.DoesNotExist:
            return Response({'error': 'Enrollment not found'}, status=status.HTTP_404_NOT_FOUND)
        
        course = enrollment.course
        course_start_datetime = datetime.datetime.combine(course.start_date, datetime.time())
        course_start_datetime_aware = timezone.make_aware(course_start_datetime, timezone.get_default_timezone())

        if course_start_datetime_aware > timezone.now():
            enrollment.delete()
            return Response({'message': 'Enrollment successfully removed'}, status=status.HTTP_200_OK)
        else:
            return Response({'error': 'You cannot leave this course as it has already started'}, status=status.HTTP_400_BAD_REQUEST)






# Retrieve all student`s courses.
class MyEnrollmentsView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        enrollments = Enrollment.objects.filter(student=request.user)
        enrollments_not_ended = enrollments.filter(course__end_date__gte=timezone.now())
        serializer = EnrollmentSerializer(enrollments_not_ended, many=True)
        return Response(serializer.data)
    



# Retrieve history courses for teacher or student
class EnrollmentHistoryView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user = request.user
        if user.user_type == 'student':
            user_enrollments = Enrollment.objects.filter(student=user, course__end_date__lt=timezone.now())
            serializer = EnrollmentSerializer(user_enrollments, many=True)
            return Response(serializer.data)
        elif user.user_type == 'teacher':
            teacher_courses = Course.objects.filter(teacher=user, end_date__lt=timezone.now())
            serializer = CourseSerializer(teacher_courses, many=True)
            return Response(serializer.data)
        else:
            return Response({'message': 'User type not supported'}, status=status.HTTP_400_BAD_REQUEST)

