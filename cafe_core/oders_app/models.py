from django.db import models

# Create your models here.
class Dish(models.Model):
    """ вьюшка для блюд """
    name = models.CharField(max_length=50, verbose_name='название блюда')
    price = models.PositiveIntegerField(verbose_name='цена')

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'блюдо'
        verbose_name_plural = 'блюда'


class Table(models.Model):
    """ вьюшка для столов """
    number = models.PositiveSmallIntegerField(verbose_name='номер стола', unique=True)
    is_free = models.BooleanField(verbose_name='свободен', default=True)
    is_active = models.BooleanField(verbose_name='активен', default=True)

    def __str__(self):
        return f"Стол {self.number}"

    class Meta:
        verbose_name = 'стол'
        verbose_name_plural = 'столы'


class Order(models.Model):
    """ вьюшка для заказа """
    STATUS_CHOICES = [
        ('padding', 'ожидает'),
        ('ready', 'готово'),
        ('paid', 'оплачен'),

    ]
    items = models.ManyToManyField(Dish, verbose_name='блюда')
    table_number = models.ForeignKey(Table , on_delete=models.CASCADE, null=True ,verbose_name='номер стола')

    total_price = models.PositiveIntegerField(
        verbose_name='общая стоимость',
        null=True,
        blank=True
    )
    status = models.CharField(
        max_length=10,
        choices=STATUS_CHOICES,
        default='padding')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Заказ {self.id} (Стол {self.table_number})"


    class Meta:
        verbose_name = 'заказ'
        verbose_name_plural = 'заказы'


class Shift(models.Model):
    """ вьюшка для смены """
    start_time = models.DateTimeField(verbose_name='начало смены', null=True, blank=True)
    end_time = models.DateTimeField(verbose_name='окончание смены', null=True, blank=True)
    total_revenue = models.DecimalField(
        verbose_name='общая выручка',
        max_digits=10,
        decimal_places=2,
        default=0
    )
    # total_orders = models.PositiveIntegerField(verbose_name='общее количество заказов', d)

    def __str__(self):
        return f"Смена {self.id} ({self.start_time} - {self.end_time})"

    class Meta:
        verbose_name = 'смена'
        verbose_name_plural = 'смены'






