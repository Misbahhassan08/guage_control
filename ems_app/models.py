# models.py
from django.db import models

class MetaData(models.Model):
    Value = models.FloatField(blank=True, null=True)
    Velocity = models.FloatField(blank=True, null=True)
    Flow = models.FloatField(blank=True, null=True)
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"MetaData at {self.timestamp}"
