<?php
/**
 * The template for displaying the footer.
 *
 */

if ( ! defined( 'ABSPATH' ) ) {
	exit; // Exit if accessed directly.
}
?>

	</div><!-- #content -->
</div><!-- #page -->

<?php
/**
 * lingam_before_footer hook.
 *
 */
do_action( 'lingam_before_footer' );
?>

<div <?php lingam_footer_class(); ?>>
	<?php
	/**
	 * lingam_before_footer_content hook.
	 *
	 */
	do_action( 'lingam_before_footer_content' );

	/**
	 * lingam_footer hook.
	 *
	 *
	 * @hooked lingam_construct_footer_widgets - 5
	 * @hooked lingam_construct_footer - 10
	 */
	do_action( 'lingam_footer' );

	/**
	 * lingam_after_footer_content hook.
	 *
	 */
	do_action( 'lingam_after_footer_content' );
	?>
</div><!-- .site-footer -->

<?php
/**
 * lingam_after_footer hook.
 *
 */
do_action( 'lingam_after_footer' );

wp_footer();
?>

</body>
</html>
