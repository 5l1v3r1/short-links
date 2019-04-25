from django.urls import path, include
from django.contrib.auth.views import LoginView, LogoutView

from ..users import views

app_name = 'users'

urlpatterns = [
    path('signup/', views.SignUp.as_view(redirect_authenticated_user=True), name='signup'),
    path('login/', LoginView.as_view(redirect_authenticated_user=True), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
]
