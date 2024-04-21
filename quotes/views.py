import json
import os
import requests
# import WebSite2PDF

from django.shortcuts import render

# Create your views here.
from django.template import loader
from django.views.decorators.csrf import csrf_exempt

from config.settings import BASE_DIR
from quotes.models import Quote, SERVICES, ServiceIncludes, ServiceExcludes

import pdfkit



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


    pdf_template = loader.render_to_string(
        'EnglishQuote.html',
        context={
            'object': quote,
            'origin_services': origin_services,
            'international_freight': international_freight,
            'destination_services': destination_services,
            'services_exclude': services_exclude,
            'is_not_pdf': False
        },
        request=request)
    html_template = f'media/{quote.name}_{quote.id}_{quote.quotation_number}_pdf_template.html'
    with open(html_template, "w+", encoding='utf-8') as file:
        file.write(pdf_template)

    # c = WebSite2PDF.Client()
    # with open(f'media/{quote.name}_{quote.id}_{quote.quotation_number}.pdf', "wb+") as file:
    #     file.write(c.pdf(f"file:///{html_template}"))

    # config = pdfkit.configuration(wkhtmltopdf=r'D:\wkhtmltopdf\bin\wkhtmltopdf.exe')
    pdfkit.from_string(
        pdf_template,
        # 'out.pdf',
        f'media/{quote.name}_{quote.id}_{quote.quotation_number}.pdf',
        configuration=config,
        options={"enable-local-file-access": ""}
    )

    # r = requests.post('https://hook.eu1.make.com/r2dalfesh6xpfp8a7as3d2lndo2d5epz',
    #                   json={
    #                       'quotation_num': quote.quotation_number,
    #                        'name': quote.name,
    #                         'quotation_ref': quote.quotation_ref,
    #                         'origin_country': quote.origin_country,
    #                         'origin_city': quote.origin_city,
    #                         'service_type': quote.service_type,
    #                         'method': quote.method,
    #                         'volume': quote.volume,
    #                         'destination': quote.destination_country,
    #                         'freight_mode': quote.freight_mode,
    #                         'transit_time': quote.transit_time,
    #                         'weight_up_to': quote.weight_up_to,
    #                         'currency': 'US$'
    #                       })

    return render(request, 'EnglishQuote.html', context={
        'object': quote,
        'origin_services': origin_services,
        'international_freight': international_freight,
        'destination_services': destination_services,
        'services_exclude': services_exclude,
        'is_not_pdf': True
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
