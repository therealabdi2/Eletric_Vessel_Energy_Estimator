from django.contrib import admin
from .models import Job, CustomUser
from django.contrib.auth.models import User

class JobsAdmin(admin.ModelAdmin):
    pass

class UsersAdmin(admin.ModelAdmin):
    pass       
    

admin.site.register(Job, JobsAdmin)
admin.site.register(CustomUser, UsersAdmin)

admin = list(CustomUser.objects.filter(username='admin'))
if admin == []:
    user = CustomUser.objects.create_user('admin', 'jose.guerrero10@yahoo.com', 'admin', is_superuser=True, isAdminUser=True, is_staff=True)