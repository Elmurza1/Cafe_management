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
from oders_app.views import HomePageView, TableOrders, OrderPageView, OrderCreateView, OrderDetailView, OrderListView, OrderUpdateView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', HomePageView.as_view(), name='home-url'),
    path('table/<int:table_id>/', TableOrders.as_view(), name='table_orders'),
    path('orders/<int:table_id>/', OrderPageView.as_view(), name='orders-url'),
    path('orders/create/', OrderCreateView.as_view(), name='order-create'),
    path('orders-list/', OrderListView.as_view(), name='orders-list'),
    path('orders-detail/<int:pk>/', OrderDetailView.as_view(), name='order-detail'),
    path('orders-edit/<int:pk>/', OrderUpdateView.as_view(), name='order-edit'),
]
