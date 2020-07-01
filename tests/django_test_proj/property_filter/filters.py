
import os
import sys

sys.path.append(os.path.abspath(R'..\..'))

from django_filters.filters import (
    BooleanFilter,
    CharFilter,
    ChoiceFilter,
    DateFilter,
    DateFromToRangeFilter,
    DateTimeFilter,
    DateTimeFromToRangeFilter,
    DurationFilter,
    IsoDateTimeFilter,
    IsoDateTimeFromToRangeFilter,
    NumberFilter,
    RangeFilter,
    TimeFilter,
    TimeRangeFilter,
    UUIDFilter,
)

from django_property_filter import (
    PropertyFilterSet,
    PropertyBooleanFilter,
    PropertyCharFilter,
    PropertyChoiceFilter,
    PropertyDateFilter,
    PropertyDateFromToRangeFilter,
    PropertyDateTimeFilter,
    PropertyDateTimeFromToRangeFilter,
    PropertyDurationFilter,
    PropertyIsoDateTimeFilter,
    PropertyIsoDateTimeFromToRangeFilter,
    PropertyNumberFilter,
    PropertyRangeFilter,
    PropertyTimeFilter,
    PropertyTimeRangeFilter,
    PropertyUUIDFilter,
)

from property_filter import models


def add_filter(filter_list, filter_class, field_name, lookup_expr, *, choices):
    filter_name = field_name + lookup_expr
    label = F'{field_name} [{lookup_expr}]'

    kwargs = {}
    if choices is not None:
        kwargs['choices'] = choices
    filter_list[filter_name] = filter_class(label=label, field_name=field_name,
                                            lookup_expr=lookup_expr, **kwargs)

def add_supported_filters(filter_list, filter_class, field_name, expression_list, *, choices=None):
    for lookup in expression_list:
        add_filter(filter_list, filter_class, field_name, lookup, choices=choices)


def add_property_filter(filter_list, filter_class, property_fld_name, lookup_expr, *, choices):
    filter_name = property_fld_name + lookup_expr

    kwargs = {}
    if choices is not None:
        kwargs['choices'] = choices
    filter_list[filter_name] = filter_class(
        property_fld_name=property_fld_name, lookup_expr=lookup_expr, **kwargs)


def add_supported_property_filters(filter_list, filter_class, property_fld_name, expression_list, *, choices=None):
    for lookup in expression_list:
        add_property_filter(filter_list, filter_class, property_fld_name, lookup, choices=choices)


class PropertyNumberFilterSet(PropertyFilterSet):

    class Meta:
        model = models.NumberFilterModel
        exclude = ['number']
        property_fields = [('prop_number', PropertyNumberFilter, PropertyNumberFilter.supported_lookups)]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        add_supported_filters(self.filters, NumberFilter, 'number', PropertyNumberFilter.supported_lookups)


class PropertyBooleanFilterSet(PropertyFilterSet):

    class Meta:
        model = models.BooleanFilterModel
        exclude = ['is_true']
        property_fields = [('prop_is_true', PropertyBooleanFilter, PropertyBooleanFilter.supported_lookups)]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        add_supported_filters(self.filters, BooleanFilter, 'is_true', PropertyBooleanFilter.supported_lookups)


class PropertyCharFilterSet(PropertyFilterSet):

    class Meta:
        model = models.CharFilterModel
        exclude = ['name']
        property_fields = [('prop_name', PropertyCharFilter, PropertyCharFilter.supported_lookups)]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        add_supported_filters(self.filters, CharFilter, 'name', PropertyCharFilter.supported_lookups)













class ERIcChoiceFilter(ChoiceFilter):

    def filter(self, qs, value):
        print('ERIcChoiceFilter.filter()', type(value), value)
        if value != self.null_value:
            eric_qs = super().filter(qs, value)
            print('  qs-filtered', eric_qs)
            return eric_qs

        qs = self.get_method(qs)(**{'%s__%s' % (self.field_name, self.lookup_expr): None})
        print('  self.distinct', self.distinct)
        print('  qs-filtered', qs)
        print('  qs-filtered-distinct', qs.distinct())
        print('  self.get_method(qs)', self.get_method(qs))
        return qs.distinct() if self.distinct else qs









class PropertyChoiceFilterSet(PropertyFilterSet):


 



    class Meta:
        model = models.ChoiceFilterModel
        exclude = ['number']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        choices = [(c.number, F'Number: {c.number}') for c in models.ChoiceFilterModel.objects.order_by('id')]
        choices = [
            (1, 'Number 1'),
            (True, 'Boolean True'),
            (1.1, '1.1'),
        ]
        add_supported_filters(self.filters, ERIcChoiceFilter, 'number', PropertyChoiceFilter.supported_lookups, choices=choices)
        add_supported_property_filters(self.filters, PropertyChoiceFilter, 'prop_number', PropertyChoiceFilter.supported_lookups, choices=choices)


class PropertyDateFilterSet(PropertyFilterSet):

    class Meta:
        model = models.DateFilterModel
        exclude = ['date']
        property_fields = [('prop_date', PropertyDateFilter, PropertyDateFilter.supported_lookups)]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        add_supported_filters(self.filters, DateFilter, 'date', PropertyDateFilter.supported_lookups)


class PropertyDateFromToRangeFilterSet(PropertyFilterSet):

    class Meta:
        model = models.DateFromToRangeFilterModel
        exclude = ['date', 'date_time']
        property_fields = [
            ('prop_date', PropertyDateFromToRangeFilter, PropertyDateFromToRangeFilter.supported_lookups),
            ('prop_date_time', PropertyDateFromToRangeFilter, PropertyDateFromToRangeFilter.supported_lookups)
            ]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        add_supported_filters(self.filters, DateFromToRangeFilter, 'date', PropertyDateFromToRangeFilter.supported_lookups)
        add_supported_filters(self.filters, DateFromToRangeFilter, 'date_time', PropertyDateFromToRangeFilter.supported_lookups)


class PropertyDateTimeFilterSet(PropertyFilterSet):

    class Meta:
        model = models.DateTimeFilterModel
        exclude = ['date_time']
        property_fields = [('prop_date_time', PropertyDateTimeFilter, PropertyDateTimeFilter.supported_lookups)]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        add_supported_filters(self.filters, DateTimeFilter, 'date_time', PropertyDateTimeFilter.supported_lookups)


class PropertyDateTimeFromToRangeFilterSet(PropertyFilterSet):

    class Meta:
        model = models.DateTimeFromToRangeFilterModel
        exclude = ['date_time']
        property_fields = [('prop_date_time', PropertyDateTimeFromToRangeFilter, PropertyDateTimeFromToRangeFilter.supported_lookups)]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        add_supported_filters(self.filters, DateTimeFromToRangeFilter, 'date_time', PropertyDateTimeFromToRangeFilter.supported_lookups)


class PropertyDurationFilterSet(PropertyFilterSet):

    class Meta:
        model = models.DurationFilterModel
        exclude = ['duration']
        property_fields = [('prop_duration', PropertyDurationFilter, PropertyDurationFilter.supported_lookups)]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        add_supported_filters(self.filters, DurationFilter, 'duration', PropertyDurationFilter.supported_lookups)


class PropertyIsoDateTimeFilterSet(PropertyFilterSet):

    class Meta:
        model = models.IsoDateTimeFilterModel
        exclude = ['date_time']
        property_fields = [('prop_date_time', PropertyIsoDateTimeFilter, PropertyIsoDateTimeFilter.supported_lookups)]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        add_supported_filters(self.filters, IsoDateTimeFilter, 'date_time', PropertyIsoDateTimeFilter.supported_lookups)


class PropertyIsoDateTimeFromToRangeFilterSet(PropertyFilterSet):

    class Meta:
        model = models.IsoDateTimeFromToRangeFilterModel
        exclude = ['date_time']
        property_fields = [('prop_date_time', PropertyIsoDateTimeFromToRangeFilter, PropertyIsoDateTimeFromToRangeFilter.supported_lookups)]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        add_supported_filters(self.filters, IsoDateTimeFromToRangeFilter, 'date_time', PropertyIsoDateTimeFromToRangeFilter.supported_lookups)


class PropertyRangeFilterSet(PropertyFilterSet):

    class Meta:
        model = models.RangeFilterModel
        exclude = ['number']
        property_fields = [('prop_number', PropertyRangeFilter, PropertyRangeFilter.supported_lookups)]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        add_supported_filters(self.filters, RangeFilter, 'number', PropertyRangeFilter.supported_lookups)


class PropertyTimeFilterSet(PropertyFilterSet):

    class Meta:
        model = models.TimeFilterModel
        exclude = ['time']
        property_fields = [('prop_time', PropertyTimeFilter, PropertyTimeFilter.supported_lookups)]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        add_supported_filters(self.filters, TimeFilter, 'time', PropertyTimeFilter.supported_lookups)


class PropertyTimeRangeFilterSet(PropertyFilterSet):

    class Meta:
        model = models.TimeRangeFilterModel
        exclude = ['time']
        property_fields = [('prop_time', PropertyTimeRangeFilter, PropertyTimeRangeFilter.supported_lookups)]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        add_supported_filters(self.filters, TimeRangeFilter, 'time', PropertyTimeRangeFilter.supported_lookups)

class PropertyUUIDFilterSet(PropertyFilterSet):

    class Meta:
        model = models.UUIDFilterModel
        exclude = ['uuid']
        property_fields = [('prop_uuid', PropertyUUIDFilter, PropertyUUIDFilter.supported_lookups)]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        add_supported_filters(self.filters, UUIDFilter, 'uuid', PropertyUUIDFilter.supported_lookups)
