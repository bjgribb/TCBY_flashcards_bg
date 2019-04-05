from django.shortcuts import render
from core.models import Category, Deck, User, Card, Quiz
from django.views import generic
from django.shortcuts import render, get_object_or_404

# Create your views here.

def index(request):
    """View function for home page of site."""
    categories = Category.objects.all()
    decks = Deck.objects.all()

    context = {
<<<<<<< Updated upstream
       'categories': categories,
       'decks': decks
=======
        'num_decks': num_decks,
        'decks': decks,
        'categories': categories,
        'user': user,
>>>>>>> Stashed changes
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

def quiz_view(request, slug):
    """
    View defining the quiz/game portion of the flashcard app.
    """
    categories = Category.objects.all()
    user = User.objects.all()
    cards = Card.objects.all()
    quiz = get_object_or_404(Quiz, slug=slug)

    context = {
        'categories': categories,
        'user': user,
        'cards': cards,
        'quiz': quiz,
    }

    return render(request, 'core/quiz.html', context=context)
