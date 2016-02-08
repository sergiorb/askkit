function container_margin_top_handler() {
	var nav_bar = $('#askkit-navbar');
	var container = $('#askkit-container');
	container.css('margin-top', nav_bar.height() + "px");
}


function avatar_handler() {

	var wrapper = $('.profile-landscape-wrapper');
	var avatar = $('.profile-info-avatar');

	var avatar_width = (wrapper.width() * 25)/100;
	var avatar_margin = (wrapper.width() * 2)/100;
	var avatar_margin_left = (wrapper.width() * 4)/100;

	if(avatar_width > 180) {

		avatar_width = 180;
	}

	if(avatar_margin > 10) {

		avatar_margin = 10;
	}

	if(avatar_margin_left > 50) {

		avatar_margin_left = 50;
	}
	/* new check it */
	if(avatar_margin_left < 20) {
		avatar_margin_left = 20;
	}

	avatar.css('height', avatar_width + 'px');
	avatar.css('width', avatar_width + 'px');
	avatar.css('margin-top', avatar_margin + 'px');
	avatar.css('margin-bottom', avatar_margin + 'px');
	avatar.css('margin-left', avatar_margin_left + 'px');
}


function askkit_collapse() {
	$('.askkit-collapse').each(function(){
	    var panel = $(this);
	    var minus = panel.find('.glyphicon-minus');
	    var plus =  panel.find('.glyphicon-plus');
	    var toggle = panel.find('.panel-toggle');
	    var collapse = panel.find('.panel-collapse');
	    var mobhidden = panel.data('mobhidden');

	    var windowWidth = $(window).width();

	    if(windowWidth <= 992) {
	    	if(mobhidden === true){
	    		collapse.collapse('hide');
	      		minus.addClass('hidden');
	    	} else {
	    		collapse.collapse('show');
	      		plus.addClass('hidden');
	    	}
	      
	    } else {
	      collapse.collapse('show');
	      plus.addClass('hidden');
	    }

	    toggle.click(function(){
	      collapse.collapse('toggle');
	    });

	    collapse.on('hidden.bs.collapse', function () {
	      minus.addClass('hidden');
	      plus.removeClass('hidden');
	    });

	    collapse.on('show.bs.collapse', function () {
	      plus.addClass('hidden');
	      minus.removeClass('hidden');
	    });        
  	});
}

function align_center(parent_id, divone_id, divtwo_id, min_screen, max_screen) {
	var parent = $(parent_id);
	var divone = parent.find(divone_id);
	var divtwo = parent.find(divtwo_id);
	var difference = Math.abs(divone.height() - divtwo.height());
	var windowWidth = $(window).width();

	if(windowWidth >= min_screen && windowWidth <= max_screen) {
		if(divone.height() > divtwo.height()) {
			divtwo.css('margin-top', difference/2 + 'px');
		} else {
			divone.css('margin-top', difference/2 + 'px');
		}
	}
}

function level_elements(from, to, min_screen, max_screen) {
	
	var windowWidth = $(window).width();
	
	if(windowWidth >= min_screen && windowWidth <= max_screen) {
		var from = $(from);
		var to = $(to);
		to.css({'height': from.height()+18+'px'});
	}
}

function center_vertical_element(parent, obj, min_screen, max_screen) {
	
	var windowWidth = $(window).width();
	var parent_height = $(parent).height();
	if(windowWidth >= min_screen && windowWidth <= max_screen) {
		$(obj).css({'margin-top':Math.abs((parent_height-$(obj).height())/2)+'px'});
	} else {
		$(obj).css({'margin-top': 0+'px'});
	}	
}