from django.shortcuts import render, get_object_or_404
from core.models import Deck

# Create your views here.

def index(request):
    decks = Deck.objects.all()

    context = {
        'decks': decks,
    }
    return render(request, 'index.html', context=context)

def deck_list_view(request, slug):
    decks = get_object_or_404(Deck, slug=slug)

    context = {
        'decks':decks
    }

    return render(request, 'core/deck_list.html', context=context)
