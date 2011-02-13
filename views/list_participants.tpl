<table>
	% for participant in participants:
	<tr>
		<td>{{participant.user.username}}</td>
		<td>{{participant.user.email}}</td>
	</tr>
	%end
</table>
