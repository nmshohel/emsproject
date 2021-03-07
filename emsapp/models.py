from django.db import models
from django.contrib.auth.models import User
#from .models import Blog
from django.views.generic import ListView

# Create your models here.

# class Department(models.Model):
#     name=models.CharField(max_length=250)

#     def __str__(self):
#         return self.name

class UserProfile(models.Model):
    user=models.OneToOneField(User, on_delete=models.CASCADE)
    profile_image=models.ImageField(blank=True, null=True)
    address=models.CharField(max_length=300, blank=True, null=True)
    # department=models.ForeignKey(Department, on_delete=models.CASCADE,blank=True, null=True)
    designation=models.CharField(max_length=300, blank=True, null=True)
    date_of_birth=models.DateField(blank=True, null=True)
    email_address=models.CharField(max_length=300, blank=True, null=True)
    mobile_number=models.CharField(max_length=100, blank=True, null=True)

    def __str__(self):
        return str(self.user)

class SocialLink(models.Model):
    user=models.OneToOneField(User, on_delete=models.CASCADE)
    web_link=models.CharField(max_length=300, blank=True, null=True)
    git_link=models.CharField(max_length=300, blank=True, null=True)
    twitter_link=models.CharField(max_length=300, blank=True, null=True)
    instragram_link=models.CharField(max_length=300, blank=True, null=True)
    fb_link=models.CharField(max_length=300, blank=True, null=True)
    
    def __str__(self):
        return str(self.user)
class LeaveApplication(models.Model):
    user=models.ForeignKey(User, on_delete=models.CASCADE)
    case_of_leave=models.TextField(blank=True, null=True)
    leave_category=models.CharField(max_length=250)
    star_date=models.DateField(blank=True, null=True)
    end_date=models.DateField(blank=True, null=True)
    date=models.DateField(auto_now_add=True)
    checked=models.BooleanField(default=False)
    approved=models.BooleanField(default=False)

    def __str__(self):
        return str(self.user)

class ToDoList(models.Model):
    user=models.ForeignKey(User, on_delete=models.CASCADE)
    what_to_do=models.TextField(blank=True, null=True)
    when_to_do=models.DateField(blank=True, null=True)
    pending_status=models.BooleanField(default=True)
    working_status=models.BooleanField(default=False)
    done_status=models.BooleanField(default=False)

    def __str__(self):
        return str(self.user) 


