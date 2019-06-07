from django.db import models
from django.urls import reverse
from django.contrib.auth.models import User
from django.utils.text import slugify

# Create your models here.

class Quiz(models.Model):
    """Model representing each instance of a user quizzing themself."""
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    deck = models.ForeignKey(to='Deck', on_delete=models.SET_NULL, null=True, blank=True, related_name='quiz')
    

class Deck(models.Model):
    """
    Model representing deck of flashcards
    """
    title = models.CharField(max_length=200, unique=True)
    creator = models.ForeignKey(to=User, on_delete=models.SET_NULL, null=True, related_name='deck')
    public = models.BooleanField(default=False, editable=True)
    slug = models.SlugField(unique=True, null=True, blank=True)

    def set_slug(self):
        """
        Creates unique slug for every deck
        """
        if self.slug:
            return

        base_slug = slugify(self.title)
        slug = base_slug
        n = 0

        while Deck.objects.filter(slug=slug).count():
            n += 1
            slug = base_slug + '-' + str(n)

        self.slug = slug

    def save(self, *args, **kwargs):
        """
        Hides slug field in admin, saves slug to use in url
        """
        self.set_slug()
        super().save(*args, **kwargs)

    def get_absolute_url(self):
        # need to create view and template 
        return reverse('quiz-view', args=[(self.slug)])
    
    def __str__(self):
        return self.title

    def display_card(self):
        """Create a string for Cards. This is required to display Cards in Admin."""
        return ', '.join(card.question for card in self.card.all()[:10])

class Card(models.Model):
    question = models.CharField(max_length=500)
    answer = models.CharField(max_length=500)
    decks = models.ManyToManyField(to=Deck, related_name='card', blank=True)

    def display_deck(self):
        """Create a string for Decks. This is required to display Decks in Admin."""
        return ', '.join(deck.title for deck in self.decks.all()[:3])
    
    def __str__(self):
        return self.question 

    def get_absolute_url(self):
        """Returns the url to access a detail record for this card."""
        return reverse('index')
