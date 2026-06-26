<?php
/**
 * CF7SA_Front_Action Class
 *
 * Handles the Frontend Actions.
 *
 * @package WordPress
 * @subpackage Contact Form 7 - Stripe Add-on
 * @since 1.0
 */

// Exit if accessed directly
if ( !defined( 'ABSPATH' ) ) exit;

if ( !class_exists( 'CF7SA_Front_Action' ) ){

	/**
	 *  The CF7SA_Front_Action Class
	 */
	class CF7SA_Front_Action {

		function __construct()  {

			add_action( 'wp_enqueue_scripts', array( $this, 'action__wp_enqueue_scripts' ) );

		}

		/*
		   ###     ######  ######## ####  #######  ##    ##  ######
		  ## ##   ##    ##    ##     ##  ##     ## ###   ## ##    ##
		 ##   ##  ##          ##     ##  ##     ## ####  ## ##
		##     ## ##          ##     ##  ##     ## ## ## ##  ######
		######### ##          ##     ##  ##     ## ##  ####       ##
		##     ## ##    ##    ##     ##  ##     ## ##   ### ##    ##
		##     ##  ######     ##    ####  #######  ##    ##  ######
		*/

		function action__wp_enqueue_scripts() {

			// phpcs:disable WordPress.DB.SlowDBQuery.slow_db_query_meta_key, WordPress.DB.SlowDBQuery.slow_db_query_meta_value -- Required to find forms with Stripe enabled
			$get_posts = get_posts(
				array(
					'post_type'   => 'wpcf7_contact_form',
					'numberposts' => -1,
					'meta_key'    => CF7SA_META_PREFIX . 'use_stripe',
					'meta_value'  => '1',
					'fields'      => 'ids',
				)
			);
			// phpcs:enable WordPress.DB.SlowDBQuery.slow_db_query_meta_key, WordPress.DB.SlowDBQuery.slow_db_query_meta_value

			$stripe_api = array();
			$stripe_api_style = array();

			$style = array(
				'base' => array(
					'color' => '#32325d',
					'fontSmoothing' => 'antialiased',
					'fontSize' => '16px',
				),
				'invalid' => array(
					'color' => '#fa755a',
					'iconColor' => '#fa755a'
				)
			);

			if ( !empty( $get_posts ) ) {
				foreach ( $get_posts as $id ) {
					$enable_test_mode 		 = get_post_meta( $id, CF7SA_META_PREFIX . 'enable_test_mode', true );
					$test_publishable_key    = get_post_meta( $id, CF7SA_META_PREFIX . 'test_publishable_key', true );
					$live_publishable_key    = get_post_meta( $id, CF7SA_META_PREFIX . 'live_publishable_key', true );
					$stripe_api[$id] = ( !empty( $enable_test_mode ) ? $test_publishable_key : $live_publishable_key );
					$enable_postal_code = get_post_meta($id, CF7SA_META_PREFIX . 'enable_postal_code', true);
					$stripe_api_style[$id] = apply_filters(
						CF7SA_PREFIX . '/form/stripe/' . $id,
						json_encode( $style )
					);
				}

			}

			 wp_enqueue_script( CF7SA_PREFIX . '_front_js', CF7SA_URL . 'assets/js/front.js', array( 'jquery-core' ), CF7SA_VERSION, true );
			wp_localize_script( CF7SA_PREFIX . '_front_js', 'cf7sa_object',
				array(
					'home_url' => home_url(),
					'ajax_url' => admin_url( 'admin-ajax.php' ),
					'cf7sa_active' => $get_posts,
					'cf7sa_stripe' => $stripe_api,
					'cf7sa_stripe_style' => $stripe_api_style,
					'enablePostalCode' => $enable_postal_code,
					'nonce' => wp_create_nonce( 'cf7sa_stripe_intent' ), // Security: CSRF nonce for AJAX
				)
			);

			if ( !empty( $get_posts ) ) {
				wp_enqueue_script( CF7SA_PREFIX . '_stripe', 'https://js.stripe.com/v3/', array( 'jquery-core', 'contact-form-7', CF7SA_PREFIX . '_front_js' ), '3', true );
			}

			/**
			 * Initialize script from CF7.
			 *
			 * @version 5.1.3
			 */
			wp_enqueue_script( CF7SA_PREFIX . '_front_script', CF7SA_URL . 'assets/js/scripts.js', array( 'jquery-core', 'contact-form-7', CF7SA_PREFIX . '_front_js' ), '5.1.3', true );

			wp_enqueue_style( CF7SA_PREFIX . '_front_css', CF7SA_URL . 'assets/css/front-style.min.css', array(), CF7SA_VERSION );
		}



		/*
		######## ##     ## ##    ##  ######  ######## ####  #######  ##    ##  ######
		##       ##     ## ###   ## ##    ##    ##     ##  ##     ## ###   ## ##    ##
		##       ##     ## ####  ## ##          ##     ##  ##     ## ####  ## ##
		######   ##     ## ## ## ## ##          ##     ##  ##     ## ## ## ##  ######
		##       ##     ## ##  #### ##          ##     ##  ##     ## ##  ####       ##
		##       ##     ## ##   ### ##    ##    ##     ##  ##     ## ##   ### ##    ##
		##        #######  ##    ##  ######     ##    ####  #######  ##    ##  ######
		*/

	}
}
