document.addEventListener('DOMContentLoaded', function () {
    var calendarEl = document.getElementById('calendar');

    var calendar = new FullCalendar.Calendar(calendarEl, {
        initialView: 'dayGridMonth', // Define a visualização inicial como um calendário mensal
        selectable: true, // Permite selecionar datas
        editable: false, // Define se os eventos são editáveis
        eventSources: [
            {
                url: '/appointments/json', // Rota que retorna os eventos em JSON
                method: 'GET',
                failure: function () {
                    alert('Erro ao carregar eventos!');
                }
            }
        ],
        eventClick: function (info) {
            alert('Evento: ' + info.event.title);
        }
    });

    calendar.render();
});
