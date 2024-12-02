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
        events: '/bookings/api/events/',  // We'll create this endpoint later
        selectable: true,
        select: function(info) {
            // Handle time slot selection
            var startTime = info.start;
            var endTime = info.end;
            
            // Check if selected time is in the future
            if (startTime < new Date()) {
                alert('Cannot book appointments in the past');
                return;
            }
            
            // Redirect to booking form with selected time
            var serviceId = document.querySelector('.selected-service')?.dataset.serviceId;
            if (serviceId) {
                window.location.href = `/bookings/create/${serviceId}/?start=${startTime.toISOString()}`;
            } else {
                alert('Please select a service first');
            }
        }
    });
    calendar.render();
}); 