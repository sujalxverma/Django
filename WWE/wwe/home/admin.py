from django.contrib import admin

# Register your models here.
# Import the model you want to register
# For example, if you have a model named Home in home/models.py, you would do
# from home.models import Home
from .models import Home  # or your model name
admin.site.register(Home)
