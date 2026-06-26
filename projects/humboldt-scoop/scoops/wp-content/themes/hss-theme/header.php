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
    <?php
    $logo_url = get_theme_mod( 'custom_logo' )
        ? wp_get_attachment_image_url( get_theme_mod( 'custom_logo' ), 'full' )
        : get_template_directory_uri() . '/assets/logo_clean.jpg';
    ?>
    <img src="<?php echo esc_url( $logo_url ); ?>" alt="<?php bloginfo( 'name' ); ?>" />
    <div>
      <span class="hss-brand-main">Humboldt</span>
      <span class="hss-brand-sub">Scoop Solutions</span>
    </div>
  </a>

  <button
    class="hss-nav-toggle"
    onclick="document.getElementById('hss-nav-links').classList.toggle('hss-open')"
    aria-label="Toggle navigation"
    aria-controls="hss-nav-links"
    aria-expanded="false"
  >
    <span></span><span></span><span></span>
  </button>

  <?php
  if ( has_nav_menu( 'primary' ) ) :
      wp_nav_menu([
          'theme_location' => 'primary',
          'container'      => false,
          'menu_id'        => 'hss-nav-links',
          'menu_class'     => 'hss-nav-links',
          'fallback_cb'    => false,
      ]);
  else : ?>
  <ul class="hss-nav-links" id="hss-nav-links">
    <li><a href="#hss-why">Why Us</a></li>
    <li><a href="#hss-services">What We Offer</a></li>
    <li><a href="#hss-pricing">Pricing</a></li>
    <li><a href="#hss-who">Who We Serve</a></li>
    <li><a href="#hss-faq">FAQ</a></li>
    <li><a href="#hss-poopstakes">Poopstakes</a></li>
    <li><a href="#hss-contact" class="hss-nav-cta">Get a Quote</a></li>
  </ul>
  <?php endif; ?>
</nav>

<main class="site-main">