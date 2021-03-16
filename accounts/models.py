from django.db import models
import datetime

# Create your models here.


class PassEvents(models.Model):

    pass_event_type = models.CharField(max_length=200)
    event_stamp = models.DateTimeField(auto_now_add=True)
    user_related_event = models.CharField(max_length=200)
    ip_source = models.CharField(max_length=16)
    user_browser = models.CharField(max_length=200)
    user_os = models.CharField(max_length=200)
    user_agent = models.CharField(max_length=200)
    user_reset_reason = models.TextField(max_length=500,default=None, null=True, blank=True)

    def __str__(self):
        return self.user_related_event