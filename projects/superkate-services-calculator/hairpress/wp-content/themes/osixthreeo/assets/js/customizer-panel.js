/**
 * Customizer Hide/Show Panel functions
 *
 * @package    osixthreeo
 * @subpackage osixthreeo/assets/js
 * @author     Chip Sheppard
 * @since      1.0.0
 * @license    GPL-2.0+
 */


/*
 * Live Update Panel mods
 * https://wordpress.stackexchange.com/questions/249706/customizer-active-callback-live-toggle-controls
 */
( function( api ) {
    'use strict';

    api( 'osixthreeo_settings[home_header_fullheight]', function(setting) {
        var linkSettingValueToControlActiveState;

		/**
		  * Update a control's active state according to the boxed_body setting's value.
		  *
		  * @param {api.Control} control Boxed body control.
		  */
		 linkSettingValueToControlActiveState = function( control ) {
			 var visibility = function() {
				 if ( 'adjustable' === setting.get() || 1 === setting.get() ) {
					 control.container.slideDown( 180 );
				 } else {
					 control.container.slideUp( 180 );
				 }
			 };

			// Set initial active state.
			visibility();
			//Update activate state whenever the setting is changed.
			setting.bind( visibility );
        };

        // Call linkSettingValueToControlActiveState on the Header Height control.
		api.control( 'osixthreeo_settings[home_header_height]', linkSettingValueToControlActiveState );
		api.control( 'osixthreeo_settings[home_mobile_header_height]', linkSettingValueToControlActiveState );
    });

}( wp.customize ) );
