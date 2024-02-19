# from django.shortcuts import render


# from django.shortcuts import render
from rest_framework import generics, filters
from django.shortcuts import get_object_or_404
from datetime import date
# from django.views.decorators.csrf import csrf_exempt
# from datetime import datetime
# from django.core import serializers
# from django.http import HttpResponse
# import json

from rest_framework.decorators import permission_classes
from rest_framework.permissions import IsAuthenticated
from django.contrib.auth.models import User, Group
from rest_framework import viewsets
from rest_framework.views import APIView
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status

from restaurant.models import MenuItem, Category, Cart, Order, OrderItem
from restaurant.models import Booking

from restaurant.serializers import MenuItemSerializer, CategoryMenuSerializer
from restaurant.serializers import UserSerializer
from restaurant.serializers import OrderItemSerializer
from restaurant.serializers import OrderSerializer
from restaurant.serializers import BookingSerializer
from restaurant.serializers import CartSerializerView

from .permissions import MenuItemPermission
from .permissions import SingleMenuItemPermission
from .permissions import ManagerGroupPermissions
from .permissions import CartItemsPermissions
from .permissions import SingleOrderItemPermission


# Create your views here.
class BookingViewSet(viewsets.ModelViewSet ):
    queryset = Booking.objects.all()
    serializer_class = BookingSerializer
    permission_classes = [IsAuthenticated]
    


class CategorItemsView(generics.ListCreateAPIView):
     queryset = Category.objects.all()
     serializer_class = CategoryMenuSerializer
     permission_classes = [MenuItemPermission]
     


class MenuItemViews(generics.ListCreateAPIView):
    queryset = MenuItem.objects.select_related('category').all()
    serializer_class = MenuItemSerializer
    permission_classes = [MenuItemPermission]
    filter_backends = [filters.SearchFilter]
    search_fields = ['title', 'category__title']
    


class SingleMenuItemsView(generics.RetrieveUpdateAPIView, generics.DestroyAPIView):
    queryset = MenuItem.objects.all()
    serializer_class = MenuItemSerializer
    permission_classes = [SingleMenuItemPermission]


class ManagerUsersView(generics.ListCreateAPIView):
    queryset = User.objects.filter(groups__name='Manager')
    serializer_class = UserSerializer
    permission_classes = [ManagerGroupPermissions]

    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        username = request.data.get("username")
        if username:
            user = get_object_or_404(User, username=username)
            managers = Group.objects.get(name="Manager")
            managers.user_set.add(user)
            return Response({"message": "User {} added to Manager group.".format(username)}, status=status.HTTP_201_CREATED)
        return Response({"message":"error"}, status=status.HTTP_400_BAD_REQUEST)
    
    def delete(self, request, *args, **kwargs):
        username = request.data.get("username")
        if username:
            user = get_object_or_404(User, username=username)
            managers = Group.objects.get(name="Manager")
            if user in managers.user_set.all():
                managers.user_set.remove(user)
                return Response({"message": "User {} removed from Manager group.".format(username)}, status=status.HTTP_204_NO_CONTENT)
            else:
                return Response({"message": "User {} is not in Manager group.".format(username)}, status=status.HTTP_400_BAD_REQUEST)
        return Response({"message":"error"}, status=status.HTTP_400_BAD_REQUEST)
    

class SingleManagerUsersView(generics.RetrieveUpdateAPIView, generics.DestroyAPIView):
    queryset = MenuItem.objects.all()
    serializer_class = MenuItemSerializer
    permission_classes = [SingleMenuItemPermission]
    

class DeliveryCrewView(generics.ListCreateAPIView):
    queryset = User.objects.filter(groups__name='Delivery')
    serializer_class = UserSerializer
    permission_classes = [ManagerGroupPermissions]

    def post(self, request, *args, **kwargs):
        username = request.data.get("username")
        if username:
            user = get_object_or_404(User, username=username)
            delivery = Group.objects.get(name="Delivery")
            delivery.user_set.add(user)
            return Response({"message": "User {} added to Delivery group.".format(username)}, status=status.HTTP_201_CREATED)
        return Response({"message":"error"}, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, *args, **kwargs):
        username = request.data.get("username")
        if username:
            user = get_object_or_404(User, username=username)
            delivery = Group.objects.get(name="Delivery")
            if user in delivery.user_set.all():
                delivery.user_set.remove(user)
                return Response({"message": "User {} removed from Delivery group.".format(username)}, status=status.HTTP_204_NO_CONTENT)
            else:
                return Response({"message": "User {} is not in Delivery group.".format(username)}, status=status.HTTP_400_BAD_REQUEST)
        return Response({"message":"error"}, status=status.HTTP_400_BAD_REQUEST)

 
class SingleDeliveryCrewView(generics.RetrieveUpdateAPIView, generics.DestroyAPIView):
    queryset = MenuItem.objects.all()
    serializer_class = MenuItemSerializer
    permission_classes = [SingleMenuItemPermission]
    

@api_view(['GET', 'POST', 'DELETE'])
@permission_classes([ManagerGroupPermissions])
def add_to_managers(request):
    username = request.data.get("username")
    if username:
        user = get_object_or_404(User, username=username)
        managers = Group.objects.get(name="Manager")
        if request.method == 'POST':
            managers.user_set.add(user)
            message = "User {} added to Manager group.".format(username)
            res_status = status.HTTP_201_CREATED
        if request.method == 'DELETE':
            managers.user_set.remove(user)
            message = "User {} removed from Manager group.".format(username)
            res_status = status.HTTP_200_OK
        return Response({"message":message}, status=res_status) 
    return Response({"message":"error"}, status=status.HTTP_400_BAD_REQUEST)



class CartView(APIView):
    permission_classes = [CartItemsPermissions]

    def post(self, request, format=None):
        menu_item_id = request.data.get('menuitem')
        quantity = int(request.data.get('quantity'))
        menu_item = get_object_or_404(MenuItem, pk=menu_item_id)
        unit_price = menu_item.price
        price = quantity * unit_price
        cart_item = Cart.objects.create(
            user=request.user,
            menuitem=menu_item,
            quantity=quantity,
            unit_price=unit_price,
            price=price
        )
        serializer = CartSerializerView(cart_item)
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    
    def get(self, request, format=None):
        cart_items = Cart.objects.filter(user=request.user)
        serializer = CartSerializerView(cart_items, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    def delete(self, request, format=None):
        Cart.objects.filter(user=request.user).delete()
        return Response(status=status.HTTP_200_OK)
    


class OrdersView(APIView):

    permission_classes = [IsAuthenticated]

    def get(self, request):
            if request.user.groups.filter(name='Customer').exists():
                orders = Order.objects.filter(user=request.user)
            elif request.user.groups.filter(name='Manager').exists():
                orders = Order.objects.all()
            elif request.user.groups.filter(name='Delivery').exists():
                orders = Order.objects.filter(delivery_crew=request.user)
            elif request.user.is_superuser:
                orders = Order.objects.all()
            else:
                return Response({"message": "You do not have permission to perform this action."}, status=status.HTTP_403_FORBIDDEN)
            serializer = OrderSerializer(orders, many=True)
            return Response(serializer.data)
    
    def post(self, request):
        if request.user.groups.filter(name='Customer').exists():
            cart_items = Cart.objects.filter(user=request.user)
            if cart_items.exists():
                order = Order.objects.create(user=request.user, total=sum(item.price for item in cart_items), date=date.today())
                for item in cart_items:
                    OrderItem.objects.create(order=order, menuitem=item.menuitem, quantity=item.quantity, unit_price=item.unit_price, price=item.price)
                cart_items.delete()
                serializer = OrderSerializer(order)
                return Response(serializer.data, status=201)
            else:
                return Response({"message": "No items in cart to create an order."}, status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response({"message": "You do not have permission to perform this action."}, status=status.HTTP_403_FORBIDDEN)
    


class OrderDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer
    permission_classes = [SingleOrderItemPermission]

    def patch(self, request, pk, format=None):
        if request.user.groups.filter(name='Manager').exists() or request.user.is_superuser:
            username = request.data.get("delivery_crew")
            if username:
                user = get_object_or_404(User, username=username)
                order = get_object_or_404(Order, id=pk)
                delivery = Group.objects.get(name="Delivery")
                if user in delivery.user_set.all():
                    order.delivery_crew = user
                    order.save()  # Save the updated order
                    return Response({"message": "The delivery crew {} successfully assigned to deliver order {}".format(username, pk)}, status=status.HTTP_200_OK)
                else:
                    return Response({"message": "The user {} is not a member of the Delivery group".format(username)}, status=status.HTTP_400_BAD_REQUEST)
            else:
                return Response({"message": "Missing data. Check delivery crew username exists in the request."}, status=status.HTTP_400_BAD_REQUEST)
        
        elif request.user.groups.filter(name='Delivery').exists():
            user = request.user
            status_str = request.data.get("status")
            if status_str is not None:
                bool_status = status_str.lower() in ['true', '1', 'yes']
                delivery = Group.objects.get(name="Delivery")
                if user in delivery.user_set.all():
                    order = get_object_or_404(Order, id=pk)
                    if order.delivery_crew == user:
                        order.status = bool_status
                        order.save()
                        return Response({"message": "The status of the requested order {} is updated".format(pk)}, status=status.HTTP_200_OK)
                    else:
                        return Response({"message": "The order is not assigned to this delivery crew"}, status=status.HTTP_400_BAD_REQUEST)
                else:
                    return Response({"message": "The user is not a member of the Delivery group"}, status=status.HTTP_400_BAD_REQUEST)
            else:
                return Response({"message": "Missing the status field"}, status=status.HTTP_404_NOT_FOUND)
        else:
            return Response({"message": "You do not have permission to perform this task."}, status=status.HTTP_403_FORBIDDEN)




class OrderItemView(APIView):
    permission_classes = [IsAuthenticated]

    def get_object(self, pk):
        try:
            return OrderItem.objects.get(pk=pk)
        except OrderItem.DoesNotExist:
            return Response({"error": "OrderItem with id {} does not exist".format(pk)}, status=status.HTTP_404_NOT_FOUND)

    def get(self, request, pk, format=None):
        order_item = self.get_object(pk)
        if isinstance(order_item, Response):
            return order_item
        
        if request.user.groups.filter(name='Customer').exists() and order_item.order.user == request.user:
            serializer = OrderItemSerializer(order_item)
            return Response(serializer.data)
        else:
            return Response({"detail": "You do not have permission to perform this action."}, status=status.HTTP_403_FORBIDDEN)

    def put(self, request, pk, format=None):
        order_item = self.get_object(pk)
        if isinstance(order_item, Response):
            return order_item
        if request.user.groups.filter(name='Customer').exists() and order_item.order.user == request.user:
            serializer = OrderItemSerializer(order_item, data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response({"detail": "You do not have permission to perform this action."}, status=status.HTTP_403_FORBIDDEN)

    def delete(self, request, pk, format=None):
        order_item = self.get_object(pk)
        if isinstance(order_item, Response):
            return order_item
        if request.user.groups.filter(name='Manager').exists():
            order_item.delete()
            return Response(status=status.HTTP_200_OK)
        else:
            return Response({"detail": "You do not have permission to perform this action."}, status=status.HTTP_403_FORBIDDEN)

    def patch(self, request, pk, format=None):
        order_item = self.get_object(pk)
        if isinstance(order_item, Response):
            return order_item
        if request.user.groups.filter(name='Delivery').exists() and order_item.order.delivery_crew == request.user:
            serializer = OrderItemSerializer(order_item, data=request.data, partial=True) # set partial=True to update a data partially
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response({"detail": "You do not have permission to perform this action."}, status=status.HTTP_403_FORBIDDEN)
