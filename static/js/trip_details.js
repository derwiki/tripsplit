var trip_details = {};

trip_details.pageLoaded = function() {
	console.log('entering pageLoaded');
	$('#add-participant-form').submit(trip_details.addParticipantHandler);
};


trip_details.addParticipantHandler = function () {
	var data = {
		'user': $('select#add-participant').val(),
		'trip': $('select#add-participant-trip').val(),
	};

	$.post('/add_participant', data, function(resp) {
		var respJSON = JSON.parse(resp)
		console.log(respJSON);
		if (respJSON.success) {
			var new_participant = '<tr>\n';
			new_participatn += '<td><a href="#">[ X ]</a></td>';
			new_participant += ('<td>' + respJSON.username + '</td>\n');
			new_participant += ('<td>' + respJSON.email+ '</td>\n');
			new_participant += '</tr>\n';
			$('#list-participants tr:last').after(new_participant);
			$('select#add-participant option[value="' + data['user'] +'"]').remove();
		} else {
			console.log(respJSON.error);
		}
	});
	return false;
};
