<?php
/**
 * Header — site nav.
 * @package hss
 */
if ( ! defined( 'ABSPATH' ) ) { exit; }
?>
<!DOCTYPE html>
<html <?php language_attributes(); ?>>
<head>
	<meta charset="<?php bloginfo( 'charset' ); ?>" />
	<meta name="viewport" content="width=device-width, initial-scale=1.0" />
	<?php wp_head(); ?>
</head>
<body <?php body_class(); ?>>
<?php wp_body_open(); ?>

<nav class="hss-nav">
	<a href="<?php echo esc_url( home_url( '/' ) ); ?>" class="hss-nav-logo">
		<img src="<?php echo esc_url( hss_logo_url() ); ?>" alt="<?php bloginfo( 'name' ); ?>" />
		<span class="hss-brand">
			<span class="hss-brand-main">Humboldt</span>
			<span class="hss-brand-sub">Scoop Solutions</span>
		</span>
	</a>

	<button
		class="hss-nav-toggle"
		aria-label="Toggle navigation"
		aria-controls="hss-nav-links"
		aria-expanded="false"
	>
		<span></span><span></span><span></span>
	</button>

	<?php
	if ( has_nav_menu( 'primary' ) ) :
		wp_nav_menu( [
			'theme_location' => 'primary',
			'container'      => false,
			'menu_id'        => 'hss-nav-links',
			'menu_class'     => 'hss-nav-links',
			'fallback_cb'    => false,
		] );
	else : ?>
		<ul class="hss-nav-links" id="hss-nav-links">
			<li><a href="<?php echo esc_url( home_url( '/#hss-services' ) ); ?>">Services</a></li>
			<li><a href="<?php echo esc_url( home_url( '/#hss-pricing' ) ); ?>">Pricing</a></li>
			<li><a href="<?php echo esc_url( home_url( '/#hss-who' ) ); ?>">Who We Serve</a></li>
			<li><a href="<?php echo esc_url( home_url( '/#hss-about' ) ); ?>">About</a></li>
			<li><a href="<?php echo esc_url( home_url( '/#hss-faq' ) ); ?>">FAQ</a></li>
			<li><a href="<?php echo esc_url( home_url( '/#hss-poopstakes' ) ); ?>">Poopstakes</a></li>
			<li><a href="<?php echo esc_url( hss_portal_url() ); ?>" class="hss-nav-account">
				<?php echo is_user_logged_in() ? 'My Account' : 'Log In'; ?>
			</a></li>
			<li><a href="<?php echo esc_url( home_url( '/#hss-contact' ) ); ?>" class="hss-nav-cta">Get a Quote</a></li>
		</ul>
	<?php endif; ?>
</nav>

<main class="site-main">
