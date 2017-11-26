from django.db import models
from django.conf import settings

# Create your models here.
class library_profile(models.Model):
    username = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    library_id = models.CharField(max_length=50)
    library_password = models.CharField(max_length=50)

    def __str__(self):
        return "%s"%self.username

class user_barrow_books(models.Model):
    username = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    info = models.TextField(blank=True)

    def __str__(self):
        return  "%s"%self.username

class user_token(models.Model):
    username = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    token = models.CharField(max_length=100)

class server_api(models.Model):
    server_api = models.CharField(max_length=100, blank=True)