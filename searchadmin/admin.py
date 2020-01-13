from django.contrib import admin

from django.db.models.constants import LOOKUP_SEP
from django.core.exceptions import (
    FieldDoesNotExist, FieldError, PermissionDenied, ValidationError,
)
from functools import partial, reduce, update_wrapper
from django.db import models, router, transaction
from django.contrib.admin.utils import (
    NestedObjects, construct_change_message, flatten_fieldsets,
    get_deleted_objects, lookup_needs_distinct, model_format_dict,
    model_ngettext, quote, unquote,
)
import operator


class SelectModelAdmin(admin.ModelAdmin):
    """
    Custom admin for a search select box.
    * Make sure you have search_fields.
    * Search fields are listed in the search box.
    """
    change_list_template = 'select_admin_template.html'

    def changelist_view(self, request, extra_context=None):
        extra_context = {
            'select_field': request.GET['field'] if 'field' in request.GET else 'all'}
        return admin.ModelAdmin.changelist_view(self, request, extra_context)

    class FieldFilter(admin.SimpleListFilter):
        title = 'searchbox'
        parameter_name = 'field'

        def lookups(self, request, model_admin):
            return (('', ''),)

        def queryset(self, request, queryset):
            return queryset.all()

    def get_search_results(self, request, queryset, search_term):
        print("search_term:", search_term)
        queryset, use_distinct = super(SelectModelAdmin, self).get_search_results(
            request, queryset, search_term)
        field = request.GET['field'] if 'field' in request.GET else 'all'
        # Apply keyword searches.

        def construct_search(field_name):
            if field_name.startswith('^'):
                return "%s__istartswith" % field_name[1:]
            elif field_name.startswith('='):
                return "%s__iexact" % field_name[1:]
            elif field_name.startswith('@'):
                return "%s__search" % field_name[1:]
            elif field_name.endswith('__exact'):
                return field_name

            # Use field_name if it includes a lookup.
            opts = queryset.model._meta
            lookup_fields = field_name.split(LOOKUP_SEP)
            # Go through the fields, following all relations.
            prev_field = None
            for path_part in lookup_fields:
                if path_part == 'pk':
                    path_part = opts.pk.name
                try:
                    field = opts.get_field(path_part)
                except FieldDoesNotExist:
                    # Use valid query lookups.
                    if prev_field and prev_field.get_lookup(path_part):
                        return field_name
                else:
                    prev_field = field
                    if hasattr(field, 'get_path_info'):
                        # Update opts to follow the relation.
                        opts = field.get_path_info()[-1].to_opts
            # Otherwise, use the field with icontains.
            return "%s__icontains" % field_name

        # use_distinct = False
        # search_fields = self.get_search_fields(request)
        # if search_fields and search_term:
        #     orm_lookups = [construct_search(str(search_field))
        #                    for search_field in search_fields]
        #     for bit in search_term.split():
        #         or_queries = [models.Q(**{orm_lookup: bit})
        #                       for orm_lookup in orm_lookups]
        #         queryset = queryset.filter(reduce(operator.or_, or_queries))
        #     use_distinct |= any(lookup_needs_distinct(self.opts, search_spec) for search_spec in orm_lookups)
        if field == 'all':
            return queryset, use_distinct
        else:
            queryset &= self.model.objects.filter(
                **{construct_search(field): search_term})
            return queryset, use_distinct

    def get_list_filter(self, request):
        new_filter = tuple(
            [filter for filter in self.list_filter] + [self.FieldFilter])
        return new_filter
