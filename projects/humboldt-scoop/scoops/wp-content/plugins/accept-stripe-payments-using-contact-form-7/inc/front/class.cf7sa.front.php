<?php
/**
 * CF7SA_Front Class
 *
 * Handles the Frontend functionality.
 *
 * @package WordPress
 * @subpackage Contact Form 7 - Stripe Add-on
 * @since 1.0
 */

// Exit if accessed directly
if ( !defined( 'ABSPATH' ) ) exit;

if ( !class_exists( 'CF7SA_Front' ) ) {

	/**
	 * The CF7SA_Front Class
	 */
	class CF7SA_Front {

		/**
		 * @var string Base URL endpoint for pages.
		 */
		
		const WEBHOOK_ENDPOINT = 'cf7sa-webhook';

		var $action = null,
		    $filter = null;

		function __construct() {
			add_filter( 'query_vars',                array( $this, 'filter__query_vars' ) );
			add_filter( 'template_include',          array( $this, 'filter__template_include' ) );

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


		/*
		######## #### ##       ######## ######## ########   ######
		##        ##  ##          ##    ##       ##     ## ##    ##
		##        ##  ##          ##    ##       ##     ## ##
		######    ##  ##          ##    ######   ########   ######
		##        ##  ##          ##    ##       ##   ##         ##
		##        ##  ##          ##    ##       ##    ##  ##    ##
		##       #### ########    ##    ######## ##     ##  ######
		*/
		/**
		 * Filter: query_vars
		 *
		 * - added query variable for custom endpoint.
		 *
		 * @param array $vars
		 *
		 * @return array
		 */
		function filter__query_vars( $vars ) {
			$vars[] = $this::WEBHOOK_ENDPOINT;
			return $vars;
		}

		/**
		 * Filter: template_include
		 *
		 * - change template call for the server configuration
		 *
		 * @param string $template
		 * @return string
		 */
		function filter__template_include( $template ) {
			global $wp_query;

			if ( isset( $wp_query->query_vars[$this::WEBHOOK_ENDPOINT] ) ) {
				return CF7SA_DIR . '/inc/front/template/cf7sa-webhook.php';
			}

			return $template;
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
