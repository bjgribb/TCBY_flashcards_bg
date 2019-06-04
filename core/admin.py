from django.contrib import admin
from core.models import Deck, Card, Quiz
# Register your models here.

@admin.register(Deck)
class DeckAdmin(admin.ModelAdmin):
    list_display = ('title', 'public', 'display_card')

@admin.register(Card)
class CardAdmin(admin.ModelAdmin):
    list_display = ('question', 'answer', 'display_deck')
    
@admin.register(Quiz)
class QuizAdmin(admin.ModelAdmin):
    pass
