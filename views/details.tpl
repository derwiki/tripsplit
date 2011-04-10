%def jsblock():
<script src='/static/js/details.js'></script>
<script type='text/javascript'>
var details = details || {};
$(document).ready(function() {
	details.pageLoaded();
});
details.tripid = {{ trip.key().id() }};
</script>
%end

%# this would be nice
%# nav = (('newtrip', 'New Trip'), ('participants', 'Participants'), ('expenses', 'Expenses'), ('trips', 'Trips')
%#{{ ' | '.join("<a href='#%s'>%s</a>" % (action, label) for action, label in nav) }}
<a href='#participants'>Participants</a> |
<a href='#expenses'>Expenses</a> |
<a href='#settle'>Settle</a> |
<a href='#trips'>Trips</a>

<div id='participants-content' class='navtab hidden'>
	<div id='invite-content'>
		<div class='ui-widget'>
			<label for='add-participant'>Invite Participants</label><br>
			<input type='text' id='add-participant'>
		</div>
	</div>
	%include add_participant trip=trip, users=users
	%include list_participants participants=participants
</div>

<div id='expenses-content' class='navtab hidden'>
	<h3>Expenses</h3>
	%include list_expenses expenses=expenses
	<div>Add new expense</div>
	%include add_expense trip=trip, participants=participants
</div>

<div id='settle-content' class='navtab hidden'>
    <h3>Settle Up</h3>
    <button id='btn-refresh-settle'>refresh &raquo;</button>
    <div id='settle-story'>Press refresh to load data</div>
</div>

<div id='trips-content' class='navtab hidden'>
	<h3>Trips</h3>
	%include list_trips trips=trips
	<div>Add new trip</div>
	%include add_trip
</div>
	

%rebase base title='Trip Details', jsblock=jsblock, loggedin_user=loggedin_user
