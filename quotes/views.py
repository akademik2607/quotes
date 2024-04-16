from django.shortcuts import render

# Create your views here.
from quotes.models import Quote


def create_pdf(request):
    quote = Quote.objects.filter(pk=request.GET.get('id')).get()
    print(quote)
    return render(request, 'EnglishQuote.html', context={'object': quote})
