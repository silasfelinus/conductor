<?php
/**
 * Jetpack Compatibility File.
 *
 * @package    osixthreeo
 * @subpackage osixthreeo/inc
 * @author     Chip Sheppard
 * @since      1.0.0
 * @license    GPL-2.0+
 * @link       https://jetpack.com/
 */

if ( ! defined( 'ABSPATH' ) ) {
	exit;
}

/**
 * Jetpack setup function.
 *
 * See: https://jetpack.com/support/infinite-scroll/
 * See: https://jetpack.com/support/responsive-videos/
 * See: https://jetpack.com/support/content-options/
 */
function osixthreeo_jetpack_setup() {
	/**
	 * Add theme support for Infinite Scroll.
	 */
	add_theme_support(
		'infinite-scroll',
		array(
			'container' => 'main',
			'render'    => 'osixthreeo_infinite_scroll_render',
			'footer'    => 'page',
		)
	);

	/**
	 * Add theme support for Responsive Videos.
	 */
	add_theme_support( 'jetpack-responsive-videos' );
}
add_action( 'after_setup_theme', 'osixthreeo_jetpack_setup' );

/**
 * Custom render function for Infinite Scroll.
 */
function osixthreeo_infinite_scroll_render() {
	while ( have_posts() ) {
		the_post();
		if ( is_search() ) :
			get_template_part( 'template-parts/content', 'search' );
		else :
			get_template_part( 'template-parts/content', get_post_format() );
		endif;
	}
}


/**
 * Add Theme support for JetPack Social Menu
 *
 * @link http://fikrirasy.id/2015/01/how-to-implement-jetpacks-site-logo-on-your-theme/
 * USAGE <?php themename_social_menu(); ?>
 */
function osixthreeo_social_menu() {
	if ( ! function_exists( 'jetpack_social_menu' ) ) {
		return;
	} else {
		jetpack_social_menu();
	}
}
add_theme_support( 'jetpack-social-menu' );
