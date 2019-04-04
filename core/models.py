from django.db import models
from django.urls import reverse
    # Used to generate URLs by reversing the URL patterns
from django.contrib.auth.models import User
    # Required to make use of 'User' class
from django.utils.text import slugify

# Create your models here.
class Kreator(models.Model):
    """Model representing a deck creator."""
    name = models.ForeignKey(User, on_delete=models.CASCADE)
    # https://docs.djangoproject.com/en/2.1/ref/models/fields/#foreign-key-arguments
    # Foreign Key used b/c Kreator of a deck can only be 1 User, but User can be Kreator of many decks
    slug = models.SlugField(unique=True, null=True, blank=True)

    class Meta:
        ordering = ['name']

    def save(self, *args, **kwargs):
        self.set_slug()
        super().save(*args, **kwargs)

    def set_slug(self):
        if self.slug:
            return
        base_slug = slugify(self.name.username)
        slug = base_slug
        n = 0
        while Kreator.objects.filter(slug=slug).count():
            n += 1
            slug = base_slug + "-" + str(n)
        self.slug =slug

    def get_absolute_url(self):
        """Returns the url to access a particular author instance."""
        return reverse('kreator-detail', args=[str(self.slug)])

    def __str__(self):
        """String for representing the Model object."""
        return self.name.username

class Category(models.Model):
    """Model representing a deck category."""
    name = models.CharField(max_length=200, help_text='Enter a deck category (e.g. Math, Geography, etc.)')
    slug = models.SlugField(unique=True, null=True, blank=True)

    class Meta:
        ordering = ['name']

    def save(self, *args, **kwargs):
        self.set_slug()
        super().save(*args, **kwargs)

    def set_slug(self):
        if self.slug:
            return
        base_slug = slugify(self.name)
        slug = base_slug
        n = 0
        while Category.objects.filter(slug=slug).count():
            n += 1
            slug = base_slug + "-" + str(n)
        self.slug =slug

    def get_absolute_url(self):
        """Returns the url to access a particular category instance."""
        return reverse('category-detail', args=[str(self.slug)])
    
    def __str__(self):
        """String for representing the Model object."""
        return self.name

class Quiz(models.Model):
    """Model representing each instance of a user quizzing themself."""
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    # Foreign Key used b/c a Quiz can only be taken by 1 User, but User can take many quizzes.
    total_score = models.IntegerField(null=True, blank=True)
    # https://docs.djangoproject.com/en/2.2/ref/models/fields/#integerfield
    deck = models.ForeignKey(to='Deck', on_delete=models.SET_NULL, null=True, blank=True, related_name='quiz')

class Deck(models.Model):
    """
    Model representing deck of flashcards
    """
    title = models.CharField(max_length=200, default="Deck")
    kreator = models.ForeignKey(to=Kreator, on_delete=models.SET_NULL, null=True, related_name='deck')
    users = models.ManyToManyField(to=User, related_name='deck_user')
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
    correct = models.BooleanField(blank=True, null=True, default=None)
    deck = models.ForeignKey(to=Deck, on_delete=models.SET_NULL, related_name='card', null=True, blank=True)

    def __str__(self):
        return self.question 
