from django.shortcuts import render, redirect, get_object_or_404
from django.views import View
from django.views.generic import TemplateView, ListView

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


class TableOrders(View):
    """Страница заказов для выбранного стола."""
    def get(self, request, table_id):
        table = Table.objects.get(id=table_id)
        orders = Order.objects.filter(table_number=table)
        return render(request, 'index.html', {'orders': orders, 'table': table})


class OrderPageView(TemplateView):
    """ вьюшка для показа заказов """
    template_name = 'dish.html'

    def get_context_data(self, **kwargs):
        context = {
          'dishes': Dish.objects.all(),
          'table': Table.objects.get(id=kwargs['table_id']),
        }
        return context


class OrderCreateView(View):
    """ вьюшка для создания заказа """
    def post(self, request):
        selected_dishes = request.POST.getlist('dish')  # Получаем список выбранных блюд
        selected_table = request.POST.get('table')  # Получаем выбранный стол
        selected_status = request.POST.get('status')

        order = Order.objects.create(status=selected_status, total_price=0)
        dishes = Dish.objects.filter(id__in=selected_dishes)
        table = Table.objects.get(id=selected_table)

        order.table_number = table

        order.items.set(dishes)

        order.total_price = sum(dish.price for dish in dishes)
        order.save()
        return redirect('home-url')


class OrderListView(ListView):
    """ вьюшка для списка и поиска заказов """
    model = Order
    template_name = 'order.html'
    context_object_name = 'orders'

    def get_queryset(self):
        search_query = self.request.GET.get('search', '')
        if search_query:
            return Order.objects.filter(
                id__icontains=search_query
            ) | Order.objects.filter(
                table_number__number__icontains=search_query
            )
        else:
            return Order.objects.all()

class OrderUpdateView(View):
    """ вьюшка для обновления заказа """

    def get(self, request, pk):
        order = get_object_or_404(Order, pk=pk)
        tables = Table.objects.all()  # Получаем список всех столов
        dishes = Dish.objects.all()  # Все доступные блюда
        return render(request, 'order_edit.html', {
            'order': order,
            'tables': tables,
            'dishes': dishes
        })

    def post(self, request, pk):
        order = get_object_or_404(Order, pk=pk)

        # Получаем данные из формы
        table_id = request.POST.get('table_number')
        selected_dishes = request.POST.getlist('dishes')
        status = request.POST.get('status')

        dishes = Dish.objects.filter(id__in=[int(dish_id) for dish_id in selected_dishes])

        order.table_number = get_object_or_404(Table, id=table_id)
        order.status = status
        order.items.set(dishes)

        order.total_price = sum(dish.price for dish in dishes)
        order.save()

        return redirect('order-detail', pk=order.pk)


class OrderDetailView(View):
    """🔹 Детальная страница заказа"""
    def get(self, request, pk):
        order = get_object_or_404(Order, pk=pk)
        return render(request, 'order_detail.html', {'order': order})