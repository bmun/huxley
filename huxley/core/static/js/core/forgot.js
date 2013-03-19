$(function() {
	$(document).on("submit", "#forgot-form", function(){
		var uri = $(this).attr("action");
		ContentManager.loadNewContent(uri, $("#forgot-form").serializeArray());
		return false;
	});
});