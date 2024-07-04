from django.contrib import admin

from userauths.models import User,Profiles

# Register your models here.
class UserAdmin(admin.ModelAdmin):
    list_display = ['username', 'email', 'bio']
    
class ProfilesAdmin(admin.ModelAdmin):
    list_display = ['user']

admin.site.register(User,UserAdmin)
admin.site.register(Profiles,ProfilesAdmin)