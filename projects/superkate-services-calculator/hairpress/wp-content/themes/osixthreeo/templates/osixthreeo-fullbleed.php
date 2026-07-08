<?php
/**
 * The template for displaying a page with no sidebar.
 *
 * Template Name: Osixthreeo Fullbleed
 *
 * @since      1.0.0
 *
 * @package    osixthreeo
 * @subpackage osixthreeo/public/partials/templates
 */

remove_action( 'osixthreeo_content_before', 'osixthreeo_get_left_sidebar' );
remove_action( 'osixthreeo_content_after', 'osixthreeo_get_right_sidebar' );
remove_action( 'osixthreeo_header_before', 'osixthreeo_widgets_display_preheader' );
remove_action( 'osixthreeo_footer_before', 'osixthreeo_widgets_display_prefooter' );
remove_filter( 'body_class', 'osixthreeo_sidebar_bodyclass' );

/**
 * Add a body class
 *
 * @param Array $classes the body classes.
 */
function osixthreeo_fullbleed_template_body_classes( $classes ) {
	$classes[] = 'osixthreeo-fullbleed';
	return $classes;
}
add_filter( 'body_class', 'osixthreeo_fullbleed_template_body_classes' );

// Build the page.
get_template_part( 'index' );
