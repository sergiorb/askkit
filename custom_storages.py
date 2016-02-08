from django.conf import settings
from storages.backends.s3boto import S3BotoStorage
from django.core.files.storage import get_storage_class

class CachedS3BotoStorage(S3BotoStorage):
    """
    S3 storage backend that saves the files locally, too.
    """
    def __init__(self, *args, **kwargs):
        super(CachedS3BotoStorage, self).__init__(*args, **kwargs)
        self.local_storage = get_storage_class(
            "compressor.storage.CompressorFileStorage")()

    def save(self, name, content):
        name = super(CachedS3BotoStorage, self).save(name, content)
        self.local_storage._save(name, content)
        return name

class StaticStorage(S3BotoStorage):
    location = '/static/'
    def url(self, name):
        name = self._clean_name(name)
        return '{0}{1}'.format(settings.STATIC_URL, name)


class MediaStorage(S3BotoStorage):
    location = '/media/'

