from django.shortcuts import render
from django.core import serializers
from rest_framework.decorators import permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework import viewsets
from django.http import HttpResponse
import json

from datetime import datetime
from .models import MenuItem #Category, Cart, Order, OrderItem
from .models import Booking

from .forms import BookingForm

from .serializers import BookingSerializer

# Create your views here.
def home(request):
    return render(request, 'index.html')

# Add your code here to create new views
def menu(request):
    menu_data = MenuItem.objects.all()
    main_data = {"menu": menu_data}
    return render(request, 'menu.html', {"menu": main_data})

def about(request):
    return render(request, 'about.html')

@permission_classes([IsAuthenticated])
def reservations(request):
    booking_json = []
    date = request.GET.get('date',datetime.today().date())
    bookings = Booking.objects.all()
    booking_json = serializers.serialize('json', bookings)
    return render(request, 'bookings.html',{"bookings":booking_json})

def book(request):
    form = BookingForm()
    if request.method == 'POST':
        form = BookingForm(request.POST)
        if form.is_valid():
            form.save()
    context = {'form':form}
    return render(request, 'book.html', context)


def menu_item(request, pk):
   menu_item = MenuItem.objects.filter(pk=pk)
   return render(request, 'menu_item.html',{"menu_item":menu_item})
#    if menu_item:
#        return render(request, 'menu_item.html',{"menu_item":menu_item})
#    else:
#        context = {
#         'status': '400', 'reason': 'Cant find any menu item with id: {0}'.format(pk)  
#         }
#        response = HttpResponse(json.dumps(context), content_type='application/json')
#        response.status_code = 400
#        return response
   
#@csrf_exempt
@permission_classes([IsAuthenticated])
def bookings(request):
    if request.method == 'POST':
        data = json.load(request)
        exist = Booking.objects.filter(reservation_date=data['reservation_date']).filter(
            reservation_slot=data['reservation_slot']).exists()
        if exist==False:
            booking = Booking(
                first_name=data['first_name'],
                reservation_date=data['reservation_date'],
                reservation_slot=data['reservation_slot'],
            )
            booking.save()
        else:
            return HttpResponse("{'error':1}", content_type='application/json')
    
    date = request.GET.get('date', datetime.today().date())
    
    if not date:
        date = datetime.today().date()    
        
    bookings = Booking.objects.all().filter(reservation_date=date)
    booking_json = serializers.serialize('json', bookings)

    return HttpResponse(booking_json, content_type='application/json')