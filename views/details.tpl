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
%#{{ ' | '.join('<a href='#%s' id='%s-tab'>%s</a>' % (action, label) for action, label in nav) }}
<a href='#newtrip' id='newtrip-tab'>New Trip</a> |
<a href='#participants' id='participants-tab'>Participants</a> |
<a href='#expenses' id='expenses-tab'>Expenses</a> |
<a href='#trips' id='trips-tab'>Trips</a>


<div id='newtrip-content' class='navtab hidden'>
	<h3>I Just Went on a Trip</h3>
	%include add_trip
</div>


<div id='expenses-content' class='navtab hidden'>
	<h3>Expenses</h3>
	%include list_expenses expenses=expenses
	<div>Add new expense</div>
	%include add_expense trip=trip, participants=participants
</div>

<div id='participants-content' class='navtab hidden'>
	<div id='invite-content'>
		<h3>Invite Trip Participants</h3>
		<div class='ui-widget'>
			<label for='add-participant'>Participant</label><br>
			<input type='text' id='add-participant'>
		</div>
	</div>
	%include add_participant trip=trip, users=users
	%include list_participants participants=participants
</div>

<div id='trips-content' class='navtab hidden'>
	<h3>Trips</h3>
	%include list_trips trips=trips
	<div>Add new trip</div>
	%include add_trip
</div>
	

%rebase base title='Trip Details', jsblock=jsblock, loggedin_user=loggedin_user
