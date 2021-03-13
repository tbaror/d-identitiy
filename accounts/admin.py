from django.contrib import admin
from .models import PassEvents

# Register your models here.



class EventsAdmin(admin.ModelAdmin):
    list_display = ('pass_event_type', 'event_stamp', 'user_related_event','ip_source', )

admin.site.register(PassEvents, EventsAdmin)

#admin.site.register(PassEvents)