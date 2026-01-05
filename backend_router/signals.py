from django.db.models.signals import post_save
from django.dispatch import receiver
from backend_router.models import DiseaseDetection
from ml_pipeline.image_batch_processor import process_new_images

@receiver(post_save, sender=DiseaseDetection)
def trigger_pipeline(sender, instance, created, **kwargs):
    if created and not instance.is_processed:
        process_new_images()
