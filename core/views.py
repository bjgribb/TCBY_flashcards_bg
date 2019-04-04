from django.shortcuts import render
from core.models import Card, Deck, User, Category

# Create your views here.

def index(request):
    """
    View function for index view of site.
    """
    num_decks = Deck.objects.all().count()
    decks = Deck.objects.all()
    categories = Category.objects.all()
    user = User.objects.all()


    context = {
        'num_decks': num_decks,
        'decks': decks,
        'categories': categories,
        'user': user,
    }
    return render(request, 'index.html', context=context)
