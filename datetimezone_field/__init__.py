from django.conf import settings

from .widgets import *
from .fields import *


if getattr(settings, 'USE_TZ_FIELDS', False):
    from django.contrib.admin import options
    from django.db import models

    options.FORMFIELD_FOR_DBFIELD_DEFAULTS.update({
        models.DateTimeField: {
          'form_class': SplitDateTimeTimeZoneField,
          'widget': AdminSplitDateTimeTimeZone,
        },
        models.TimeField: {
          'form_class': SplitTimeTimeZoneField,
          'widget': AdminSplitTimeTimeZone,
        }
    })
