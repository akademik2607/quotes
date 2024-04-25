from .appconstants import SERVICES, nullable, METHODS, SERVICE_TYPES, FREIGHT_MODES

from django.utils.translation import gettext_lazy as _

from django.db import models

from tools.functions import get_show_perms




class Currencies(models.Model):
    label = models.CharField(_('Currency label'), max_length=20, **nullable)

    class Meta:
        verbose_name = _('Currency')
        verbose_name_plural = _('Currencies')

    def __str__(self):
        return self.label


class CalculateType(models.Model):
    label = models.CharField(_('Calculate type label'), max_length=20, **nullable)

    class Meta:
        verbose_name = _('Calculate type')
        verbose_name_plural = _('Calculate types')

    def __str__(self):
        return self.label


class ServiceIncludes(models.Model):
    label = models.CharField(_('Service name'), max_length=125, **nullable)
    is_checked = models.BooleanField('', default=False)
    quote = models.ForeignKey('Quote', on_delete=models.SET_NULL, related_query_name='quote', **nullable)
    service = models.CharField(_('Services'), choices=SERVICES, max_length=25, **nullable)

    class Meta:
        verbose_name = _('Service inclues')
        verbose_name_plural = _('Services includes')

    def __str__(self):
        return self.label


class ServiceExcludes(models.Model):
    label = models.CharField(_('Service name'), max_length=125, **nullable)
    is_checked = models.BooleanField('', default=False)
    quote = models.ForeignKey('Quote', on_delete=models.SET_NULL, related_query_name='quote', **nullable)

    class Meta:
        verbose_name = _('Services excludes')
        verbose_name_plural = _('Services excludes')

    def __str__(self):
        return self.label


class Services(models.Model):
    description = models.CharField(_('Description'), max_length=125, **nullable)
    supplier = models.CharField(_('Supplier'), max_length=125, **nullable)
    quantity = models.IntegerField(_('Quantity'), **nullable)
    currency = models.ForeignKey(Currencies, on_delete=models.CASCADE, **nullable)
    buy_price = models.IntegerField(_('Buy price'), **nullable)
    sale_price = models.IntegerField(_('Sale price'), **nullable)
    vat = models.BooleanField(_('Vat'), default=False)
    type = models.ForeignKey(CalculateType, on_delete=models.CASCADE, **nullable)
    quote = models.ForeignKey('Quote', on_delete=models.CASCADE)
    is_required = models.BooleanField(_('Is required service'), default=False)

    class Meta:
        verbose_name = _('Service')
        verbose_name_plural = _('Services')

    def __str__(self):
        return f'{self.quote.name}: {self.description}'


class Quote(models.Model):
    title = models.CharField(_('Title'), max_length=125, **nullable)

    item_id = models.CharField(_('Item id'), max_length=25, **nullable)
    additional_details = models.CharField(_('Additional details'), max_length=300, **nullable)
    name = models.CharField(_('Name'), max_length=125, **nullable)
    date = models.DateField(_('Date'), **nullable)
    quotation_ref = models.IntegerField(_('Quotation ref'), **nullable)
    quotation_number = models.CharField(_('Quotation number'), max_length=25, **nullable)
    origin_country = models.CharField(_('Origin Country'), max_length=125, **nullable)
    origin_city = models.CharField(_('Origin City'), max_length=125, **nullable)
    service_type = models.CharField(_('Service type'), choices=SERVICE_TYPES, max_length=125, default=SERVICE_TYPES[0][0], **nullable)
    method = models.CharField(_('Method'), choices=METHODS, max_length=125, **nullable)
    volume = models.FloatField(_('Volume'), **nullable)
    destination_country = models.CharField(_('Destination Country'), max_length=125, **nullable)
    destination_city = models.CharField(_('Destination City'), max_length=125, **nullable)
    freight_mode = models.CharField(_('Freight mode'), choices=FREIGHT_MODES, max_length=125, **nullable)
    transit_time = models.CharField(_('Transit time'), max_length=25, **nullable)
    weight_up_to = models.CharField(_('Weight Up to'), max_length=125, **nullable)
    total_total_sale = models.FloatField(_('Total sale'), **nullable)
    sum_buy_fields = models.FloatField(_('Sum buy'), **nullable)
    currency = models.ForeignKey(Currencies, verbose_name=_('Currencies'), related_name='currency',
                                 on_delete=models.SET_NULL, **nullable)

    class Meta:
        verbose_name = _('Quote')
        verbose_name_plural = _('Quotes')

    def __str__(self):
        return self.title if self.title else 'Unknown'

    def save(self, *args, **kwargs):
        is_create = False
        if not self.pk:
            is_create = True
        super(Quote, self).save(*args, **kwargs)
        show_service_perms = get_show_perms(self.service_type)

        if is_create:
            Services.objects.bulk_create([
                Services(description='Origin service', quote=self, is_required=True),
                Services(description='International freight', quote=self, is_required=True),
                Services(description='Destination Services', quote=self, is_required=True),

                Services(description='Freight Surcharges', quote=self, is_required=True),
                Services(description='Port & local fees at destination', quote=self, is_required=True),
            ])

            ServiceIncludes.objects.bulk_create([
                ServiceIncludes(
                    label='Export packing all small goods into cartons',
                    is_checked=show_service_perms['check_origin'],
                    service=SERVICES[0][0],
                    quote=self
                ),
                ServiceIncludes(
                    label='Export wrapping all furniture items including disassembling, if required.',
                    is_checked=show_service_perms['check_origin'],
                    service=SERVICES[0][0],
                    quote=self
                ),
                ServiceIncludes(
                    label='Labeling and creating an inventory of all items',
                    is_checked=show_service_perms['check_origin'],
                    service=SERVICES[0][0],
                    quote=self
                ),
                ServiceIncludes(
                    label='Loading and securing into shipping container',
                    is_checked=show_service_perms['check_origin'],
                    service=SERVICES[0][0],
                    quote=self
                ),
                ServiceIncludes(
                    label='Transfer of container to the port/terminal',
                    is_checked=show_service_perms['check_origin'],
                    service=SERVICES[0][0],
                    quote=self
                ),
                ServiceIncludes(
                    label='Payment of all port/terminal handling fees',
                    is_checked=show_service_perms['check_origin'],
                    service=SERVICES[0][0],
                    quote=self
                ),
                ServiceIncludes(
                    label='Preparation of all export documentation & Export customs clearance',
                    is_checked=show_service_perms['check_origin'],
                    service=SERVICES[0][0],
                    quote=self
                ),

                ServiceIncludes(
                    label='Payment of international freight charges to arrival terminal',
                    is_checked=show_service_perms['check_freight'],
                    service=SERVICES[1][0],
                    quote=self
                ),

                ServiceIncludes(
                    label='Securing customs and clearance',
                    is_checked=show_service_perms['check_destination'],
                    service=SERVICES[2][0],
                    quote=self
                ),
                ServiceIncludes(
                    label='Delivery to residence within 25 miles from a.m. destination',
                    is_checked=show_service_perms['check_destination'],
                    service=SERVICES[2][0],
                    quote=self
                ),
                ServiceIncludes(
                    label='Unwrapping all furniture items',
                    is_checked=show_service_perms['check_destination'],
                    service=SERVICES[2][0],
                    quote=self
                ),
                ServiceIncludes(
                    label='Removal of used packaging materials at time of delivery',
                    is_checked=show_service_perms['check_destination'],
                    service=SERVICES[2][0],
                    quote=self
                ),
                ServiceIncludes(
                    label='Setting up at residence',
                    is_checked=show_service_perms['check_destination'],
                    service=SERVICES[2][0],
                    quote=self
                ),
                ServiceIncludes(
                    label='Basic assembling of furniture (e.g. beds & tables- not IKEA)',
                    is_checked=show_service_perms['check_destination'],
                    service=SERVICES[2][0],
                    quote=self
                ),
            ])

            check_exludes = True
            ServiceExcludes.objects.bulk_create([
                ServiceIncludes(
                    label='Insurance coverage (as per below option)',
                    is_checked=check_exludes,
                    quote=self
                ),
                ServiceIncludes(
                    label='For US Shipments only: ISF Filing $ 45.00',
                    is_checked=check_exludes,
                    quote=self
                ),
                ServiceIncludes(
                    label='Port, local fees & DO & NVOCC fees at destination, if any.',
                    is_checked=check_exludes,
                    quote=self
                ),
                ServiceIncludes(
                    label='Customs duty/tax and/or local VAT',
                    is_checked=check_exludes,
                    quote=self
                ),
                ServiceIncludes(
                    label='Customs inspection and\or Quarantine inspection',
                    is_checked=check_exludes,
                    quote=self
                ),
                ServiceIncludes(
                    label='Customs inspection and\or Quarantine inspection',
                    is_checked=check_exludes,
                    quote=self
                ),
                ServiceIncludes(
                    label='Quarantine treatment, i.e. fumigation, steam cleaning',
                    is_checked=check_exludes,
                    quote=self
                ),
                ServiceIncludes(
                    label='Storage and store handling and/or Demurrage',
                    is_checked=check_exludes,
                    quote=self
                ),
                ServiceIncludes(
                    label='Delivery above 2nd level',
                    is_checked=check_exludes,
                    quote=self
                ),
                ServiceIncludes(
                    label='Dis/Assembling of furniture specially IKEA (beside basic furniture e.g.beds & tables)',
                    is_checked=check_exludes,
                    quote=self
                ),
                ServiceIncludes(
                    label='Bad access with long/step carry (20 m) or shuttle vehicle requirements',
                    is_checked=check_exludes,
                    quote=self
                ),
                ServiceIncludes(
                    label='Heavy items handling (Piano/ Safe)',
                    is_checked=check_exludes,
                    quote=self
                ),
                ServiceIncludes(
                    label='Parking permits, lift fees',
                    is_checked=check_exludes,
                    quote=self
                ),


            ])

        else:
            ServiceIncludes.objects.filter(service=SERVICES[0][0], quote=self).update(is_checked=show_service_perms['check_origin'])
            ServiceIncludes.objects.filter(service=SERVICES[1][0], quote=self).update(is_checked=show_service_perms['check_freight'])
            ServiceIncludes.objects.filter(service=SERVICES[2][0], quote=self).update(is_checked=show_service_perms['check_destination'])




















