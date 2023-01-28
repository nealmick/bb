from django.db import models
from django.contrib.auth.models import User
from PIL import Image
# Create your models here.

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    image = models.ImageField(default='default.jpg', upload_to='profile_pics')
    predictions = models.IntegerField(default=0)
    correct = models.IntegerField(default=0)
    loss = models.DecimalField(decimal_places=4, max_digits=10, default=0)
    gain = models.DecimalField(decimal_places=4, max_digits=10, default=0)
    
    def __str__(self):
        return f'{self.user.username} Profile'
    def save(self, *args, **kawrgs):
        super().save(*args, **kawrgs)
        img = Image.open(self.image.path)
        if img.height > 300 or img.width > 300:
            output_size = (300,300)
            img.thumbnail(output_size)
            img.save(self.image.path)
