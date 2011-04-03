<form id='add-expense-form'>
<input type='hidden' name='trip' value='{{ trip.key().id() }}' />
<table>
	<tbody>
		<tr>
			<td><label for='payer'>Payer</label></td>
			<td>
				<select name='payer' id='payer'>
				% for participant in participants:
					<option value='{{ participant.user.key().id() }}'>{{ participant.user.name }}</option>
				% end
				</select>
			</td>
		</tr>
		% fields = (('amount', 'Amount'), ('description', 'Description'), ('notes', 'Notes'))
		% for key, label in fields:
		<tr>
			<td><label for='{{  key  }}'>{{  label  }}</label></td>
			<td><input type='text' id='{{  key  }}' name='{{  key  }}'></td>
		</tr>
		% end
		<tr>
			<td></td>
			<td><input type='submit' value='Create Expense &raquo;'></td>
		</tr>
	</tbody>
</table>
</form>
