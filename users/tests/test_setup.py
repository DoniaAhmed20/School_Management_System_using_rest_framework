from rest_framework.test import APITestCase
from django.urls import reverse

class TestSetUp(APITestCase):
    
    def setUp(self) :
        self.register_url = reverse('register')
        self.login_url = reverse('login')
       
        self.user_data = {
            "username": "test",
            "password": "12345678",
            "email": "test@gmail.com",
            "user_type": "student",
            "gender": "male",
            "date_of_birth": "2024-01-01",
            # "cv": File(cv_file),
            "enrollments_as_student": []
        }
        return super().setUp()
    

    def tearDown(self) :
        return super().tearDown()
    