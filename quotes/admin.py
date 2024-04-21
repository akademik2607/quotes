import os

from django.contrib import admin
from django.db.models import Q
from django.utils.html import format_html

from config.settings import BASE_DIR
from quotes.models import Quote, Services, Currencies, ServiceIncludes, ServiceExcludes, SERVICE_TYPES


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
    extra = 1

    def get_queryset(self, request):
        qs = super(ServiceInstanceInline, self).get_queryset(request)
        service_id = request.path.split(r'/')[4]
        try:
            int(service_id)
        except ValueError:
            return qs
        service = Quote.objects.get(pk=service_id)
        check_origin = True
        check_freight = True
        check_destination = True

        if service.service_type == SERVICE_TYPES[0][0]:
            check_origin = True
            check_freight = True
            check_destination = True
        elif service.service_type == SERVICE_TYPES[1][0]:
            check_origin = True
            check_freight = True
            check_destination = False
        elif service.service_type == SERVICE_TYPES[2][0]:
            check_origin = False
            check_freight = True
            check_destination = True
        elif service.service_type == SERVICE_TYPES[3][0]:
            check_origin = False
            check_freight = True
            check_destination = False
        rules = None
        if check_origin:
            rules = qs.filter(description='Origin service', is_required=True)
        if check_freight:
            if rules:
                rules |= qs.filter(description='International freight', is_required=True)
            else:
                rules = qs.filter(description='International freight', is_required=True)
        if check_destination:
            if rules:
                rules |= qs.filter(description='Destination Services', is_required=True)
            else:
                rules = qs.filter(description='Destination Services', is_required=True)

        # Services(description='Origin service', quote=self, is_required=True),
        # Services(description='International freight', quote=self, is_required=True),
        # Services(description='Destination Services', quote=self, is_required=True)

        return rules


@admin.register(Quote)
class QuoteAdminModel(admin.ModelAdmin):
    change_form_template = 'admin/quote_form.html'
    save_on_top = True
    readonly_fields = ('view_pdf_link', )
    fieldsets = (
        (None, {
            'fields': ['title'],

        }),
        ('Contact information', {
            'classes': ('contact-information',),
            'fields': [
                    ('name', 'date', 'quotation_ref', 'quotation_number'),
                    ('origin_country', 'origin_city', 'service_type', 'method', 'volume'),
                    ('destination_country', 'destination_city', 'freight_mode', 'transit_time', 'weight_up_to', 'additional_details', 'total_total_sale', 'sum_buy_fields')
                ]
            }
        ),
        # ('Service charge', {'fields': []})
    )
    inlines = [ServiceInstanceInline, ServiceIncludesInstanceInline, ServiceExcludesInstanceInline]

    def get_inline_instances(self, request, obj=None):
        print(obj)
        print(self.inlines[0])

        return super().get_inline_instances(request, obj)

    def get_list_display(self, request):
        print('hello')
        return super().get_list_display(request)

    def save_model(self, request, obj, form, change):
        super().save_model(request, obj, form, change)

        services = Services.objects.filter(quote=obj, is_required=True)
        total_total_sale = 0
        sum_buy_fields = 0
        for service in services:
            q = None
            s = None
            b = None
            try:
                q = int(service.quantity)
                s = int(service.sale_price)
                b = int(service.buy_price)
            except TypeError:
                continue

            vat_mult = 1.17 if service.vat else 1
            total_total_sale += q * s * vat_mult
            sum_buy_fields += q * b * vat_mult
        Quote.objects.filter(pk=obj.id).update(sum_buy_fields=sum_buy_fields, total_total_sale=total_total_sale)

    def get_fields(self, request, obj=None):
        print(self.fields)

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


@admin.register(Currencies)
class CurrenciesAdminModel(admin.ModelAdmin):
    pass





# from django.contrib import admin
# from django.http import HttpResponseRedirect
# from django.conf.urls import url
# from monitor.models import LoginMonitor
# from monitor.import_custom import ImportCustom
# @admin.register(LoginMonitor)<br>
# class LoginMonitorAdmin(admin.ModelAdmin):<br>
#     change_list_template = "admin/monitor_change_list.html"
#     def get_urls(self):
#         urls = super(LoginMonitorAdmin, self).get_urls()
#   custom_urls = [
#       url('^import/$', self.process_import, name='process_import'),]
#   return custom_urls + urls
#     def process_import_btmp(self, request):
#   import_custom = ImportCustom()
#   count = import_custom.import_data()
#   self.message_user(request, f"создано {count} новых записей")
#   return HttpResponseRedirect("../")



# {% extends 'admin/change_list.html' %}
# {% block object-tools %}
#   <form action="import/" method="POST">
#     {% csrf_token %}
#     <input type="submit" value="Импорт" />
#   </form>
#     {{ block.super }}
# {% endblock %}