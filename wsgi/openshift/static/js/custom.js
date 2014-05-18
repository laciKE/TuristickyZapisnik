$(document).on('pageinit', function() {
	$('.message').click(function() {
		$(this).hide(500);
	});

	$('.datetimepicker').datetimepicker({
		format:'Y-m-d H:i',
	});

	$('#photos_edit a').click(function() {
		$(this).parent().hide(500, function() {
			$(this).remove();
		});
	});
});
