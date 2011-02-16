<form method="POST" action='/add_participant' id='add-participant-form'>
<table>
	<tr>
		<td><label for='trip'>Trip</label></td>
		<td>
			<select name='trip' id='add-participant-trip'>
			% for trip in trips:
				<option value='{{ trip.key().id() }}'>{{ trip.name }} ({{ trip.created.strftime('%Y-%m-%d') }})</option>
			% end
			</select>
		</td>
	</tr>

	<tr>
		<td><label for='add-participant'>User</label></td>
		<td>
			<select name='user' id='add-participant'>
			% for user in users:
				<option value='{{ user.key().id() }}'>{{ user.username }}</option>
			% end
			</select>
		</td>
	<tr>
		<td></td>
		<td><input type='submit' value='Add Participant &raquo;'></td>
	</tr></tr>
</table>
</form>
