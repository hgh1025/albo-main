from django.contrib import admin
from . models import *
# Register your models here.


class UserAdmin(admin.ModelAdmin):
  search_fields=['subject']
  
admin.site.register(User,UserAdmin)
admin.site.register(Item)
admin.site.register(Comment)
admin.site.register(Trade)
