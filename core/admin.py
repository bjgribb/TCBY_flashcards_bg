from django.contrib import admin
from core.models import Kreator, Category, Quiz

# Register your models here.
@admin.register(Kreator)
class KreatorAdmin(admin.ModelAdmin):
   list_display = ('name',)

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
   list_display = ('name',)