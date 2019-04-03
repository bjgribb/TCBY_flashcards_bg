from django.contrib import admin
from core.models import Kreator, Category, Deck, Card, Quiz

# Register your models here.
@admin.register(Kreator)
class KreatorAdmin(admin.ModelAdmin):
   list_display = ('name',)

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
   list_display = ('name',)
from core.models import Deck, Card

@admin.register(Deck)
class DeckAdmin(admin.ModelAdmin):
    list_display = ('title', 'kreator', 'public')

@admin.register(Card)
class CardAdmin(admin.ModelAdmin):
    list_display = ('question', 'answer', 'deck')
    
@admin.register(Quiz)
class QuizAdmin(admin.ModelAdmin):
   pass
