<ul>
% for trip in trips:
	<li><a href='/trip_details/{{ trip.key().id() }}'>{{ trip.name }} ({{ trip.created.strftime('%Y-%m-%d') }})</a></li>
% end
</ul>
