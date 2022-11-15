from django.contrib import admin
from .models import MyUser,todolist

admin.site.register(MyUser)
admin.site.register(todolist)