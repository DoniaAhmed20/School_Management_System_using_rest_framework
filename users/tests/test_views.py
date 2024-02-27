from .test_setup import TestSetUp

class TestViews(TestSetUp):

    def test_user_cannot_register_with_no_data(self):
        res = self.client.post(self.register_url)
        self.assertEqual(res.status_code , 400)


    def test_user_can_register_correctly(self):
        res = self.client.post(self.register_url, self.user_data,format="json")
        # import pdb
        # pdb.set_trace()
        # self.assertEqual(res.data['email'],self.user_data['email'])
        self.assertEqual(res.status_code , 201)
        


    

    # def test_user_can_login(self):
    #     # Register a user first
    #     register_response = self.client.post(self.register_url, self.user_data, format="json")
    #     self.assertEqual(register_response.status_code, 201)

    #     # Now attempt to log in with the registered user credentials
    #     login_data = {
    #         'username': self.user_data['username'],
    #         'password': self.user_data['password']
    #     }
    #     login_response = self.client.post(self.login_url, login_data, format="json")
    #     self.assertEqual(login_response.status_code, 200)
    #     self.assertIn('token', login_response.data)



from rest_framework.test import APITestCase
from django.urls import reverse
from rest_framework import status

class UserExportViewTest(APITestCase):
    def test_user_export(self):
        url = reverse('user_export')  
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response['Content-Type'], 'text/csv')

       
        self.assertIn('Email,User Type,Gender,Date of Birth,Is Active', str(response.content))








# from rest_framework.test import APITestCase
# from django.urls import reverse
# from rest_framework import status
# from django.core.files.uploadedfile import SimpleUploadedFile
# from users.models import CustomUser

# class UserImportViewTestCase(APITestCase):
#     def test_user_import(self):
#         # Create a sample CSV file with user data
#         csv_data = (
#             b"Email,User Type,Gender,Date of Birth,Is Active\n"
#             b"test1@example.com,student,male,1990-01-01,True\n"
#             b"test2@example.com,teacher,female,1985-05-15,False\n"
#         )
#         csv_file = SimpleUploadedFile("users.csv", csv_data, content_type="text/csv")

#         # Make a POST request to the UserImportView endpoint with the CSV file
#         url = reverse("user_import")
#         response = self.client.post(url, {"file": csv_file}, format="multipart")

#         # Check if the request was successful (status code 200)
#         self.assertEqual(response.status_code, status.HTTP_200_OK)

#         # Verify that the users are imported successfully
#         self.assertEqual(response.data["success"], "Users imported successfully")

#         # Optionally, you can check if the users are actually created in the database
#         self.assertEqual(CustomUser.objects.count(), 2)
