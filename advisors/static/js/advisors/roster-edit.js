    
    var Roster = {
        nodelegate: '[Delegate Name]',
        switch1: undefined,
        switch2: undefined,
        opQueue: [],
		init: function(){
			
			// Add new delegate.
			$(".content").delegate('.nodelegate', "click", function(){
	            var sid = $(this).closest('tr').attr('slotid');
	            $(this).closest('tr').attr('delegateop', 'new');
	            $("tr[slotid=" + sid + "] td.delegatename span").fadeOut(150, function(){
	                $("tr[slotid=" + sid + "] td.delegatename").html("<input type=\"text\" name=\"delegatename\" value=\"Delegate Name\" />").hide().fadeIn(150);
	                $("tr[slotid=" + sid + "] td.delegateemail").html("<input type=\"text\" name=\"delegateemail\" value=\"delegate@site.com\" />").hide().fadeIn(150);  
	            });
	            Roster.opQueue.push({'op':'new', 'sid':sid});
	            Roster.setUnsaved();
	        });
        	
			// Delete a delegate.
			$(".content").delegate("#delete.delegateoption", "click", function() {
				var sid = $(this).closest('tr').attr('slotid');
				$(this).closest('tr').attr('delegateop', 'delete');
				$("tr[slotid=" + sid + "] td input[type=text]").fadeOut(150, function(){
				    $("tr[slotid=" + sid + "] td.delegatename").html("<span class=\"nodelegate\"> Click here to add a Delegate.</span>").hide().fadeIn(150);
				    $("tr[slotid=" + sid + "] td.delegateemail").html("")
				});
				Roster.opQueue.push({'op':'delete', 'sid':sid});
				Roster.setUnsaved();
			});
		},
        getDelegateId: function(obj){
            return $(obj).closest('tr').attr('delegateid');
        },
        getDelegateInput: function(did){
            return $("#roster tr.rosterrow[delegateid=" + did + "] td.delegatename input");
        },
        getDelegateName: function(did){
            return $("#roster tr.rosterrow[delegateid=" + did + "] td.delegatename input").attr('value');
        },
        getDelegateCountry: function(did){
            return $("#roster tr.rosterrow[delegateid=" + did + "] td.delegatecountry").html().trim();
        },
        getDelegateCommittee: function(did){
            return $("#roster tr.rosterrow[delegateid=" + did + "] td.delegatecommittee").html().trim();
        },
        setUnsaved: function(){
            $("#tablemenu input[type=submit]").removeClass('saved').addClass('unsaved');
        },
        setSaved: function(){
            $("#tablemenu input[type=submit]").removeClass('unsaved').addClass('saved');
        }
    };
    
    var aggregateData = function(){
        var payload = {};
        payload['csrfmiddlewaretoken'] = $("input[name=csrfmiddlewaretoken]").attr('value');
        delegates = {};
        $(".rosterrow").each(function(){
            delegates[$(this).attr('slotid')] = {
                'name': $("input[name=delegatename]", $(this)).attr('value'),
                'email': $("input[name=delegateemail]", $(this)).attr('value')
            }
        });
        payload['delegates'] = JSON.stringify(delegates);
        
        return payload;
    };
    
    $(function() {
        $(document).on("submit", "#theRoster", function() {
            var uri = $(this).attr("action");
            $.ajax({
                type: 'POST',
                url: uri,
                data: aggregateData(),
                contentType: 'application/json',
                success: function(response){ Roster.setSaved();},
                error: function(something, error, msg) {alert('didnt work, sorry: ' + msg)}
            });
            Roster.opQueue = []
            return false;
        });
        
        // Move to UI
        $("#roster input[value='" + Roster.nodelegate + "']").addClass('empty');
        
        // Move... somewhere else? Also UI?
        //$("#roster").tablesorter();
        
        /*$(document).on("click", "#switch.delegateoption", function(){
            var did = Roster.getDelegateId(this);
            if(Roster.switch1 == undefined){
                Roster.switch1 = did;
                $(this).addClass('active');
            }
            else {
                Roster.switch2 = did;
                var row1 = $("#roster tr.rosterrow[delegateid=" + Roster.switch1 + "]");
                var row2 = $("#roster tr.rosterrow[delegateid=" + Roster.switch2 + "]");
                var input1 = Roster.getDelegateInput(Roster.switch1);
                var input2 = Roster.getDelegateInput(Roster.switch2);
                var val1 = input1.val();
                var val2 = input2.val();
                Roster.setUnsaved();
                input1.fadeOut(250, function() {input1.val(val2).fadeIn(250)});
                input2.fadeOut(250, function() {input2.val(val1).fadeIn(250)});
                row1.attr('delegateid', Roster.switch2);
                row2.attr('delegateid', Roster.switch1);
                Roster.switch1 = undefined;
                Roster.switch2 = undefined;
            }
        });*/
        
        $(document).on("focus", "#roster input[type=text]", function() {
            var input = $(this);
            if(input.hasClass('empty')){
                input.val('').toggleClass('empty');
            }
        });
    
        $(document).on("blur", "#roster input[type=text]", function(){
            var input = $(this);
            if(input.val() == ''){
                input.val(Roster.nodelegate);
                input.addClass('empty');
            }
        });
    
        $(document).on("change", "#roster input[type=text]", function(){
            Roster.setUnsaved();
        });
    
        $(document).on("mouseover", "#theRoster .button", function() {
			$(this).css('cursor', 'pointer');
		});
		
		$(document).on("mouseout", "#theRoster .button", function() {
			$(this).css('cursor', 'auto');
		});
        
        
        // NEW CODE BEYOND THIS POINT
		Roster.init();
        
    });