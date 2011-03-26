var tripsplit = tripsplit || {};
tripsplit.home = tripsplit.home || {};

tripsplit.home.pageLoaded = function() {
	console.log('entering pageLoaded');
	$('#add-trip-form').submit(tripsplit.home.addTripHandler);
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

