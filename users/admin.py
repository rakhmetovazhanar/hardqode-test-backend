from django.contrib import admin
from .models import Balance, CustomUser

# Register your models here.
admin.site.register(CustomUser)
admin.site.register(Balance)