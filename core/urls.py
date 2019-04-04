from django.urls import path
from . import views

urlpatterns = [
      path('', views.index, name='index'),
      path('user_list/', views.user_list_view, name='user_list')
]
