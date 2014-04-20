$(document).on('pageinit', function() {
	$('.message').click(function() {
		$(this).hide(500);
	});

	$('.datetimepicker').datetimepicker({
		format:'Y-m-d H:i',
	});
});
