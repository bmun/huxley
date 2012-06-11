$(function() {	
	
	function setUnsaved(){
		$("#tablemenu input[type=submit]").removeClass('saved').addClass('unsaved');
	}
		
	function setSaved(){
		$("#tablemenu input[type=submit]").removeClass('unsaved').addClass('saved');
	}

	$(".content").delegate("#editprefs", "submit", function() {
		$.ajax({
			type: 'POST',
			url: 'updateprefs/',
			data: $(this).serializeArray(),
			success: function(name) {
				setSaved();
			}
		});
		return false;
	});
	
	$(".content").delegate(".button", "hover", function() {
		$(this).css('cursor', 'pointer');
	}, function() {
		$(this).css('cursor', 'auto');
	});
	
	$(".content").delegate(".select", "change", function() {
		setUnsaved();
	});
	
});