<table id='list-participants'>
	% for participant in participants:
	<tr id='participant-{{ participant.key().id() }}'>
		<td><a href='#'>[ X ]</a></td>
        <td><img src="{{ participant.user.facebook_profile_photo_url }}" /></td>
		<td>{{ participant.user.name }}</td>
	</tr>
	%end
</table>
