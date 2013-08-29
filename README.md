# django-datetimezone-field

Written on top of `django-timezone-field`.

A Django app providing database and form fields for split datetime/time and pytz timezone objects.

* Use `SplitDateTimeTimeZoneField` in place of `forms.DateTimeField`.
* Use `SplitTimeTimeZoneField` in place of `forms.TimeField`.

The setting `USE_TZ_FIELDS = True` will convert all `admin.ModelAdmin`s to use 
`SplitDateTimeTimeZoneField` for `models.DateTimeField`s and `SplitTimeTimeZoneField` for `models.TimeField`s.

Requires `USE_TZ = True`

## Note

If using a database that does not support timezone-aware times then the initial values of model forms will always be in the UTC timezone.

## Form Field

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

## Installation

1. `pip install django-timezone-field`
2. `pip install django-datetimezone-field`
3. Add `datetimezone_field` to your `settings.INSTALLED_APPS`:

    INSTALLED_APPS = (
        ...
        timezone_field,
        datetimezone_field,
        ...
    )

## Running sample project

1. `cd test/sample_project`
2. `virtualenv sample-env`
3. `source sample-env/bin/activate`
4. `pip install -r requirements.txt`
5. `python manage.py syncdb`
6. `python manage.py runserver`

## TODO

* Unit tests

