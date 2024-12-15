from django.shortcuts import render
from django.core.mail import send_mail
from django.contrib import messages
from django.shortcuts import render, redirect
from .forms import ContactForm
from django.conf import settings

def index(request):
    return render(request, 'home/index.html')

def about(request):
    return render(request, 'home/about.html')

def contact(request):
    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            # Send email to admin
            send_mail(
                subject=f"Contact Form: {form.cleaned_data['subject']}",
                message=f"From: {form.cleaned_data['name']}\nEmail: {form.cleaned_data['email']}\n\nMessage:\n{form.cleaned_data['message']}",
                from_email=settings.DEFAULT_FROM_EMAIL,
                recipient_list=[settings.DEFAULT_FROM_EMAIL],
                fail_silently=False,
            )
            
            # Send confirmation to user
            send_mail(
                subject='Contact Form Received - Clean Services Platform',
                message=f"""Dear {form.cleaned_data['name']},

Thank you for contacting us. We have received your message and will respond shortly.

Your message details:
Subject: {form.cleaned_data['subject']}
Message:
{form.cleaned_data['message']}

Best regards,
Clean Services Platform Team""",
                from_email=settings.DEFAULT_FROM_EMAIL,
                recipient_list=[form.cleaned_data['email']],
                fail_silently=False,
            )
            
            messages.success(request, 'Your message has been sent successfully!')
            return redirect('home:contact')
    else:
        form = ContactForm()

    return render(request, 'home/contact.html', {'form': form}) 