
import os
import sys

sys.path.append(os.path.abspath(R'..\..'))

from django_filters.filters import (
    AllValuesFilter,
    BooleanFilter,
    CharFilter,
    ChoiceFilter,
    DateFilter,
    DateFromToRangeFilter,
    DateRangeFilter,
    DateTimeFilter,
    DateTimeFromToRangeFilter,
    DurationFilter,
    IsoDateTimeFilter,
    IsoDateTimeFromToRangeFilter,
    ModelChoiceFilter,
    NumberFilter,
    RangeFilter,
    TimeFilter,
    TimeRangeFilter,
    TypedChoiceFilter,
    UUIDFilter,
)

from django_property_filter import (
    PropertyFilterSet,
    PropertyAllValuesFilter,
    PropertyBooleanFilter,
    PropertyCharFilter,
    PropertyChoiceFilter,
    PropertyDateFilter,
    PropertyDateFromToRangeFilter,
    PropertyDateRangeFilter,
    PropertyDateTimeFilter,
    PropertyDateTimeFromToRangeFilter,
    PropertyDurationFilter,
    PropertyIsoDateTimeFilter,
    PropertyIsoDateTimeFromToRangeFilter,
    PropertyNumberFilter,
    PropertyRangeFilter,
    PropertyTimeFilter,
    PropertyTimeRangeFilter,
    PropertyTypedChoiceFilter,
    PropertyUUIDFilter,
)

from property_filter import models


def add_filter(filterset_ref, filter_class, field_name, lookup_expr, **kwargs):
    filter_name = field_name + lookup_expr
    label = F'{field_name} [{lookup_expr}]'
    filterset_ref.filters[filter_name] = filter_class(label=label, field_name=field_name,
                                                      lookup_expr=lookup_expr, **kwargs)
    filterset_ref.filters[filter_name].model = filterset_ref.queryset.model
    filterset_ref.filters[filter_name].parent = filterset_ref


def add_supported_filters(filterset_ref, filter_class, field_name, expression_list, **kwargs):
    for lookup in expression_list:
        add_filter(filterset_ref, filter_class, field_name, lookup, **kwargs)


def add_property_filter(filter_list, filter_class, property_fld_name, lookup_expr, **kwargs):
    filter_name = property_fld_name + lookup_expr
    filter_list[filter_name] = filter_class(
        property_fld_name=property_fld_name, lookup_expr=lookup_expr, **kwargs)


def add_supported_property_filters(filter_list, filter_class, property_fld_name, expression_list, **kwargs):
    for lookup in expression_list:
        add_property_filter(filter_list, filter_class, property_fld_name, lookup, **kwargs)


class PropertyAllValuesFilterSet(PropertyFilterSet):

    class Meta:
        model = models.AllValuesFilterModel
        exclude = ['number']
        property_fields = [('prop_number', PropertyAllValuesFilter, PropertyAllValuesFilter.supported_lookups)]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        add_supported_filters(self, AllValuesFilter, 'number', PropertyAllValuesFilter.supported_lookups)


class PropertyBooleanFilterSet(PropertyFilterSet):

    class Meta:
        model = models.BooleanFilterModel
        exclude = ['is_true']
        property_fields = [('prop_is_true', PropertyBooleanFilter, PropertyBooleanFilter.supported_lookups)]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        add_supported_filters(self, BooleanFilter, 'is_true', PropertyBooleanFilter.supported_lookups)


class PropertyCharFilterSet(PropertyFilterSet):

    class Meta:
        model = models.CharFilterModel
        exclude = ['name']
        property_fields = [('prop_name', PropertyCharFilter, PropertyCharFilter.supported_lookups)]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        add_supported_filters(self, CharFilter, 'name', PropertyCharFilter.supported_lookups)


class PropertyChoiceFilterSet(PropertyFilterSet):

    class Meta:
        model = models.ChoiceFilterModel
        exclude = ['number']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        choices = [(c.number, F'Number: {c.number}') for c in models.ChoiceFilterModel.objects.order_by('id')]
        choices.append((-1, 'Number: -1'))
        choices.append((666, 'Number: 666'))
        add_supported_filters(self, ChoiceFilter, 'number', PropertyChoiceFilter.supported_lookups, choices=choices)
        add_supported_property_filters(self.filters, PropertyChoiceFilter, 'prop_number', PropertyChoiceFilter.supported_lookups, choices=choices)


class PropertyDateFilterSet(PropertyFilterSet):

    class Meta:
        model = models.DateFilterModel
        exclude = ['date']
        property_fields = [('prop_date', PropertyDateFilter, PropertyDateFilter.supported_lookups)]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        add_supported_filters(self, DateFilter, 'date', PropertyDateFilter.supported_lookups)


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
        add_supported_filters(self, DateFromToRangeFilter, 'date', PropertyDateFromToRangeFilter.supported_lookups)
        add_supported_filters(self, DateFromToRangeFilter, 'date_time', PropertyDateFromToRangeFilter.supported_lookups)


class PropertyDateRangeFilterSet(PropertyFilterSet):

    class Meta:
        model = models.DateRangeFilterModel
        exclude = ['date', 'date_time']
        property_fields = [
            ('prop_date', PropertyDateRangeFilter, PropertyDateRangeFilter.supported_lookups),
            ('prop_date_time', PropertyDateRangeFilter, PropertyDateRangeFilter.supported_lookups)
            ]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        add_supported_filters(self, DateRangeFilter, 'date', PropertyDateRangeFilter.supported_lookups)
        add_supported_filters(self, DateRangeFilter, 'date_time', PropertyDateRangeFilter.supported_lookups)


class PropertyDateTimeFilterSet(PropertyFilterSet):

    class Meta:
        model = models.DateTimeFilterModel
        exclude = ['date_time']
        property_fields = [('prop_date_time', PropertyDateTimeFilter, PropertyDateTimeFilter.supported_lookups)]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        add_supported_filters(self, DateTimeFilter, 'date_time', PropertyDateTimeFilter.supported_lookups)


class PropertyDateTimeFromToRangeFilterSet(PropertyFilterSet):

    class Meta:
        model = models.DateTimeFromToRangeFilterModel
        exclude = ['date_time']
        property_fields = [('prop_date_time', PropertyDateTimeFromToRangeFilter, PropertyDateTimeFromToRangeFilter.supported_lookups)]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        add_supported_filters(self, DateTimeFromToRangeFilter, 'date_time', PropertyDateTimeFromToRangeFilter.supported_lookups)


class PropertyDurationFilterSet(PropertyFilterSet):

    class Meta:
        model = models.DurationFilterModel
        exclude = ['duration']
        property_fields = [('prop_duration', PropertyDurationFilter, PropertyDurationFilter.supported_lookups)]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        add_supported_filters(self, DurationFilter, 'duration', PropertyDurationFilter.supported_lookups)


class PropertyIsoDateTimeFilterSet(PropertyFilterSet):

    class Meta:
        model = models.IsoDateTimeFilterModel
        exclude = ['date_time']
        property_fields = [('prop_date_time', PropertyIsoDateTimeFilter, PropertyIsoDateTimeFilter.supported_lookups)]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        add_supported_filters(self, IsoDateTimeFilter, 'date_time', PropertyIsoDateTimeFilter.supported_lookups)


class PropertyIsoDateTimeFromToRangeFilterSet(PropertyFilterSet):

    class Meta:
        model = models.IsoDateTimeFromToRangeFilterModel
        exclude = ['date_time']
        property_fields = [('prop_date_time', PropertyIsoDateTimeFromToRangeFilter, PropertyIsoDateTimeFromToRangeFilter.supported_lookups)]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        add_supported_filters(self, IsoDateTimeFromToRangeFilter, 'date_time', PropertyIsoDateTimeFromToRangeFilter.supported_lookups)


class PropertyModelChoiceFilterSet(PropertyFilterSet):

    # No Property filter since working directly with FOreign Keys

    related = ModelChoiceFilter(queryset=models.ModelChoiceFilterRelatedModel.objects.all())

    class Meta:
        model = models.ModelChoiceFilterModel
        fields = ['related']


class PropertyNumberFilterSet(PropertyFilterSet):

    class Meta:
        model = models.NumberFilterModel
        exclude = ['number']
        property_fields = [('prop_number', PropertyNumberFilter, PropertyNumberFilter.supported_lookups)]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        add_supported_filters(self, NumberFilter, 'number', PropertyNumberFilter.supported_lookups)


class PropertyRangeFilterSet(PropertyFilterSet):

    class Meta:
        model = models.RangeFilterModel
        exclude = ['number']
        property_fields = [('prop_number', PropertyRangeFilter, PropertyRangeFilter.supported_lookups)]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        add_supported_filters(self, RangeFilter, 'number', PropertyRangeFilter.supported_lookups)


class PropertyTimeFilterSet(PropertyFilterSet):

    class Meta:
        model = models.TimeFilterModel
        exclude = ['time']
        property_fields = [('prop_time', PropertyTimeFilter, PropertyTimeFilter.supported_lookups)]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        add_supported_filters(self, TimeFilter, 'time', PropertyTimeFilter.supported_lookups)


class PropertyTimeRangeFilterSet(PropertyFilterSet):

    class Meta:
        model = models.TimeRangeFilterModel
        exclude = ['time']
        property_fields = [('prop_time', PropertyTimeRangeFilter, PropertyTimeRangeFilter.supported_lookups)]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        add_supported_filters(self, TimeRangeFilter, 'time', PropertyTimeRangeFilter.supported_lookups)


class PropertyTypedChoiceFilterSet(PropertyFilterSet):

    class Meta:
        model = models.TypedChoiceFilterModel
        exclude = ['text']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        choices = [(c.text, F'{c.text}') for c in models.TypedChoiceFilterModel.objects.order_by('id')]
        add_supported_filters(self, TypedChoiceFilter, 'text', PropertyTypedChoiceFilter.supported_lookups, choices=choices, coerce=int)
        add_supported_property_filters(self.filters, PropertyTypedChoiceFilter, 'prop_text', PropertyTypedChoiceFilter.supported_lookups, choices=choices, coerce=int)


class PropertyUUIDFilterSet(PropertyFilterSet):

    class Meta:
        model = models.UUIDFilterModel
        exclude = ['uuid']
        property_fields = [('prop_uuid', PropertyUUIDFilter, PropertyUUIDFilter.supported_lookups)]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        add_supported_filters(self, UUIDFilter, 'uuid', PropertyUUIDFilter.supported_lookups)
