from django.urls import path
from Clinica import views

app_name = "Clinica"

urlpatterns = [
    path('index',views.Index.as_view(),name="index"),
    path('logout',views.Logout.as_view(), name="logout"),
]
