from django import forms
from django.forms import ModelForm
from core.models import Card, Deck, Category
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
    categories = forms.ModelMultipleChoiceField(queryset=Category.objects.all())
        # https://docs.djangoproject.com/en/2.2/ref/forms/fields/#fields-which-handle-relationships

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
    
    # Overriding __init__ here allows us to provide initial
    # data for 'categories' field
    def __init__(self, *args, **kwargs):
        # Only in case we build the form from an instance
        # (otherwise, 'categories' list should be empty)
        if kwargs.get('instance'):
            # We get the 'initial' keyword argument or initialize it
            # as a dict if it didn't exist.                
            initial = kwargs.setdefault('initial', {})
            # The widget for a ModelMultipleChoiceField expects
            # a list of primary key for the selected data.
            initial['categories'] = [t.pk for t in kwargs['instance'].category_set.all()]

        forms.Form.__init__(self, *args, **kwargs)

    # Overriding save allows us to process the value of 'categories' field    
    def save(self, commit=True):
        # Get the unsave Pizza instance
        instance = forms.Form.save(self, False)

        # Prepare a 'save_m2m' method for the form,
        old_save_m2m = self.save_m2m
        def save_m2m():
           old_save_m2m()
           # This is where we actually link the deck with categories
           instance.category_set.clear()
           instance.category_set.add(*self.cleaned_data['categories'])
        self.save_m2m = save_m2m

        # Do we need to save all changes now?
        # if commit:
        instance.save()
        self.save_m2m()

        return instance





