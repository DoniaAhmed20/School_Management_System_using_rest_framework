from django.core.exceptions import ValidationError
from django.db import models
from users.models import CustomUser
from django.contrib import admin
# from .models import Course

class Course(models.Model):
    name = models.CharField(max_length=100)
    start_date = models.DateField()
    end_date = models.DateField()
    active = models.BooleanField(default=False)
    teacher = models.ForeignKey(CustomUser, related_name='courses_taught', on_delete=models.CASCADE)
    image = models.ImageField(upload_to='course_images/', null=True, blank=True) 

    def save(self, *args, **kwargs):
        if not self.pk:  
            if Course.objects.filter(teacher=self.teacher, active=True).exists():
                raise ValidationError('The selected teacher already has an active course.')
            else:
                self.active = True
        super().save(*args, **kwargs)


    def __str__(self):
        return self.name 


class CourseAdmin(admin.ModelAdmin):
    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == "teacher":
            kwargs["queryset"] = CustomUser.objects.filter(user_type="teacher")
        return super().formfield_for_foreignkey(db_field, request, **kwargs)

admin.site.register(Course, CourseAdmin)




