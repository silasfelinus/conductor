<?php
/**
 * Custom Header.
 *
 * @package    osixthreeo
 * @subpackage osixthreeo/inc
 * @author     Chip Sheppard
 * @since      1.2.0
 * @license    GPL-2.0+
 */

if ( ! defined( 'ABSPATH' ) ) {
	exit; // Exit if accessed directly.
}


if ( ! function_exists( 'osixthreeo_header_setup' ) ) :
	/**
	 * Sets up theme defaults and registers support for various WordPress features.
	 *
	 * @since 0.1
	 */
	function osixthreeo_header_setup() {
		// Custom header.
		add_theme_support( 'custom-header',
			apply_filters(
				'osixthreeo_custom_header_args',
				array(
					'default-text-color' => 'ffffff',
					'height'             => 800,
					'width'              => 1600,
					'flex-height'        => true,
					'flex-width'         => true,
					'video'              => true,
					'wp-head-callback'   => 'osixthreeo_base_css',
				)
			)
		);
	}
endif;
add_action( 'after_setup_theme', 'osixthreeo_header_setup' );


/**
 * CUSTOM HEADER
 * -----------------------------------------------------------------
 */
if ( ! function_exists( 'osixthreeo_display_customheader' ) ) {
	/**
	 * Get the Custom Header
	 * Uses  osixthreeo_customheader_image_url()
	 *       osixthreeo_customheader_content()
	 */
	function osixthreeo_display_customheader() {
		echo '<div class="custom-header">';
		echo '<div class="custom-header-image"';
		osixthreeo_customheader_image_url();
		echo '>';
		if ( is_front_page() ) :
			osixthreeo_customheader_content();
		endif;
		echo '</div>';
		echo '</div>';
	}
}
add_action( 'osixthreeo_header_after_wrap', 'osixthreeo_display_customheader' );


if ( ! function_exists( 'osixthreeo_customheader_image_url' ) ) {
	/**
	 * Write out the custom header image URL for the function above.
	 */
	function osixthreeo_customheader_image_url() {

		$blog_id        = get_option( 'page_for_posts' );
		$_post          = get_queried_object();
		$key_value      = get_post_meta( get_the_ID(), '_osixthreeo_show_featured_image', true );
		$blog_key_value = get_post_meta( $blog_id, '_osixthreeo_show_featured_image', true );

		/**
		 * Is it a Blog page (or home) that has a featured image with checkbox checked?
		 * or is it a Page or Post that has a featured image with checkbox checked?
		 */

		if ( is_home() && ! is_front_page() && has_post_thumbnail( $blog_id ) && $blog_key_value ) :
			echo ' style="background-image:url(' . esc_url( get_the_post_thumbnail_url( $blog_id, 'full' ) ) . ')"';
		elseif ( is_singular() && get_the_post_thumbnail( $_post->ID ) && $key_value ) :
			echo ' style="background-image:url(' . esc_url( get_the_post_thumbnail_url( $_post->ID, 'full' ) ) . ')"';
		elseif ( get_header_image() ) :
			echo ' style="background-image:url(' . esc_url( get_header_image() ) . ')"';
		else :
			return;
		endif;
	}
}

if ( ! function_exists( 'osixthreeo_customheader_content' ) ) {
	/**
	 * Put Video or Header Image and the Text into the Custom Header.
	 */
	function osixthreeo_customheader_content() {

		if ( ! is_front_page() ) :
			return;
		endif;

		// Get Customizer options.
		$osixthreeo_settings = wp_parse_args(
			get_option( 'osixthreeo_settings', array() ),
			osixthreeo_get_defaults()
		);

		$herotextprimary   = $osixthreeo_settings['hero_text_primary'];
		$herotextsecondary = $osixthreeo_settings['hero_text_secondary'];
		$heroscrollbar     = $osixthreeo_settings['hero_scroll_button'];

		// Get the video if there is one.
		if ( is_header_video_active() && ( has_header_video() || is_customize_preview() ) ) {
			echo '<div class="custom-header-media">';
				the_custom_header_markup();
			echo '</div>';
		}

		echo '<div class="custom-header-image-text">';

		if ( '' !== $herotextprimary ) :
			echo '<div class="hero-primary">' . wp_kses_post( $herotextprimary ) . '</div>';
		endif;
		if ( '' !== $herotextsecondary ) :
			echo '<div class="hero-secondary">' . wp_kses_post( $herotextsecondary ) . '</div>';
		endif;
		if ( true === $heroscrollbar ) :
			echo '<div class="hero-scroll-button"><a href="#custom-header-scroll-target" class="scrollbutton"><div class="arrow-down white"></div></a></div>';
		endif;

		echo '</div>';

		if ( true === $heroscrollbar ) :
			echo '<div id="custom-header-scroll-target"></div>';
		endif;
	}
}
