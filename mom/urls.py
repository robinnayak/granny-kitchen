
from django.urls import path
from . import views
from validations.views import LoginPage,Logout
app_name = 'moms'

urlpatterns = [
    path("",views.HomeView,name="home"),
    
    path("product/<str:pk>/",views.ProductView,name='product'),
    path("product-view/",views.ProductViewPage,name='productview'),

    path('profile/',views.ProfileView,name="profile"),
    path('update-profile/<str:pk>/',views.ProfileUpdateView,name='updateprofile'),
    path('delete-profile/',views.ProfileDelete,name="deleteprofile"),
    
    path("menu/",views.CreateMenu,name="menu"),
    path("menu-update/<str:pk>/",views.MenuUpdateView,name="menuupdate"),
    path("menu-delete/<str:pk>/",views.MenuDeleteView,name="menudelete"),

    path('menuitem/',views.createMenuItem,name='menuitems'),
    path('menuview/<str:mom_id>/item/<str:menu_id>/',views.MenuItemView,name='menuview'),
    path('itemupdate/<str:pk>/',views.MenuItemUpdateView,name='itemupdate'),
    path('itemdelete/<str:pk>/',views.MenuItemDeleteView,name='itemdelete'),
    
    path('notify-mom/',views.notify_purchase_to_mom,name='notify_mom'),
    path('order-accept/<str:pk>/',views.order_accept,name="order_accept"),
    
    path('mom-view/',views.mom_view,name="mom_view"),
    
    path("login/",LoginPage,name="login"),
    path("logout/",Logout,name="logout"),
    
]

 