django-datetimezone-field
=========================

Written on top of `django-timezone-field`__.

A Django app providing database and form fields for split datetime/time and pytz timezone objects.

* Use :code:`SplitDateTimeTimeZoneField` in place of :code:`forms.DateTimeField`.
* Use :code:`SplitTimeTimeZoneField` in place of :code:`forms.TimeField`.

The setting :code:`USE_TZ_FIELDS = True` will convert all :code:`admin.ModelAdmin` to use :code:`SplitDateTimeTimeZoneField` for :code:`models.DateTimeField` and :code:`SplitTimeTimeZoneField` for :code:`models.TimeField`.

Requires :code:`USE_TZ = True` in :code:`settings.py`

Note
----

If using a database that does not support timezone-aware times then the initial values of model forms will always be in the UTC timezone.

Form Field
----------

.. code:: python

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

Installation
------------

#.  From `pypi`__ using `pip`__:

    .. code:: sh

        pip install django-datetimezone-field

#. Add :code:`timezone_field` and :code:`datetimezone_field` to your :code:`settings.INSTALLED_APPS`

.. code:: python

        INSTALLED_APPS = (
            ...
            timezone_field,
            datetimezone_field,
            ...
        )

Running sample project
----------------------

1. :code:`cd test/sample_project`
2. :code:`virtualenv sample-env`
3. :code:`source sample-env/bin/activate`
4. :code:`pip install -r requirements.txt`
5. :code:`python manage.py syncdb`
6. :code:`python manage.py runserver`

TODO
----

#. Unit tests

Found a Bug?
------------

To file a bug or submit a patch, please head over to `django-datetimezone-field on github`__.

Credits
-------

Built on top of `Mike Fogel's django-timezone-field`__.

__ https://github.com/mfogel/django-timezone-field/
__ http://pypi.python.org/pypi/django-datetimezone-field/
__ http://www.pip-installer.org/
__ https://github.com/mfogel/django-datetimezone-field/
__ https://github.com/mfogel/django-timezone-field/



