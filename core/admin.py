from django.contrib import admin
from core.models import Kreator, Category, Deck, Card

# Register your models here.
@admin.register(Kreator)
class KreatorAdmin(admin.ModelAdmin):
   list_display = ('name',)

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
   list_display = ('name',)

@admin.register(Deck)
class DeckAdmin(admin.ModelAdmin):
    list_display = ('title', 'kreator', 'public')

@admin.register(Card)
class CardAdmin(admin.ModelAdmin):
    list_display = ('question', 'answer', 'display_deck')
      # 4/4/2019 added 'display_deck' since deck was changed to a M2M field
    
