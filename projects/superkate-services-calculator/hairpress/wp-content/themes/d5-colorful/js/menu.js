jQuery(document).ready(function(){ 'use strict';
								  
	jQuery("#main-menu-con ul ul").css({display: "none"}); 
	jQuery('#main-menu-con ul li').hover( function() {
		if ( jQuery(this).closest('#main-menu-con').hasClass('mainmenuconx') ) {
			jQuery(this).find('ul:first').stop(true, true).slideDown(200).css('visibility', 'visible'); jQuery(this).addClass('selected');
		}
	}, function() { 
		if ( jQuery(this).closest('#main-menu-con').hasClass('mainmenuconx') ) {
			jQuery(this).find('ul:first').stop(true, true).slideUp(200); jQuery(this).removeClass('selected'); 
		}
	});	
								  
	jQuery('.main-menu-items > li').addClass('top-level-menu');							  
	jQuery(".page_item_has_children").addClass("menu-item-has-children");
	jQuery(".page_item_has_children .children").addClass("sub-menu");
	jQuery("#main-menu-con .menu-item-home").removeClass("current-menu-item current_page_item");							  
								  
	jQuery( "#main-menu-con a" ).focusin(function() { 
		if ( jQuery(this).closest('#main-menu-con').hasClass('mainmenuconx') ) {
			jQuery(this).closest('.top-level-menu').siblings().find('.sub-menu').stop(true, true).slideUp(200);		
			jQuery(this).next('.sub-menu').stop(true, true).slideToggle(200).parent().siblings().find('.sub-menu').stop(true, true).slideUp(200); 
		}
	});								  
								  
								  
});