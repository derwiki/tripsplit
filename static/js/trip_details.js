var trip_details = {};

trip_details.pageLoaded = function() {
	console.log('entering pageLoaded');

	$('#add-participant-form').submit(function(e) {
		var data = {
			'user': $('select#add-participant').val(),
			'trip': $('select#add-participant-trip').val(),
		};

		$.post('/add_participant', data, function(resp) {
			var respJSON = JSON.parse(resp)
			var new_participant = '<tr>\n';
			new_participant += ('<td>' + respJSON.username + '</td>\n');
			new_participant += ('<td>' + respJSON.email+ '</td>\n');
			new_participant += '</tr>\n';
			$('#list-participants tr:last').after(new_participant);
		});
		return false;
	});
};
