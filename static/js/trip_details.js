var trip_details = {};

trip_details.pageLoaded = function() {
	$('addParticipantSubmit').click(function(e) {
		e.preventDefault();
		var data = {'user': $('select#add-participant').val()}
		$.post('/add_participant', data, function(respJSON) {
			console.log(respJSON);
		});
	});
       // format and output result
       //        $("#rating").html(
       //                 "Thanks for rating, current average: " +
       //                          $("average", xml).text() +
       //                                   ", number of votes: " +
       //                                            $("count", xml).text()
       //                                                   );
};
