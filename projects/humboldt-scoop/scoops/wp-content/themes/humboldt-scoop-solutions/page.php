<?php
/**
 * page.php — full-width canvas page (used by the portal page and any
 * content pages). Renders the block/shortcode content with no chrome.
 * @package hss
 */
if ( ! defined( 'ABSPATH' ) ) { exit; }
get_header();
?>
<?php while ( have_posts() ) : the_post(); ?>
	<div class="hss-page hss-container hss-section">
		<?php if ( ! is_front_page() ) : ?>
			<h1 class="hss-title"><?php the_title(); ?></h1>
		<?php endif; ?>
		<div class="hss-prose"><?php the_content(); ?></div>
	</div>
<?php endwhile; ?>
<?php
get_footer();
