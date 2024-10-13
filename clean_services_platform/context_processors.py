from django.conf import settings


def global_settings(request):
    return {
        'free_delivery_threshold': settings.FREE_DELIVERY_THRESHOLD,
    }