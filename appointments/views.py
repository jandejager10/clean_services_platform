from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Appointment
from services.models import Service
from .forms import AppointmentForm
from django.core.mail import send_mail
from django.conf import settings


# Create your views here.
@login_required
def appointments(request):
    appointments = Appointment.objects.filter(user=request.user)
    return render(request, 'appointments/appointments.html', {'appointments': appointments})


@login_required
def add_appointment(request, service_id):
    service = get_object_or_404(Service, id=service_id)
    if request.method == 'POST':
        form = AppointmentForm(request.POST)
        if form.is_valid():
            appointment = form.save(commit=False)
            appointment.user = request.user
            appointment.service = service
            appointment.save()
            return redirect('appointments:appointments')
    else:
        form = AppointmentForm()
    return render(request, 'appointments/add_appointment.html', {'form': form, 'service': service})


@login_required
def confirm_appointment(request, appointment_id):
    appointment = get_object_or_404(Appointment, id=appointment_id, user=request.user)
    if request.method == 'POST':
        appointment.confirmed = True
        appointment.save()

        # Send confirmation email
        subject = 'Appointment Confirmation'
        message = f'Your appointment for {appointment.service.name} on {appointment.date} at {appointment.time} has been confirmed.'
        from_email = settings.DEFAULT_FROM_EMAIL
        recipient_list = [request.user.email]

        send_mail(subject, message, from_email, recipient_list)

        messages.success(request, 'Your appointment has been confirmed and a confirmation email has been sent.')
        return redirect('appointments:appointments')

    return render(request, 'appointments/confirm_appointment.html', {'appointment': appointment})


@login_required
def cancel_appointment(request, appointment_id):
    appointment = get_object_or_404(Appointment, id=appointment_id, user=request.user)
    if request.method == 'POST':
        appointment.status = 'cancelled'
        appointment.save()

        # Send cancellation email
        subject = 'Appointment Cancellation'
        message = f'Your appointment for {appointment.service.name} on {appointment.date} at {appointment.time} has been cancelled.'
        from_email = settings.DEFAULT_FROM_EMAIL
        recipient_list = [request.user.email]

        send_mail(subject, message, from_email, recipient_list)

        messages.success(request, 'Your appointment has been cancelled and a confirmation email has been sent.')
        return redirect('appointments:appointments')

    return render(request, 'appointments/cancel_appointment.html', {'appointment': appointment})
