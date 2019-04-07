from core.models import Category, Deck, User, Card, Quiz
from core.forms import NewCardForm, NewDeckForm
from django.views import generic
from django.shortcuts import render, get_object_or_404
from django.http import JsonResponse
from django.core import serializers
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.decorators.http import require_http_methods
from django.views.generic.edit import CreateView
from django.http import HttpResponseRedirect
from django.urls import reverse
import json
from django import forms

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
    user_created_decks = Deck.objects.filter(creator=request.user)

    context = {
        'decks': decks,
        'users': users,
        'user_created_decks': user_created_decks,
    }

    return render(request, 'core/user_list.html', context=context)

def quiz_view(request, slug):
    """
    View defining the quiz/game portion of the flashcard app.
    """
    categories = Category.objects.all()
    user = User.objects.all()
    cards = Card.objects.all()
    quiz = Quiz.objects.all()
    # get the slug for the deck, because the quiz is essentially 
    ####### Deck Detail view #######
    deck = get_object_or_404(Deck, slug=slug)

    context = {
        'categories': categories,
        'user': user,
        'cards': cards,
        'quiz': quiz,
        'deck': deck,
    }

    return render(request, 'core/quiz.html', context=context)

def new_card(request):
    new_card_form = NewCardForm()
    if request.method == 'POST':
        new_card_form = NewCardForm(data=request.POST)

        if new_card_form.is_valid():
            # https://docs.djangoproject.com/en/2.2/ref/forms/api/#django.forms.Form.is_valid
            question = request.POST.get('question', '')
                # https://docs.djangoproject.com/en/2.1/ref/request-response/#django.http.HttpRequest.POST
                # https://docs.djangoproject.com/en/2.1/ref/request-response/#django.http.QueryDict.get
            answer = request.POST.get('answer', '')
            query_dict_copy = request.POST.copy()
                # https://docs.djangoproject.com/en/2.2/ref/request-response/#django.http.QueryDict
            deck_keys = query_dict_copy.pop('existing_decks')
                # https://docs.djangoproject.com/en/2.2/ref/request-response/#django.http.QueryDict.pop
            card = Card.objects.create(
                question=question,
                answer=answer,
            )
            for key in deck_keys:
                card.decks.add(Deck.objects.get(pk=key))
            card.save()

            return HttpResponseRedirect(reverse('user_list'))
    else:
        new_card_form = NewCardForm()

    return render(request, 'core/card_form.html', {"form": new_card_form})

def new_deck(request):
    new_deck_form = NewDeckForm()
    if request.method == 'POST':
        new_deck_form = NewDeckForm(request.POST)
        if new_deck_form.is_valid():
            title = request.POST.get('deck_name', '')
            query_dict_copy = request.POST.copy()
            category_keys = query_dict_copy.pop('categories')
            card_keys = query_dict_copy.pop('existing_cards')
            deck = Deck.objects.create(
                title=title,
                creator=request.user,
            )
            for key in category_keys:
                deck.categories.add(Category.objects.get(pk=key))

            deck.save()

            for key in card_keys:
                card = Card.objects.get(pk=key)
                card.decks.add(deck)
                card.save()
            
            return HttpResponseRedirect(reverse('user_list'))
    else:
        new_deck_form = NewDeckForm()

    return render(request, 'core/deck_form.html', {"form": new_deck_form})

def get_card_data(request, slug):
    deck = get_object_or_404(Deck, slug=slug)
    cards = deck.card.all()
    return JsonResponse({'deck_cards': [(card.question, card.answer) for card in cards]})
