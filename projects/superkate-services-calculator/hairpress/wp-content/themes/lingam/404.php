<?php
/**
 * The template for displaying 404 pages (Not Found).
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
			?>

			<div class="inside-article">

				<?php
				/**
				 * lingam_before_content hook.
				 *
				 *
				 * @hooked lingam_featured_page_header_inside_single - 10
				 */
				do_action( 'lingam_before_content' );
				?>

				<header class="entry-header">
					<h1 class="entry-title" itemprop="headline"><?php echo apply_filters( 'lingam_404_title', __( 'Oops! That page can&rsquo;t be found.', 'lingam' ) ); // WPCS: XSS OK. ?></h1>
				</header><!-- .entry-header -->

				<?php
				/**
				 * lingam_after_entry_header hook.
				 *
				 *
				 * @hooked lingam_post_image - 10
				 */
				do_action( 'lingam_after_entry_header' );
				?>

				<div class="entry-content" itemprop="text">
					<?php
					echo '<p>' . apply_filters( 'lingam_404_text', __( 'It looks like nothing was found at this location. Maybe try searching?', 'lingam' ) ) . '</p>'; // WPCS: XSS OK.

					get_search_form();
					?>
				</div><!-- .entry-content -->

				<?php
				/**
				 * lingam_after_content hook.
				 *
				 */
				do_action( 'lingam_after_content' );
				?>

			</div><!-- .inside-article -->

			<?php
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
