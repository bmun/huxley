$(function(){
	$("#container").delegate("#loginform", "submit", function(){
		var credentials = $("#loginform").serializeArray();

		$.post('/login/', credentials, function(data){
			if(data == 'OK'){
				ContentManager.onLogin();
			}
			else{
				$("#errorcontainer").hide().html('<label class="error">' + data + '</label>').fadeIn(250);
				$("#app").effect("shake", { direction:"up", times:2, distance:2 }, 50);
			}
		});

		return false;
	});
	
	$("#container").delegate("#logout", "click", function(){
     	$.get("/logout/", function(){
           	ContentManager.onLogout();
          });
     	return false;
	});
});