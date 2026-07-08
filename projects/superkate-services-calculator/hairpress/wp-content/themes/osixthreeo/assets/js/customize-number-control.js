/**
 * Customizer Range slider
 *
 * @package    osixthreeo
 * @subpackage osixthreeo/assets/js
 * @author     Chip Sheppard
 * @since      1.0.0
 * @license    GPL-2.0+
 */

(function ($) {
    $(document).ready(function ($) {

		// Handle the reset button
		$( '.osixthreeo-reset-number' ).on('click', function() {
			var this_input, input_default;
			var val = $(this).val();
			this_input 		= $( this ).closest( 'label' ).find( 'input' );
			input_default 	= this_input.data( 'reset_value' );

			this_input.val( input_default );
			this_input.change();

		} );
    });
})(jQuery);
