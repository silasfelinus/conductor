<?php
/**
 * The main template file.
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
	osixthreeo_content_loop();
	osixthreeo_content_bottom();
	echo '</main>';
	osixthreeo_content_wrap_after();
echo '</div>';
osixthreeo_content_after();

get_footer();
