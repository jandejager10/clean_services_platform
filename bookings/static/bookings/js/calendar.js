document.addEventListener('DOMContentLoaded', function() {
    var calendarEl = document.getElementById('calendar');
    var calendar = new FullCalendar.Calendar(calendarEl, {
        initialView: 'timeGridWeek',
        slotMinTime: '08:00:00',
        slotMaxTime: '20:00:00',
        allDaySlot: false,
        slotDuration: '00:30:00',
        headerToolbar: {
            left: 'prev,next today',
            center: 'title',
            right: 'timeGridWeek,timeGridDay'
        },
        events: '/bookings/api/events/',
        selectable: true,
        eventClick: function(info) {
            // Handle clicking on an existing booking
            var bookingId = info.event.id;
            if (bookingId) {
                window.location.href = `/bookings/detail/${bookingId}/`;
            }
        },
        select: function(info) {
            // Handle time slot selection for new bookings
            var startTime = info.start;
            var endTime = info.end;
            
            if (startTime < new Date()) {
                alert('Cannot book appointments in the past');
                return;
            }
            
            var serviceId = document.querySelector('.selected-service')?.dataset.serviceId;
            if (serviceId) {
                window.location.href = `/bookings/create/${serviceId}/?start=${startTime.toISOString()}`;
            } else {
                alert('Please select a service first');
            }
        },
        eventDidMount: function(info) {
            // Add tooltip with booking details
            var tooltipTitle = info.event.title;
            if (info.event.extendedProps.customer) {
                tooltipTitle += `\nCustomer: ${info.event.extendedProps.customer}`;
            }
            tooltipTitle += '\nClick to view details';
            
            $(info.el).tooltip({
                title: tooltipTitle,
                placement: 'top',
                trigger: 'hover'
            });
        }
    });
    calendar.render();
}); 