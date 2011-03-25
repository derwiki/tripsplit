%def jsblock():
<script src='/static/js/trip_details.js'></script>
<script type='text/javascript'>
var trip_details = trip_details || {};
$(document).ready(function() {
	trip_details.pageLoaded();
});
</script>
%end

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
	%include add_expense trips=[trip]
</div>

<div id='participants-content' class='navtab hidden'>
	<h3>Participants</h3>
	%include list_participants participants=participants
	<div id='invite-content'>
		<h3>Invite Trip Participants</h3>
		<ul id='list-participants'>
		</ul>
		<div class='ui-widget'>
			<label for='add-participant'>Participant</label><br>
			<input type='text' id='add-participant'>
		</div>
	</div>
	%#include add_participant trips=[trip], users=users
</div>

<div id='trips-content' class='navtab hidden'>
	<h3>Trips</h3>
	%include list_trips trips=trips
	<div>Add new trip</div>
	%include add_trip
</div>
	

%rebase base title='Trip Details', jsblock=jsblock, loggedin_user=loggedin_user
