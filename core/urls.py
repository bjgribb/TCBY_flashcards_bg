from django.urls import path
from . import views

urlpatterns = [
      path('', views.index, name='index'),
      path('category/<slug:slug>', views.CategoryDetailView.as_view(), name='category_detail'),
      path('user_list/', views.user_list_view, name='user_list'),
      path('quiz/<slug:slug>', views.quiz_view, name='quiz-view'),
      # path('get_cards/', views.get_cards, name='get_cards'),
      path('quiz/<slug:slug>/get_card_data/', views.get_card_data, name='get_card_data'),
      path('quiz/<slug:slug>/flashcards/', views.quiz_play, name='quiz_play')
      path('card/new/', views.CardCreate.as_view(), name='card_form'),
]
