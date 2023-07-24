from django.db import models
from django.contrib.auth.models import User
from PIL import Image

from club.models import Club


# Create your models here.

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    bio = models.CharField(max_length=200)
    profile_pic = models.ImageField(default='default.jpg', upload_to='profile_pics')
    is_teacher = models.BooleanField(default=False)
    club = models.ForeignKey(Club, on_delete=models.CASCADE, default='1')

    def __str__(self):
        return self.user.username + ' Profile'

    def set_club(self, club):
        self.club = club

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)

        img = Image.open(self.profile_pic.path)
        if img.height > 100 or img.width > 100:
            output_size = (200, 200)
            img.thumbnail(output_size)
            img.save(self.profile_pic.path)
