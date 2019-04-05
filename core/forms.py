from django import forms
from core.models import Card, Deck
from django.core.exceptions import ValidationError
from django.utils.translation import ugettext_lazy as _

class NewCardForm(forms.Form):
    question = forms.CharField(max_length=500, help_text="Enter a question")
    answer = forms.CharField(max_length=500, help_text="Enter the answer")
 
    def clean_question(self):
        data = self.cleaned_data['question']
            # https://docs.djangoproject.com/en/2.2/ref/forms/validation/
        
        # Check if flashcard already exists. 
        if data in Card.objects.all():
            raise ValidationError(_('Flashcard question already exists'))
            # https://docs.djangoproject.com/en/2.1/ref/exceptions/#validationerror
            # https://docs.djangoproject.com/en/2.1/ref/utils/#django.utils.translation.ugettext_lazy

        # Return the cleaned data.
        return data



