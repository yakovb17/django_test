from django.db import models
from django.conf import settings
from .utils import generate_key

# Create your models here.


class Url(models.Model):
    url = models.CharField(max_length=500, null=False)
    key = models.CharField(max_length=100, unique=True, null=False)
    redirects_count = models.IntegerField(default=0)
