from django.shortcuts import render,HttpResponse,redirect
from django.contrib.auth import login, logout, authenticate
from django.core.paginator import Paginator, EmptyPage

# Create your views here.
from .models import *
from .forms import *


def user_login(request):
    if request.method == 'POST':
        username = request.POST['u_email']
        password = request.POST['u_password']
        print(username)
        print(password)

        user=authenticate(username=username, password=password)
        if(user):
            login(request, user)
            return redirect('/userprofile')


    return render(request, 'login.html')

def user_profile(request):
    user=request.user
    user=User.objects.get(username=user)
    print(user)
    userprofile=UserProfile.objects.get(user = user)
    usersociallink=SocialLink.objects.get(user=user)
    context={'userprofile':userprofile,'usersociallink':usersociallink}
    return render(request, 'userprofile.html', context)


def add_leave_from(request):
    if request.method == 'POST':
        print(request.user)
        #user = request.user
        form = LeaveApplicationForm(request.POST)
        # print('startdate')
        # print(request.POST['start_date'])
        # print("enddate")
        # print(request.POST['end_date'])

        # print(form)
        if form.is_valid():
            print(1)
            form = form.save(commit = False)
            print(2)
            form.user = request.user
            print(3)
            form.save()
            print(5)
            form = LeaveApplicationForm()
            context={'msg':"Leave Application Successfully Saved",'form':form}
            return render(request, 'add_leave_from.html', context)
    else:
        user_application=LeaveApplication.objects.filter(checked=False, user=request.user)
        if user_application:
            context={'msg':"You have already a pending application"}
            return render(request, 'add_leave_from.html', context)
        else:
            form = LeaveApplicationForm()
            context={'form':form}
            return render(request, 'add_leave_from.html', context)

def all_application(request):
    applications=LeaveApplication.objects.filter(checked=False)
    print(applications)
    paginator = Paginator(applications, 25)
    print(paginator) # Show 25 contacts per page.
    page_number = request.GET.get('page')
    print(page_number)
    page_obj = paginator.get_page(page_number)
    print(page_obj)
    context={'applications':page_obj}
    return render(request, 'all_application.html',context)

def applicatin_approval(request, id, sts):
    application=LeaveApplication.objects.get(id=id)
    application.checked=True
    if sts == 0:
        # application.approved=False
        # application.save()
        application.delete()
        # #application.save()
        # print("Leave application Rejected")
        # return redirect('/all-application')
        context={'msg':"Leave application Rejected"}
        return render(request, 'all_application.html', context)
    else:
        application.approved=True
        application.save()
        context={'msg':"Leave application Approved"}
        return render(request, 'all_application.html', context)

def to_do_list(request):
    my_todo_list_pending=ToDoList.objects.filter(user=request.user,pending_status=True)
    working_todo_list=ToDoList.objects.filter(user=request.user,working_status=True) 
    done_todo_list=ToDoList.objects.filter(user=request.user,done_status=True)
    my_todo_list_pending_count=my_todo_list_pending.count()
    working_todo_list_count=working_todo_list.count()
    done_todo_list_count=done_todo_list.count()
    form=TodolistForm()
    context={'my_todo_list_pending':my_todo_list_pending,'my_todo_list_pending_count':my_todo_list_pending_count,
             'working_todo_list':working_todo_list,'working_todo_list_count':working_todo_list_count,
             'done_todo_list':done_todo_list,'done_todo_list_count':done_todo_list_count,
             'form':form
    }
    return render(request, 'todolist.html',context)

def to_do_list_move(request, id, sts):
    print(sts)
    print(id)

    my_todo_list=ToDoList.objects.get(id=id)
    if sts=="working":
        my_todo_list.pending_status=False
        my_todo_list.working_status=True
        my_todo_list.save()
        return redirect('/todolist')
        # my_todo_list=ToDoList.objects.get(id=id)


    elif sts=="done":
        my_todo_list.working_status=False
        my_todo_list.done_status=True
        my_todo_list.save()
        return redirect('/todolist')

    return redirect('/todolist')
def add_todo_list(request):
    if request.method == 'POST':
        form=TodolistForm(request.POST)
        if form.is_valid():
            form=form.save(commit=False)
            form.user=request.user
            form.save()
            return redirect('/todolist')

def user_logout(request):
    logout(request)
    return redirect('/')