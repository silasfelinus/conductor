/**
 * Global JS file
 *
 * @package    osixthreeo
 * @subpackage osixthreeo/assets/js
 * @author     Chip Sheppard
 * @since      1.0.0
 * @license    GPL-2.0+
 */

/*
 * Navigation
 */
(function( $ ) {
	var masthead, menuToggle, siteNavContain, siteNavigation;

	function initMainNavigation( container ) {

		var dropdownToggle = $( '<button />', { 'class': 'dropdown-toggle', 'aria-expanded': false } )
			.append( $( '<span />', { 'class': 'screen-reader-text', 'text': 'Expand child menu' } ) );

		container.find( '.menu-item-has-children > a, .page_item_has_children > a' ).after( dropdownToggle );

		container.find( '.current-menu-ancestor > button' )
			.addClass( 'not-toggled' )
			.attr( 'aria-expanded', 'false' )
			.find( '.screen-reader-text' )
			.text( 'Expand child menu' );

		container.find( '.current-menu-ancestor > .sub-menu' ).addClass( 'not-toggled' );

		container.find( '.dropdown-toggle' ).click( function( e ) {
			var _this = $( this ),
				screenReaderSpan = _this.find( '.screen-reader-text' );

			e.preventDefault();
			_this.toggleClass( 'toggled-on' );
			_this.next( '.children, .sub-menu' ).toggleClass( 'toggled-on' );

			_this.attr( 'aria-expanded', _this.attr( 'aria-expanded' ) === 'false' ? 'true' : 'false' );

			screenReaderSpan.text( screenReaderSpan.text() === 'Expand child menu' ? 'Collapse child menu' : 'Expand child menu' );
		});
	}

	initMainNavigation( $( '.site-navigation, .topbar-widget.widget_nav_menu' ) );

	masthead       = $( '#masthead' );
	menuToggle     = masthead.find( '.responsive-menu-icon' );
	siteNavContain = masthead.find( '.site-navigation' );
	siteNavigation = masthead.find( '.site-navigation > .menu-wrap > div > ul' );

	(function() {

		if ( ! menuToggle.length ) {
			return;
		}

		menuToggle.attr( 'aria-expanded', 'false' );

		menuToggle.on( 'click', function() {
			siteNavContain.toggleClass( 'toggled-on' );

			$( this ).attr( 'aria-expanded', siteNavContain.hasClass( 'toggled-on' ) );
		});
	})();

	(function() {
		if ( ! siteNavigation.length || ! siteNavigation.children().length ) {
			return;
		}

		function toggleFocusClassTouchScreen() {
			if ( 'none' === $( '.responsive-menu-icon' ).css( 'display' ) ) {

				$( document.body ).on( 'touchstart', function( e ) {
					if ( ! $( e.target ).closest( '.site-navigation li' ).length ) {
						$( '.site-navigation li' ).removeClass( 'focus' );
					}
				} );

				siteNavigation.find( '.menu-item-has-children > a, .page_item_has_children > a' )
					.on( 'touchstart', function( e ) {
						var el = $( this ).parent( 'li' );

						if ( ! el.hasClass( 'focus' ) ) {
							e.preventDefault();
							el.toggleClass( 'focus' );
							el.siblings( '.focus' ).removeClass( 'focus' );
						}
					} );

			} else {
				siteNavigation.find( '.menu-item-has-children > a, .page_item_has_children > a' ).unbind( 'touchstart' );
			}
		}

		if ( 'ontouchstart' in window ) {
			$( window ).on( 'resize', toggleFocusClassTouchScreen );
			toggleFocusClassTouchScreen();
		}

		siteNavigation.find( 'a' ).on( 'focus blur', function() {
			$( this ).parents( '.menu-item, .page_item' ).toggleClass( 'focus' );
		} );
	} )();

	/*
	 * Adjust the tabindex of the buttons next to 'parent' menu items
	 * so they do not interfere with keyboard navigation.
	**/
	$(window).on('load resize', function() {
		if(window.innerWidth > 768) {
			$('.dropdown-toggle').attr('tabindex', -1);
		}
		if(window.innerWidth < 769) {
			$('.dropdown-toggle').removeAttr( 'tabindex' );
		}
	});


	/*
	 * SMOOTH SCROLL - homebutton
	 */
	$( '.scrollbutton' ).click(function(event) {

		if ( location.pathname.replace( /^\//, '' ) === this.pathname.replace( /^\//, '' ) && location.hostname === this.hostname ) {

			var target = $( this.hash );
			target = target.length ? target : $( '[name=' + this.hash.slice( 1 ) + ']' );

			if ( target.length ) {

				event.preventDefault();
				$( 'html, body' ).animate( {
					scrollTop: target.offset().top
					}, 600, function() {

					var $target = $( target );
					$target.focus();
					if ( $target.is( ":focus" ) ) {
						return false;
					} else {
						$target.attr( 'tabindex','-1' );
						$target.focus();
					}
				} );
			}
		}
	} );

	/*
	 * BACK TO TOP
	 */
	$( '.osixthreeo-backtotop' ).click(function() {
		$( 'html, body' ).animate( { scrollTop: 0 }, 'slow' );
		return false;
	} );

} )( jQuery );
