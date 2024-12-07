import logging
from django.conf import settings
from storages.backends.s3boto3 import S3Boto3Storage

logger = logging.getLogger(__name__)

class StaticStorage(S3Boto3Storage):
    location = settings.STATICFILES_LOCATION
    
    def _save(self, name, content):
        logger.info(f'Saving static file: {name}')
        return super()._save(name, content)

class MediaStorage(S3Boto3Storage):
    location = settings.MEDIAFILES_LOCATION 