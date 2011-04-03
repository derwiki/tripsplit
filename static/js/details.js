var details = details || {};

details.pageLoaded = function() {
	console.log('entering pageLoaded');
	$('#add-participant-form').submit(details.addParticipantHandler);
	$('#list-participants').click(details.removeParticipantHandler);
	$('#add-expense-form').submit(details.addExpenseHandler);
	$('#list-expenses').click(details.removeExpenseHandler);

	var selectedTab = window.location.hash;
	console.log('selected tab from URL', selectedTab);
	selectedTab = selectedTab || '#trips';
	console.log('selected tab displaying', selectedTab);
	var selectedTabSel = 'div' + selectedTab + '-content'
	console.log(selectedTabSel);
	$(selectedTabSel).removeClass('hidden').show();

	$('.navtab').each(function(index, node) {
		var field = node.id.split('-')[0];
		$('#' + field +'-tab').click(function() {
			$('.navtab[id!="' + node.id + '"]').hide();
			$('div#' + field + '-content').show()
		});
	});

	details.initAutocomplete();
};

details.addExpenseHandler = function() {
	var data = {'payer': $('#add-expense-form select#payer').val()};
	$.each($('#add-expense-form input'), function(index, field) {
		data[field.name] = field.value;
	});
	console.log('addExpense data', data);

	$.post('/add_expense', data, function(respJSON) {
		console.log(respJSON);
		if (respJSON.success) {
			var new_row = "<tr><td><a href='#'>[ X ]</a></td>";
			$.each(['created', 'payer', 'amount', 'description'], function(index, key) {
				new_row += "<td>" + respJSON[key] + "</td>";
			});
			new_row += "</tr>";
			$('table#list-expenses tbody').append(new_row);
			console.log(respJSON);
		} else {
			console.log(respJSON.error);
		}
	});

	return false;
};

details.removeParticipantHandler = function(e) {
	// id='participant,<id>'
	var participantRowId = e.target.parentNode.parentNode.id;
	var participantId = participantRowId.split('-')[1];
	var data = {'participant': participantId};

	console.log('data', data);
	$.post('/remove_participant', data, function(respJSON) {
		console.log('remove_participant', respJSON);
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

details.removeExpenseHandler = function(e) {
	var expenseRowId= e.target.parentElement.parentElement.id;
	var expenseId = expenseRowId.split('-')[1];
	var data = {'expense': expenseId};
	console.log('removeExpenseHandler data', data);

	$.post('/remove_expense', data, function(respJSON) {
		console.log(respJSON);
		if (respJSON.success) {
			// remove row
			$('#' + expenseRowId).remove();
		} else {
			console.log(respJSON.error);
		}
	});
	return false;
};

details.addParticipantHandler = function(data) {
	$.post('/add_participant', data, function(respJSON) {
		if (respJSON.success) {
			var new_participant = '<tr id="participant-' + respJSON.participant_id + '">\n';
			new_participant += '<td><a href="#">[ X ]</a></td>';
			new_participant += ('<td><img src="' + respJSON.facebook_profile_photo_url + '" /></td>\n');
            console.log(respJSON.facebook_profile_photo_url );
			new_participant += ('<td>' + respJSON.name + '</td>\n');
			new_participant += '</tr>\n';
			$('table#list-participants').append(new_participant);
            var new_payer = "<option value='" + respJSON.user_id + "'>" + respJSON.name + "</option>"
			$('select#payer').append(new_payer);
		} else {
			console.log(respJSON.error);
		}
	});
	return false;
};

details.initAutocomplete = function() {
	//$.getJSON('/json/users', function(data) {
    FB.api('/me/friends?fields=id,name,picture', function(resp) {
        details.autocompleteMap = {};
        var keys = [];
        $.each(resp['data'], function(index, user) {
			details.autocompleteMap[user.name] = {};
			details.autocompleteMap[user.name]['id'] = user.id;
			details.autocompleteMap[user.name]['profile_photo_url'] = user.picture;
            keys.push(user.name);
        });

		$('#add-participant').autocomplete({source: keys});
		$('#add-participant').bind('autocompleteselect', function(e, ui) {
            user_data = details.autocompleteMap[ui.item.value];
			var data = {
				'user': user_data.id,
				'trip': details.tripid,
                'profile_photo_url': user_data.profile_photo_url,
                'name': ui.item.value
			}
			console.log('addParticipant data', data);
			details.addParticipantHandler(data);	
			$(this).val('');
			return false;
		});
	});
};
