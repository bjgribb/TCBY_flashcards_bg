from django.urls import path
from . import views

urlpatterns = [
      path('', views.index, name='index'),
      path('category/<slug:slug>', views.CategoryDetailView.as_view(), name='category-detail'),
      path('user_list/', views.user_list_view, name='user_list'),
      path('quiz/<slug:slug>', views.quiz_view, name='quiz-view')
      path('card/new/', views.CardCreate.as_view(), name='card_form'),
]
