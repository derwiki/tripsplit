%def jsblock():
<script src='/static/js/trip_details.js'></script>
<script type='text/javascript'>
var trip_details = trip_details || {};
$(document).ready(function() {
	trip_details.pageLoaded();
});
</script>
%end

<h3>Expenses</h3>
%include list_expenses expenses=expenses
<div>Add new expense</div>
%include add_expense trips=[trip]
<br>

<h3>Participants</h3>
%include list_participants participants=participants
<div>Add new participant</div>
%include add_participant trips=[trip], users=users

%rebase base title='Trip Details', jsblock=jsblock, loggedin_user=loggedin_user
