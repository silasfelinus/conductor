<?php
/**
 * Template part for displaying a message that posts cannot be found.
 *
 * @package    osixthreeo
 * @subpackage osixthreeo/template-parts
 * @author     Chip Sheppard
 * @since      1.0.0
 * @license    GPL-2.0+
 */

echo '<section class="no-results not-found">';
echo '<header class="page-header">';
echo '<div class="title-wrap">';

if ( is_search() ) :
	echo '<h1 class="page-title">';
	/* translators: %$2s: is the search term */
	printf( '<span>' . esc_html__( 'Search Results for:%1$s %2$s', 'osixthreeo' ), '</span>', get_search_query() );
	echo '</h1>';
else :
	echo '<h1 class="page-title">' . esc_html__( 'Nothing Found', 'osixthreeo' ) . '</h1>';
endif;

echo '</div>';
echo '</header>';

echo '<div class="page-content">';

if ( is_home() && current_user_can( 'publish_posts' ) ) :

	echo '<p>' . esc_html__( 'No posts to display.', 'osixthreeo' ) . '</p>';

elseif ( is_search() ) :

	echo '<p>' . esc_html__( 'Sorry, but nothing matched your search terms. Please try again with some different keywords.', 'osixthreeo' ) . '</p>';
	get_search_form();

else :

	echo '<p>' . esc_html__( 'It seems we can&rsquo;t find what you&rsquo;re looking for. Perhaps searching can help.', 'osixthreeo' ) . '</p>';
	get_search_form();

endif;
echo '</div>';
echo '</section>';
