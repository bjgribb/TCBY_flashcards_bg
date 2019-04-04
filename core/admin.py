from django.contrib import admin
from core.models import Kreator, Category, Deck, Card

# Register your models here.
class DeckInline(admin.TabularInline):
    model = Deck
    
@admin.register(Kreator)
class KreatorAdmin(admin.ModelAdmin):
    list_display = ('name',)
    inlines = [
        DeckInline,
    ]

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name',)
    exclude = ('slug',)

@admin.register(Deck)
class DeckAdmin(admin.ModelAdmin):
    list_display = ('title', 'kreator', 'public')
    exclude = ('slug',)
   

@admin.register(Card)
class CardAdmin(admin.ModelAdmin):
    list_display = ('question', 'answer', 'deck')
    
