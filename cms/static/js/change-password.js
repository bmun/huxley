$(function(){

$(document).on("click", "#newpassword", function(e){
    if($("#changepassword").is(":visible")){
        $("#changepassword").slideUp(function(){
            $("#changepassword div.input input").val('');
            $("#changepassword #message").hide();
        });
        
    }
    else{
        $("#changepassword").slideDown();
    }
    return false;
});

$(document).click(function(){
    if($("#changepassword").is(":visible")){
        $("#changepassword").slideUp(function(){
            $("#changepassword div.input input").val('');
            $("#changepassword #message").hide();
        });
    }
});

$(document).on("click", ".changepassword", function(e){
    e.stopPropagation();
});


$(document).on("submit", "#changepasswordform", function(){
	var uri = $(this).attr("action");
    $.post(uri, $(this).serializeArray(), function(data){
        if(data == 'OK'){
        	$("#changepassword input[type=password]").val("");
        	if ($("#changepassword #message").is(":visible")) {
        		$("#changepassword #message").hide().html('<label class="success"> Success! </label>').fadeIn(250);
        	} else {
        		$("#changepassword #message").hide().html('<label class="success"> Success! </label>').slideDown(250);
        	}
            $("#changepassword").delay(750).slideUp();
            $("#changepassword #message").delay(750).slideUp();
        }
        else{
            if($("#changepassword #message").is(":visible")){
                $("#changepassword #message").hide().html('<label class="error">' + data + '</label>').fadeIn(250);
            }
            else{
                $("#changepassword #message").hide().html('<label class="error">' + data + '</label>').slideDown(250);
            }
            $("#changepassword").effect("shake", { direction:"left", times:2, distance:2 }, 50);
        }
    });
    return false;
});

});