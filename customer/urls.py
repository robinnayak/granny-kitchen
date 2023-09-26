from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static

app_name ='customer'

urlpatterns = [
    path("",views.customer_profile,name="customer"),
    path("customer-update/<str:pk>/",views.customer_update,name="customer_update"),
    path("customer-delete/<str:pk>/",views.customer_delete,name="customer_delete"),
    path("create-order/<str:pk>/",views.create_or_get_order,name='createorder'),
    path('momprofile/<str:pk>/',views.MomProfileView,name="momprofile"),
    path('momprofile/',views.MomsProfileView,name="mom-profile"),
    path('order-view/',views.OrderView,name="orderview"),
    path('buy/<str:pk>/',views.buy_order,name='buy'),
    path('delete-item/<str:pk>/',views.order_item_delete,name="deleteitem"),
    path('delete-order/<str:pk>/',views.order_delete,name="delete_order"),
    path('notify-customer/',views.notify_purchase_to_customer,name='notify_customer'),
    path('payment/<str:pk>/',views.accept_order_payment,name='accept-order-payment'),
    path('recipt/',views.recipt,name='recipt'),
]
