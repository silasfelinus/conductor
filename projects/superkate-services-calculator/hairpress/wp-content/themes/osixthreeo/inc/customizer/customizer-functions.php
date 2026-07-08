<?php
/**
 * Customizer functions.
 *
 * @package    osixthreeo
 * @subpackage osixthreeo/inc/customizer
 * @author     Chip Sheppard
 * @since      1.2.0
 * @license    GPL-2.0+
 */

if ( ! defined( 'ABSPATH' ) ) {
	exit; // Exit if accessed directly.
}

/**
 * A wrapper function to get our settings.
 *
 * @since 1.3.40
 *
 * @param string $setting The option name to look up.
 * @return string The option value.
 * @todo Ability to specify different option name and defaults.
 */
function osixthreeo_get_setting( $setting ) {
	$defaults = osixthreeo_get_defaults();

	if ( ! isset( $defaults[ $setting ] ) ) {
		return;
	}

	$osixthreeo_settings = wp_parse_args(
		get_option( 'osixthreeo_settings', array() ),
		$defaults
	);
	return $osixthreeo_settings[ $setting ];
}

/**
 * SIDEBAR LAYOUTS
 * -----------------------------------------------------------------
 *
 * @return string The sidebar layout location.
 */
function osixthreeo_get_layout() {
	$layout = null;

	// Get Customizer options.
	$osixthreeo_settings = wp_parse_args(
		get_option( 'osixthreeo_settings', array() ),
		osixthreeo_get_defaults()
	);

	// If on Homepage (page.php).
	if ( is_front_page() ) {
		$layout = $osixthreeo_settings['home_layout_setting'];
	}

	// If on PAGE but not the homepage (page.php).
	if ( ! is_front_page() && ! is_search() && 'page' === get_post_type() ) {
		$layout = $osixthreeo_settings['page_layout_setting'];
	}

	// If on SINGLE (single.php) - Works for any post type, except attachments and pages.
	if ( is_single() ) {
		$layout = $osixthreeo_settings['single_layout_setting'];
	}

	// If on SEARCH (search.php).
	if ( is_search() ) {
		$layout = $osixthreeo_settings['search_layout_setting'];
	}

	// If on ARCHIVE (archive.php), HOME-blog (index.php), 404 (404.php), attachment etc...
	if ( is_home() && ! is_front_page() || is_archive() || is_tax() || is_404() ) {
		$layout = $osixthreeo_settings['archive_layout_setting'];
	}

	// Return the layout.
	return apply_filters( 'osixthreeo_sidebar_layout', $layout );
}
add_action( 'osixthreeo_init', 'osixthreeo_get_layout' );

/**
 * SIDEBAR Body Classes
 * -----------------------------------------------------------------
 *
 * @param array $classes The body classes.
 */
function osixthreeo_sidebar_bodyclass( $classes ) {
	$layout = osixthreeo_get_layout();
	if ( 'layout-ls' === $layout ) :
		$classes[] = 'sidebar-left';
	elseif ( 'layout-rs' === $layout ) :
		$classes[] = 'sidebar-right';
	elseif ( 'layout-c' === $layout ) :
		$classes[] = 'nosidebar-silo';
	endif;
	return $classes;
}
add_filter( 'body_class', 'osixthreeo_sidebar_bodyclass' );

/**
 * SIDEBAR LEFT ------------------------
 * If layout is left sidebar...
 */
function osixthreeo_get_left_sidebar() {
	$layout = osixthreeo_get_layout();
	if ( 'layout-ls' !== $layout ) :
		return;
	endif;
	get_sidebar();
}
add_action( 'osixthreeo_content_before', 'osixthreeo_get_left_sidebar' );

/**
 * SIDEBAR RIGHT ----------------------
 * If layout is right sidebar...
 */
function osixthreeo_get_right_sidebar() {
	$layout = osixthreeo_get_layout();
	if ( 'layout-rs' !== $layout ) :
		return;
	endif;
	get_sidebar();
}
add_action( 'osixthreeo_content_after', 'osixthreeo_get_right_sidebar' );


/**
 * SITE CONTAINMENT
 * -----------------------------------------------------------------
 * Adds custom class to section containers.
 */
function osixthreeo_sitecontain_class() {

	$osixthreeo_settings = wp_parse_args(
		get_option( 'osixthreeo_settings', array() ),
		osixthreeo_get_defaults()
	);

	$site_layout = $osixthreeo_settings['containment_setting'];

	if ( 'contained' === $site_layout ) {
		add_filter(
			'body_class',
			function( $classes ) {
				return array_merge( $classes, array( 'contained' ) );
			}
		);
	} else {
		return;
	}
}
add_action( 'osixthreeo_init', 'osixthreeo_sitecontain_class' );


/**
 * HEADER LAYOUT
 * -----------------------------------------------------------------
 * Adds custom class to section containers.
 */
function osixthreeo_header_layout_class() {

	$osixthreeo_settings = wp_parse_args(
		get_option( 'osixthreeo_settings', array() ),
		osixthreeo_get_defaults()
	);

	$header_layout = $osixthreeo_settings['header_layout'];

	if ( 'headercentered' === $header_layout ) {
		add_filter(
			'body_class',
			function( $classes ) {
				return array_merge( $classes, array( 'headercentered' ) );
			}
		);
	} else {
		return;
	}
}
add_action( 'osixthreeo_init', 'osixthreeo_header_layout_class' );


/**
 * HOMEPAGE HEADER FULL-HEIGHT Checkbox
 * -----------------------------------------------------------------
 * Check if full-height is selected, write a body class if it is..
 */
function osixthreeo_home_header_fullheight() {

	if ( ! is_front_page() ) {
		return;
	}

	$osixthreeo_settings = wp_parse_args(
		get_option( 'osixthreeo_settings', array() ),
		osixthreeo_get_defaults()
	);

	$header_height = $osixthreeo_settings['home_header_fullheight'];

	if ( 'full' === $header_height ) {
		add_filter(
			'body_class',
			function( $classes ) {
				return array_merge( $classes, array( 'fullheight' ) );
			}
		);
	} else {
		return;
	}
}
add_action( 'osixthreeo_init', 'osixthreeo_home_header_fullheight' );


/**
 * TAGLINE ALIGN - Checkbox
 * -----------------------------------------------------------------
 * Add a body class that aligns the tagline next to the title/logo.
 */
function osixthreeo_tagline_align() {
	$osixthreeo_settings = wp_parse_args(
		get_option( 'osixthreeo_settings', array() ),
		osixthreeo_get_defaults()
	);

	if ( ! $osixthreeo_settings['tagline_align'] ) {
		return;
	}

	add_filter(
		'body_class',
		function( $classes ) {
			return array_merge( $classes, array( 'tagline-align' ) );
		}
	);
}
add_action( 'osixthreeo_init', 'osixthreeo_tagline_align' );


/**
 * MENU SEARCH FORM - Checkbox
 * -----------------------------------------------------------------
 * Add search to primary menu if set.
 */
function osixthreeo_navigation_search() {
	$osixthreeo_settings = wp_parse_args(
		get_option( 'osixthreeo_settings', array() ),
		osixthreeo_get_defaults()
	);

	if ( ! $osixthreeo_settings['nav_search'] ) {
		return;
	}

	get_search_form();
}
add_action( 'osixthreeo_inside_navigation', 'osixthreeo_navigation_search' );


/**
 * MENU SEARCH ICON
 *
 * @param string   $nav The HTML list of menu items.
 * @param stdClass $args Object containing wp_nav_menu() arguments.
 * @return string The search icon HTML.
 */
function osixthreeo_menu_search_icon( $nav, $args ) {
	if ( ! has_nav_menu( 'primary' ) ) {
		return;
	}

	$osixthreeo_settings = wp_parse_args(
		get_option( 'osixthreeo_settings', array() ),
		osixthreeo_get_defaults()
	);

	if ( ! $osixthreeo_settings['nav_search'] ) {
		return $nav;
	}

	// only for primary menu.
	if ( 'primary' === $args->theme_location ) {
		return $nav . '<li class="search-icon" title="' . esc_attr_x( 'Search', 'submit button', 'osixthreeo' ) . '"><div class="theicon"><span class="screen-reader-text">' . _x( 'Search', 'submit button', 'osixthreeo' ) . '</span></div></li>';
	}

	return $nav;
}
add_filter( 'wp_nav_menu_items', 'osixthreeo_menu_search_icon', 10, 2 );


/**
 * TITLE LIFT - Checkbox
 * -----------------------------------------------------------------
 * Adds body class if customizer setting is true.
 */
function osixthreeo_content_title_lift_class() {

	$osixthreeo_settings = wp_parse_args(
		get_option( 'osixthreeo_settings', array() ),
		osixthreeo_get_defaults()
	);

	if ( ! $osixthreeo_settings['content_title_lift'] || is_page_template( array( 'osixthreeo-blank.php', 'osixthreeo-fullbleed.php' ) ) ) {
		return;
	}

	add_filter(
		'body_class',
		function( $classes ) {
			return array_merge(
				$classes,
				array(
					'titlelift',
				)
			);
		}
	);
}
add_action( 'osixthreeo_init', 'osixthreeo_content_title_lift_class' );


/**
 * PARALLAX HEADER - Checkbox
 * -----------------------------------------------------------------
 * Adds body class if customizer setting is true.
 */
function osixthreeo_parallax_header_class() {

	$osixthreeo_settings = wp_parse_args(
		get_option( 'osixthreeo_settings', array() ),
		osixthreeo_get_defaults()
	);

	if ( ! $osixthreeo_settings['parallax_header'] || is_page_template( array( 'page-blank.php', 'page-landing.php' ) ) ) {
		return;
	}

	add_filter(
		'body_class',
		function( $classes ) {
			return array_merge(
				$classes,
				array(
					'osixthreeo-parallax-header',
				)
			);
		}
	);
}
add_action( 'osixthreeo_init', 'osixthreeo_parallax_header_class' );


/**
 * BACK TO TOP - Checkbox
 * -----------------------------------------------------------------
 * Build the back to top button
 */
function osixthreeo_back_to_top() {

	$osixthreeo_settings = wp_parse_args(
		get_option( 'osixthreeo_settings', array() ),
		osixthreeo_get_defaults()
	);

	if ( ! $osixthreeo_settings['back_to_top'] ) {
		return;
	}

	echo '<div class="cf"></div>';
	echo '<div class="osixthreeo-backtotop"></div>';
}
add_action( 'osixthreeo_inside_footer', 'osixthreeo_back_to_top' );


/**
 * FOOTER COLUMNS - Checkbox
 * -----------------------------------------------------------------
 * Give footer widgets a class depending on how many there are.
 *
 * @link https://wordpress.stackexchange.com/questions/54162/get-number-of-widgets-in-sidebar
 * @param Array $params Sidebar parameters to target.
 */
function osixthreeo_footer_widget_params( $params ) {

	$osixthreeo_settings = wp_parse_args(
		get_option( 'osixthreeo_settings', array() ),
		osixthreeo_get_defaults()
	);

	if ( ! $osixthreeo_settings['footer_columns'] ) {
		return $params;
	}

	$sidebar_id = $params[0]['id'];

	if ( 'footer' === $sidebar_id ) {

		$total_widgets   = wp_get_sidebars_widgets();
		$sidebar_widgets = count( $total_widgets[ $sidebar_id ] );

		$params[0]['before_widget'] = str_replace( 'class="', 'class="col-1-' . floor( $sidebar_widgets ) . ' ', $params[0]['before_widget'] );
	}

	return $params;
}
add_filter( 'dynamic_sidebar_params', 'osixthreeo_footer_widget_params' );
