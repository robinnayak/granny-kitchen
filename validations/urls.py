from django.urls import path
from . import views


app_name = 'register'

urlpatterns = [
    path("",views.Register,name="register"),
    # path("login/",views.LoginPage,name="login"),
    path("customer-register/",views.CustomerRegister,name="customerregister"),
    # path("logout/",views.Logout,name="logout"),

]

