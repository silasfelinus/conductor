<?php
/**
 * The template for displaying posts within the loop.
 *
 */

if ( ! defined( 'ABSPATH' ) ) {
	exit; // Exit if accessed directly.
}
?>
<article id="post-<?php the_ID(); ?>" <?php post_class(); ?> <?php lingam_article_schema( 'CreativeWork' ); ?>>
	<div class="inside-article">
    	<div class="article-holder">
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
			<?php
			/**
			 * lingam_before_entry_title hook.
			 *
			 */
			do_action( 'lingam_before_entry_title' );

			the_title( sprintf( '<h2 class="entry-title" itemprop="headline"><a href="%s" rel="bookmark">', esc_url( get_permalink() ) ), '</a></h2>' );

			/**
			 * lingam_after_entry_title hook.
			 *
			 *
			 * @hooked lingam_post_meta - 10
			 */
			do_action( 'lingam_after_entry_title' );
			?>
		</header><!-- .entry-header -->

		<?php
		/**
		 * lingam_after_entry_header hook.
		 *
		 *
		 * @hooked lingam_post_image - 10
		 */
		do_action( 'lingam_after_entry_header' );

		if ( lingam_show_excerpt() ) : ?>

			<div class="entry-summary" itemprop="text">
				<?php the_excerpt(); ?>
			</div><!-- .entry-summary -->

		<?php else : ?>

			<div class="entry-content" itemprop="text">
				<?php
				the_content();

				wp_link_pages( array(
					'before' => '<div class="page-links">' . __( 'Pages:', 'lingam' ),
					'after'  => '</div>',
				) );
				?>
			</div><!-- .entry-content -->

		<?php endif;

		/**
		 * lingam_after_entry_content hook.
		 *
		 *
		 * @hooked lingam_footer_meta - 10
		 */
		do_action( 'lingam_after_entry_content' );

		/**
		 * lingam_after_content hook.
		 *
		 */
		do_action( 'lingam_after_content' );
		?>
        </div>
	</div><!-- .inside-article -->
</article><!-- #post-## -->
