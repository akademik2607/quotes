from django.contrib import admin
from quotes.models import Quote, Services, Currencies, ServiceIncludes, ServiceExcludes


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


@admin.register(Quote)
class QuoteAdminModel(admin.ModelAdmin):
    change_form_template = 'admin/quote_form.html'
    save_on_top = True
    fieldsets = (
        (None, {
            'fields': ['title']
        }),
        ('Contact information', {
            'classes': ('contact-information',),
            'fields': [
                    ('name', 'date', 'quotation_ref', 'quotation_number'),
                    ('origin', 'service_type', 'method', 'volume'),
                    ('destination', 'freight_mode', 'transit_time', 'weight_up_to', 'additional_details')
                ]
            }
        ),
        # ('Service charge', {'fields': []})
    )
    inlines = [ServiceInstanceInline, ServiceIncludesInstanceInline, ServiceExcludesInstanceInline]

    def get_inline_instances(self, request, obj=None):
        # print(obj.is_show_numbers)
        return super().get_inline_instances(request, obj)

    def get_list_display(self, request):
        print('hello')
        return super().get_list_display(request)

    def save_model(self, request, obj, form, change):

        super().save_model(request, obj, form, change)

    def get_fields(self, request, obj=None):
        print(self.fields)

        return super().get_fields(request, obj)

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


@admin.register(ServiceExcludes)
class ServiceExcludesAdminModel(admin.ModelAdmin):
    pass


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