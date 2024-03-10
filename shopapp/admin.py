from django.contrib import admin
from .models import Category, Product


# prepopulated_fields - указываем поля, значение которых устанавливается
# автоматически с использованием значения других полей.
# list_editable используется для того, чтобы задать поля, которые можно редактировать,
# находясь на странице отображения списка на сайте администрирования. Такой подход
# позволит редактировать несколько строк одновременно. Любое поле в list_editable также
# должно быть указано в атрибуте list_display, поскольку редактировать можно только
# отображаемые поля.

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'slug']
    prepopulated_fields = {'slug': ('name',)}


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ['name', 'slug', 'price',
                    'available', 'created', 'updated']
    list_filter = ['available', 'created', 'updated']
    list_editable = ['price', 'available']
    prepopulated_fields = {'slug': ('name',)}

# Register your models here.
