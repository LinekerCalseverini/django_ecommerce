from django.urls import path
from .views import Criar, Login, Logout

app_name = 'perfil'

urlpatterns = [
    path('', Criar.as_view(), name='criar'),
    path('login/', Login.as_view(), name='login'),
    path('logout/', Logout.as_view(), name='logout'),
]
