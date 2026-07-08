/**
 * Navigation Search
 *
 * @since      1.4.0
 *
 * @package    osixthreeo
 * @subpackage osixthreeo/assets/js
 */

( function() {

	var container, form, button;

	container = document.getElementById( 'primary-navigation' );
	if ( ! container ) {
		return;
	}

	form = container.querySelector( '.search-form' );
	if ( ! form ) {
		return;
	}
	button = container.querySelector( '.search-icon' );

	button.onclick = function() {

		if ( -1 !== container.className.indexOf( 'nav-search-active' ) ) {
			container.className = container.className.replace( ' nav-search-active', '' );
			button.setAttribute( 'aria-expanded', 'false' );
		} else {
			container.className += ' nav-search-active';
			button.setAttribute( 'aria-expanded', 'true' );
		}
	};

})();
