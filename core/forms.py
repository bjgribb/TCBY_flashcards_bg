from django import forms
from django.forms import ModelForm
from core.models import Card, Deck
from django.core.exceptions import ValidationError
from django.utils.translation import ugettext_lazy as _

class NewCardForm(forms.Form):
    question = forms.CharField(max_length=500)
    answer = forms.CharField(max_length=500)
 
    def clean_question(self):
        data = self.cleaned_data['question']
            # https://docs.djangoproject.com/en/2.2/ref/forms/validation/
        
        # Check if flashcard already exists. 
        questions = []
        for card in Card.objects.all():
            questions.append(card.question.lower())

        if data.lower() in questions:
            raise ValidationError(_('Flashcard question already exists'))
            # https://docs.djangoproject.com/en/2.1/ref/exceptions/#validationerror
            # https://docs.djangoproject.com/en/2.1/ref/utils/#django.utils.translation.ugettext_lazy

        # Return the cleaned data.
        return data

class NewDeckForm(forms.Form):
    deck_name = forms.CharField(max_length=200)
 
    def clean_deck_name(self):
        data = self.cleaned_data['deck_name']
        
        # Check if flashcard already exists. 
        titles = []
        for deck in Deck.objects.all():
            titles.append(deck.title.lower())

        if data.lower() in titles:
            raise ValidationError(_('Deck name already exists'))
            # https://docs.djangoproject.com/en/2.1/ref/exceptions/#validationerror
            # https://docs.djangoproject.com/en/2.1/ref/utils/#django.utils.translation.ugettext_lazy

        # Return the cleaned data.
        return data





