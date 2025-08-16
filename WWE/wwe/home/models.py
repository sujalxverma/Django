from django.db import models

# Create your models here.


# creating the model to take input from users about WWE wrestlers.

class Home(models.Model):
    
    username = models.CharField(max_length = 100)
    email = models.EmailField()
    wrestler_name = models.CharField(max_length = 100)
    wrestler_image = models.ImageField(upload_to='wrestler_images/',blank=True, null=True)
    wrestler_description = models.TextField()
    
    def __str__(self):
        return self.username
    
    