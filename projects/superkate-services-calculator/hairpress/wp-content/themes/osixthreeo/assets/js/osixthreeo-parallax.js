/**
 * Public Javascript
 *
 * @since      1.4.0
 *
 * @package    osixthreeo
 * @subpackage osixthreeo/assets/js
 */

(function( $ ) {
	'use strict';

	$( window ).scroll( function() {
		$( '.osixthreeo-parallax-header .custom-header-image' ).css( 'background-position', 'center ' + (40 + $( this ).scrollTop() * -0.125) + '%' );
	} ).scroll();

})( jQuery );
