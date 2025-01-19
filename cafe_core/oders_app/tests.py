from django.test import TestCase
from django.urls import reverse
from oders_app.models import Shift
from django.utils.timezone import now

from oders_app.models import Dish, Table, Order


class HomePageTest(TestCase):
    """ Тесты для домашней страницы """
    def test_home_page(self):
        response = self.client.get('/')
        self.assertEqual(response.status_code, 200)


class OrderCreateTest(TestCase):
    """  Тесты для создания заказа """
    def setUp(self):
        self.table = Table.objects.create(number=1)
        self.dish = Dish.objects.create(name="Pizza", price=100)

    def test_create_order(self):
        response = self.client.post(reverse('order-create-url'), {
            'table': self.table.id,
            'dishes': [self.dish.id],
            'status': 'pending'  # Добавляем статус
        })
        self.assertEqual(response.status_code, 302)  # Редирект
        self.assertEqual(Order.objects.count(), 1)



class OrderDetailTest(TestCase):
    """ Тесты для детального просмотра заказа """
    def setUp(self):
        self.table = Table.objects.create(number=2)
        self.order = Order.objects.create(table_number=self.table, status='paid')

    def test_order_detail_view(self):
        response = self.client.get(reverse('order-detail-url', args=[self.order.id]))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'order_detail.html')



class OrderUpdateTest(TestCase):
    """  Тесты для обновления заказа """
    def setUp(self):
        self.table = Table.objects.create(number=3)
        self.dish = Dish.objects.create(name="Burger", price=50)
        self.order = Order.objects.create(table_number=self.table, status='pending')
        self.order.items.add(self.dish)

    def test_update_order(self):
        response = self.client.post(reverse('order-edit-url', args=[self.order.id]), {
            'table_number': self.table.id,
            'dishes': [self.dish.id],
            'status': 'ready'
        })
        self.assertEqual(response.status_code, 302)
        self.order.refresh_from_db()
        self.assertEqual(self.order.status, 'ready')


class OrderDeleteTest(TestCase):
    """ Тесты для удаления заказа """
    def setUp(self):
        self.table = Table.objects.create(number=4)
        self.order = Order.objects.create(table_number=self.table, status='paid')

    def test_delete_order(self):
        response = self.client.post(reverse('order-delete-url', args=[self.order.id]))
        self.assertEqual(response.status_code, 302)
        self.assertEqual(Order.objects.count(), 0)  # Заказ должен удалиться


class StartShiftTest(TestCase):
    """ Тесты для начала смены """
    def test_start_shift(self):
        response = self.client.post(reverse('start-shift-url'), {'start_time': now()})
        self.assertEqual(response.status_code, 302)
        self.assertEqual(Shift.objects.count(), 1)




