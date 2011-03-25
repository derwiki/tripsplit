%def jsblock():
<script src='/static/js/home.js'></script>
<script type='text/javascript'>
var tripsplit = tripsplit || {};
tripsplit.home = tripsplit.home || {};
$(document).ready(function() {
	tripsplit.home.pageLoaded();
});
</script>
%end

<div id='newtrip-content' class='navtab'>
	<h3>I Just Went on a Trip</h3>
	%include add_trip
</div>

<div id='invite-content' class='navtab hidden'>
	<h3>Invite Trip Participants</h3>
	<ul id='list-participants'>
	</ul>
	<div class='ui-widget'>
		<label for='add-participant'>Participant</label><br>
		<input type='text' id='add-participant'>
	</div>
</div>

%rebase base title='TripSplit', jsblock=jsblock, loggedin_user=user
