from django.shortcuts import render, get_object_or_404
from core.models import Deck, User, Category

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

def deck_detail_view(request):
    pass

def user_list_view(request):
    decks = Deck.objects.all()
    users = User.objects.all()

    context = {
        'decks': decks,
        'users': users,
    }

    return render(request, 'core/user_list.html', context=context)
