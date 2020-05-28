
from django_filters.filters import (
    NumberFilter,
)

from django_filters.utils import verbose_lookup_expr

from django_property_filter.utils import (
    get_value_for_db_field,
    compare_by_lookup_expression
)


class PropertyBaseFilterMixin():
    def __init__(self, field_name=None, lookup_expr=None, *, label=None,
                 method=None, distinct=False, exclude=False, property_fld_name, **kwargs):
        label = F'{label} {verbose_lookup_expr(lookup_expr)}'
        self.property_fld_name = property_fld_name
        super().__init__(field_name=field_name, lookup_expr=lookup_expr, label=label,
                         method=method, distinct=distinct, exclude=exclude, **kwargs)

    def filter(self, qs, value):
        # Carefull, a filter value of 0 will be Valid so can't just do 'if value:'
        if value is not None and value != '':
            wanted_ids = set()
            for obj in qs:
                property_value = get_value_for_db_field(obj, self.property_fld_name)
                if property_value:
                    if compare_by_lookup_expression(self.lookup_expr, property_value, value):
                        wanted_ids.add(obj.pk)
            return qs.filter(pk__in=wanted_ids)

        return qs

class PropertyNumberFilter(PropertyBaseFilterMixin, NumberFilter):
    pass









