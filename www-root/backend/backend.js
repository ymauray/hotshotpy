($ => {

    'use strict';

    $(document).ready(() => {
        let event_selector = $('select[name=event-selector]');

        let init = () => {
            $.getJSON('/api?controller=events&method=get').done(result => {
                let events = result.payload;
                event_selector.empty();
                events.events.forEach(event => {
                    let option = $('<option/>').val(event.id).text(event.name);
                    if (event.id == events.current_event_id) {
                        option.attr('selected', 'selected');
                        option.text(event.name + '*')
                    }
                    event_selector.append(option);
                });
                //get_results(events.current_event_id);
            });
        };

        $('#save-button').click(e => {
            e.stopPropagation();
            e.preventDefault();
            let event_id = event_selector.val();
            $.ajax({
                type: 'GET',
                url: '/api?controller=events&method=set_current&current=' + event_id
            }).done(response => {
                console.log('Current event successfully updated');
                init();
            });
        });

        init();

    });

})(window.jQuery);