<?php
/**
 * Humboldt Scoop Solutions – functions.php
 *
 * @package hss
 */

if ( ! defined( 'ABSPATH' ) ) { exit; }

define( 'HSS_THEME_VERSION', '2.0' );

/* ── Enqueue styles & scripts ─────────────────────────────────────────── */
function hss_enqueue_assets() {
	wp_enqueue_style(
		'hss-styles',
		get_template_directory_uri() . '/assets/hss.css',
		[],
		HSS_THEME_VERSION
	);

	wp_enqueue_script(
		'hss-main',
		get_template_directory_uri() . '/assets/hss.js',
		[],
		HSS_THEME_VERSION,
		true
	);
}
add_action( 'wp_enqueue_scripts', 'hss_enqueue_assets' );

/* ── Theme setup ──────────────────────────────────────────────────────── */
function hss_theme_setup() {
	add_theme_support( 'title-tag' );
	add_theme_support( 'post-thumbnails' );
	add_theme_support( 'align-wide' );
	add_theme_support( 'custom-logo' );
	add_theme_support( 'html5', [ 'search-form', 'gallery', 'caption', 'style', 'script' ] );

	register_nav_menus( [
		'primary' => __( 'Primary Navigation', 'hss' ),
	] );

	add_editor_style( 'assets/hss.css' );
}
add_action( 'after_setup_theme', 'hss_theme_setup' );

/* ── Drop Gutenberg block library styles we don't use on the brochure ──── */
function hss_dequeue_block_styles() {
	if ( is_admin() ) { return; }
	wp_dequeue_style( 'wp-block-library' );
	wp_dequeue_style( 'wp-block-library-theme' );
	wp_dequeue_style( 'global-styles' );
}
add_action( 'wp_enqueue_scripts', 'hss_dequeue_block_styles', 100 );

/**
 * Resolve the brand logo URL with a graceful fallback.
 */
function hss_logo_url() {
	$logo_id = get_theme_mod( 'custom_logo' );
	if ( $logo_id ) {
		$url = wp_get_attachment_image_url( $logo_id, 'full' );
		if ( $url ) { return $url; }
	}
	return get_template_directory_uri() . '/assets/img/logo_clean.jpg';
}

/**
 * Pricing matrix — the single source of truth for the brochure pricing
 * section. The portal plugin defines its own authoritative copy for
 * checkout; this keeps the front page working even if the plugin is off.
 * Amounts are whole dollars per month.
 */
function hss_pricing() {
	if ( function_exists( 'hss_portal_pricing' ) ) {
		return hss_portal_pricing();
	}
	return [
		'monthly'  => [ 'label' => 'Monthly',   'desc' => '1 visit per month',        'prices' => [ 1 => 19, 2 => 22, 3 => 25 ] ],
		'biweekly' => [ 'label' => 'Bi-Weekly',  'desc' => '2 visits per month',       'prices' => [ 1 => 30, 2 => 35, 3 => 40 ] ],
		'weekly'   => [ 'label' => 'Weekly',     'desc' => 'Weekly visits (~4/month)', 'prices' => [ 1 => 50, 2 => 60, 3 => 70 ] ],
	];
}

/**
 * URL of the customer portal page (created by the plugin on activation).
 */
function hss_portal_url() {
	$page = get_page_by_path( 'portal' );
	return $page ? get_permalink( $page ) : home_url( '/portal/' );
}
