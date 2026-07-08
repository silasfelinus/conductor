<?php
/**
 * Site header
 *
 * @package  osixthreeo
 * @author   Chip Sheppard
 * @since    1.0.0
 * @license  GPL-2.0+
 */

?><!doctype html>
<?php osixthreeo_html_before(); ?>
<html <?php language_attributes(); ?>>
<head>
<?php
osixthreeo_head_top();
wp_head();
osixthreeo_head_bottom();
?>
</head>
<body <?php body_class(); ?>>
<?php
if ( function_exists( 'wp_body_open' ) ) {
	wp_body_open();
} else {
	do_action( 'wp_body_open' );
}

osixthreeo_body_top();
?>
<div id="page" class="site">
	<a class="skip-link screen-reader-text" href="#content"><?php esc_html_e( 'Skip to content', 'osixthreeo' ); ?></a>

	<?php osixthreeo_header_before(); ?>
	<?php osixthreeo_header_after(); ?>

	<div id="content" class="site-content">
		<div class="content-inner-wrap">
