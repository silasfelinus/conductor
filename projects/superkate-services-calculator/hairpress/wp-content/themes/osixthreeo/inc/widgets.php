<?php
/**
 * Widgets.
 *
 * @package    osixthreeo
 * @subpackage osixthreeo/inc
 * @author     Chip Sheppard
 * @since      1.0.0
 * @license    GPL-2.0+
 */

if ( ! defined( 'ABSPATH' ) ) {
	exit;
}

/**
 * Register widget areas.
 */
function osixthreeo_widgets_init() {

	register_sidebar(
		array(
			'name'          => esc_html__( 'Posts Sidebar Widget Area', 'osixthreeo' ),
			'id'            => 'sidebar',
			'description'   => esc_html__( 'Posts Sidebar Widget', 'osixthreeo' ),
			'before_widget' => '<section id="%1$s" class="sidebar-widget %2$s">',
			'after_widget'  => '</section>',
			'before_title'  => '<h5 class="widget-title">',
			'after_title'   => '</h5>',
		)
	);

	register_sidebar(
		array(
			'name'          => esc_html__( 'Footer Widget Area', 'osixthreeo' ),
			'id'            => 'footer',
			'description'   => esc_html__( 'An optional widget area for your site footer. Displays at the very bottom of your website.', 'osixthreeo' ),
			'before_widget' => '<div id="%1$s" class="footer-widget %2$s">',
			'after_widget'  => '</div>',
			'before_title'  => '<h5 class="widget-title">',
			'after_title'   => '</h5>',
		)
	);
}
add_action( 'widgets_init', 'osixthreeo_widgets_init' );
