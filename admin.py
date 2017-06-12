from django.contrib import admin


class SelectModelAdmin(admin.ModelAdmin):
    """
    Custom admin for a search select box.
    * Make sure you have search_fields.
    * Search fields are listed in the search box.
    """
    change_list_template = 'select_admin_template.html'

    def changelist_view(self, request, extra_context=None):
        extra_context = {'select_field': request.GET['field'] if 'field' in request.GET else 'all'}
        return admin.ModelAdmin.changelist_view(self, request, extra_context)

    class FieldFilter(admin.SimpleListFilter):
        title = 'searchbox'
        parameter_name = 'field'

        def lookups(self, request, model_admin):
            return (('', ''),)

        def queryset(self, request, queryset):
            return queryset.all()

    def get_search_results(self, request, queryset, search_term):
        queryset, use_distinct = super(SelectModelAdmin, self).get_search_results(request, queryset, search_term)
        field = request.GET['field'] if 'field' in request.GET else 'all'
        if field == 'all':
            return queryset, use_distinct
        else:
            queryset &= self.model.objects.filter(**{field + '__icontains': search_term})
            return queryset, use_distinct

    def get_list_filter(self, request):
        new_filter = tuple([filter for filter in self.list_filter] + [self.FieldFilter])
        return new_filter
