from django.db.models import Sum
from django.http import HttpResponseBadRequest
from django.shortcuts import render, redirect, get_object_or_404
from django.utils import timezone
from django.utils.dateparse import parse_datetime
from django.views import View
from django.views.generic import TemplateView, ListView

from oders_app.models import Order, Table, Dish, Shift


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

        return redirect('order-detail-url', pk=order.pk)


class OrderDetailView(View):
    """🔹 Детальная страница заказа"""
    def get(self, request, pk):
        order = get_object_or_404(Order, pk=pk)
        return render(request, 'order_detail.html', {'order': order})


class DishAddView(TemplateView):
    """ вьюшка для страницы добавления блюда """
    template_name = 'new_order.html'

    def get_context_data(self, **kwargs):
        context = {
            'dishes': Dish.objects.all(),
            'tables': Table.objects.all(),
        }
        return context


class DishCreateView(View):
    """ вьюшка для создания блюда """
    def post(self, request):
        name = request.POST.get('name')
        price = request.POST.get('price')

        Dish.objects.create(name=name, price=price)
        return redirect('dish-add-url')


class DishDeleteView(View):
    """ вьюшка для удаления блюда """
    def post(self, request, pk):
        dish = Dish.objects.get(id=pk)
        dish.delete()
        return redirect('dish-add-url')



class TableCreateView(View):
    """ вьюшка для создания стола """
    def post(self, request):
        number = request.POST.get('number')
        Table.objects.create(number=number)
        return redirect('dish-add-url')


class TableDeleteView(View):
    """ вьюшка для удаления стола """
    def post(self, request, pk):
        table = Table.objects.get(id=pk)
        table.delete()
        return redirect('dish-add-url')


class ShiftListView(TemplateView):
    template_name = 'shift.html'

    def get_context_data(self, **kwargs):
        # Получаем все смены
        shifts = Shift.objects.all()
        return {'shifts': shifts}

# Представление для начала смены
class StartShiftView(View):
    def post(self, request):
        # Получаем время начала смены
        start_time = request.POST.get('start_time')

        # Создаем новую смену
        Shift.objects.create(start_time=start_time, end_time=None)

        return redirect('shift-list-url')



class EndShiftView(View):
    def post(self, request):
        shift_id = request.POST.get('shift_id')
        end_time_str = request.POST.get('end_time')

        print(f"DEBUG: request.POST = {request.POST}")
        print(f"DEBUG: end_time = {end_time_str}")

        if not end_time_str:
            return HttpResponseBadRequest("Ошибка: end_time не передан")

        end_time = parse_datetime(end_time_str)
        if not end_time:
            return HttpResponseBadRequest("Ошибка: неверный формат даты")

        end_time = timezone.make_aware(end_time) if timezone.is_naive(end_time) else end_time

        shift = get_object_or_404(Shift, id=shift_id)
        shift.end_time = end_time
        shift.save()

        # Убедимся, что start_time и end_time с временной зоной
        shift.start_time = timezone.make_aware(shift.start_time) if timezone.is_naive(shift.start_time) else shift.start_time
        shift.end_time = timezone.make_aware(shift.end_time) if timezone.is_naive(shift.end_time) else shift.end_time

        print(f"DEBUG: Shift start_time = {shift.start_time} (type: {type(shift.start_time)})")
        print(f"DEBUG: Shift end_time = {shift.end_time} (type: {type(shift.end_time)})")

        # Проверяем все заказы
        all_orders = Order.objects.filter(status='paid')
        print(f"DEBUG: Всего заказов со статусом 'paid': {all_orders.count()}")
        print(f"DEBUG: Все заказы: {list(all_orders.values('id', 'created_at', 'total_price'))}")

        # Фильтруем заказы в диапазоне времени смены
        print(f"DEBUG: Фильтруем заказы в диапазоне {shift.start_time} - {shift.end_time}")
        orders = Order.objects.filter(
            status='paid',
            created_at__gte=shift.start_time,
            created_at__lte=shift.end_time
        )

        print(f"DEBUG: Найдено заказов: {orders.count()}")
        print(f"DEBUG: Заказы: {list(orders.values('id', 'total_price', 'created_at'))}")

        orders.filter(total_price__isnull=True).update(total_price=0)
        total_revenue = orders.aggregate(total=Sum('total_price'))['total'] or 0
        shift.total_revenue = total_revenue
        shift.save()

        print(f"DEBUG: Выручка за смену = {total_revenue}")

        return redirect('shift-list-url')