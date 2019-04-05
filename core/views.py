from django.shortcuts import render
from core.models import Category, Deck, User
from django.views import generic
from django.shortcuts import render, get_object_or_404

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
    # Render the HTML template index.html with the data in the context variable
    return render(request, 'index.html', context=context)

class CategoryDetailView(generic.DetailView):
    """View class for category page of site."""
    model = Category

    def get_context_data(self, **kwargs):
        # Call the base implementation first to get the context
        context = super(CategoryDetailView, self).get_context_data(**kwargs)
        # Create any data and add it to the context
        context['decks'] = Deck.objects.all()
        return context


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
