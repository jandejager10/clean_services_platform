from django.apps import AppConfig


class FAQConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'faq'
    verbose_name = 'FAQ'

    def ready(self):
        """
        Import signals or perform other initialization when the app is ready
        """
        pass 