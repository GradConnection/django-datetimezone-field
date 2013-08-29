import pytz

from django import http
from django import forms
from django.utils import timezone
from django.forms.util import to_current_timezone
from django.conf import settings

from datetimezone_field import SplitDateTimeTimeZoneField, \
    SplitTimeTimeZoneField


def index(request):
    
    class MyForm(forms.Form):
        a_datetime = SplitDateTimeTimeZoneField()
        a_time = SplitTimeTimeZoneField()

    tz = pytz.timezone("Australia/Sydney")
    timezone.activate(tz)
    now = to_current_timezone(timezone.now()).replace(tzinfo=tz)

    my_form = MyForm(initial={
        'a_datetime': now,
        'a_time': now.time().replace(tzinfo=now.tzinfo)
    })

    return http.HttpResponse(my_form.as_p())
    