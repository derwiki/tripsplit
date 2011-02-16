<form id='add-expense-form'>
<table>
	<tbody>
		<tr>
			<td><label for='trip'>Trip</label></td>
			<td>
				<select name='trip' id='add-expense-trip'>
				% for trip in trips:
					<option value='{{trip.key().id()}}'>{{trip.name}} ({{trip.created.strftime('%Y-%m-%d')}})</option>
				% end
				</select>
			</td>
		</tr>
		% fields = (('amount', 'Amount'), ('description', 'Description'), ('notes', 'Notes'))
		% for key, label in fields:
		<tr>
			<td><label for='{{ key }}'>{{ label }}</label></td>
			<td><input type='text' id='{{ key }}' name='{{ key }}'></td>
		</tr>
		% end
		<tr>
			<td></td>
			<td><input type='submit' value='Create Expense &raquo;'></td>
		</tr>
	</tbody>
</table>
</form>
