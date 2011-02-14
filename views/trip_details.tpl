<html>
<head>
<title>Trip Details</title>
<script src='https://ajax.googleapis.com/ajax/libs/jquery/1.5.0/jquery.min.js' type='text/javascript'></script>
<script src='/static/js/trip_details.js'></script>
<script type='text/javascript'>
var trip_details = trip_details || {};
$(document).ready(function() {
	trip_details.pageLoaded();
});
</script>
</head>
<body>

<div style='text-align: right;'>Logged in as <a href='#'>{{loggedin_user.username}}</a></div>

<h3>Expenses</h3>
%include list_expenses expenses=expenses
<div>Add new expense</div>
%include create_expense trips=[trip]
<br>

<h3>Participants</h3>
%include list_participants participants=participants
<div>Add new participant</div>
%include add_participant trips=[trip], users=users

</body>
</html>