from django.shortcuts import render, get_object_or_404
from core.models import Deck, User

# Create your views here.

def index(request):
    return render(request, 'index.html')


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
