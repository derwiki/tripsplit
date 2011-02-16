<table id='list-participants'>
	% for participant in participants:
	<tr id='participant-{{ participant.key().id() }}'>
		<td><a href='#'>[ X ]</a></td>
		<td>{{ participant.user.username }}</td>
		<td>{{ participant.user.email }}</td>
	</tr>
	%end
</table>
