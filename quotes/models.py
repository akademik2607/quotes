from importlib.resources import _

from django.db import models

TransportTypes = (
    ('TR', 'tractor'),
    ('CA', 'car')
)

nullable = {
    'null': True,
    'blank': True
}


SERVICE_TYPES = (
    ('DOOR2DOOR', 'Door to Door'),
    ('Door2Port', 'Door to Port'),
    ('Port2Door', 'Port to Door'),
    ('Port2Port', 'Port to Port'),
)

SERVICES = (
    ('origin_services', 'Origin Services'),
    ('international_freight', 'International Freight'),
    ('destination_services', 'Destination Services'),
    ('add', 'add')
)


class Currencies(models.Model):
    label = models.CharField(_('Currency label'), max_length=20, **nullable)

    class Meta:
        verbose_name = _('Currency')
        verbose_name_plural = _('Currencies')

    def __str__(self):
        return self.label




class ServiceIncludes(models.Model):
    label = models.CharField(_('Service name'), max_length=125, **nullable)
    is_checked = models.BooleanField('', default=False)
    quote = models.ForeignKey(_('Quote'), on_delete=models.SET_NULL, related_query_name='quote', **nullable)
    service = models.CharField(_('Services'), choices=SERVICES, max_length=25, **nullable)

    class Meta:
        verbose_name = _('Service item')
        verbose_name_plural = _('Service items')

    def __str__(self):
        return self.label


class ServiceExcludes(models.Model):
    label = models.CharField(_('Service name'), max_length=125, **nullable)
    is_checked = models.BooleanField('', default=False)
    quote = models.ForeignKey(_('Quote'), on_delete=models.SET_NULL, related_query_name='quote', **nullable)

    class Meta:
        verbose_name = _('Service item')
        verbose_name_plural = _('Service items')

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
    quote = models.ForeignKey(_('Quote'), on_delete=models.CASCADE)
    is_required = models.BooleanField(_('Is required service'), default=False)

    class Meta:
        verbose_name = _('Service')
        verbose_name_plural = _('Services')

    def __str__(self):
        return f'{self.quote.name}: {self.description}'


class Quote(models.Model):
    title = models.CharField(_('Title'), max_length=125, **nullable)

    additional_details = models.CharField(_('Additional details'), max_length=300, **nullable)
    name = models.CharField(_('Name'), max_length=125, **nullable)
    date = models.DateField(_('Date'), **nullable)
    quotation_ref = models.IntegerField(_('Quotation ref'), **nullable)
    quotation_number = models.IntegerField(_('Quotation number'), **nullable)
    origin = models.CharField(_('Origin'), max_length=125, **nullable)
    service_type = models.CharField(_('Service type'), choices=SERVICE_TYPES, max_length=125, default=SERVICE_TYPES[0][0], **nullable)
    method = models.CharField(_('Method'), max_length=125, **nullable)
    volume = models.IntegerField(_('Volume'), **nullable)
    destination = models.CharField(_('Destination'), max_length=125, **nullable)
    freight_mode = models.CharField(_('Freight mode'), max_length=125, **nullable)
    transit_time = models.IntegerField(_('Transit time'), **nullable)
    weight_up_to = models.CharField(_('Weight Up to'), max_length=125, **nullable)

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

        if self.service_type == SERVICE_TYPES[0][0]:
            check_origin = True
            check_freight = True
            check_destination = True
        elif self.service_type == SERVICE_TYPES[1][0]:
            check_origin = True
            check_freight = True
            check_destination = False
        elif self.service_type == SERVICE_TYPES[2][0]:
            check_origin = False
            check_freight = True
            check_destination = True
        elif self.service_type == SERVICE_TYPES[3][0]:
            check_origin = False
            check_freight = True
            check_destination = False

        if is_create:
            Services.objects.bulk_create([
                Services(description='Origin service', quote=self, is_required=True),
                Services(description='International freight', quote=self, is_required=True),
                Services(description='Destination Services', quote=self, is_required=True)
            ])

            ServiceIncludes.objects.bulk_create([
                ServiceIncludes(
                    label='Export packing all small goods into cartons',
                    is_checked=check_origin,
                    service=SERVICES[0][0],
                    quote=self
                ),
                ServiceIncludes(
                    label='Export wrapping all furniture items including disassembling, if required.',
                    is_checked=check_origin,
                    service=SERVICES[0][0],
                    quote=self
                ),
                ServiceIncludes(
                    label='Labeling and creating an inventory of all items',
                    is_checked=check_origin,
                    service=SERVICES[0][0],
                    quote=self
                ),
                ServiceIncludes(
                    label='Loading and securing into shipping container',
                    is_checked=check_origin,
                    service=SERVICES[0][0],
                    quote=self
                ),
                ServiceIncludes(
                    label='Transfer of container to the port/terminal',
                    is_checked=check_origin,
                    service=SERVICES[0][0],
                    quote=self
                ),
                ServiceIncludes(
                    label='Payment of all port/terminal handling fees',
                    is_checked=check_origin,
                    service=SERVICES[0][0],
                    quote=self
                ),
                ServiceIncludes(
                    label='Preparation of all export documentation & Export customs clearance',
                    is_checked=check_origin,
                    service=SERVICES[0][0],
                    quote=self
                ),

                ServiceIncludes(
                    label='Payment of international freight charges to arrival terminal',
                    is_checked=check_origin,
                    service=SERVICES[1][0],
                    quote=self
                ),

                ServiceIncludes(
                    label='Securing customs and clearance',
                    is_checked=check_origin,
                    service=SERVICES[2][0],
                    quote=self
                ),
                ServiceIncludes(
                    label='Delivery to residence within 25 miles from a.m. destination',
                    is_checked=check_origin,
                    service=SERVICES[2][0],
                    quote=self
                ),
                ServiceIncludes(
                    label='Unwrapping all furniture items',
                    is_checked=check_origin,
                    service=SERVICES[2][0],
                    quote=self
                ),
                ServiceIncludes(
                    label='Removal of used packaging materials at time of delivery',
                    is_checked=check_origin,
                    service=SERVICES[2][0],
                    quote=self
                ),
                ServiceIncludes(
                    label='Setting up at residence',
                    is_checked=check_origin,
                    service=SERVICES[2][0],
                    quote=self
                ),
                ServiceIncludes(
                    label='Basic assembling of furniture (e.g. beds & tables- not IKEA)',
                    is_checked=check_origin,
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



















