    
    var ContentManager = {
		
		advisorManagers: [],
		chairManagers: [],
		
		/* Initializer function */
		init: function(){
			$(window).bind('hashchange', function() {
		        var newHash = window.location.hash.substring(1);
		        
		        if ($("#app").is(":hidden")) {
		            ContentManager.loadInitContent(newHash);
		        }
		        else {
		            ContentManager.loadNewContent(newHash);
		        }
   	 		});
			
			$("#container").delegate("a.nav", "click", function(){
            	window.location.hash = $(this).attr('href');
            	return false;
        	});
			
		$("#container").delegate("#appnavbar a.nav", "click", function(){
            	$("#appnavbar a.nav.currentpage").removeClass('currentpage');
            	$(this).addClass('currentpage');
        	});
			
			ContentManager.onPageLoad();
		},
		
		/* Changes the page title. */
		loadPageTitle: function(hash){
			$("title").load(hash + " title", function(){
				document.title = $(this).text();
			});
		},
		
        /* Fades the initial content into view. */
        onPageLoad: function(){
            if (window.location.hash == "") {
                if (window.location.pathname == "/") {
                    var hash = $("a.nav.default").attr("href");
                    window.location.href = "/#" + (hash ? hash : "/login");
                } else {
                    window.location.href = "/#" + window.location.pathname;
                }
            } else {
                ContentManager.triggerHashChange();
            }
        },
        
        /* Loads initial content into the application content container.*/
        loadInitContent: function(hash, data){
			ContentManager.initializeManagers();
			ContentManager.loadPageTitle(hash);
            if($("#splash").is(":visible")){
                $(".content #contentwrapper").load(hash + " #capsule", data, function(){
					$("#appnavbar a[href='" + window.location.hash.substring(1) + "']").addClass('currentpage');
                    $("#splash").delay(250).fadeOut(250, function(){
                        $("#app").delay(250).fadeIn(500, function(){
                            $("#headerwrapper").slideDown(350, function(){
                                $("#header").slideDown(350);
                            });
                        });
                    });
                });
            }
            else{
                $(".content #contentwrapper").load(hash + " #capsule", data, function(){
                    $("#app").delay(250).fadeIn(500);
                });
            }
        },
        
        /* Loads new content into the application content container. */
        loadNewContent: function(hash, data){
            $(".content").css('height', $(".content").height() + "px");
            $(".content #contentwrapper").fadeOut(150, function(){
            	$(".content").addClass("content-loading");
				ContentManager.loadPageTitle(hash);
                $(".content #contentwrapper").load(hash + " #capsule", data, function(response, status, xhr){
                    if(status == 'error') { 
                    	$("#osx-modal").modal({
                    		overlayId: 'osx-overlay',
                		containerId: 'osx-container',
                    	});
                    	//alert("Sorry, there was an error.");
                    	parent.history.back();
                    };
                    $("#contentwrapper").css({'visibility':'hidden', 'display': 'block'});
                    var height = $("#contentwrapper").height();
                    $("#contentwrapper").css({'visibility':'', 'display': 'none'});
                    $(".content").animate({height: height}, 500, function(){
                    		$(".content").removeClass("content-loading");
                            $("#contentwrapper").fadeIn(150, function(){
                                    $(".content").css('height','');
                            });
                    });
                });
            });
        },
        
		onLoginLogout: function(redirect, fadetime){
			$("#container").fadeOut(150, function(){
				$("#container").load(redirect + " #appcontainer", null, function(){
					$("#container").fadeIn(fadetime, function() {
     					window.location.href = "/#" + redirect;
     				});
				});
			});
		},
		
        /* Triggers a hash change event. */
        triggerHashChange: function(){
            $(window).trigger('hashchange');
        },
		
		/* Initializes all the managers in the advisorManagers array */
		initializeManagers: function(){
			var managers;
			type = $("span.usertype span").attr("usertype");
			if (type == "advisor"){
				managers = ContentManager.advisorManagers;	
			}
			else if (type == "chair"){
				managers = ContentManager.chairManagers;
			}
			else {
				managers = [];
			}
			for(var i = 0; i < managers.length; i++){
				managers[i].init();
			}
		}
        
    };
    
    $(function(){
		ContentManager.init();
    });

