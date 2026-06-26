<?php
/**
 * Plugin Name:       Humboldt Scoop Solutions — Customer Portal
 * Plugin URI:        https://humboldtscoopsolutions.com
 * Description:        Customer accounts, service plans, Stripe subscriptions & one-time payments, invoices, quote requests, and an admin dashboard for Humboldt Scoop Solutions. No paid add-ons, no plugin sprawl — direct Stripe integration.
 * Version:           1.0.0
 * Author:            Humboldt Scoop Solutions
 * License:           GPL-2.0-or-later
 * Text Domain:       hss-portal
 *
 * Stripe keys are read from the environment (constants in wp-config.php,
 * real environment variables, or a .env file in this plugin folder).
 * Nothing secret is stored in the database. See README_INSTALL.md.
 */

if ( ! defined( 'ABSPATH' ) ) { exit; }

define( 'HSS_PORTAL_VERSION', '1.1.0' );
define( 'HSS_PORTAL_FILE', __FILE__ );
define( 'HSS_PORTAL_DIR', plugin_dir_path( __FILE__ ) );
define( 'HSS_PORTAL_URL', plugin_dir_url( __FILE__ ) );

/* ── Lightweight .env loader (optional convenience) ───────────────────────
   Lets you keep keys in plugin/.env. Constants in wp-config.php and real
   server env vars both take precedence and are the recommended approach. */
if ( file_exists( HSS_PORTAL_DIR . '.env' ) ) {
	foreach ( file( HSS_PORTAL_DIR . '.env', FILE_IGNORE_NEW_LINES | FILE_SKIP_EMPTY_LINES ) as $line ) {
		$line = trim( $line );
		if ( $line === '' || $line[0] === '#' || strpos( $line, '=' ) === false ) { continue; }
		list( $k, $v ) = array_map( 'trim', explode( '=', $line, 2 ) );
		$v = trim( $v, "\"'" );
		if ( $k !== '' && ! defined( $k ) ) { define( $k, $v ); }
	}
}

/* ── Includes ─────────────────────────────────────────────────────────── */
require_once HSS_PORTAL_DIR . 'includes/class-hss-config.php';
require_once HSS_PORTAL_DIR . 'includes/class-hss-db.php';
require_once HSS_PORTAL_DIR . 'includes/class-hss-stripe.php';
require_once HSS_PORTAL_DIR . 'includes/class-hss-mail.php';
require_once HSS_PORTAL_DIR . 'includes/class-hss-sms.php';
require_once HSS_PORTAL_DIR . 'includes/class-hss-customers.php';
require_once HSS_PORTAL_DIR . 'includes/class-hss-portal.php';
require_once HSS_PORTAL_DIR . 'includes/class-hss-visits.php';
require_once HSS_PORTAL_DIR . 'includes/class-hss-change-requests.php';
require_once HSS_PORTAL_DIR . 'includes/class-hss-rest.php';
require_once HSS_PORTAL_DIR . 'admin/class-hss-admin.php';

/* ── Activation / deactivation ────────────────────────────────────────── */
register_activation_hook( __FILE__, function () {
	HSS_DB::install();
	HSS_Portal::ensure_portal_page();
	flush_rewrite_rules();
} );
register_deactivation_hook( __FILE__, 'flush_rewrite_rules' );

/* Run DB upgrades if the schema version changed between releases. */
add_action( 'plugins_loaded', [ 'HSS_DB', 'maybe_upgrade' ] );

/* ── Boot ─────────────────────────────────────────────────────────────── */
add_action( 'init', function () {
	HSS_Portal::init();
	HSS_Rest::init();
	if ( is_admin() ) {
		HSS_Admin::init();
	}
} );

/* Theme helper bridge — the front-page pricing section calls this. */
if ( ! function_exists( 'hss_portal_pricing' ) ) {
	function hss_portal_pricing() {
		return HSS_Config::pricing();
	}
}
