import pytz
import datetime
import decimal

from django.forms.widgets import Select, MultiWidget, DateInput, TimeInput
from django.contrib.admin.widgets import AdminDateWidget, AdminTimeWidget
from django.utils.html import format_html
from django.utils.translation import ugettext as _
from django.utils import timezone
from django.conf import settings


__all__ = (
    'TimeZoneSelect', 'SplitDateTimeTimeZoneWidget', 
    'SplitHiddenDateTimeTimeZoneWidget', 'AdminSplitDateTimeTimeZone'
)


def _utcoffset(tz):
    """
    Returns the UTC Offset measured in hours for a timezone for this time of
    the year.
    """
    tz = pytz.timezone(tz)
    offset = datetime.datetime.now(tz).utcoffset()
    hours = (offset.days * 86400.0 + offset.seconds) / 3600.0
    if hours == int(hours):
        hours = int(hours)
    if hours >= 0:
        return "+" + str(hours)
    return str(hours)
    

class TimeZoneSelect(Select):
    """
    A Widget that allows the selection of a timezone.
    """
    def __init__(self, attrs=None):
        super(TimeZoneSelect, self).__init__(attrs)
        now = timezone.now()
        self.choices = [(tz, "%s (%s)" % (tz, _utcoffset(tz)))
            for tz in pytz.common_timezones]


class SplitTimeTimeZoneWidget(MultiWidget):
    """
    A Widget that splits time & timezone input into one <input type="text"> 
    boxes plus a timezone select.
    """
    def __init__(self, attrs=None, time_format=None):
        widgets = (TimeInput(attrs=attrs, format=time_format),
                   TimeZoneSelect(attrs=attrs))
        super(SplitTimeTimeZoneWidget, self).__init__(widgets, attrs)

    def decompress(self, value):
        tzinfo = timezone.get_current_timezone()
        if value:
            if value.tzinfo:
                tzinfo = value.tzinfo
            return [value.replace(microsecond=0), tzinfo]
        return [None, tzinfo]


class SplitHiddenTimeTimeZoneWidget(SplitTimeTimeZoneWidget):
    """
    A Widget that splits timezone input into two <input type="hidden"> inputs.
    """
    is_hidden = True

    def __init__(self, attrs=None, time_format=None):
        super(SplitHiddenTimeTimeZoneWidget, self).__init__(attrs, time_format)
        for widget in self.widgets:
            widget.input_type = 'hidden'
            widget.is_hidden = True


class AdminSplitTimeTimeZone(SplitTimeTimeZoneWidget):
    """
    A SplitTimeTimeZoneWidget Widget that has some admin-specific styling.
    """
    def __init__(self, attrs=None):
        widgets = [AdminTimeWidget, TimeZoneSelect]
        # Note that we're calling MultiWidget, not SplitTimeTimeZoneWidget, 
        # because we want to define widgets.
        MultiWidget.__init__(self, widgets, attrs)

    def format_output(self, rendered_widgets):

        return format_html('<p class="datetime">{0} {1} {2}</p>',
                           _('Time:'), rendered_widgets[0],
                           rendered_widgets[1])


class SplitDateTimeTimeZoneWidget(MultiWidget):
    """
    A Widget that splits datetime & timezone input into two <input type="text"> 
    boxes plus a timezone select.
    """
    def __init__(self, attrs=None, date_format=None, time_format=None):
        widgets = (DateInput(attrs=attrs, format=date_format),
                   TimeInput(attrs=attrs, format=time_format),
                   TimeZoneSelect(attrs=attrs))
        super(SplitDateTimeTimeZoneWidget, self).__init__(widgets, attrs)

    def decompress(self, value):
        tzinfo = timezone.get_current_timezone()
        if value:
            if value.tzinfo:
                tzinfo = value.tzinfo
            return [value.date(), value.time().replace(microsecond=0), tzinfo]
        return [None, None, tzinfo]


class SplitHiddenDateTimeTimeZoneWidget(SplitDateTimeTimeZoneWidget):
    """
    A Widget that splits datetimezone input into three <input type="hidden"> inputs.
    """
    is_hidden = True

    def __init__(self, attrs=None, date_format=None, time_format=None):
        super(SplitHiddenDateTimeTimeZoneWidget, self).__init__(attrs, date_format, time_format)
        for widget in self.widgets:
            widget.input_type = 'hidden'
            widget.is_hidden = True


class AdminSplitDateTimeTimeZone(SplitDateTimeTimeZoneWidget):
    """
    A SplitDateTimeTimeZoneWidget Widget that has some admin-specific styling.
    """
    def __init__(self, attrs=None):
        widgets = [AdminDateWidget, AdminTimeWidget, 
          TimeZoneSelect]
        # Note that we're calling MultiWidget, not SplitDateTimeTimeZoneWidget, 
        # because we want to define widgets.
        MultiWidget.__init__(self, widgets, attrs)

    def format_output(self, rendered_widgets):

        return format_html('<p class="datetime">{0} {1}<br />{2} {3} {4}</p>',
                           _('Date:'), rendered_widgets[0],
                           _('Time:'), rendered_widgets[1],
                           rendered_widgets[2])

