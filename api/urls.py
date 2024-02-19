from django.urls import path, include
from rest_framework.routers import DefaultRouter

from . import views

router = DefaultRouter()
router.register(r"bookings", views.BookingViewSet, basename="tables-bookings")

urlpatterns = [
    path('menu-items', views.MenuItemViews.as_view(), name = "menu-items"),
    path('menu-items/<int:pk>', views.SingleMenuItemsView.as_view(), name = "menu-item"),
    path('categories/', views.CategorItemsView.as_view(), name= "categories"),
    path('groups/manager/users', views.ManagerUsersView.as_view(), name="managers"),
    path('groups/manager/users/<int:pk>', views.SingleManagerUsersView.as_view(), name="manager"),
    path('groups/delivery-crew/users', views.DeliveryCrewView.as_view(), name="deliveries"),
    path('groups/delivery-crew/users/<int:pk>', views.SingleDeliveryCrewView.as_view(), name="delivery"),
    path('cart/menu-items', views.CartView.as_view(), name="cart-view"), 
    path('orders', views.OrdersView.as_view(), name="orders"),
    path('orders/<int:pk>', views.OrderDetailView.as_view(), name="order-detail"),
    path('cart/orders', views.OrdersView.as_view(), name="cart-order"),
    path('cart/orders/<int:pk>', views.OrderItemView.as_view(), name="order-item"),
    path("", include(router.urls)),
    ]