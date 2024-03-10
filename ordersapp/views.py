from django.shortcuts import render, redirect
from django.urls import reverse
from .models import OrderItem, ClientOrder, Order
from .forms import OrderCreateForm
from cartapp.cart import Cart
from .tasks import order_created
from django.http import HttpResponse

def order_create(request):
    if not request.user.is_authenticated:
        return redirect('login', permanent=True)
    cart = Cart(request)
    if request.method == 'POST':
        form = OrderCreateForm(request.POST)
        if form.is_valid():
            order = form.save()
            for item in cart:
                OrderItem.objects.create(order=order,
                                         product=item['product'],
                                         price=item['price'],
                                         quantity=item['quantity'])
            # очищаем корзину
            cart.clear()
            order_created.delay(order.id) # запуск асинхронного задания
            request.session['order_id'] = order.id # задать заказ в сеансе
            # context = {'order': order}

            return redirect(reverse('payment:process'))
            #return render(request, 'ordersapp/order/created.html', context)
    else:
        form = OrderCreateForm()
        context = {'cart': cart, 'form': form}
        return render(request,'ordersapp/order/create.html', context)

def order_list(request):
    if not request.user.is_authenticated:
        return redirect('login', permanent=True)
    # получаем ИД авторизованного пользователя
    user_id = request.user.id
    # получаем все данные из ClientOrder
    client = ClientOrder.objects.all()
    orders_client = []
    # в orders_client получаем ИД заказов которые создал авторизованный пользователь
    for item in client:
        if item.order_id_client == user_id:
            orders_client.append(item.order_id_order)
    # получаем все заказы
    orders = OrderItem.objects.all()
    client_info_list = []
    client_order_list = []
    # проходим по списку заказов авторизованного пользователя
    for order_client in orders_client:
        # здесь сохраняем: на кого оформлен заказ
        client_info_list.append(Order.objects.get(pk=order_client))
        total_price = 0
        # проходим по orders для получения списка товаров авторизованного пользователя
        for order in orders:
            if order.order_id == order_client:
                client_order_list.append(order)
                total_price = order.price * order.quantity

    context = {'client_order_list': client_order_list, 'total_price': total_price}
    return render(request,'ordersapp/order/show_order.html', context)


















# Create your views here.
