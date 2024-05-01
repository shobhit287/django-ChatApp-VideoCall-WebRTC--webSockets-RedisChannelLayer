from django.urls import path
from django.conf import settings
from . import views
from django.conf.urls.static import static

urlpatterns = [
    path('',views.index,name="index"),
    path('<str:slug>',views.index,name="demo"),
    path('signup/form',views.signup,name="signup"),
    path('login/form',views.login_user,name="login"),
    path('logout/user',views.logout_user,name="logout"),
    path('video/call',views.video_call,name="logout"),
]+ static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)