from django.urls import path
from rest_framework.urlpatterns import format_suffix_patterns
from api  import views

api_name = 'api'


urlpatterns = [
    path('lista_usuario', views.UsuarioListSet.as_view(), name ="lista_usuario"),
    path('detalles_usuario/<int:pk>', views.UsuarioDetailSet.as_view(), name ="detalles_usuario"),
    #path('usuario_detail/<int:pk>/', views.UsuarioDetail.as_view(), name ="usuario_detail"),
]
urlpatterns = format_suffix_patterns(urlpatterns)
