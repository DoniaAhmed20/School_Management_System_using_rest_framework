from django.shortcuts import render
from rest_framework import  viewsets
from .models import Course
from .serializers import CourseSerializer
from rest_framework import pagination
from rest_framework.decorators import action
from rest_framework import generics
from rest_framework import filters
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from enrollments.serializers import EnrollmentSerializer 
from rest_framework import status



# custom pagination
class CustomPagination(pagination.PageNumberPagination):
    page_size = 2
    page_size_query_param = 'page_size'
    max_page_size = 100


# Retrieve all courses with pagination #option 1.
class viewsets_Course(viewsets.ModelViewSet):
    queryset = Course.objects.all()
    serializer_class = CourseSerializer
    pagination_class = CustomPagination

    @action(detail=False, methods=['GET'])
    def search(self, request):
        query = request.query_params.get('query', None)
        if query:
            courses = Course.search(query)
            serializer = self.get_serializer(courses, many=True)
            return Response(serializer.data)
        else:
            return Response({'error': 'Query parameter "query" is required'}, status=status.HTTP_400_BAD_REQUEST)




# Show all courses #option 2.
class CourseListView(generics.ListAPIView):
    serializer_class = CourseSerializer

    def get_queryset(self):
        queryset = Course.objects.all()

        name = self.request.query_params.get('name', None)
        teacher_name = self.request.query_params.get('teacher', None)

        if name:
            queryset = queryset.filter(name__icontains=name)
        if teacher_name:
            queryset = queryset.filter(teacher__username__icontains=teacher_name)

        return queryset
  

# add search by course_name and teacher_name
class CoursesWithSeatch(generics.ListAPIView):
    queryset = Course.objects.all()
    serializer_class = CourseSerializer
    filter_backends = [filters.SearchFilter]
    search_fields = ['name', 'teacher__username']


# show teacher course or student courses
class UserCoursesView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        if request.user.user_type == 'teacher':
            # Retrieve courses taught by the teacher
            user_courses = Course.objects.filter(teacher=request.user)
        else:
            # Retrieve courses in which the student is enrolled
            user_courses = request.user.enrollments_as_student.all().select_related('course')

        serializer = CourseSerializer(user_courses, many=True)
        return Response(serializer.data)
    

# Retrieve courses taught by the teacher (Not Using)
class TeacherCoursesView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        
        teacher_courses = Course.objects.filter(teacher=request.user)
        serializer = CourseSerializer(teacher_courses, many=True)
        return Response(serializer.data)
    


# Retrieve students enrolled to teacher course
class TeacherEnrolledUsersView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        courses = Course.objects.filter(teacher=request.user)
        if not courses.exists():
            return Response({'error': 'No courses found for this teacher'}, status=status.HTTP_404_NOT_FOUND)
        course = courses.first()
        enrollments = course.enrollments.all()
        enrolled_users = EnrollmentSerializer(enrollments, many=True).data
        return Response(enrolled_users)
