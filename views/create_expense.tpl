<form method="POST" action='/create_expense'>

<table>
	<tr>
		<td><label for='trip'>Trip</label></td>
		<td>
			<select name='trip' id='trip'>
			% for trip in trips:
				<option value='{{trip.key().id()}}'>{{trip.name}} ({{trip.created.strftime('%Y-%m-%d')}})</option>
			% end
			</select>
		</td>
	</tr>
	<tr>
		<td><label for='amount'>Amount</label></td>
		<td><input type='text' id='amount' name='amount'></td>
	</tr>
	<tr>
		<td><label for='description'>Description</label></td>
		<td><input type='text' id='description' name='description'></td>
	</tr>
	<tr>
		<td><label for='notes'>Notes</label></td>
		<td><input type='text' id='notes' name='notes'></td>
	</tr>
	<tr>
		<td></td>
		<td><input type='submit' value='Create Expense &raquo;'></td>
	</tr>
</table>
</form>
