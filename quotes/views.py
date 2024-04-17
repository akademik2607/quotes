from django.shortcuts import render

# Create your views here.
from quotes.models import Quote


def create_pdf(request):
    quote = Quote.objects.filter(pk=request.GET.get('id')).get()
    print(quote)
    return render(request, 'EnglishQuote.html', context={'object': quote})


def create_quote_hook(request):
        quotation_num = request.POST.get('quotation_num', 423)
        name = request.POST.get('name', 'TestName')
        quotation_ref = request.POST.get('quotation_ref', 123)
        item_id = request.POST.get('item_id', None)                         #Add to model
        origin_country = request.POST.get('origin', 'TestOrigin')
        origin_city = request.POST.get('origin_city', None)
        service_type = request.POST.get('service_type', 'DOOR2DOOR')
        method = request.POST.get('method', 'TestMethod')
        volume = request.POST.get('volume', 42)
        destination = request.POST.get('destination', 'DestinationTest')
        freight_mode = request.POST.get('freight_mode', 'TestFreightMode')
        transit_time = request.POST.get('transit_time', 23)
        weight_up_to = request.POST.get('weight_up_to', 'TestWeightUpTo')
        currency = request.POST.get('currency', None)                       #Check in models

        destination_city = request.POST.get('destination_city', None)
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
            destination=destination,
            freight_mode=freight_mode,
            transit_time=transit_time,
            weight_up_to=weight_up_to
        ).save()
