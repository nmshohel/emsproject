from django.contrib import admin
from django.urls import path
from .views import *
urlpatterns = [

    path('to-do-list-move/<int:id>/<sts>', to_do_list_move, name='to_do_list_move'),
    path('userprofile', user_profile, name='user_profile'),
    path('applicatin-approval/<int:id>/<int:sts>', applicatin_approval, name='applicatin_approval'),
    path('all-application', all_application, name='all_application'),
    path('add-leavefrom', add_leave_from, name='add_leave_from'),
    path('', user_login, name='user_login'),
    path('todolist', to_do_list, name='todolist'),
    path('add-todo-list', add_todo_list, name='add_todo_list'),
    path('user-logout', user_logout, name='user_logout')
    
]
