from decimal import Decimal
from django.conf import settings
from shopapp.models import Product

class Cart:
    def __init__(self, request):
        '''
        Инициализировать корзину
        '''
        self.session = request.session
        cart = self.session.get(settings.CART_SESSION_ID)
        # сохраняем пустую корзину в сеансе
        if not cart:
            cart = self.session[settings.CART_SESSION_ID] = {}
        self.cart = cart

    def add(self, product, quantity=1, override_quantity=False):
        '''
        Добавляем товар в корзину или изменяем его количество.
        '''
        product_id = str(product.id)
        if product_id not in self.cart:
            self.cart[product_id] = {'quantity': 0, 'price': str(product.price)}
        if override_quantity:
            self.cart[product_id]['quantity'] = quantity
        else:
            self.cart[product_id]['quantity'] += quantity
        self.save()

    def save(self):
        self.session.modified = True

    def remove(self, product):
        '''
            Удаление товара из корзины
        '''
        product_id = str(product.id)
        if product_id in self.cart:
            del self.cart[product_id]
            self.save()

    def __iter__(self):
        '''
        Прокручиваем позиции в корзине в цикле и получаем товары из БД
        '''

        product_ids = self.cart.keys()
        products = Product.objects.filter(id__in=product_ids)
        cart = self.cart.copy()
        for product in products:
            cart[str(product.id)]['product'] = product
        for item in cart.values():
            item['price'] = Decimal(item['price'])
            item['total_price'] = item['price'] * item['quantity']
            yield item

    def __len__(self):
        '''
        Вычисляем количество товарных позиций в корзине
        '''
        return sum(item['quantity'] for item in self.cart.values())

    def get_total_price(self):
        '''
        Рассчитываем общую стоимость товаров в корзине
        '''
        return sum(Decimal(item['price']) * item['quantity'] for item in self.cart.values())

    def clear(self):
        del self.session[settings.CART_SESSION_ID]
        self.save()
