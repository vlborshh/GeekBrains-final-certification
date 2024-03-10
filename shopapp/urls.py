from django.urls import path
from . import views




app_name = 'shopapp'

urlpatterns = [

    path('', views.product_list, name='product_list'),
    # path('registration', views.registration, name='registration'),
    path('<slug:category_slug>/', views.product_list,
         name='product_list_by_category'),
    path('<int:id>/<slug:slug>/', views.product_detail,
         name='product_detail'),

]
