from django.shortcuts import render
from django.views import View
from django.views.generic import TemplateView

from oders_app.models import Order, Table, Dish


# Create your views here.
class HomePageView(TemplateView):
    """ вьюшка для главной страницы """
    template_name = 'index.html'

    def get_context_data(self, **kwargs):
        context = {
            'orders': Order.objects.all(),
            'tables': Table.objects.filter(is_active=True).order_by('number'),
        }
        return context


def table_orders(request, table_number):
    """Страница заказов для выбранного стола."""
    orders = Order.objects.filter(table_number=table_number)  # Заказы для конкретного стола
    return render(request, 'index.html', {'table_number': table_number, 'orders': orders})

class OrderPageView(TemplateView):
    """ вьюшка для показа заказов """
    template_name = 'dish.html'

    def get_context_data(self, **kwargs):
        context = {
          'dishes': Dish.objects.all()
        }
        return context


class OrderCreateView(View):
    """ вьюшка для создания заказа """
    def post(self, request):
        pass
