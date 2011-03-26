var tripsplit = tripsplit || {};
tripsplit.home = tripsplit.home || {};

tripsplit.home.pageLoaded = function() {
	console.log('entering pageLoaded');
	$('#add-trip-form').submit(tripsplit.home.addTripHandler);

	var selectedTab = window.location.hash;
	selectedTab = selectedTab || '#home';
	var selectedTabSel = 'div' + selectedTab + '-content'
	$(selectedTabSel).removeClass('hidden').show();

	$('.navtab').each(function(index, node) {
		var field = node.id.split('-')[0];
		$('#' + field +'-tab').click(function() {
			$('.navtab[id!="' + node.id + '"]').hide();
			$('div#' + field + '-content').show()
		});
	});
	$.getJSON('/json/users', function(data) {
		tripsplit.home.users = data;
		console.log('json/users', data);
		$('#add-participant').autocomplete({source: data});
		$('#add-participant').bind('autocompleteselect', function(e, ui) {
			var email = ui.item.value;
			$('#list-participants').append('<li id=' + email + '>' + email + '</li>');
			$(this).val('');
			return false;
		});
	});

};

tripsplit.home.finishAddParticipants = function() {
	var participants = $('#list-participants li').map(function(index, ele) { return ele.id; });

}

// newtrip-content
tripsplit.home.showTab = function(selectedTab) {
	var selectedTabSel = 'div#' + selectedTab + '-content'
	$(selectedTabSel).removeClass('hidden').show();
	console.log('showTab, selected', selectedTabSel);
	$('.navtab').each(function(index, node) {
		var field = node.id.split('-')[0];
		console.log('field, nodeid', field, node.id);
		$('.navtab[id!="' + node.id + '"]').hide();
		$('div#' + field + '-content').show()
	});
};

tripsplit.home.nextJump = {
	'add_trip': 'invite_participants'
};

tripsplit.home.addTripHandler = function (e) {
	var data = {'tripname': $('#tripname').val()};

	var action = 'add_trip';
	console.log('addTrip data', data);

	$.post('/' + action, data, function(resp) {
		var respJSON = JSON.parse(resp);
		console.log('addTripHandler', respJSON);
		if (respJSON.success) {
			window.location = '/details/' + respJSON.trip_id + '#participants';
		} else {
			console.log('addTripHandler error', respJSON.error);
		}
	}, function(resp) {
        console.log('addTripHandler error', respJSON)
	});
	return false;
};



tripsplit.home.removeParticipantHandler = function(e) {
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



