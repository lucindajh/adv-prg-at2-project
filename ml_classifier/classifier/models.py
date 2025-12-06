from django.db import models


# Create your models here.
class Prediction(models.Model):
    """Represents prediction metadata from prediction process"""
    predicted_at = models.DateTimeField(auto_now_add=True)
    user = models.CharField(max_length=30)
    imagenet_class = models.TextField(max_length=30)
    probability = models.DecimalField()
