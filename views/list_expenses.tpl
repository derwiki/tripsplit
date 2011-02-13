<html>
<head>
<title>List Expenses</title>
</head>
<body>

<table cellspacing='10'>
	<tr>
		<td>Created</td>
		<td>Username</td>
		<td>Amount</td>
		<td>Description</td>
	</tr>
	% for expense in expenses:
	<tr>
		<td>{{expense.created.strftime('%Y-%m-%d')}}</td>
		<td>{{expense.payer.username or 'None Given'}}</td>
		<td>{{expense.amount}}</td>
		<td>{{expense.description}}</td>
	</tr>
	% end
</table>

<br>
Add new expense:<br>
%include create_expense trips=[trip]

<br>
Participants:<br>
%include list_participants participants=participants

%include add_participant trips=[trip], users=users

</body>
</html>
