<?php
/**
 * The template for displaying Search Results pages.
 *
 */

if ( ! defined( 'ABSPATH' ) ) {
	exit; // Exit if accessed directly.
}

get_header(); ?>

	<div id="primary" <?php lingam_content_class(); ?>>
		<main id="main" <?php lingam_main_class(); ?>>
			<?php
			/**
			 * lingam_before_main_content hook.
			 *
			 */
			do_action( 'lingam_before_main_content' );

			if ( have_posts() ) : ?>

				<header class="page-header">
					<h1 class="page-title">
						<?php
						printf( // WPCS: XSS ok.
							/* translators: 1: Search query name */
							__( 'Search Results for: %s', 'lingam' ),
							'<span>' . get_search_query() . '</span>'
						);
						?>
					</h1>
				</header><!-- .page-header -->

				<?php while ( have_posts() ) : the_post();

					get_template_part( 'content', 'search' );

				endwhile;

				lingam_content_nav( 'nav-below' );

			else :

				get_template_part( 'no-results', 'search' );

			endif;

			/**
			 * lingam_after_main_content hook.
			 *
			 */
			do_action( 'lingam_after_main_content' );
			?>
		</main><!-- #main -->
	</div><!-- #primary -->

	<?php
	/**
	 * lingam_after_primary_content_area hook.
	 *
	 */
	 do_action( 'lingam_after_primary_content_area' );

	 lingam_construct_sidebars();

get_footer();
