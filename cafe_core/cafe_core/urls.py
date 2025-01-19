"""
URL configuration for cafe_core project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from oders_app.views import (HomePageView, TableOrders, OrderPageView, OrderCreateView,
     OrderDetailView, DishDeleteView, ShiftListView, StartShiftView,EndShiftView,
     OrderListView, OrderUpdateView,  DishAddView, DishCreateView, TableCreateView, TableDeleteView)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', HomePageView.as_view(), name='home-url'),
    path('table/<int:table_id>/', TableOrders.as_view(), name='table-orders-url'),
    path('orders/<int:table_id>/', OrderPageView.as_view(), name='orders-url'),
    path('orders/create/', OrderCreateView.as_view(), name='order-create-url'),
    path('orders-list/', OrderListView.as_view(), name='orders-url'),
    path('orders-detail/<int:pk>/', OrderDetailView.as_view(), name='order-detail-url'),
    path('orders-edit/<int:pk>/', OrderUpdateView.as_view(), name='order-edit-url'),
    path('dish-add-list/', DishAddView.as_view(), name='dish-add-url'),
    path('dish-create/', DishCreateView.as_view(), name='dish-create-url'),
    path('table-create/', TableCreateView.as_view(), name='table-create-url'),
    path('table-delete/<int:pk>/', TableDeleteView.as_view(), name='table-delete-url'),
    path('dish-delete/<int:pk>/', DishDeleteView.as_view(), name='dish-delete-url'),
    path('shift-list/', ShiftListView.as_view(), name='shift-list-url'),
    path('start-shift/', StartShiftView.as_view(), name='start-shift-url'),
    path('end-shift/', EndShiftView.as_view(), name='end-shift-url'),
]
