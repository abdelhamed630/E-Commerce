from django.contrib import admin
from .models import Account

# Register your models here.
@admin.register(Account)
class accountAdmin(admin.ModelAdmin):
    list_display =('first_name','username','email')
    search_fields =['username']
    