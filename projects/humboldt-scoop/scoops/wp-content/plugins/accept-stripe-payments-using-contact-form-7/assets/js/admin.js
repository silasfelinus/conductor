( function($) {
	"use strict";

	function cf7sa_sandbox_validate() {
		if ( jQuery( '.cf7sa-settings #cf7sa_use_stripe' ).prop( 'checked' ) == true && jQuery( '.cf7sa-settings #cf7sa_enable_test_mode' ).prop( 'checked' ) == true ) {
			jQuery( '.cf7sa-settings #cf7sa_test_publishable_key, .cf7sa-settings #cf7sa_test_secret_key' ).prop( 'required', true );
		} else {
			jQuery( '.cf7sa-settings #cf7sa_test_publishable_key, .cf7sa-settings #cf7sa_test_secret_key' ).removeAttr( 'required' );
		}
	}

	function cf7sa_live_validate() {
		if ( jQuery( '.cf7sa-settings #cf7sa_use_stripe' ).prop( 'checked' ) == true && jQuery( '.cf7sa-settings #cf7sa_enable_test_mode' ).prop( 'checked' ) != true ) {
			jQuery( '.cf7sa-settings #cf7sa_live_publishable_key, .cf7sa-settings #cf7sa_live_secret_key' ).prop( 'required', true );
		} else {
			jQuery( '.cf7sa-settings #cf7sa_live_publishable_key, .cf7sa-settings #cf7sa_live_secret_key' ).removeAttr( 'required' );
		}
	}

	jQuery( document ).on( 'change', '.cf7sa-settings .enable_required', function() {
		if ( jQuery( this ).prop( 'checked' ) == true ) {
			jQuery( '.cf7sa-settings #cf7sa_amount' ).prop( 'required', true );
		} else {
			jQuery( '.cf7sa-settings #cf7sa_amount' ).removeAttr( 'required' );
		}

		cf7sa_live_validate();
		cf7sa_sandbox_validate();

	} );

	jQuery( document ).on( 'change', '.cf7sa-settings #cf7sa_enable_test_mode', function() {
		cf7sa_live_validate();
		cf7sa_sandbox_validate();
	} );

	jQuery( document ).on( 'input', '.cf7sa-settings .required', function() {
		cf7sa_live_validate();
		cf7sa_sandbox_validate();
	} );

} )( jQuery );
