from .models import *
from django import forms
from django.contrib.auth.models import User,Group
from .models import *

# from django.forms import ModelForm


class LeaveApplicationForm(forms.ModelForm):
    class Meta:
        model = LeaveApplication
        fields = ['case_of_leave','leave_category', 'star_date', 'end_date']

        widgets = {
             'case_of_leave':forms.Textarea(attrs={'class':'form-control bg-light form'}),
             'leave_category':forms.TextInput(attrs={'class':'form-control bg-light'}),
             'star_date':forms.DateInput(attrs={'type':'date', 'class':'form-control datepicker bg-light'}),
             'end_date':forms.DateInput(attrs={'type':'date', 'class':'form-control datepicker bg-light'})
        }
class TodolistForm(forms.ModelForm):
    class Meta:
        model = ToDoList 
        fields = '__all__'
        exclude=('user','pending_status','working_status','done_status',)

        widgets = {
            'when_to_do':forms.DateInput(attrs={'type':'date', 'class':'form-control datepicker bg-light'}),
            'what_to_do':forms.TextInput(attrs={'class':'form-control bg-light'}),

        }
class UserForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput(attrs={'class':'form rounded form-group col-md-6 mt-3 bg-light', 'placeholder':"Enter Password..."}))
    department = forms.ModelChoiceField(widget=forms.Select(attrs={'class':'rounded form form-group bg-light col-md-6',}), queryset =Department.objects.all())
    designation=forms.ModelChoiceField(widget=forms.Select(attrs={'class':'rounded form form-group bg-light col-md-6',}), queryset=Group.objects.all())
    
    class Meta:
        model=User
        fields=['first_name','last_name','username', 'password','department','email','designation']
        help_texts={
            'username':None, 
            'email':None
          
        }
        widgets={
            'username':forms.TextInput(attrs={'class':'form rounded form-group bg-light col-md-4 mt-3', 'placeholder':"Enter UserName..."}),
            'email':forms.TextInput(attrs={'class':'form form-control bg-light col-md-5', 'placeholder':"Enter Email..."}),
            'first_name':forms.TextInput(attrs={'class':'rounded form form-group bg-light col-md-5', 'placeholder':"Enter First Name..."}),
            'last_name':forms.TextInput(attrs={'class':'rounded form form-group bg-light col-md-5', 'placeholder':"Enter Last Name..."}),
        } 