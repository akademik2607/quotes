import codecs
import json
import os
from wsgiref.util import FileWrapper

import requests
# import WebSite2PDF
from django.db.models import Q
from django.http import HttpResponse

from django.shortcuts import render

# Create your views here.
from django.template import loader
from django.views.decorators.csrf import csrf_exempt

from config.settings import BASE_DIR
from quotes.models import Quote,  ServiceIncludes, ServiceExcludes, Services, Currencies
from quotes.appconstants import SERVICES

import pdfkit

from tools.functions import get_sale_price, get_show_perms


def create_pdf(request):
    quote = Quote.objects.filter(pk=request.GET.get('id')).get()
    print(quote)

    #
    origin_services = ServiceIncludes.objects.filter(service=SERVICES[0][0], quote=quote, is_checked=True).all()
    international_freight = ServiceIncludes.objects.filter(service=SERVICES[1][0], quote=quote, is_checked=True).all()
    destination_services = ServiceIncludes.objects.filter(service=SERVICES[2][0], quote=quote, is_checked=True).all()
    services_exclude = ServiceExcludes.objects.filter(quote=quote, is_checked=True)
    print(origin_services)
    print(international_freight)
    print(destination_services)


    origin_service = Services.objects.filter(quote=quote, is_required=True, description__startswith='Origin').first()
    international_freight_s = Services.objects.filter(quote=quote, is_required=True, description__startswith='International').first()
    destination_service = Services.objects.filter(quote=quote, is_required=True, description__startswith='Destination').first()

    #Service set
    method_services = []
    quote_service_permissions = get_show_perms(quote.service_type)
    if quote_service_permissions['check_origin']:
        method_services.append(origin_service)
    if quote_service_permissions['check_freight']:
        method_services.append(international_freight_s)
    if quote_service_permissions['check_destination']:
        method_services.append(destination_service)

    __, method_sale_price = get_sale_price(method_services)


    #Additional surcharges set
    add_services = Services.objects.filter(
        quote=quote).filter(
            Q(is_required=False) |
            ~(
                Q(is_required=True, description__startswith='Origin') |
                Q(is_required=True, description__startswith='International') |
                Q(is_required=True, description__startswith='Destination')
            )
    ).all()

    add_services_info = []
    for add_service in  add_services:
        __, add_service_sale_price = get_sale_price([add_service])
        add_services_info.append(
            (
                add_service.description,
                add_service.currency,
                add_service_sale_price,
            )
        )

    pdf_template = loader.render_to_string(
        'EnglishQuote.html',
        context={
            'object': quote,
            'service_type': quote.service_type,
            'origin_services': origin_services,
            'international_freight': international_freight,
            'destination_services': destination_services,
            'services_exclude': services_exclude,
            'is_not_pdf': False,
            'origin_service': origin_service,
            'international_freight_s': international_freight_s,
            'destination_service': destination_service,
            'add_services_info': add_services_info,
            'method_sale_price': method_sale_price,

        },
        request=request)


    # config = pdfkit.configuration(wkhtmltopdf=r'D:\wkhtmltopdf\bin\wkhtmltopdf.exe')
    pdfkit.from_string(
        pdf_template,
        f'{BASE_DIR}/media/{quote.name}_{quote.id}_{quote.quotation_number}.pdf',
        # configuration=config,
        options={"enable-local-file-access": ""}
    )


    total_sale = quote.total_total_sale
    total_buy = quote.sum_buy_fields

    origin_supplier = origin_service.supplier
    freight_supplier = international_freight_s.supplier
    destination_supplier = destination_service.supplier

    r = requests.post('https://hook.eu1.make.com/m5txkpgp588v0p6nzunv8s5v3hchquky',
                      json={
                          'item_id': quote.item_id,
                          'quotation_num': quote.quotation_number,
                           'name': quote.name,
                            'quotation_ref': quote.quotation_ref,
                            'origin_country': quote.origin_country,
                            'origin_city': quote.origin_city,
                            'service_type': quote.service_type,
                            'method': quote.method,
                            'volume': quote.volume,
                            'destination': quote.destination_country,
                            'freight_mode': quote.freight_mode,
                            'transit_time': quote.transit_time,
                            'weight_up_to': quote.weight_up_to,
                            'currency': quote.currency,
                            'total_sale': total_sale,
                            'total_buy': total_buy,

                            'origin_supplier': origin_supplier,
                            'freight_supplier': freight_supplier,
                            'destination_supplier': destination_supplier,
                            'pdf_url': f'{request.META["HTTP_HOST"]}/media/{quote.name}_{quote.id}_{quote.quotation_number}.pdf'
                          })

    return render(request, 'EnglishQuote.html', context={
        'object': quote,
        'service_type': quote.service_type,
        'origin_services': origin_services,
        'international_freight': international_freight,
        'destination_services': destination_services,
        'services_exclude': services_exclude,
        'is_not_pdf': True,
        'origin_service': origin_service,
        'international_freight_s': international_freight_s,
        'destination_service': destination_service,
        'method_sale_price': method_sale_price,
        'add_services_info': add_services_info,
    })


@csrf_exempt
def create_quote_hook(request):

    data = json.loads(request.body)
    quotation_num = data.get('quotation_num', 423)
    name = data.get('name', 'TestName')
    quotation_ref = data.get('quotation_ref', 123)
    item_id = data.get('item_id', None)                         #Add to model
    origin_country = data.get('origin', 'TestOrigin')
    origin_city = data.get('origin_city', None)
    service_type = data.get('service_type', 'Door to Door')
    method = data.get('method', 'TestMethod')
    volume = data.get('volume', 42)
    destination = data.get('destination', 'DestinationTest')
    freight_mode = data.get('freight_mode', 'TestFreightMode')
    transit_time = data.get('transit_time', 23)
    weight_up_to = data.get('weight_up_to', 'TestWeightUpTo')
    currency = data.get('currency', None)


    destination_city = data.get('destination_city', None)
    Quote(
        item_id=item_id,
        title=name,
        quotation_number=quotation_num,
        name=name,
        quotation_ref=quotation_ref,
        origin_country=origin_country,
        origin_city=origin_city,
        service_type=service_type,
        method=method,
        volume=volume,
        destination_country=destination,
        destination_city=destination_city,
        freight_mode=freight_mode,
        transit_time=transit_time,
        weight_up_to=weight_up_to
    ).save()

    # quote = Quote.objects.latest('id')
    # base_currency, created = Currencies.objects.get_or_create(label=currency)
    # Services.objects.filter(quote=quote, is_required=True).update(currency=base_currency)



def download_pdf(request, *args, **kwargs):
    filename = kwargs.get('slug')
    if filename:
        content_type = 'application/vnd.ms-excel'
        file_path = os.path.join(f'{BASE_DIR}/media/', filename)
        print(file_path)
        if os.path.exists(file_path):

            response = HttpResponse(FileWrapper(open(file_path, 'rb')), content_type=content_type)
            response['Content-Disposition'] = 'attachment; filename=%s' % (
                 filename,
            )
        response['Content-Length'] = os.path.getsize(file_path)
        return response



