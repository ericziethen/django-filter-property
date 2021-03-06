
import datetime

import pytest
from django_filters import FilterSet, TimeFilter

from django_property_filter import PropertyFilterSet, PropertyTimeFilter

from property_filter.models import TimeFilterModel


@pytest.mark.parametrize('lookup', PropertyTimeFilter.supported_lookups)
def test_supported_lookups(lookup):
    # Test expression not raises exception
    PropertyTimeFilter(field_name='fake_field', lookup_expr=lookup)


def test_unsupported_lookup():
    with pytest.raises(ValueError):
        PropertyTimeFilter(field_name='fake_field', lookup_expr='fake-lookup')


def test_default_lookup():
    my_filter = PropertyTimeFilter(field_name='fake_field')
    assert my_filter.lookup_expr == 'exact'


@pytest.fixture
def fixture_property_time_filter():
    TimeFilterModel.objects.create(id=-1, time=datetime.time(7, 30, 15))
    TimeFilterModel.objects.create(id=0, time=datetime.time(7, 30, 15))
    TimeFilterModel.objects.create(id=1, time=datetime.time(8, 0, 0))
    TimeFilterModel.objects.create(id=2, time=datetime.time(8, 0, 0))
    TimeFilterModel.objects.create(id=3, time=datetime.time(8, 0, 0))
    TimeFilterModel.objects.create(id=4, time=datetime.time(15, 15, 15))
    TimeFilterModel.objects.create(id=5, time=datetime.time(18, 30))


TEST_LOOKUPS = [
    ('exact', '08:00:00', [1, 2, 3]),
    ('gt', '08:00:00', [4, 5]),
    ('gte', '08:00:00', [1, 2, 3, 4, 5]),
    ('lt', '08:00:00', [-1, 0]),
    ('lte', '08:00:00', [-1, 0, 1, 2, 3]),
]


@pytest.mark.parametrize('lookup_xpr, lookup_val, result_list', TEST_LOOKUPS)
@pytest.mark.django_db
def test_lookup_xpr(fixture_property_time_filter, lookup_xpr, lookup_val, result_list):

    # Test using Normal Django Filter
    class TimeFilterSet(FilterSet):
        time = TimeFilter(field_name='time', lookup_expr=lookup_xpr)

        class Meta:
            model = TimeFilterModel
            fields = ['time']

    filter_fs = TimeFilterSet({'time': lookup_val}, queryset=TimeFilterModel.objects.all())
    assert set(filter_fs.qs.values_list('id', flat=True)) == set(result_list)

    # Compare with Explicit Filter using a PropertyFilterSet
    class PropertyTimeFilterSet(PropertyFilterSet):
        time = TimeFilter(field_name='time', lookup_expr=lookup_xpr)
        prop_time = PropertyTimeFilter(field_name='prop_time', lookup_expr=lookup_xpr)

        class Meta:
            model = TimeFilterModel
            fields = ['prop_time']

    filter_fs_mixed = TimeFilterSet({'time': lookup_val}, queryset=TimeFilterModel.objects.all())
    prop_filter_fs_mixed = PropertyTimeFilterSet({'prop_time': lookup_val}, queryset=TimeFilterModel.objects.all())
    assert set(filter_fs_mixed.qs) == set(filter_fs.qs)
    assert set(prop_filter_fs_mixed.qs) == set(filter_fs.qs)

    # Compare with Implicit Filter using PropertyFilterSet
    class ImplicitFilterSet(PropertyFilterSet):

        class Meta:
            model = TimeFilterModel
            exclude = ['time']
            property_fields = [('prop_time', PropertyTimeFilter, [lookup_xpr])]

    implicit_filter_fs = ImplicitFilterSet({F'prop_time__{lookup_xpr}': lookup_val}, queryset=TimeFilterModel.objects.all())
    assert set(implicit_filter_fs.qs) == set(filter_fs.qs)

def test_all_expressions_tested():
    tested_expressions = [x[0] for x in TEST_LOOKUPS]
    assert sorted(list(set(tested_expressions))) == sorted(PropertyTimeFilter.supported_lookups)
