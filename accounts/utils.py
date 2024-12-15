from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.conf import settings

def send_account_deletion_email(user):
    """Send confirmation email when account is deleted"""
    subject = 'Account Deletion Confirmation'
    from_email = settings.DEFAULT_FROM_EMAIL
    to_email = [user.email]
    
    context = {
        'user': user,
    }
    
    html_content = render_to_string(
        'accounts/emails/account_deleted.html',
        context
    )
    
    send_mail(
        subject,
        '',
        from_email,
        to_email,
        html_message=html_content,
        fail_silently=False,
    ) 