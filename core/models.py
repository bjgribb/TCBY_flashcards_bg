from django.db import models
from django.contrib.auth import get_user_model
from django.utils.text import slugify
from django.urls import reverse

# Create your models here.
User = get_user_model()

class Deck(models.Model):
    """
    Model representing deck of flashcards
    """
    title = models.CharField(max_length=200, default="Deck")
    kreator = models.ForeignKey(to='User', on_delete=models.SET_NULL, related_name='deck')
    users = models.ManyToManyField(to='User', related_name='deck')
    quiz = models.ForeignKey(to='Quiz', on_delete=models.DO_NOTHING, related_name='deck')
    categories = models.ManyToManyField(to='Category', related_name='deck')
    public = models.BooleanField(default=True, editable=True)
    slug = models.CharField(max_length=100, unique=True, default='oops')

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
        # with 'deck-detail' name to match
        return reverse('deck-detail', args=[(self.slug)])
    
    def __str__(self):
        return self.title

class Card(models.Model):
    question = models.CharField(max_length=200)
    answer = models.CharField(max_length=500)
    correct = models.BooleanField(blank=True, null=True, default=False)
    deck = models.ForeignKey(to=Deck, on_delete=models.SET_NULL, related_name='card')

def __str__(self):
    return self.question
