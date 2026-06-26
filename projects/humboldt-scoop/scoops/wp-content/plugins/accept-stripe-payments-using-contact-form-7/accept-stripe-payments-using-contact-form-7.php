<?php
/**
 * Plugin Name: Accept Stripe Payments Using Contact Form 7
 * Plugin URL: #
 * Description: This plugin will integrate Stripe payment gateway for making your payments through Contact Form 7.
 * Version: 3.3
 * Author: ZealousWeb
 * Author URI: https://www.zealousweb.com
 * Developer: The Zealousweb Team
 * Developer E-Mail: opensource@zealousweb.com
 * Text Domain: accept-stripe-payments-using-contact-form-7
 * Domain Path: /languages
 * Copyright: © 2009-2021 ZealousWeb Technologies.
 * License: GPLv3
 * License URI: http://www.gnu.org/licenses/gpl-3.0.html
 */

// Exit if accessed directly
if ( !defined( 'ABSPATH' ) ) exit;

/**
 * Basic plugin definitions
 *
 * @package Accept Stripe Payments Using Contact Form 7
 * @since 3.3
 */

if ( !defined( 'CF7SA_VERSION' ) ) {
	define( 'CF7SA_VERSION', '3.3' ); // Version of plugin
}

if ( !defined( 'CF7SA_FILE' ) ) {
	define( 'CF7SA_FILE', __FILE__ ); // Plugin File
}

if ( !defined( 'CF7SA_DIR' ) ) {
	define( 'CF7SA_DIR', dirname( __FILE__ ) ); // Plugin dir
}

if ( !defined( 'CF7SA_URL' ) ) {
	define( 'CF7SA_URL', plugin_dir_url( __FILE__ ) ); // Plugin url
}

if ( !defined( 'CF7SA_PLUGIN_BASENAME' ) ) {
	define( 'CF7SA_PLUGIN_BASENAME', plugin_basename( __FILE__ ) ); // Plugin base name
}

if ( !defined( 'CF7SA_META_PREFIX' ) ) {
	define( 'CF7SA_META_PREFIX', 'cf7sa_' ); // Plugin metabox prefix
}

if ( !defined( 'CF7SA_PREFIX' ) ) {
	define( 'CF7SA_PREFIX', 'cf7sa' ); // Plugin prefix
}

if ( !defined( 'CFSAZW_PRODUCT' ) ) {
	define( 'CFSAZW_PRODUCT', 'https://store.zealousweb.com/accept-stripe-payments-using-contact-form-7-pro' );
}

/**
 * Initialize the main class
 */
if ( !function_exists( 'CF7SA' ) ) {

	if ( is_admin() ) {
		require_once( CF7SA_DIR . '/inc/admin/class.' . CF7SA_PREFIX . '.admin.php' );
		require_once( CF7SA_DIR . '/inc/admin/class.' . CF7SA_PREFIX . '.admin.action.php' );
		require_once( CF7SA_DIR . '/inc/admin/class.' . CF7SA_PREFIX . '.admin.filter.php' );
	} else {
		require_once( CF7SA_DIR . '/inc/front/class.' . CF7SA_PREFIX . '.front.php' );
		require_once( CF7SA_DIR . '/inc/front/class.' . CF7SA_PREFIX . '.front.action.php' );
		require_once( CF7SA_DIR . '/inc/front/class.' . CF7SA_PREFIX . '.front.filter.php' );
	}

	require_once( CF7SA_DIR . '/inc/lib/class.' . CF7SA_PREFIX . '.lib.php' );

	//Initialize all the things.
	require_once( CF7SA_DIR . '/inc/class.' . CF7SA_PREFIX . '.php' );
}
