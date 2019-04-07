from django.contrib import admin
from core.models import Category, Deck, Card, Quiz
# Register your models here.

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name','display_deck')

@admin.register(Deck)
class DeckAdmin(admin.ModelAdmin):
    list_display = ('title', 'public', 'display_card')

@admin.register(Card)
class CardAdmin(admin.ModelAdmin):
    list_display = ('question', 'answer', 'display_deck')
      # 4/4/2019 added 'display_deck' since deck was changed to a M2M field
    
@admin.register(Quiz)
class QuizAdmin(admin.ModelAdmin):
    pass
