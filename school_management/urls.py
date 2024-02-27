"""
URL configuration for school_management project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from courses.views import viewsets_Course, UserCoursesView, CoursesWithSeatch, TeacherCoursesView, TeacherEnrolledUsersView, CourseListView 
from enrollments.views import viewsets_Enrollment, EnrollCourse , LeaveCourse , MyEnrollmentsView, EnrollmentHistoryView
from users.views import custom_logout, ImportAPIView, viewsets_User, UserRegistrationView, UserLoginAPIView, LoginView, MyProfileView, ActivateUserView, UserExportView, UserImportView
from rest_framework.routers import DefaultRouter
from django.contrib.auth.views import LogoutView

router = DefaultRouter()
router.register('courses', viewsets_Course)
router.register('enrollments', viewsets_Enrollment)
router.register('users', viewsets_User)


urlpatterns = [
    path('admin/', admin.site.urls),
    path('api-auth/', include('rest_framework.urls')),
    path('rest/viewsets/', include(router.urls)),
    # path('api-auth/logout/', LogoutView.as_view(), name='logout'),
    path('api-auth/logout/', custom_logout, name='logout'),
    path('register/', UserRegistrationView.as_view(), name='register'),
    path('login/', UserLoginAPIView.as_view(), name='user-login'),
    path('api/login/', LoginView.as_view(), name='login'),
    path('my_profile/', MyProfileView.as_view(), name='my_profile'),
    path('enroll/<int:course_id>/', EnrollCourse.as_view(), name='enroll-course'),
    path('enrollments/<int:enrollment_id>/leave/', LeaveCourse.as_view(), name='leave_course'),
    path('my_enrollments/', MyEnrollmentsView.as_view(), name='my_enrollments'),
    path('enrollment_history/', EnrollmentHistoryView.as_view(), name='enrollment_history'),
    path('user_courses/', UserCoursesView.as_view(), name='user_courses'),
    path('teacher_courses/', TeacherCoursesView.as_view(), name='teacher_courses'),
    path('teacher_enrolled_users/', TeacherEnrolledUsersView.as_view(), name='teacher_enrolled_users'),
    path('coursessearch/', CourseListView.as_view(), name='course-list'),
    path('coursessearch1/', CoursesWithSeatch.as_view(), name='course-list'),
    path('activate-user/', ActivateUserView.as_view(), name='activate_user'),
    path('export/', UserExportView.as_view(), name='user_export'),
    path('import/', UserImportView.as_view(), name='user_import'),
    
    path('importt/', ImportAPIView.as_view(), name='import'),

    path('', include(router.urls)),
]

