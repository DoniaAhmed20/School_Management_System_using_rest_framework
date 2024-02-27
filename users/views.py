from django.shortcuts import render
from django.core.mail import send_mail
from django.conf import settings
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .models import CustomUser
from .serializers import UserRegistrationSerializer , UserImportSerializer
from .serializers import UserRegistrationSerializer, UserProfileUpdateSerializer
from rest_framework import  viewsets
from django.utils.translation import gettext as _
from rest_framework.authtoken.models import Token
# from authentication.models import CustomToken 
from rest_framework import pagination
from rest_framework.views import APIView
from django.contrib.auth import authenticate
from .serializers import LoginSerializer
from rest_framework.permissions import IsAuthenticated
from django.contrib.auth import logout
from django.http import JsonResponse
from rest_framework.parsers import MultiPartParser , FormParser
from rest_framework import generics
from rest_framework.parsers import FileUploadParser
from django.http import HttpResponse
from datetime import datetime
import pandas as pd
import csv

# custom pagination
class CustomPagination(pagination.PageNumberPagination):
    page_size = 2
    page_size_query_param = 'page_size'
    max_page_size = 100



# Retrieve all courses with pagination.
class viewsets_User(viewsets.ModelViewSet):
    queryset = CustomUser.objects.all()
    serializer_class = UserRegistrationSerializer
    pagination_class = CustomPagination


# user registration
class UserRegistrationView(APIView):
    def post(self, request):
        serializer = UserRegistrationSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            user.set_password(request.data['password'])
            user.save()

            # Send email to admin
            admin_email = '09doniaahmed01@gmail.com' 
            message = f'A new user {user.username} has registered and requires activation. Please activate the user.'
            send_mail(
                'New User Registration - Activation Required',
                message,
                '09doniaahmed01@gmail.com',  
                [admin_email],
                fail_silently=True
            )


            token, created = Token.objects.get_or_create(user=user)
        
            if created:
                token.save()
            else:
            
                return Response({"error": "Failed to create token"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
            response_data = {
                'user': serializer.data,
                'token': token.key,
                'email': user.email  
            }
            return Response(response_data, status=status.HTTP_201_CREATED)

            # return Response({'token': token.key, 'user': serializer.data}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)



# user login (not use)
class UserLoginAPIView(APIView):

    def post(self, request):
        username = request.data.get('username')
        password = request.data.get('password')

        user = authenticate(username=username, password=password)

        if user is not None and user.is_active:
            token, _ = Token.objects.get_or_create(user=user)
            return Response({'token': token.key}, status=status.HTTP_200_OK)
        else:
            return Response({'detail': 'Invalid credentials or inactive user'}, status=status.HTTP_401_UNAUTHORIZED)




# user login
class LoginView(APIView):

    def post(self, request):
        serializer = LoginSerializer(data=request.data)

        if serializer.is_valid():
            email = serializer.validated_data['email']
            password = serializer.validated_data['password']
            
            user = authenticate(email=email, password=password)
            
            if user:
                if user.is_active:
                    token, _ = Token.objects.get_or_create(user=user)
                    return Response({'token': token.key}, status=status.HTTP_200_OK)
                else:
                    # User account is inactive
                    return Response({'error': 'Your account is inactive.'}, status=status.HTTP_401_UNAUTHORIZED)
            else:
                # Authentication failed
                return Response({'error': 'Faild to login.'}, status=status.HTTP_401_UNAUTHORIZED)
        else:
            # Invalid data provided
            return Response({'error': 'Invalid data. Please provide valid username and password.'}, status=status.HTTP_400_BAD_REQUEST)




# Get and update user profile
class MyProfileView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        profile = request.user
        
        serializer = UserRegistrationSerializer(profile)
        
        return Response(serializer.data, status=status.HTTP_200_OK)

    def put(self, request):
        profile = request.user
        serializer = UserProfileUpdateSerializer(profile, data=request.data)
        
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        



# Active user
class ActivateUserView(APIView):
    def post(self, request):
        user_id = request.data.get('user_id')
        try:
            user = CustomUser.objects.get(pk=user_id)
            user.is_active = True
            user.save()
            return Response({'message': 'User activated successfully'}, status=status.HTTP_200_OK)
        except CustomUser.DoesNotExist:
            return Response({'error': 'User not found'}, status=status.HTTP_404_NOT_FOUND)
        



# export users
class UserExportView(generics.GenericAPIView):
    def get(self, request):
        users = CustomUser.objects.all()
        serializer = UserRegistrationSerializer(users, many=True)
        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = 'attachment; filename="users.csv"'

        writer = csv.writer(response)
        writer.writerow(['Email', 'User Type', 'Gender', 'Date of Birth'])

        for user in serializer.data:
            writer.writerow([user['email'], user['user_type'], user['gender'], user['date_of_birth']])

        return response

class UserImportView(generics.GenericAPIView):
    parser_classes = (FileUploadParser,)

    def post(self, request):
        csv_file = request.FILES['file']
        if not csv_file.name.endswith('.csv'):
            return Response({'error': 'Invalid file format. Please upload a CSV file.'}, status=400)

        try:
            decoded_file = csv_file.read().decode('utf-8').splitlines()
            reader = csv.DictReader(decoded_file)
            for row in reader:
                CustomUser.objects.create(
                    email=row['Email'],
                    user_type=row['User Type'],
                    gender=row['Gender'],
                    date_of_birth=row['Date of Birth'],
                    is_active=row['Is Active']
                )
            return Response({'success': 'Users imported successfully'}, status=200)
        except Exception as e:
            return Response({'error': str(e)}, status=400)
        




# import users
class ImportAPIView(APIView):
    serializer_class = UserImportSerializer
    parser_classes = [MultiPartParser, FormParser]

    def post(self, request):
        try:
            data = request.FILES
            serializer = self.serializer_class(data=data)
            if not serializer.is_valid():
                return Response({'status': False, 'message': 'Provide a valid file'},
                                status=status.HTTP_400_BAD_REQUEST)
            csv_file = data.get('file')
            df = pd.read_csv(csv_file)  
            for index, row in df.iterrows():
                username = row['username']
                email = row['email']
                password = row['password']
                gender = row['gender']
                user_type = row['user_type']
                
                # Default date_of_birth value
                default_date_of_birth = datetime(2000, 1, 1).strftime('%Y-%m-%d')
                
                date_of_birth = str(row.get('date_of_birth', default_date_of_birth))
                
                existing_user = CustomUser.objects.filter(email=email).first()
                if existing_user:
                    # Update the existing user's information
                    existing_user.username = username
                    existing_user.password = password
                    existing_user.gender = gender
                    existing_user.user_type = user_type
                    existing_user.date_of_birth = date_of_birth
                    existing_user.save()
                else:
                    # Create a new user
                    CustomUser.objects.create(
                        username=username,
                        email=email,
                        password=password,
                        gender=gender,
                        user_type=user_type,
                        date_of_birth=date_of_birth
                    )
            return Response({'status': True, 'message': 'Users imported successfully'},
                            status=status.HTTP_201_CREATED)
        except Exception as e:
            return Response({'status': False, 'message': str(e)},
                            status=status.HTTP_400_BAD_REQUEST)
        


# logout user
def custom_logout(request):
    if request.method == 'POST':
        logout(request)
        return JsonResponse({'message': 'Logout successful.'})
    else:
        return JsonResponse({'error': 'Method not allowed. Only POST requests are allowed for logout.'}, status=405)




# class MyProfileView(APIView):
#     permission_classes = [IsAuthenticated]

#     def get(self, request):
#         # Retrieve the profile of the authenticated user
#         profile = request.user  # Get the authenticated user directly
        
#         # Serialize the profile data if needed
#         serializer = UserRegistrationSerializer(profile)  # Replace YourProfileSerializerClass with your actual serializer
        
#         return Response(serializer.data, status=status.HTTP_200_OK)
