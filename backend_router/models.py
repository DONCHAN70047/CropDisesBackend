from django.db import models
from django.conf import settings

class DiseaseDetection(models.Model):
    predicted_disease = models.CharField(max_length=100)
    confidence = models.FloatField()

    image = models.ImageField(upload_to="disease_images/")
    image_name = models.CharField(max_length=255, blank=True)
    image_link = models.URLField(max_length=500, blank=True)

    import_time = models.DateTimeField(auto_now_add=True)

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)

        updated = False

       
        if self.image and not self.image_name:
            self.image_name = self.image.name.split("/")[-1]
            updated = True

        
        if self.image and not self.image_link:
            base_url = getattr(settings, "PUBLIC_BASE_URL", "")
            self.image_link = f"{base_url}{self.image.url}"
            updated = True

        if updated:
            super().save(update_fields=["image_name", "image_link"])

    def __str__(self):
        return self.predicted_disease
