from django.contrib import admin
from django.db import models
from django import forms
from datetimezone_field import SplitDateTimeTimeZoneField, AdminSplitDateTimeTimeZone

from .models import Event
import pytz



class EventForm(forms.ModelForm):
    class Meta:
      model = Event


class EventAdmin(admin.ModelAdmin):
    form = EventForm
    formfield_overrides = {
      models.DateTimeField: {
        'form_class': SplitDateTimeTimeZoneField,
        'widget':AdminSplitDateTimeTimeZone
      }
    }


admin.site.register(Event, EventAdmin)
