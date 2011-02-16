<table cellspacing='10' id='list-expenses'>
	<thead>
		<tr>
			<td></td>
			<td>Created</td>
			<td>Username</td>
			<td>Amount</td>
			<td>Description</td>
		</tr>
	</thead>
	<tbody>
		% for expense in expenses:
		<tr id='expense-{{ expense.key().id() }}'>
			<td><a href='#'>[ X ]</a></td>
			<td>{{ expense.created.strftime('%Y-%m-%d') }}</td>
			<td>{{ getattr(expense.payer, 'username', 'None Given') }}</td>
			<td>{{ expense.amount }}</td>
			<td>{{ expense.description }}</td>
		</tr>
		% end
	</tbody>
</table>
