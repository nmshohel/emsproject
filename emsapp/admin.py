from django.contrib import admin
from.models import *
# Register your models here.
class Todolistadmin(admin.ModelAdmin):
    list_display=('user','pending_status','working_status','done_status','when_to_do')

admin.site.register(UserProfile)
admin.site.register(SocialLink)
admin.site.register(LeaveApplication)
admin.site.register(ToDoList,Todolistadmin)
admin.site.register(Department)



