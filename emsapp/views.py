from django.shortcuts import render,HttpResponse,redirect
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.core.paginator import Paginator, EmptyPage,PageNotAnInteger

# Create your views here.
from .models import *
from .forms import *
import csv,datetime,xlwt
from django.template.loader import render_to_string
from weasyprint import HTML
import tempfile
from django.db.models import Sum
from xhtml2pdf import pisa
from io import BytesIO
import sys
import matplotlib
import matplotlib.pyplot as plt
import numpy
import numpy as np

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

@login_required(login_url='')
def user_profile(request):
    user=request.user
    user=User.objects.get(username=user)
    print(user)

    y = np.array([35, 25, 25, 15])
    print(type(y))
    mylabels = ["Apples", "Bananas", "Cherries", "Dates"]
    plt.pie(y, labels = mylabels, startangle = 90)
    p=plt.show()

    plt.savefig(sys.stdout.buffer)
    sys.stdout.flush()

    print(matplotlib.__version__)
    userprofile=UserProfile.objects.get(user = user)
    usersociallink=SocialLink.objects.get(user=user)
    context={'userprofile':userprofile,'usersociallink':usersociallink,'p':p,'user':user}
    return render(request, 'userprofile.html', context)

@login_required(login_url='/')
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

@login_required(login_url='/')
def all_application(request):
    applications=LeaveApplication.objects.filter(checked=False)

    p= Paginator(applications, 2) #item per page

    total_page=p.num_pages
    
    page_number = request.GET.get('page',1)
    try:
        page=p.page(page_number)
    except EmptyPage:
        page=p.page(1)

    # page_obj = paginator.get_page(page_number)
    context={'applications':page,'total_page':total_page,'page_number':page_number}
    # context={'applications':applications,'page_obj':page}
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

@login_required(login_url='/')
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

def export_csv_all_application(request):
    response=HttpResponse(content_type='text/csv')
    response['Content-Disposition']='attachment; filename=Allapplication'+\
        str(datetime.datetime.now())+'.csv'

    writer=csv.writer(response)
    writer.writerow(['User','Case of Leave','Leave Category','Star Date','End Date'])
    all_application=LeaveApplication.objects.filter(user=request.user)
    for all_app in all_application:
        writer.writerow([all_app.user,all_app.case_of_leave,all_app.leave_category,all_app.star_date,all_app.end_date])
    return response

def export_xls_all_application(request):
    response = HttpResponse(content_type='application/ms-excel')
    response['Content-Disposition'] = 'attachment; filename="users.xls"'
    wb = xlwt.Workbook(encoding='utf-8')
    ws = wb.add_sheet('Users')
    # Sheet header, first row
    row_num = 0
    font_style = xlwt.XFStyle()
    font_style.font.bold = True
    columns = ['User','Case of Leave','Leave Category','Star Date','End Date']
    for col_num in range(len(columns)):
        ws.write(row_num, col_num, columns[col_num], font_style)
    # Sheet body, remaining rows
    font_style = xlwt.XFStyle()
    rows = LeaveApplication.objects.all().values_list('user', 'case_of_leave', 'leave_category', 'star_date','end_date')
    for row in rows:
        row_num += 1
        for col_num in range(len(row)):
            ws.write(row_num, col_num, row[col_num], font_style)
    wb.save(response)
    return response

def generate_pdf(request):
    html = '<html><body><p>To PDF or not to PDF</p></body></html>'
    write_to_file = open('media/test.pdf', "w+b")
    result = pisa.CreatePDF(html,dest=write_to_file)
    write_to_file.close()
    return HttpResponse(result.err)

def generate_pdf_through_template(request):
    context={}

    html = render_to_string('pdf_template.html',context)
    
    write_to_file = open('media/test_1.pdf', "w+b")
    
    result = pisa.CreatePDF(html,dest=write_to_file)
    
    write_to_file.close()
    
    return HttpResponse(result.err)


def render_pdf(request):
    path = "pdf_template.html"
    context = {"states" : State.objects.all()[:100]}

    html = render_to_string('pdf_template.html',context)
    io_bytes = BytesIO()
    
    pdf = pisa.pisaDocument(BytesIO(html.encode("UTF-8")), io_bytes)
    
    if not pdf.err:
        return HttpResponse(io_bytes.getvalue(), content_type='application/pdf')
    else:
        return HttpResponse("Error while rendering PDF", status=400)

def export_pdf_all_application(request):
    path = "pdf_output.html"
    context = {"LeaveApplications" : LeaveApplication.objects.all()[:100]}

    html = render_to_string('pdf_output.html',context)
    io_bytes = BytesIO()
    
    pdf = pisa.pisaDocument(BytesIO(html.encode("UTF-8")), io_bytes)
    
    if not pdf.err:
        return HttpResponse(io_bytes.getvalue(), content_type='application/pdf')
    else:
        return HttpResponse("Error while rendering PDF", status=400)
@login_required(login_url='/')
def add_employee(request):
    if request.method == 'POST':
        username=request.POST['username']
        password=request.POST['password']
        department_id=request.POST['department']
        email=request.POST['email']
        f_name=request.POST['first_name']
        l_name=request.POST['last_name']
        designation_id=request.POST['designation']
        department=Department.objects.get(id=department_id)
        designation=Group.objects.get(id=designation_id)
        print(username)
        print(password)
        print(email)
        print(department)
        # user=User.objects.create_user(username=username, password=password)
        # profile=UserProfile.objects.create(user=user,department=department.name,email_address=email)
        # sociallink=SocialLink.objects.create(user=user)

        user = User.objects.create_user(username = username, password = password, first_name=f_name, last_name=l_name)
        profile = UserProfile.objects.create(user = user, department = department, email_address = email,designation=designation)
        sociallink=SocialLink.objects.create(user=user)
        form = UserForm()
        message = "Successfully Added!"
        status = 'success'
        context = {'form':form, 'message':message, 'sts':status}
        return render(request, 'add_employee.html', context)

    else:
        form = UserForm()
        context = {'form':form}
        return render(request, 'add_employee.html', context)
    
    
        

    # else:
    #     form = UserForm()
    #     message = "password not matched"
    #     status = 'danger'
    #     context = {'form':form, 'message':message,'sts':status}
    #     return render(request, 'add_employee.html', context)

