<?php
/**
 * Custom functions for WooCommerce.
 *
 * @package    osixthreeo
 * @subpackage osixthreeo/inc
 * @author     Chip Sheppard
 * @since      1.0.0
 * @license    GPL-2.0+
 * @link https://docs.woocommerce.com/document/woocommerce-theme-developer-handbook/
 */

if ( ! defined( 'ABSPATH' ) ) {
	exit;
}

/**
 * Is this the Shop page?
 */
function osixthreeo_is_shop() {
	if ( OSIXTHREEO_WOOCOMMERCE_ACTIVE && is_shop() || OSIXTHREEO_WOOCOMMERCE_ACTIVE && is_product_category() || OSIXTHREEO_WOOCOMMERCE_ACTIVE && is_product_tag() ) {
		return true;
	} else {
		return false;
	}
}
/**
 * Is this a Product page?
 */
function osixthreeo_is_prod() {
	if ( OSIXTHREEO_WOOCOMMERCE_ACTIVE && is_product() ) {
		return true;
	} else {
		return false;
	}
}

/**
 * WooCommerce setup function.
 *
 * @link https://docs.woocommerce.com/document/third-party-custom-theme-compatibility/
 * @link https://github.com/woocommerce/woocommerce/wiki/Enabling-product-gallery-features-(zoom,-swipe,-lightbox)-in-3.0.0
 *
 * @return void
 */
function osixthreeo_woocommerce_setup() {
	add_theme_support( 'woocommerce' );
	add_theme_support( 'wc-product-gallery-zoom' );
	add_theme_support( 'wc-product-gallery-lightbox' );
	add_theme_support( 'wc-product-gallery-slider' );
}
add_action( 'after_setup_theme', 'osixthreeo_woocommerce_setup' );

/**
 * Products per page.
 *
 * @return integer number of products.
 */
function osixthreeo_woocommerce_products_per_page() {
	return 12;
}
add_filter( 'loop_shop_per_page', 'osixthreeo_woocommerce_products_per_page' );

/**
 * Product gallery thumnbail columns.
 *
 * @return integer number of columns.
 */
function osixthreeo_woocommerce_thumbnail_columns() {
	return 4;
}
add_filter( 'woocommerce_product_thumbnails_columns', 'osixthreeo_woocommerce_thumbnail_columns' );

/**
 * Default loop columns on product archives.
 *
 * @return integer products per row.
 */
function osixthreeo_woocommerce_loop_columns() {
	return 3;
}
add_filter( 'loop_shop_columns', 'osixthreeo_woocommerce_loop_columns' );

/**
 * Related Products Args.
 *
 * @param array $args related products args.
 * @return array $args related products args.
 */
function osixthreeo_woocommerce_related_products_args( $args ) {
	$defaults = array(
		'posts_per_page' => 3,
		'columns'        => 3,
	);
	$args     = wp_parse_args( $defaults, $args );
	return $args;
}
add_filter( 'woocommerce_output_related_products_args', 'osixthreeo_woocommerce_related_products_args' );

if ( ! function_exists( 'osixthreeo_woocommerce_product_columns_wrapper' ) ) {
	/**
	 * Product columns wrapper.
	 *
	 * @return  void
	 */
	function osixthreeo_woocommerce_product_columns_wrapper() {
		$columns = osixthreeo_woocommerce_loop_columns();
		echo '<div class="columns-' . absint( $columns ) . '">';
	}
}
add_action( 'woocommerce_before_shop_loop', 'osixthreeo_woocommerce_product_columns_wrapper', 40 );

if ( ! function_exists( 'osixthreeo_woocommerce_product_columns_wrapper_close' ) ) {
	/**
	 * Product columns wrapper close.
	 *
	 * @return  void
	 */
	function osixthreeo_woocommerce_product_columns_wrapper_close() {
		echo '</div>';
	}
}
add_action( 'woocommerce_after_shop_loop', 'osixthreeo_woocommerce_product_columns_wrapper_close', 40 );

// Remove their wrapper then add our own.
remove_action( 'woocommerce_before_main_content', 'woocommerce_output_content_wrapper', 10 );
remove_action( 'woocommerce_after_main_content', 'woocommerce_output_content_wrapper_end', 10 );
add_action( 'woocommerce_before_main_content', 'osixthreeo_theme_wrapper_start', 10 );
add_action( 'woocommerce_after_main_content', 'osixthreeo_theme_wrapper_end', 10 );

// Since we are using Woo templates in OsixthreeO territory
// we need to include our Global functions.
do_action( 'osixthreeo_init' );

/**
 * The opening wrapper.
 */
function osixthreeo_theme_wrapper_start() {
	osixthreeo_content_before();
	echo '<div id="primary" class="content-area">';
	osixthreeo_content_wrap_before();
	echo '<main id="main" class="site-main" role="main">';
	osixthreeo_content_top();
}

/**
 * The closing wrapper.
 */
function osixthreeo_theme_wrapper_end() {
	osixthreeo_content_bottom();
	echo '</main>';
	osixthreeo_content_wrap_after();
	echo '</div>';
	osixthreeo_content_after();
}

/**
 * Remove the sidebar.
 */
function osixthreeo_remove_wc_sidebar() {
	remove_action( 'woocommerce_sidebar', 'woocommerce_get_sidebar', 10 );
}
add_action( 'init', 'osixthreeo_remove_wc_sidebar' );

/**
 * Check if TitleLifted is selected, if so move Woo product title.
 */
function osixthreeo_woo_single_title() {

	$osixthreeo_settings = wp_parse_args(
		get_option( 'osixthreeo_settings', array() ),
		osixthreeo_get_defaults()
	);

	if ( true !== $osixthreeo_settings['content_title_lift'] || ! osixthreeo_is_prod() ) {
		return;
	}

	remove_action( 'woocommerce_single_product_summary', 'woocommerce_template_single_title', 5 );

	echo '<div class="entry-header"><div class="title-wrap">';
	echo '<h1 itemprop="name" class="product_title entry-title">';
	the_title();
	echo '</h1>';
	echo '</div></div>';

}
add_action( 'osixthreeo_content_top', 'osixthreeo_woo_single_title', 5 );

/**
 * Check if TitleLifted is selected, if so move Woo Shop title.
 */
function osixthreeo_woo_shop_title() {

	$osixthreeo_settings = wp_parse_args(
		get_option( 'osixthreeo_settings', array() ),
		osixthreeo_get_defaults()
	);

	if ( true !== $osixthreeo_settings['content_title_lift'] || ! osixthreeo_is_shop() ) {
		return;
	}

	add_filter( 'woocommerce_show_page_title', '__return_false' );

	echo '<div class="page-header"><div class="title-wrap">';
	echo '<h1 itemprop="name" class="page-title">';
	woocommerce_page_title();
	echo '</h1>';
	echo '</div></div>';

}
add_action( 'osixthreeo_content_top', 'osixthreeo_woo_shop_title', 5 );

/**
 * Move WooCommerce price
 */
remove_action( 'woocommerce_single_product_summary', 'woocommerce_template_single_price', 10 );
add_action( 'woocommerce_single_product_summary', 'woocommerce_template_single_price', 25 );
