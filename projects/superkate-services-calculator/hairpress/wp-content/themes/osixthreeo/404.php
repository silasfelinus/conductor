<?php
/**
 * The template for displaying 404 pages (not found).
 *
 * @package  osixthreeo
 * @author   Chip Sheppard
 * @since    1.0.0
 * @license  GPL-2.0+
 */

do_action( 'osixthreeo_init' );

get_header();

osixthreeo_content_before();
echo '<div id="primary" class="content-area">';
osixthreeo_content_wrap_before();
echo '<main id="main" class="site-main" role="main">';
osixthreeo_content_top();
echo '<section class="error-404 not-found">';

	echo '<header class="page-header">';
		echo '<div class="title-wrap">';
		echo '<h1 class="page-title">' . esc_html__( 'Page not found.', 'osixthreeo' ) . '</h1>';
		echo '</div>';
	echo '</header>';

	echo '<div class="page-content">';
		echo '<div class="error-message">' . esc_html__( 'ERROR - ERROR - ERROR', 'osixthreeo' ) . '</div>';
		echo '<p>' . esc_html__( 'Please use the menu in the header or try a search.', 'osixthreeo' ) . '</p>';
		get_search_form();
	echo '</div>';

echo '</section>';
osixthreeo_content_bottom();
echo '</main>';
osixthreeo_content_wrap_after();
echo '</div>';
osixthreeo_content_after();

get_footer();
