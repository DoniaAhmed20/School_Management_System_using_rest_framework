from django.core.exceptions import ValidationError
from django.db import models
from django.utils import timezone
from users.models import CustomUser
from courses.models import Course
from django.contrib import admin

class Enrollment(models.Model):
    student = models.ForeignKey(CustomUser, related_name='enrollments_as_student', on_delete=models.CASCADE)
    course = models.ForeignKey(Course, related_name='enrollments', on_delete=models.CASCADE)
    enrollment_date = models.DateTimeField(auto_now_add=True)

    def save(self, *args, **kwargs):
        if self.course.active and self.course.start_date > timezone.now().date():
            super().save(*args, **kwargs)
        else:
            raise ValidationError('Course is not active or has already started.')
        

class EnrollmentAdmin(admin.ModelAdmin):
    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == "student":
            kwargs["queryset"] = CustomUser.objects.filter(user_type="student")
        return super().formfield_for_foreignkey(db_field, request, **kwargs)

admin.site.register(Enrollment, EnrollmentAdmin)
