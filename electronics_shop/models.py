from django.conf import settings
from django.db import models
from django.utils import timezone


class NetworkNode(models.Model):
    """
    Представляет собой узел в сети поставки электроники.
    """
    LEVEL_CHOICES = (
        (0, 'Завод'),
        (1, 'Розничная сеть'),
        (2, 'Индивидуальный предприниматель'),
    )

    name = models.CharField(max_length=255, verbose_name="Название")
    email = models.EmailField(verbose_name="Email")
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, verbose_name="Автор")
    country = models.CharField(max_length=100, verbose_name="Страна")
    city = models.CharField(max_length=100, verbose_name="Город")
    street = models.CharField(max_length=100, verbose_name="Улица")
    house_number = models.CharField(max_length=20, verbose_name="Номер дома")
    supplier = models.ForeignKey(
        'self', null=True, blank=True, on_delete=models.SET_NULL, related_name='clients', verbose_name="Поставщик"
    )
    debt = models.DecimalField(max_digits=10, decimal_places=2, default=0, verbose_name="Задолженность перед поставщиком")
    created_at = models.DateTimeField(default=timezone.now, verbose_name="Время создания")

    def __str__(self):
        return self.name

    @property
    def level(self):
        """
        Вычисляет уровень звена сети.
        Уровень = 0, если поставщика нет (завод), иначе рассчитывается как 1 + уровень поставщика.
        """
        if self.supplier is None:
            return 0  # Завод всегда на уровне 0
        return self.supplier.level + 1

    class Meta:
        verbose_name = "Звено сети"
        verbose_name_plural = "Звенья сети"


class Product(models.Model):
    """
    Представляет собой продукт в сети поставки электроники.
    """
    name = models.CharField(max_length=255, verbose_name="Название продукта")
    model = models.CharField(max_length=100, verbose_name="Модель продукта")
    release_date = models.DateField(verbose_name="Дата выхода на рынок")
    network_node = models.ForeignKey(NetworkNode, on_delete=models.CASCADE, related_name='products', verbose_name="Звено сети")

    def __str__(self):
        return f'{self.name} ({self.model})'

    class Meta:
        verbose_name = "Продукт"
        verbose_name_plural = "Продукты"
