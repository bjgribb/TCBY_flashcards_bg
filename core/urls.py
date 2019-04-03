from django.urls import path
from . import views

urlpatterns = [
      path('', views.index, name='index'),
      path('/deck_list/<slug:slug>/', views.deck_list_view, name='deck_list')
]
