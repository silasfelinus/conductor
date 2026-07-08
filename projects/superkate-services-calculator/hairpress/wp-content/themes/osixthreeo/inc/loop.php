<?php
/**
 * The Loop
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
 * Default Loop
 */
function osixthreeo_default_loop() {

	if ( have_posts() ) :

		osixthreeo_content_while_before();

		echo '<div class="loop-wrap">';

		while ( have_posts() ) :
			the_post();
			osixthreeo_entry_before();
			get_template_part( 'template-parts/content', get_post_format() );
			osixthreeo_entry_after();
		endwhile;

		echo '</div>';

		osixthreeo_content_while_after();

		else :

			osixthreeo_entry_before();
			get_template_part( 'template-parts/content', 'none' );
			osixthreeo_entry_after();

		endif;
}
add_action( 'osixthreeo_content_loop', 'osixthreeo_default_loop' );
