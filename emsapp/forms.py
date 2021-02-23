from .models import *
from django import forms

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