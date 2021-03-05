($ => {

    'use strict';

    $(document).ready(() => {
        let event_selector = $('select[name=event-selector]');
		let thead_tr = $('thead > tr');
		let tbody = $('tbody');

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
                get_results(events.current_event_id);
            });
        };

        event_selector.change(e => {
			get_results(event_selector.val());
		});

		let get_results = event_id => {
			$.getJSON('/api?controller=standings&method=get&event_id=event_id').done(results => {
                let standings = results.payload;
				standings.drivers.sort((a, b) => a.name.localeCompare(b.name));
				console.log(standings);
				thead_tr.empty();
				thead_tr.append(
					$('<th/>').addClass('col-2').text('Driver')
				);
				for (var i = 1; i <= standings.race_count; i++) {
					thead_tr.append(
						$('<th/>').addClass('col-1').addClass('text-center').text('#' + i)
					);
				}

				tbody.empty();
				standings.drivers.forEach(driver => {
					let tr = $('<tr/>').attr('x-data-driver-id', driver.id).append(
						$('<td/>').text(driver.flag + ' ' + driver.name)
					);
					var i = 0;
					driver.finishes.forEach(finish => {
						tr.append(
							$('<td/>').attr('x-data-result-id', finish.result_id).attr('x-data-race-id', standings.races[i++]).append(
								$('<input/>').addClass('w-100').addClass('text-center').val(finish.pos >= 0 ? finish.pos : '')
							)
						)
					});
					tbody.append(tr);
				});
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