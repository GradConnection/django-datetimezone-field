import datetime, pytz

from django.core.exceptions import ValidationError
from django.forms.fields import MultiValueField, DateField, TimeField
from django.utils.translation import ugettext as _
from django.core.validators import EMPTY_VALUES

from timezone_field.forms import TimeZoneFormField
from .widgets import SplitTimeTimeZoneWidget, SplitHiddenTimeTimeZoneWidget, \
    SplitDateTimeTimeZoneWidget, SplitHiddenDateTimeTimeZoneWidget, \
    AdminSplitDateTimeTimeZone, AdminSplitTimeTimeZone


__all = (
    'SplitTimeTimeZoneField', 'AdminSplitTimeTimeZoneField',
    'SplitDateTimeTimeZoneField', 'AdminSplitDateTimeTimeZoneField'
)


class SplitTimeTimeZoneField(MultiValueField):
    widget = SplitTimeTimeZoneWidget
    hidden_widget = SplitHiddenTimeTimeZoneWidget
    empty_values = list(EMPTY_VALUES)

    default_error_messages = {
        'invalid_time': _('Enter a valid time.'),
        'invalid_time_zone': _('Enter a valid time zone.'),
    }

    def __init__(self, input_time_formats=None, *args, **kwargs):
        errors = self.default_error_messages.copy()
        if 'error_messages' in kwargs:
            errors.update(kwargs['error_messages'])
        localize = kwargs.get('localize', False)
        fields = (
            TimeField(input_formats=input_time_formats,
                      error_messages={'invalid': errors['invalid_time']},
                      localize=localize),
            TimeZoneFormField(error_messages={'invalid': errors['invalid_time']},
                      localize=localize, initial="Australia/Sydney"),

        )
        super(SplitTimeTimeZoneField, self).__init__(fields, *args, **kwargs)

    def compress(self, data_list):
        if data_list:
            if data_list[0] in self.empty_values:
                return None
            # Raise a validation error if time or date is empty
            # (possible if SplitTimeTimeZoneField has required=False).
            if data_list[0] in self.empty_values:
                raise ValidationError(self.error_messages['invalid_time'], code='invalid_time')
            if data_list[1] in self.empty_values:
                raise ValidationError(self.error_messages['invalid_time_zone'], code='invalid_time_zone')
            result = data_list[0].replace(tzinfo=data_list[1])
            return result
        return None


class SplitDateTimeTimeZoneField(MultiValueField):
    widget = SplitDateTimeTimeZoneWidget
    hidden_widget = SplitHiddenDateTimeTimeZoneWidget
    empty_values = list(EMPTY_VALUES)

    default_error_messages = {
        'invalid_date': _('Enter a valid date.'),
        'invalid_time': _('Enter a valid time.'),
        'invalid_time_zone': _('Enter a valid time zone.'),
    }

    def __init__(self, input_date_formats=None, input_time_formats=None, *args, **kwargs):
        errors = self.default_error_messages.copy()
        if 'error_messages' in kwargs:
            errors.update(kwargs['error_messages'])
        localize = kwargs.get('localize', False)
        fields = (
            DateField(input_formats=input_date_formats,
                      error_messages={'invalid': errors['invalid_date']},
                      localize=localize),
            TimeField(input_formats=input_time_formats,
                      error_messages={'invalid': errors['invalid_time']},
                      localize=localize),
            TimeZoneFormField(error_messages={'invalid': errors['invalid_time']},
                      localize=localize, initial="Australia/Sydney"),

        )
        super(SplitDateTimeTimeZoneField, self).__init__(fields, *args, **kwargs)

    def compress(self, data_list):
        if data_list:
            if data_list[0] in self.empty_values and data_list[1] in self.empty_values
                return None
            # Raise a validation error if time or date is empty
            # (possible if SplitDateTimeTimeZoneField has required=False).
            if data_list[0] in self.empty_values:
                raise ValidationError(self.error_messages['invalid_date'], code='invalid_date')
            if data_list[1] in self.empty_values:
                raise ValidationError(self.error_messages['invalid_time'], code='invalid_time')
            if data_list[2] in self.empty_values:
                raise ValidationError(self.error_messages['invalid_time_zone'], code='invalid_time_zone')
            result = datetime.datetime.combine(*data_list[0:2]).replace(tzinfo=data_list[2])
            return result
        return None

