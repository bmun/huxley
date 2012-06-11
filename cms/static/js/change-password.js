$(function(){

$(".content").delegate("#newpassword", "click", function(){
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

$(document).live("click", function(){
    if($("#changepassword").is(":visible")){
        $("#changepassword").slideUp(function(){
            $("#changepassword div.input input").val('');
            $("#changepassword #message").hide();
        });
    }
});

$(".content").delegate(".changepassword", "click", function(e){
    e.stopPropagation();
});


$(".content").delegate("#changepasswordform", "submit", function(){
    $.post('/changepassword/', $(this).serializeArray(), function(data){
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