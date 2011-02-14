<table id='list-participants'>
	% for participant in participants:
	<tr>
		<td><a href='/remove_participant'>[ X ]</a></td>
		<td>{{participant.user.username}}</td>
		<td>{{participant.user.email}}</td>
	</tr>
	%end
</table>
