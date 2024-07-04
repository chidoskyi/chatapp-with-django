from django.contrib import admin
from chatapp.models import Messages,Message,Room,Topic
from import_export.admin import ImportExportModelAdmin

class MessagesAdmin(ImportExportModelAdmin):
    list_display = ['user', 'recipient', 'body', 'is_read']
    list_filter = ['is_read']
    
admin.site.register(Messages,MessagesAdmin)
admin.site.register(Message)
admin.site.register(Room)
admin.site.register(Topic)
    
