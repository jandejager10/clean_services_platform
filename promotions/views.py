from django.shortcuts import render


# Create your views here.
def offers(request):
    # Your view logic here
    return render(request, 'promotions/offers.html')
