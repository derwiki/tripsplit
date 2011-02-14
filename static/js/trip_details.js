var trip_details = trip_details || {};

trip_details.pageLoaded = function() {
	console.log('entering pageLoaded');
	$('#add-participant-form').submit(trip_details.addParticipantHandler);
	$('#list-participants').click(trip_details.removeParticipantHandler);
};


trip_details.addParticipantHandler = function () {
	var data = {
		'user': $('select#add-participant').val(),
		'trip': $('select#add-participant-trip').val()
	};

	$.post('/add_participant', data, function(resp) {
		var respJSON = JSON.parse(resp)
		console.log(respJSON);
		if (respJSON.success) {
			var new_participant = '<tr id="participant-' + respJSON.participant + '">\n';
			new_participant += '<td><a href="#">[ X ]</a></td>';
			new_participant += ('<td>' + respJSON.username + '</td>\n');
			new_participant += ('<td>' + respJSON.email+ '</td>\n');
			new_participant += '</tr>\n';
			$('#list-participants').append(new_participant);
			$('select#add-participant option[value="' + data['user'] +'"]').remove();
		} else {
			console.log(respJSON.error);
		}
	});
	return false;
};

trip_details.removeParticipantHandler = function(e) {
	// id='participant,<id>'
	var participantRowId = e.target.parentElement.parentElement.id;
	var participantId = participantRowId.split('-')[1];
	var data = {'participant': participantId};

	console.log('data', data);
	$.post('/remove_participant', data, function(resp) {
		var respJSON = JSON.parse(resp)
		console.log(respJSON);
		if (respJSON.success) {
			// remove row
			$('#' + participantRowId).remove();

			// add participant back to dropdown
			var new_option = '<option value="' + respJSON['user_id'] + '">' + respJSON['username'] + '</option>\n';
			$('select#add-participant').append(new_option);
		} else {
			console.log(respJSON.error);
		}
	});
	return false;
};
	
