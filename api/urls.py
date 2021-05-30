from django.urls import path
from api import views

app_name = "api"

urlpatterns = [
    path('usuario_list/', views.UsuarioList.as_view(), name ="usuario_list"),
    path('usuario_detail/<int:pk>/', views.UsuarioDetail.as_view(), name ="usuario_detail"),
]
