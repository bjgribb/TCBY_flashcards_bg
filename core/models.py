from django.db import models
from django.urls import reverse
    # Used to generate URLs by reversing the URL patterns
from django.contrib.auth.models import User
    # Required to make use of 'User' class
from django.utils.text import slugify

# Create your models here.

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
    creator = models.ForeignKey(to=User, on_delete=models.SET_NULL, null=True, related_name='deck')
    categories = models.ManyToManyField(to='Category', related_name='deck')
    public = models.BooleanField(default=True, editable=True)
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
        # with 'deck-detail' name to match
        return reverse('deck-detail', args=[(self.slug)])
    
    def __str__(self):
        return self.title

class Card(models.Model):
    question = models.CharField(max_length=500)
    answer = models.CharField(max_length=500)
    correct = models.BooleanField(blank=True, null=True, default=None)
        # https://docs.djangoproject.com/en/2.1/ref/models/fields/#booleanfield
    decks = models.ManyToManyField(to=Deck, related_name='card', blank=True)

    def display_deck(self):
        """Create a string for Decks. This is required to display Decks in Admin."""
        return ', '.join(deck.name for deck in self.decks.all()[:3])
            # str.join(iterable) --> https://docs.python.org/3.7/library/stdtypes.html?highlight=join#str.join
            # 1st three '[:3]' deck items in the 'self.deck.all()' for a 'Card' object will be joined separated by a comma ', '
    

    def __str__(self):
        return self.question

    


# started by running '$ ./manage.py makemigrations --empty core'

from django.db import migrations
from django.conf import settings
import os.path
import csv
from django.core.files import File
from django.utils.text import slugify
from django.contrib.auth.models import User

def load_decks_data(apps, schema_editor):
    """
    Read a CSV file full of decks and insert them into the database
    """
    Deck = apps.get_model('core', 'Deck')
        # https://docs.djangoproject.com/en/2.1/ref/applications/#application-registry
        # 'apps.get_model(app_label, model_name, require_ready=True)' returns the 'Deck' model in the 'core' app
    Category = apps.get_model('core', 'Category')
    Kreator = apps.get_model('core', 'Kreator')
    User = apps.get_model('auth', 'User')

    datapath = os.path.join(settings.BASE_DIR, 'initial_data')
        # data to be read is stored in the 'initial_data' directory
    datafile = os.path.join(datapath, 'decks.csv')
        # data file to be read is named 'decks.csv'
    Deck.objects.all().delete()
        # delete all existing 'Deck' objects in the database
    Category.objects.all().delete()
        # delete all existing 'Category' objects in the database

    with open(datafile) as file: 
        reader = csv.DictReader(file)
            # https://docs.python.org/3.7/library/csv.html?highlight=csv%20dictreader#csv.DictReader
            # 'csv.DictReader' creates an object that operates like a regular reader but maps the information in each row to an 'OrderedDict' whose keys are given by the optional fieldnames parameter
            # if fieldnames is omitted (as we do here), the values in the first row of the file will be used as the fieldnames
        for row in reader:
            deck_title = row['title']
            if Deck.objects.filter(title=deck_title).count():
                continue
                    # if a post with that title already exists, then skip the rest of the statements in the loop and 'continue' on to the next iteration of the loop
                    # prevents duplicate posts
            if User.objects.filter(username=row['kreator']).count():
                kreator = User.objects.filter(username=row['kreator'])[0]
                # if Kreator.objects.filter(name=user).count():
                #     kreator = Kreator.objects.filter(name=user)[0]
                # else:
                #     kreator, _ = Kreator.objects.get_or_create(name=user)
            else:
                user, _ = User.objects.get_or_create(username=row['kreator'])
                user.save()
                kreator, _ = Kreator.objects.get_or_create(name=user)
               
            kreator.save()

            if not row['categories']:
                categories, _ = Category.objects.get_or_create(name='No Category', slug="no-category")
                categories = [categories]
            else:
                categories = []
                category_list = [category.strip() for category in row['categories'].split('/')]
                for category in category_list:
                    new_category, _ = Category.objects.get_or_create(name=category, slug=slugify(category))
                    categories.append(new_category)

            deck = Deck.objects.create(
                title=row['title'],
                kreator=kreator,
            )
            for category in categories:
                deck.categories.add(category)
            deck.save()

            if row['slug'] == '':
                base_slug = slugify(row['title'])
                slug = base_slug
                n = 0
                while Deck.objects.filter(slug=slug).count():
                    n += 1
                    slug = base_slug + "-" + str(n)
                deck.slug = slug[:50]
            deck.save()