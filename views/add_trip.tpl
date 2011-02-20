<form id='add-trip-form'>
<table>
	<tbody>
		% fields = (('tripname', 'Trip Name'),)#, ('description', 'Description'), ('notes', 'Notes'))
		% for key, label in fields:
		<tr>
			<td><label for='{{ key }}'>{{ label }}</label></td>
			<td><input type='text' id='{{ key }}' name='{{ key }}'></td>
		</tr>
		% end
		<tr>
			<td></td>
			<td><input type='submit' value='Create Trip &raquo;'></td>
		</tr>
	</tbody>
</table>
</form>
