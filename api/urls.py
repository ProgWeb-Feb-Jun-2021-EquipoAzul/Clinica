from django.urls import path
from rest_framework.urlpatterns import format_suffix_patterns
from api  import views

api_name = 'api'


urlpatterns = [
    path('crear_usuario', views.UsuarioCreateSet.as_view(), name ="crear_usuario"),
    path('lista_usuario', views.UsuarioListSet.as_view(), name ="lista_usuario"),
    path('detalles_usuario/<int:pk>/', views.UsuarioDetailSet.as_view(), name ="detalles_usuario"),
    path('editar_usuario/<int:pk>/', views.UsuarioUpdateSet.as_view(), name ="editar_usuario"),
    path('eliminar_usuario/<int:pk>/', views.UsuarioDeleteSet.as_view(), name ="eliminar_usuario"),
]
urlpatterns = format_suffix_patterns(urlpatterns)
