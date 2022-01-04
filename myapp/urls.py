from django.urls import path, include
from myapp import views

app_name = "myapp"

urlpatterns = [
    path('', views.index, name="index"),
    path('create/', views.create, name="create"),
    path('read/<id>/', views.read, name ="read"),
    path('update/<id>/',views.update, name="update"),
    path('delete/', views.delete, name="delete"),
]