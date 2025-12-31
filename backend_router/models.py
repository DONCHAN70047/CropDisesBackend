# backend_router/models.py
from django.db import models

class DiseaseDetection(models.Model):
    disease_name = models.CharField(max_length=100)
    confidence = models.FloatField()
    image = models.ImageField(upload_to='disease_images/')
    image_url = models.URLField(max_length=500, blank=True)
    predicted_at = models.DateTimeField(auto_now_add=True)

    def save(self, *args, **kwargs):
        creating = self.pk is None
        super().save(*args, **kwargs)

        
        if creating and self.image and not self.image_url:
            self.image_url = f"https://cropdisesbackend-1.onrender.com{self.image.url}"
            super().save(update_fields=['image_url'])

    def __str__(self):
        return self.disease_name
