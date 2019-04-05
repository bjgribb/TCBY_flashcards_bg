from flashcard.settings import *

import django_heroku

DEBUG = True

django_heroku.settings(locals())
