from django.conf import settings
from django.contrib import messages
from django.core.mail import send_mail
from django.shortcuts import redirect, render

from .forms import ContactForm


def index(request):
    return render(request, 'home/index.html')


def about(request):
    return render(request, 'home/about.html')


def contact(request):
    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            data = form.cleaned_data
            # Send to admin
            send_mail(
                f"Contact Form: {data['subject']}",
                f"From: {data['name']}\nEmail: {data['email']}\n\n"
                f"Message:\n{data['message']}",
                settings.DEFAULT_FROM_EMAIL,
                [settings.DEFAULT_FROM_EMAIL],
                fail_silently=False,
            )
            # Send to user
            send_mail(
                'Contact Form Received - Clean Services Platform',
                f"Dear {data['name']},\n\nThank you for contacting us. "
                f"We have received your message and will respond shortly.\n\n"
                f"Your message details:\nSubject: {data['subject']}\n"
                f"Message:\n{data['message']}\n\nBest regards,\n"
                "Clean Services Platform Team",
                settings.DEFAULT_FROM_EMAIL,
                [data['email']],
                fail_silently=False,
            )
            messages.success(request, 'Your message has been sent successfully!')
            return redirect('home:contact')
    else:
        form = ContactForm()

    return render(request, 'home/contact.html', {'form': form})
