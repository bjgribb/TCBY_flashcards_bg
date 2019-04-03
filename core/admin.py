from django.contrib import admin
from core.models import Deck, Card
# Register your models here.

@admin.register(Deck)
class DeckAdmin(admin.ModelAdmin):
    list_display = ('title', 'kreator', 'public')

@admin.register(Card)
class CardAdmin(admin.ModelAdmin):
    list_display = ('question', 'answer', 'deck')
    