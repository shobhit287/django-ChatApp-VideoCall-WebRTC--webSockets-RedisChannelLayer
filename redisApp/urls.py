from django.urls import path
from . import views

urlpatterns = [
    path('',views.index,name="index"),
    path('<str:slug>',views.index,name="demo"),
    path('signup/form',views.signup,name="signup"),
    path('login/form',views.login_user,name="login"),
    path('logout/user',views.logout_user,name="logout"),
]