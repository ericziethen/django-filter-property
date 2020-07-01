

import pytest
from django_filters import FilterSet, ChoiceFilter

from django_property_filter import PropertyFilterSet, PropertyChoiceFilter

from property_filter.models import ChoiceFilterModel


@pytest.mark.parametrize('lookup', PropertyChoiceFilter.supported_lookups)
def test_supported_lookups(lookup):
    # Test expression not raises exception
    PropertyChoiceFilter(property_fld_name='fake_field', lookup_expr=lookup)


def test_unsupported_lookup():
    with pytest.raises(ValueError):
        PropertyChoiceFilter(property_fld_name='fake_field', lookup_expr='fake-lookup')


@pytest.fixture
def fixture_property_choice_filter():
    ChoiceFilterModel.objects.create(id=-1, number=-1)
    ChoiceFilterModel.objects.create(id=0, number=0)
    ChoiceFilterModel.objects.create(id=1, number=1)
    ChoiceFilterModel.objects.create(id=2, number=2)
    ChoiceFilterModel.objects.create(id=3, number=2)
    ChoiceFilterModel.objects.create(id=4, number=2)
    ChoiceFilterModel.objects.create(id=5, number=3)
    ChoiceFilterModel.objects.create(id=6, number=4)
    ChoiceFilterModel.objects.create(id=7, number=10)
    ChoiceFilterModel.objects.create(id=8, number=20)
    #ChoiceFilterModel.objects.create(id=9)

TEST_LOOKUPS = [
    #('exact', '-1', [-1]),
    ('exact', '15', []),
    #('exact', 0, [0]),
    #('exact', None, [-1, 0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14]),  # None returns full queryset
    #('exact', 15, []),
    #('exact', 5, [8, 9, 10, 11]),
    #('iexact', 15, []),
    #('iexact', 5, [8, 9, 10, 11]),
    #('contains', 100, []),
    #('contains', 4, [6, 7]),
    #('icontains', 100, []),
    #('icontains', 4, [6, 7]),
    #('gt', 20, []),
    #('gt', 4, [8, 9, 10, 11, 12, 13]),
    #('gte', 4, [6, 7, 8, 9, 10, 11, 12, 13]),
    #('gte', 21, []),
    #('lt', 2, [-1, 0, 1]),
    #('lt', 4, [-1, 0, 1, 2, 3, 4, 5]),
    #('lte', 0.9, [-1, 0]),
    #('lte', 4, [-1, 0, 1, 2, 3, 4, 5, 6, 7]),
    #('startswith', 7, []),
    #('startswith', 2, [2, 3, 4, 13]),
    #('startswith', 3, [5]),
    #('istartswith', 7, []),
    #('istartswith', 3, [5]),
    #('endswith', 7, []),
    #('endswith', 0, [0, 12, 13]),
    #('endswith', 3, [5]),
    #('iendswith', 7, []),
    #('iendswith', 3, [5])
]


@pytest.mark.parametrize('lookup_xpr, lookup_val, result_list', TEST_LOOKUPS)
@pytest.mark.django_db
@pytest.mark.debug
def test_lookup_xpr(fixture_property_choice_filter, lookup_xpr, lookup_val, result_list):

    choices = [(c.number, F'Number: {c.number}') for c in ChoiceFilterModel.objects.order_by('id')]
    # Test using Normal Django Filter
    class ChoiceFilterSet(FilterSet):
        number = ChoiceFilter(field_name='number', lookup_expr=lookup_xpr, choices=choices)

        class Meta:
            model = ChoiceFilterModel
            fields = ['number']

    filter_fs = ChoiceFilterSet({'number': lookup_val}, queryset=ChoiceFilterModel.objects.all())
    assert set(filter_fs.qs.values_list('id', flat=True)) == set(result_list)

    # Compare with Explicit Filter using a normal Filterset
    class PropertyChoiceFilterSet(FilterSet):
        prop_number = PropertyChoiceFilter(property_fld_name='prop_number', lookup_expr=lookup_xpr, choices=choices)

        class Meta:
            model = ChoiceFilterModel
            fields = ['prop_number']

    prop_filter_fs = PropertyChoiceFilterSet({'prop_number': lookup_val}, queryset=ChoiceFilterModel.objects.all())
    assert set(prop_filter_fs.qs) == set(filter_fs.qs)

    # Compare with Implicit Filter using PropertyFilterSet
    class ImplicitFilterSet(PropertyFilterSet):

        class Meta:
            model = ChoiceFilterModel
            exclude = ['number']
            property_fields = [('prop_number', PropertyChoiceFilter, [lookup_xpr])]

    # Since choices are required as argument we cannot create this filter explicitly
    with pytest.raises(ValueError):
        ImplicitFilterSet({F'prop_number__{lookup_xpr}': lookup_val}, queryset=ChoiceFilterModel.objects.all())


def test_all_expressions_tested():
    tested_expressions = [x[0] for x in TEST_LOOKUPS]
    assert sorted(list(set(tested_expressions))) == sorted(PropertyChoiceFilter.supported_lookups)
