from django.db import models
from django.urls import reverse

# Модели Category и Product. Модель Category состоит из поля name и
# уникального поля slug
class Category(models.Model):
    name = models.CharField(max_length=100)
    slug = models.SlugField(max_length=100, unique=True)

    class Meta:
        ordering = ['name']
        indexes = [models.Index(fields=['name']),]
        verbose_name = 'category'
        verbose_name_plural = 'categories'

    def get_absolute_url(self):
        return reverse('shopapp:product_list_by_category', args=[self.slug])

    def __str__(self):
        return self.name

    # Поля модели Product:
    #     category: внешний ключ(ForeignKey) к модели Category.Это взаимосвязь
    #     один - ко - многим: товар принадлежит одной категории, а категория
    #     содержит несколько товаров;
    #     name: название товара;
    #     slug: слаг этого товара для создания красивых URL - адресов;
    #     image: опциональное изображение товара;
    #     description: опциональное описание товара;
    #     price: в этом поле используется тип Python decimal.Decimal, чтобы хранить
    #     десятичное число фиксированной точности.Максимальное количество цифр(включая
    #     десятичные разряды) устанавливается с помощью атрибута max_digits, а десятичных
    #     разрядов – с помощью атрибута  decimal_places;
    #     available: булево значение, указывающее на наличие или отсутствие товара.Оно
    #     будет использоваться для активирования / деактивирования товара в каталоге;
    #     created: в этом поле хранится информация о дате / времени создания объекта;
    #     updated: в этом поле хранится информация о дате / времени обновления объекта


class Product(models.Model):
    category = models.ForeignKey(Category,
                                 related_name='products',
                                 on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    slug = models.SlugField(max_length=100)
    image = models.ImageField(upload_to='products/%Y/%m/%d',
                              blank=True)
    description = models.TextField(blank=True)
    price = models.DecimalField(max_digits=10,
                                decimal_places=2)
    available = models.BooleanField(default=True)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['name']
        indexes = [
            models.Index(fields=['id', 'slug']),
            models.Index(fields=['name']),
            models.Index(fields=['-created']),
        ]
    def get_absolute_url(self):
        return reverse('shopapp:product_detail', args=[self.id, self.slug])

    def __str__(self):
        return self.name

# Create your models here.
