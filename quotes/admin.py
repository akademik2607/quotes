import os

from django.contrib import admin
from django.db.models import Q
from django.utils.html import format_html

from config.settings import BASE_DIR
from quotes.models import Quote, Services, Currencies, ServiceIncludes, ServiceExcludes, SERVICE_TYPES, CalculateType
from tools.functions import get_show_perms, get_sale_price


class ServiceIncludesInstanceInline(admin.TabularInline):
    model = ServiceIncludes
    fields = ('service', 'label', 'is_checked',)
    extra = 0


class ServiceExcludesInstanceInline(admin.TabularInline):
    model = ServiceExcludes
    fields = ('label', 'is_checked',)
    extra = 0


class ServiceInstanceInline(admin.TabularInline):
    model = Services
    exclude = ('is_required',)
    extra = 0


class ServiceInstanceInline(admin.TabularInline):
    model = Services
    fields = ('description', 'supplier', 'type', 'quantity', 'currency', 'buy_price', 'sale_price', 'vat')
    can_delete = False
    extra = 0

    def get_queryset(self, request):
        qs = super(ServiceInstanceInline, self).get_queryset(request)
        service_id = request.path.split(r'/')[4]
        try:
            int(service_id)
        except ValueError:
            return qs
        service = Quote.objects.get(pk=service_id)

        show_serviece_perms = get_show_perms(service.service_type)
        rules = None
        if show_serviece_perms['check_origin']:
            rules = qs.filter(description='Origin service', is_required=True)
        if show_serviece_perms['check_freight']:
            if rules:
                rules |= qs.filter(description='International freight', is_required=True)
            else:
                rules = qs.filter(description='International freight', is_required=True)
        if show_serviece_perms['check_destination']:
            if rules:
                rules |= qs.filter(description='Destination Services', is_required=True)
            else:
                rules = qs.filter(description='Destination Services', is_required=True)


        # Services(description='Origin service', quote=self, is_required=True),
        # Services(description='International freight', quote=self, is_required=True),
        # Services(description='Destination Services', quote=self, is_required=True)

        return rules

    def has_add_permission(self, request, obj):
        perms = super(ServiceInstanceInline, self).has_add_permission(request, obj)
        return False


class ServiceSurchargesInline(admin.TabularInline):
    model = Services
    verbose_name = 'Additional charge'
    verbose_name_plural = 'Additional charges'
    fields = ('description', 'supplier', 'type', 'quantity', 'currency', 'buy_price', 'sale_price', 'vat')
    extra = 1


    def get_queryset(self, request):
        qs = super(ServiceSurchargesInline, self).get_queryset(request)
        qs = qs.filter(
            Q(is_required=False) |
            ~(
                Q(is_required=True, description__startswith='Origin') |
                Q(is_required=True, description__startswith='International') |
                Q(is_required=True, description__startswith='Destination')
            )
        )
        print(qs)

        return qs



@admin.register(Quote)
class QuoteAdminModel(admin.ModelAdmin):
    change_form_template = 'admin/quote_form.html'
    save_on_top = True
    list_display = ('title', 'quotation_number',)
    #readonly_fields = ('view_pdf_link', )
    fieldsets = (
        (None, {
            'fields': ['title'],

        }),
        ('Contact information', {
            'classes': ('contact-information',),
            'fields': [
                    ('name', 'date', 'quotation_ref', 'quotation_number'),
                    ('origin_country', 'origin_city', 'service_type', 'method', 'volume'),
                    ('destination_country', 'destination_city', 'freight_mode',
                     'transit_time', 'weight_up_to', 'additional_details',
                     'total_total_sale', 'sum_buy_fields', 'currency'
                     )
                ]
            }
        ),
        # ('Service charge', {'fields': []})
    )
    inlines = [ServiceInstanceInline, ServiceSurchargesInline, ServiceIncludesInstanceInline, ServiceExcludesInstanceInline]

    def get_inline_instances(self, request, obj=None):


        return super().get_inline_instances(request, obj)

    def get_list_display(self, request):

        return super().get_list_display(request)

    def save_model(self, request, obj, form, change):
        super().save_model(request, obj, form, change)

        services = Services.objects.filter(quote=obj, is_required=True)
        sum_buy_fields, total_total_sale = get_sale_price(services)
        Quote.objects.filter(pk=obj.id).update(sum_buy_fields=sum_buy_fields, total_total_sale=total_total_sale)

    def get_fields(self, request, obj=None):
        # print(self.fields)

        return super().get_fields(request, obj)

    def view_pdf_link(self, obj):
        name = obj.name
        id = obj.id
        quotation_num= obj.quotation_number
        url = f'{BASE_DIR}/media/{name}_{id}_{quotation_num}'
        if os.path.exists(url):
            return format_html('<a href="{}">{} Students</a>', url)
        return 'PDf place'

    view_pdf_link.allow_tags = True
    view_pdf_link.short_description = 'Pdf link'

    class Media:
        css = {
            'all': ('admin_css/admin_custom_css.css',),
        }


@admin.register(Services)
class ServiceAdminModel(admin.ModelAdmin):
    pass


@admin.register(ServiceIncludes)
class ServiceIncludesAdminModel(admin.ModelAdmin):
    pass


# @admin.register(ServiceExcludes)
# class ServiceExcludesAdminModel(admin.ModelAdmin):
#     pass


@admin.register(CalculateType)
class CalculateTypeModel(admin.ModelAdmin):
    pass


@admin.register(Currencies)
class CurrenciesAdminModel(admin.ModelAdmin):
    pass

