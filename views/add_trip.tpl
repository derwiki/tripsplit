<form id='add-trip-form' action='/add_trip' method='post'>
<table>
	<tbody>
		% fields = (('name', 'Trip Name'), ('description', 'Description'), ('notes', 'Notes'))
		% for key, label in fields:
		<tr>
			<td><label for='{{ key }}'>{{ label }}</label></td>
			<td><input type='test' id='{{ key }}' name='{{ key }}'></td>
		</tr>
		% end
		<tr>
			<td></td>
			<td><input type='submit' value='Create Expense &raquo;'></td>
		</tr>
	</tbody>
</table>
</form>
