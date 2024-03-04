

## **INTRODUCTION**

School Management System



## **INSTALLATION**

- **CLONE THE REPOSITORY**
  <pre>
    git clone https://github.com/DoniaAhmed20/School_Management_System_using_rest_framework.git
  </pre>

- **STAND ON THE RIGHT PATH**
  <h4>Use the command cd followed by the directory path School_Management_System_Without_Rest_Framework</h4>
  <pre>
    cd School_Management_System_using_rest_framework
  </pre>

- **Create a Virtual Environment**
  <pre>
    python -m venv venv
  </pre>

- **Activate the Virtual Environment**
  <pre>
    venv\Scripts\activate
  </pre>

- **INSTALL DEPENDENCIES**
  <pre>
    pip install -r requirements.txt
    python -m pip install Pillow
  </pre>

- **Apply Migrations**
  <pre>
    python manage.py makemigrations
  </pre>

- **Apply Migrations**
  <pre>
    python manage.py migrate
  </pre>

- **RUN SERVER**
  <h4>Use the command cd followed by the directory path frontend</h4>
  <pre>
    python manage.py runserver 
  </pre>

  -**NOTE**
   <h4>to access admin panel should comment the line <h1>AUTH_USER_MODEL = 'users.User'</h1> in settings.py file</h4>

  
<h4>Open your web browser and navigate to ` http://127.0.0.1:8000/` to access the Threads & Beads website.</h4><br>


## **DEMO**

🎥 Watch Our Demo Video from [Here](https://drive.google.com/file/d/1iM9JdXfcUACD6MPkI0O4cvLsJKxN7F4Z/view?usp=sharing)


## **Postman**
[Here](https://bold-equinox-118713.postman.co/workspace/My-Workspace~911ad57c-b301-4305-8cbb-a8d0adf2a497/collection/26326579-7ea6bb0c-0828-4c1f-ba75-13633ef61f79?action=share&creator=26326579)


## **FEATURES**

- **Rest Framework Interface**<br>
   Useers can see all the courses with pagination

- **Authorization and Authentication**<br>
  User can Register and login.

- **Users Types**<br>
  The sytem offers to users to be login and register as teacher or user.

- **User Profile**<br>
  The user (teacher or student) can see his profile and update his data.

- **Search Functionality**<br>
  The sytem offers searching for courses based on it`s name and teacher name.

- **Enroll courses**<br>
  The website provides to users to enroll to many courses but with some conditions: before the course start date, and the course must be active.
  
- **Leave Course**<br>
  The website provides users to leave their courses before the course start date.

- **Enrollments History**<br>
  The website offers to users to see their enrollments history.

- **Courses History**<br>
  The website offers to teachers to see their courses history.
  
- **Active Profile**<br>
  The admin can active user profile with many ways from admin panale or by command can active by user_id or username and can active all users with one comand.



## **TECHNOLOGIES**

- Django (Python).
- Rest FrameWork.

<br>
