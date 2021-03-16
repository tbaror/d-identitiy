from django.contrib import admin
from .models import PassEvents

# Register your models here.



class EventsAdmin(admin.ModelAdmin):
    list_display = ('user_related_event','pass_event_type', 'event_stamp', 'user_related_event','ip_source','user_browser','user_os','user_agent','user_reset_reason',)
    search_fields = ('user_related_event','pass_event_type', 'event_stamp', 'user_related_event','ip_source','user_browser','user_os','user_agent','user_reset_reason',)
    #readonly_fields = ('user_related_event','pass_event_type', 'event_stamp', 'user_related_event','ip_source','user_browser','user_os','user_agent','user_reset_reason',)

admin.site.register(PassEvents, EventsAdmin)

#admin.site.register(PassEvents)