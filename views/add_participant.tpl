<form method="POST" action='/add_participant' id='add-participant-form'>
<input type='hidden' name='trip' value='{{ trip.key().id() }}' />
<table>
	<tr>
		<td></td>
		<td><input type='submit' value='Add Participant &raquo;'></td>
        <td><a href='#expenses'>Add Expenses &raquo;</a></td>
	</tr></tr>
</table>
</form>
