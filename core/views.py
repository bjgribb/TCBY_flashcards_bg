from django.shortcuts import render
from core.models import Category, Deck
from django.views import generic

# Create your views here.

def index(request):
    """View function for home page of site."""
    categories = Category.objects.all()
    decks = Deck.objects.all()

    context = {
       'categories': categories,
       'decks': decks
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