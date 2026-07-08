<?php
/**
 * Theme Customizer.
 *
 * @package    osixthreeo
 * @subpackage osixthreeo/inc
 * @author     Chip Sheppard
 * @since      1.0.0
 * @license    GPL-2.0+
 */

if ( ! defined( 'ABSPATH' ) ) {
	exit; // Exit if accessed directly.
}

add_action( 'customize_register', 'osixthreeo_set_customizer_helpers', 1 );
/**
 * Set up helpers early so they're always available.
 * Other modules might need access to them at some point.
 *
 * @since 1.0
 */
function osixthreeo_set_customizer_helpers() {
	require_once trailingslashit( get_template_directory() ) . 'inc/customizer/customizer-helpers.php';
}

if ( ! function_exists( 'osixthreeo_customize_register' ) ) {
	add_action( 'customize_register', 'osixthreeo_customize_register' );
	/**
	 * Add the Customizer options.
	 *
	 * @param WP_Customize_Manager $wp_customize Theme Customizer object.
	 */
	function osixthreeo_customize_register( $wp_customize ) {

		$defaults = osixthreeo_get_defaults();

		require_once trailingslashit( get_template_directory() ) . 'inc/customizer/customizer-helpers.php';

		$wp_customize->get_setting( 'blogname' )->transport         = 'postMessage';
		$wp_customize->get_setting( 'blogdescription' )->transport  = 'postMessage';
		$wp_customize->get_setting( 'header_image' )->transport     = 'refresh';
		$wp_customize->get_setting( 'header_textcolor' )->transport = 'postMessage';
		$wp_customize->get_control( 'header_textcolor' )->priority  = 22;

		if ( isset( $wp_customize->selective_refresh ) ) {
			$wp_customize->selective_refresh->add_partial(
				'blogname',
				array(
					'selector'        => '.site-title a',
					'render_callback' => 'osixthreeo_customize_partial_blogname',
				)
			);
			$wp_customize->selective_refresh->add_partial(
				'blogdescription',
				array(
					'selector'        => '.site-description',
					'render_callback' => 'osixthreeo_customize_partial_blogdescription',
				)
			);
		}

		/**
		 * Render the site title for the selective refresh partial.
		 */
		function osixthreeo_customize_partial_blogname() {
			bloginfo( 'name' );
		}

		/**
		 * Render the site tagline for the selective refresh partial.
		 */
		function osixthreeo_customize_partial_blogdescription() {
			bloginfo( 'description' );
		}

		$wp_customize->add_setting(
			'osixthreeo_settings[tagline_align]',
			array(
				'default'           => $defaults['tagline_align'],
				'type'              => 'option',
				'sanitize_callback' => 'osixthreeo_sanitize_checkbox',
			)
		);
		$wp_customize->add_control(
			'osixthreeo_settings[tagline_align]',
			array(
				'type'        => 'checkbox',
				'label'       => esc_html__( 'Tagline align', 'osixthreeo' ),
				'description' => esc_html__( 'Place the tagline next to the title or logo', 'osixthreeo' ),
				'section'     => 'title_tagline',
				'settings'    => 'osixthreeo_settings[tagline_align]',
				'priority'    => 50,
			)
		);

		/*
		 * LAYOUTS -------------------------------------------------------------------------
		 * tab -----------------------------------------------------------------------------
		 * ---------------------------------------------------------------------------------
		 * ---------------------------------------------------------------------------------
		 */
		$wp_customize->add_section(
			'osixthreeo_site_layout',
			array(
				'title'    => esc_html__( 'Layouts', 'osixthreeo' ),
				'priority' => 20,
			)
		);

		// SITE WIDTH.
		$wp_customize->add_setting(
			'layout-sitewidth-message',
			array(
				'sanitize_callback' => 'wp_kses_post',
			)
		);
		$wp_customize->add_control(
			new Osixthreeo_Content_Area(
				$wp_customize,
				'layout-sitewidth-message',
				array(
					'section'  => 'osixthreeo_site_layout',
					'label'    => esc_html__( 'Site Width', 'osixthreeo' ),
					'priority' => 10,
				)
			)
		);

		// Site Containment.
		$wp_customize->add_setting(
			'osixthreeo_settings[containment_setting]',
			array(
				'default'           => $defaults['containment_setting'],
				'type'              => 'option',
				'sanitize_callback' => 'osixthreeo_sanitize_choices',
				'transport'         => 'postMessage',
			)
		);
		$wp_customize->add_control(
			'osixthreeo_settings[containment_setting]',
			array(
				'type'     => 'radio',
				'label'    => esc_html__( 'Site Containment', 'osixthreeo' ),
				'section'  => 'osixthreeo_site_layout',
				'choices'  => array(
					'full'      => esc_html__( 'Full Width', 'osixthreeo' ),
					'contained' => esc_html__( 'Contained', 'osixthreeo' ),
				),
				'settings' => 'osixthreeo_settings[containment_setting]',
				'priority' => 11,
			)
		);

		// Max Width.
		$wp_customize->add_setting(
			'osixthreeo_settings[max_width]',
			array(
				'default'           => $defaults['max_width'],
				'type'              => 'option',
				'sanitize_callback' => 'osixthreeo_sanitize_integer',
				'transport'         => 'postMessage',
			)
		);
		$wp_customize->add_control(
			new Osixthreeo_Range_Control(
				$wp_customize,
				'osixthreeo_settings[max_width]',
				array(
					'type'        => 'range',
					'label'       => esc_html__( 'Max width for contained site', 'osixthreeo' ),
					'section'     => 'osixthreeo_site_layout',
					'settings'    => 'osixthreeo_settings[max_width]',
					'input_attrs' => array(
						'min'  => 800,
						'max'  => 2400,
						'step' => 5,
					),
					'priority'    => 12,
				)
			)
		);

		// LOGO/NAV BAR.
		$wp_customize->add_setting(
			'layout-header-message',
			array(
				'sanitize_callback' => 'wp_kses_post',
			)
		);
		$wp_customize->add_control(
			new Osixthreeo_Content_Area(
				$wp_customize,
				'layout-header-message',
				array(
					'label'    => esc_html__( 'Logo/Menu Align', 'osixthreeo' ),
					'section'  => 'osixthreeo_site_layout',
					'priority' => 13,
				)
			)
		);

		// Logo/Nav layout.
		$wp_customize->add_setting(
			'osixthreeo_settings[header_layout]',
			array(
				'default'           => $defaults['header_layout'],
				'type'              => 'option',
				'sanitize_callback' => 'osixthreeo_sanitize_choices',
				'transport'         => 'postMessage',
			)
		);
		$wp_customize->add_control(
			new Osixthreeo_Radio_Image_Control(
				$wp_customize,
				'osixthreeo_settings[header_layout]',
				array(
					'type'     => 'select',
					'label'    => esc_html__( 'left & right &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; centered', 'osixthreeo' ),
					'section'  => 'osixthreeo_site_layout',
					'choices'  => array(
						'headernormal'   => esc_html__( 'headernormal', 'osixthreeo' ),
						'headercentered' => esc_html__( 'headercentered', 'osixthreeo' ),
					),
					'settings' => 'osixthreeo_settings[header_layout]',
					'priority' => 14,
				)
			)
		);
		// Padding.
		$wp_customize->add_setting(
			'osixthreeo_settings[header_padding]',
			array(
				'default'           => $defaults['header_padding'],
				'type'              => 'option',
				'sanitize_callback' => 'osixthreeo_sanitize_integer',
				'transport'         => 'postMessage',
			)
		);
		$wp_customize->add_control(
			new Osixthreeo_Range_Control(
				$wp_customize,
				'osixthreeo_settings[header_padding]',
				array(
					'type'        => 'range',
					'label'       => esc_html__( 'Top/Bottom Padding', 'osixthreeo' ),
					'section'     => 'osixthreeo_site_layout',
					'settings'    => 'osixthreeo_settings[header_padding]',
					'input_attrs' => array(
						'min'  => 0,
						'max'  => 100,
						'step' => 2,
					),
					'priority'    => 15,
				)
			)
		);

		// HOMEPAGE HEADER HEIGHT ------------------------------.
		$wp_customize->add_setting(
			'layout-homeheight-message',
			array(
				'sanitize_callback' => 'wp_kses_post',
			)
		);
		$wp_customize->add_control(
			new Osixthreeo_Content_Area(
				$wp_customize,
				'layout-homeheight-message',
				array(
					'section'  => 'osixthreeo_site_layout',
					'label'    => esc_html__( 'Homepage Header Height', 'osixthreeo' ),
					'priority' => 16,
				)
			)
		);

		// homepage full height.
		$wp_customize->add_setting(
			'osixthreeo_settings[home_header_fullheight]',
			array(
				'default'           => $defaults['home_header_fullheight'],
				'type'              => 'option',
				'sanitize_callback' => 'osixthreeo_sanitize_choices',
			)
		);
		$wp_customize->add_control(
			'osixthreeo_settings[home_header_fullheight]',
			array(
				'type'     => 'radio',
				'section'  => 'osixthreeo_site_layout',
				'choices'  => array(
					'full'       => esc_html__( 'Full Height', 'osixthreeo' ),
					'adjustable' => esc_html__( 'Adjustable', 'osixthreeo' ),
				),
				'settings' => 'osixthreeo_settings[home_header_fullheight]',
				'priority' => 17,
			)
		);

		// homepage adjustable height.
		$wp_customize->add_setting(
			'osixthreeo_settings[home_header_height]',
			array(
				'default'           => $defaults['home_header_height'],
				'type'              => 'option',
				'sanitize_callback' => 'osixthreeo_sanitize_integer',
			)
		);
		$wp_customize->add_control(
			new Osixthreeo_Range_Control(
				$wp_customize,
				'osixthreeo_settings[home_header_height]',
				array(
					'type'        => 'range',
					'label'       => esc_html__( 'Desktop & large screens', 'osixthreeo' ),
					'section'     => 'osixthreeo_site_layout',
					'settings'    => 'osixthreeo_settings[home_header_height]',
					'input_attrs' => array(
						'min'  => 0,
						'max'  => 1000,
						'step' => 10,
					),
					'priority'    => 18,
				)
			)
		);
		// Homepage MOBILE height.
		$wp_customize->add_setting(
			'osixthreeo_settings[home_mobile_header_height]',
			array(
				'default'           => $defaults['home_mobile_header_height'],
				'type'              => 'option',
				'sanitize_callback' => 'osixthreeo_sanitize_integer',
			)
		);
		$wp_customize->add_control(
			new Osixthreeo_Range_Control(
				$wp_customize,
				'osixthreeo_settings[home_mobile_header_height]',
				array(
					'type'        => 'range',
					'label'       => esc_html__( 'Mobile & small screens', 'osixthreeo' ),
					'section'     => 'osixthreeo_site_layout',
					'settings'    => 'osixthreeo_settings[home_mobile_header_height]',
					'input_attrs' => array(
						'min'  => 0,
						'max'  => 600,
						'step' => 10,
					),
					'priority'    => 19,
				)
			)
		);

		// SUBPAGE HEADER.
		$wp_customize->add_setting(
			'layout-subheight-message',
			array(
				'sanitize_callback' => 'wp_kses_post',
			)
		);
		$wp_customize->add_control(
			new Osixthreeo_Content_Area(
				$wp_customize,
				'layout-subheight-message',
				array(
					'section'  => 'osixthreeo_site_layout',
					'label'    => esc_html__( 'Subpage Header Height', 'osixthreeo' ),
					'priority' => 20,
				)
			)
		);

		// subpage height.
		$wp_customize->add_setting(
			'osixthreeo_settings[subpage_header_height]',
			array(
				'default'           => $defaults['subpage_header_height'],
				'type'              => 'option',
				'sanitize_callback' => 'osixthreeo_sanitize_integer',
			)
		);
		$wp_customize->add_control(
			new Osixthreeo_Range_Control(
				$wp_customize,
				'osixthreeo_settings[subpage_header_height]',
				array(
					'type'        => 'range',
					'label'       => esc_html__( 'Desktop & large screens', 'osixthreeo' ),
					'section'     => 'osixthreeo_site_layout',
					'settings'    => 'osixthreeo_settings[subpage_header_height]',
					'input_attrs' => array(
						'min'  => 0,
						'max'  => 800,
						'step' => 5,
					),
					'priority'    => 21,
				)
			)
		);
		// subpage mobile height.
		$wp_customize->add_setting(
			'osixthreeo_settings[subpage_mobile_header_height]',
			array(
				'default'           => $defaults['subpage_mobile_header_height'],
				'type'              => 'option',
				'sanitize_callback' => 'osixthreeo_sanitize_integer',
			)
		);
		$wp_customize->add_control(
			new Osixthreeo_Range_Control(
				$wp_customize,
				'osixthreeo_settings[subpage_mobile_header_height]',
				array(
					'type'        => 'range',
					'label'       => esc_html__( 'Mobile & small screens', 'osixthreeo' ),
					'section'     => 'osixthreeo_site_layout',
					'settings'    => 'osixthreeo_settings[subpage_mobile_header_height]',
					'input_attrs' => array(
						'min'  => 0,
						'max'  => 400,
						'step' => 5,
					),
					'priority'    => 22,
				)
			)
		);

		// TITLES.
		$wp_customize->add_setting(
			'layout-titles-message',
			array(
				'sanitize_callback' => 'wp_kses_post',
			)
		);
		$wp_customize->add_control(
			new Osixthreeo_Content_Area(
				$wp_customize,
				'layout-titles-message',
				array(
					'section'  => 'osixthreeo_site_layout',
					'label'    => esc_html__( 'Title Lift', 'osixthreeo' ),
					'priority' => 23,
				)
			)
		);

		// Title Lift.
		$wp_customize->add_setting(
			'osixthreeo_settings[content_title_lift]',
			array(
				'default'           => $defaults['content_title_lift'],
				'type'              => 'option',
				'sanitize_callback' => 'osixthreeo_sanitize_checkbox',
			)
		);
		$wp_customize->add_control(
			'osixthreeo_settings[content_title_lift]',
			array(
				'type'     => 'checkbox',
				'label'    => esc_html__( 'Lift Post & Page titles up into the custom header area.', 'osixthreeo' ),
				'section'  => 'osixthreeo_site_layout',
				'settings' => 'osixthreeo_settings[content_title_lift]',
				'priority' => 24,
			)
		);

		// SIDEBARS.
		$wp_customize->add_setting(
			'layout-sidebars-message',
			array(
				'sanitize_callback' => 'wp_kses_post',
			)
		);
		$wp_customize->add_control(
			new Osixthreeo_Content_Area(
				$wp_customize,
				'layout-sidebars-message',
				array(
					'section'  => 'osixthreeo_site_layout',
					'label'    => esc_html__( 'Sidebars', 'osixthreeo' ),
					'priority' => 25,
				)
			)
		);

		// layout - home.
		$wp_customize->add_setting(
			'osixthreeo_settings[home_layout_setting]',
			array(
				'default'           => $defaults['home_layout_setting'],
				'type'              => 'option',
				'sanitize_callback' => 'osixthreeo_sanitize_choices',
			)
		);
		$wp_customize->add_control(
			new Osixthreeo_Radio_Image_Control(
				$wp_customize,
				'osixthreeo_settings[home_layout_setting]',
				array(
					'type'     => 'select',
					'label'    => esc_html__( 'Homepage', 'osixthreeo' ),
					'section'  => 'osixthreeo_site_layout',
					'choices'  => array(
						'layout-ns' => esc_html__( 'layout-ns', 'osixthreeo' ),
						'layout-ls' => esc_html__( 'layout-ls', 'osixthreeo' ),
						'layout-rs' => esc_html__( 'layout-rs', 'osixthreeo' ),
						'layout-c'  => esc_html__( 'layout-c', 'osixthreeo' ),
					),
					'settings' => 'osixthreeo_settings[home_layout_setting]',
					'priority' => 26,
				)
			)
		);

		// layout - pages.
		$wp_customize->add_setting(
			'osixthreeo_settings[page_layout_setting]',
			array(
				'default'           => $defaults['page_layout_setting'],
				'type'              => 'option',
				'sanitize_callback' => 'osixthreeo_sanitize_choices',
			)
		);
		$wp_customize->add_control(
			new Osixthreeo_Radio_Image_Control(
				$wp_customize,
				'osixthreeo_settings[page_layout_setting]',
				array(
					'type'     => 'select',
					'label'    => esc_html__( 'Pages', 'osixthreeo' ),
					'section'  => 'osixthreeo_site_layout',
					'choices'  => array(
						'layout-ns' => esc_html__( 'layout-ns', 'osixthreeo' ),
						'layout-ls' => esc_html__( 'layout-ls', 'osixthreeo' ),
						'layout-rs' => esc_html__( 'layout-rs', 'osixthreeo' ),
						'layout-c'  => esc_html__( 'layout-c', 'osixthreeo' ),
					),
					'settings' => 'osixthreeo_settings[page_layout_setting]',
					'priority' => 27,
				)
			)
		);

		// layout - single posts.
		$wp_customize->add_setting(
			'osixthreeo_settings[single_layout_setting]',
			array(
				'default'           => $defaults['single_layout_setting'],
				'type'              => 'option',
				'sanitize_callback' => 'osixthreeo_sanitize_choices',
			)
		);
		$wp_customize->add_control(
			new Osixthreeo_Radio_Image_Control(
				$wp_customize,
				'osixthreeo_settings[single_layout_setting]',
				array(
					'type'     => 'select',
					'label'    => esc_html__( 'Single Post', 'osixthreeo' ),
					'section'  => 'osixthreeo_site_layout',
					'choices'  => array(
						'layout-ns' => esc_html__( 'layout-ns', 'osixthreeo' ),
						'layout-ls' => esc_html__( 'layout-ls', 'osixthreeo' ),
						'layout-rs' => esc_html__( 'layout-rs', 'osixthreeo' ),
						'layout-c'  => esc_html__( 'layout-c', 'osixthreeo' ),
					),
					'settings' => 'osixthreeo_settings[single_layout_setting]',
					'priority' => 28,
				)
			)
		);

		// layout - archive, index & 404.
		$wp_customize->add_setting(
			'osixthreeo_settings[archive_layout_setting]',
			array(
				'default'           => $defaults['archive_layout_setting'],
				'type'              => 'option',
				'sanitize_callback' => 'osixthreeo_sanitize_choices',
			)
		);
		$wp_customize->add_control(
			new Osixthreeo_Radio_Image_Control(
				$wp_customize,
				'osixthreeo_settings[archive_layout_setting]',
				array(
					'type'     => 'select',
					'label'    => esc_html__( 'Archive/Blog', 'osixthreeo' ),
					'section'  => 'osixthreeo_site_layout',
					'choices'  => array(
						'layout-ns' => esc_html__( 'layout-ns', 'osixthreeo' ),
						'layout-ls' => esc_html__( 'layout-ls', 'osixthreeo' ),
						'layout-rs' => esc_html__( 'layout-rs', 'osixthreeo' ),
						'layout-c'  => esc_html__( 'layout-c', 'osixthreeo' ),
					),
					'settings' => 'osixthreeo_settings[archive_layout_setting]',
					'priority' => 29,
				)
			)
		);

		// layout - search.
		$wp_customize->add_setting(
			'osixthreeo_settings[search_layout_setting]',
			array(
				'default'           => $defaults['search_layout_setting'],
				'type'              => 'option',
				'sanitize_callback' => 'osixthreeo_sanitize_choices',
			)
		);
		$wp_customize->add_control(
			new Osixthreeo_Radio_Image_Control(
				$wp_customize,
				'osixthreeo_settings[search_layout_setting]',
				array(
					'type'     => 'select',
					'label'    => esc_html__( 'Search Results', 'osixthreeo' ),
					'section'  => 'osixthreeo_site_layout',
					'choices'  => array(
						'layout-ns' => esc_html__( 'layout-ns', 'osixthreeo' ),
						'layout-ls' => esc_html__( 'layout-ls', 'osixthreeo' ),
						'layout-rs' => esc_html__( 'layout-rs', 'osixthreeo' ),
						'layout-c'  => esc_html__( 'layout-c', 'osixthreeo' ),
					),
					'settings' => 'osixthreeo_settings[search_layout_setting]',
					'priority' => 30,
				)
			)
		);

		// GET EXTENSIONS.
		if ( ! OSTO_XTRAS ) :
			$wp_customize->add_setting(
				'layout-pro-callout',
				array(
					'sanitize_callback' => 'wp_kses_post',
				)
			);
			$wp_customize->add_control(
				new Osixthreeo_Content_Area(
					$wp_customize,
					'layout-pro-callout',
					array(
						'section'  => 'osixthreeo_site_layout',
						'label'    => esc_html__( 'Get more layout controls with an OsixthreeO Extension', 'osixthreeo' ),
						'content'  => '<a href="' . OSIXTHREEO_THEME_LINK . '" class="probtn" target="_blank" rel="noopener">OsixthreeO.com</a>',
						'priority' => 100,
					)
				)
			);
		endif;

		/*
		 * COLORS --------------------------------------------------------------------------
		 * tab -----------------------------------------------------------------------------
		 * ---------------------------------------------------------------------------------
		 * ---------------------------------------------------------------------------------
		 */

		// HEADER ---------------------------------------------------
		// section message.
		$wp_customize->add_setting(
			'colors-logomenu-message',
			array(
				'sanitize_callback' => 'wp_kses_post',
			)
		);
		$wp_customize->add_control(
			new Osixthreeo_Content_Area(
				$wp_customize,
				'colors-logomenu-message',
				array(
					'section'  => 'colors',
					'label'    => esc_html__( 'Header Bar', 'osixthreeo' ),
					'priority' => 20,
				)
			)
		);

		// background.
		$wp_customize->add_setting(
			'osixthreeo_settings[header_background_color]',
			array(
				'default'           => $defaults['header_background_color'],
				'type'              => 'option',
				'sanitize_callback' => 'osixthreeo_sanitize_rgba',
				'transport'         => 'postMessage',
			)
		);
		$wp_customize->add_control(
			new Osixthreeo_Alpha_Color_Control(
				$wp_customize,
				'osixthreeo_settings[header_background_color]',
				array(
					'label'        => esc_html__( 'Background color', 'osixthreeo' ),
					'section'      => 'colors',
					'settings'     => 'osixthreeo_settings[header_background_color]',
					'show_opacity' => true,
					'priority'     => 21,
				)
			)
		);

		// menu link.
		// lots of :before & :after used here... NO 'transport' => 'postMessage'.
		$wp_customize->add_setting(
			'osixthreeo_settings[nav_link_color]',
			array(
				'default'           => $defaults['nav_link_color'],
				'type'              => 'option',
				'sanitize_callback' => 'sanitize_hex_color',
			)
		);
		$wp_customize->add_control(
			new WP_Customize_Color_Control(
				$wp_customize,
				'osixthreeo_settings[nav_link_color]',
				array(
					'label'    => esc_html__( 'Menu links', 'osixthreeo' ),
					'section'  => 'colors',
					'settings' => 'osixthreeo_settings[nav_link_color]',
					'priority' => 23,
				)
			)
		);
		// background HOMEPAGE.
		$wp_customize->add_setting(
			'osixthreeo_settings[header_background_color_home]',
			array(
				'default'           => $defaults['header_background_color_home'],
				'type'              => 'option',
				'sanitize_callback' => 'osixthreeo_sanitize_rgba',
			)
		);
		$wp_customize->add_control(
			new Osixthreeo_Alpha_Color_Control(
				$wp_customize,
				'osixthreeo_settings[header_background_color_home]',
				array(
					'label'        => esc_html__( 'Background color (homepage only)', 'osixthreeo' ),
					'section'      => 'colors',
					'settings'     => 'osixthreeo_settings[header_background_color_home]',
					'show_opacity' => true,
					'priority'     => 24,
				)
			)
		);

		// MOBILE/SUBNAV section message.
		$wp_customize->add_setting(
			'colors-subnav-message',
			array(
				'sanitize_callback' => 'wp_kses_post',
			)
		);
		$wp_customize->add_control(
			new Osixthreeo_Content_Area(
				$wp_customize,
				'colors-subnav-message',
				array(
					'section'  => 'colors',
					'label'    => esc_html__( 'Mobile menu & Sub menus', 'osixthreeo' ),
					'priority' => 30,
				)
			)
		);

		// subnav link bg.
		$wp_customize->add_setting(
			'osixthreeo_settings[subnav_bg_color]',
			array(
				'default'           => $defaults['subnav_bg_color'],
				'type'              => 'option',
				'sanitize_callback' => 'sanitize_hex_color',
			)
		);
		$wp_customize->add_control(
			new WP_Customize_Color_Control(
				$wp_customize,
				'osixthreeo_settings[subnav_bg_color]',
				array(
					'label'    => esc_html__( 'Background', 'osixthreeo' ),
					'section'  => 'colors',
					'settings' => 'osixthreeo_settings[subnav_bg_color]',
					'priority' => 31,
				)
			)
		);
		// subnav hover bg.
		$wp_customize->add_setting(
			'osixthreeo_settings[subnav_hover_bg_color]',
			array(
				'default'           => $defaults['subnav_hover_bg_color'],
				'type'              => 'option',
				'sanitize_callback' => 'sanitize_hex_color',
			)
		);
		$wp_customize->add_control(
			new WP_Customize_Color_Control(
				$wp_customize,
				'osixthreeo_settings[subnav_hover_bg_color]',
				array(
					'label'    => esc_html__( 'Hover background', 'osixthreeo' ),
					'section'  => 'colors',
					'settings' => 'osixthreeo_settings[subnav_hover_bg_color]',
					'priority' => 32,
				)
			)
		);
		// subnav links.
		$wp_customize->add_setting(
			'osixthreeo_settings[subnav_text_color]',
			array(
				'default'           => $defaults['subnav_text_color'],
				'type'              => 'option',
				'sanitize_callback' => 'sanitize_hex_color',
			)
		);
		$wp_customize->add_control(
			new WP_Customize_Color_Control(
				$wp_customize,
				'osixthreeo_settings[subnav_text_color]',
				array(
					'label'    => esc_html__( 'Links', 'osixthreeo' ),
					'section'  => 'colors',
					'settings' => 'osixthreeo_settings[subnav_text_color]',
					'priority' => 33,
				)
			)
		);
		// subnav links hover.
		$wp_customize->add_setting(
			'osixthreeo_settings[subnav_hover_text_color]',
			array(
				'default'           => $defaults['subnav_hover_text_color'],
				'type'              => 'option',
				'sanitize_callback' => 'sanitize_hex_color',
			)
		);
		$wp_customize->add_control(
			new WP_Customize_Color_Control(
				$wp_customize,
				'osixthreeo_settings[subnav_hover_text_color]',
				array(
					'label'    => esc_html__( 'Hover links', 'osixthreeo' ),
					'section'  => 'colors',
					'settings' => 'osixthreeo_settings[subnav_hover_text_color]',
					'priority' => 34,
				)
			)
		);
		// subnav border.
		$wp_customize->add_setting(
			'osixthreeo_settings[subnav_border_color]',
			array(
				'default'           => $defaults['subnav_border_color'],
				'type'              => 'option',
				'sanitize_callback' => 'sanitize_hex_color',
			)
		);
		$wp_customize->add_control(
			new WP_Customize_Color_Control(
				$wp_customize,
				'osixthreeo_settings[subnav_border_color]',
				array(
					'label'    => esc_html__( 'Border', 'osixthreeo' ),
					'section'  => 'colors',
					'settings' => 'osixthreeo_settings[subnav_border_color]',
					'priority' => 35,
				)
			)
		);

		// sticky nav colors 40s.
		// CONTENT AREA section message ------------------------------------.
		$wp_customize->add_setting(
			'colors-content-message',
			array(
				'sanitize_callback' => 'wp_kses_post',
			)
		);
		$wp_customize->add_control(
			new Osixthreeo_Content_Area(
				$wp_customize,
				'colors-content-message',
				array(
					'section'  => 'colors',
					'label'    => esc_html__( 'Post & Page Content', 'osixthreeo' ),
					'priority' => 50,
				)
			)
		);

		// content area bg.
		$wp_customize->add_setting(
			'osixthreeo_settings[content_bgcolor]',
			array(
				'default'           => $defaults['content_bgcolor'],
				'type'              => 'option',
				'sanitize_callback' => 'osixthreeo_sanitize_rgba',
				'transport'         => 'postMessage',
			)
		);
		$wp_customize->add_control(
			new Osixthreeo_Alpha_Color_Control(
				$wp_customize,
				'osixthreeo_settings[content_bgcolor]',
				array(
					'label'        => esc_html__( 'Background', 'osixthreeo' ),
					'section'      => 'colors',
					'settings'     => 'osixthreeo_settings[content_bgcolor]',
					'show_opacity' => true,
					'priority'     => 51,
				)
			)
		);
		// TITLEs.
		$wp_customize->add_setting(
			'osixthreeo_settings[content_title_color]',
			array(
				'default'           => $defaults['content_title_color'],
				'type'              => 'option',
				'sanitize_callback' => 'sanitize_hex_color',
				'transport'         => 'postMessage',
			)
		);
		$wp_customize->add_control(
			new WP_Customize_Color_Control(
				$wp_customize,
				'osixthreeo_settings[content_title_color]',
				array(
					'label'    => esc_html__( 'Title Color', 'osixthreeo' ),
					'section'  => 'colors',
					'settings' => 'osixthreeo_settings[content_title_color]',
					'priority' => 52,
				)
			)
		);
		// text.
		$wp_customize->add_setting(
			'osixthreeo_settings[text_color]',
			array(
				'default'           => $defaults['text_color'],
				'type'              => 'option',
				'sanitize_callback' => 'sanitize_hex_color',
				'transport'         => 'postMessage',
			)
		);
		$wp_customize->add_control(
			new WP_Customize_Color_Control(
				$wp_customize,
				'osixthreeo_settings[text_color]',
				array(
					'label'    => esc_html__( 'Text', 'osixthreeo' ),
					'section'  => 'colors',
					'settings' => 'osixthreeo_settings[text_color]',
					'priority' => 53,
				)
			)
		);
		// links - primary highlight.
		$wp_customize->add_setting(
			'osixthreeo_settings[link_color]',
			array(
				'default'           => $defaults['link_color'],
				'type'              => 'option',
				'sanitize_callback' => 'sanitize_hex_color',
			)
		);
		$wp_customize->add_control(
			new WP_Customize_Color_Control(
				$wp_customize,
				'osixthreeo_settings[link_color]',
				array(
					'label'    => esc_html__( 'Links', 'osixthreeo' ),
					'section'  => 'colors',
					'settings' => 'osixthreeo_settings[link_color]',
					'priority' => 54,
				)
			)
		);
		// links hover - secondary highlight.
		$wp_customize->add_setting(
			'osixthreeo_settings[link_color_hover]',
			array(
				'default'           => $defaults['link_color_hover'],
				'type'              => 'option',
				'sanitize_callback' => 'sanitize_hex_color',
			)
		);
		$wp_customize->add_control(
			new WP_Customize_Color_Control(
				$wp_customize,
				'osixthreeo_settings[link_color_hover]',
				array(
					'label'    => esc_html__( 'Hover links', 'osixthreeo' ),
					'section'  => 'colors',
					'settings' => 'osixthreeo_settings[link_color_hover]',
					'priority' => 55,
				)
			)
		);
		// Post Meta color.
		$wp_customize->add_setting(
			'osixthreeo_settings[meta_color]',
			array(
				'default'           => $defaults['meta_color'],
				'type'              => 'option',
				'sanitize_callback' => 'sanitize_hex_color',
				'transport'         => 'postMessage',
			)
		);
		$wp_customize->add_control(
			new WP_Customize_Color_Control(
				$wp_customize,
				'osixthreeo_settings[meta_color]',
				array(
					'label'    => esc_html__( 'Meta Data (author, date, tags, etc...)', 'osixthreeo' ),
					'section'  => 'colors',
					'settings' => 'osixthreeo_settings[meta_color]',
					'priority' => 56,
				)
			)
		);

		// Archives section message --------------------------------------.
		$wp_customize->add_setting(
			'colors-archives-message',
			array(
				'sanitize_callback' => 'wp_kses_post',
			)
		);
		$wp_customize->add_control(
			new Osixthreeo_Content_Area(
				$wp_customize,
				'colors-archives-message',
				array(
					'section'  => 'colors',
					'label'    => esc_html__( 'Blog, Archive & Search entries', 'osixthreeo' ),
					'priority' => 60,
				)
			)
		);
		// Background.
		$wp_customize->add_setting(
			'osixthreeo_settings[archives_background_color]',
			array(
				'default'           => $defaults['archives_background_color'],
				'type'              => 'option',
				'sanitize_callback' => 'osixthreeo_sanitize_rgba',
				'transport'         => 'postMessage',
			)
		);
		$wp_customize->add_control(
			new Osixthreeo_Alpha_Color_Control(
				$wp_customize,
				'osixthreeo_settings[archives_background_color]',
				array(
					'label'    => esc_html__( 'Background', 'osixthreeo' ),
					'section'  => 'colors',
					'settings' => 'osixthreeo_settings[archives_background_color]',
					'priority' => 61,
				)
			)
		);
		// text.
		$wp_customize->add_setting(
			'osixthreeo_settings[archives_title_color]',
			array(
				'default'           => $defaults['archives_title_color'],
				'type'              => 'option',
				'sanitize_callback' => 'sanitize_hex_color',
				'transport'         => 'postMessage',
			)
		);
		$wp_customize->add_control(
			new WP_Customize_Color_Control(
				$wp_customize,
				'osixthreeo_settings[archives_title_color]',
				array(
					'label'    => esc_html__( 'Titles', 'osixthreeo' ),
					'section'  => 'colors',
					'settings' => 'osixthreeo_settings[archives_title_color]',
					'priority' => 62,
				)
			)
		);
		// text.
		$wp_customize->add_setting(
			'osixthreeo_settings[archives_text_color]',
			array(
				'default'           => $defaults['archives_text_color'],
				'type'              => 'option',
				'sanitize_callback' => 'sanitize_hex_color',
				'transport'         => 'postMessage',
			)
		);
		$wp_customize->add_control(
			new WP_Customize_Color_Control(
				$wp_customize,
				'osixthreeo_settings[archives_text_color]',
				array(
					'label'    => esc_html__( 'Text', 'osixthreeo' ),
					'section'  => 'colors',
					'settings' => 'osixthreeo_settings[archives_text_color]',
					'priority' => 63,
				)
			)
		);
		// links.
		$wp_customize->add_setting(
			'osixthreeo_settings[archives_link_color]',
			array(
				'default'           => $defaults['archives_link_color'],
				'type'              => 'option',
				'sanitize_callback' => 'sanitize_hex_color',
				'transport'         => 'postMessage',
			)
		);
		$wp_customize->add_control(
			new WP_Customize_Color_Control(
				$wp_customize,
				'osixthreeo_settings[archives_link_color]',
				array(
					'label'    => esc_html__( 'Links', 'osixthreeo' ),
					'section'  => 'colors',
					'settings' => 'osixthreeo_settings[archives_link_color]',
					'priority' => 64,
				)
			)
		);
		// links hover.
		$wp_customize->add_setting(
			'osixthreeo_settings[archives_link_color_hover]',
			array(
				'default'           => $defaults['archives_link_color_hover'],
				'type'              => 'option',
				'sanitize_callback' => 'sanitize_hex_color',
				'transport'         => 'postMessage',
			)
		);
		$wp_customize->add_control(
			new WP_Customize_Color_Control(
				$wp_customize,
				'osixthreeo_settings[archives_link_color_hover]',
				array(
					'label'    => esc_html__( 'Hover links', 'osixthreeo' ),
					'section'  => 'colors',
					'settings' => 'osixthreeo_settings[archives_link_color_hover]',
					'priority' => 65,
				)
			)
		);
		// Post Meta color.
		$wp_customize->add_setting(
			'osixthreeo_settings[archives_meta_color]',
			array(
				'default'           => $defaults['archives_meta_color'],
				'type'              => 'option',
				'sanitize_callback' => 'sanitize_hex_color',
				'transport'         => 'postMessage',
			)
		);
		$wp_customize->add_control(
			new WP_Customize_Color_Control(
				$wp_customize,
				'osixthreeo_settings[archives_meta_color]',
				array(
					'label'    => esc_html__( 'Meta Data (author, date, comments, etc...)', 'osixthreeo' ),
					'section'  => 'colors',
					'settings' => 'osixthreeo_settings[archives_meta_color]',
					'priority' => 66,
				)
			)
		);

		// FOOTER section message --------------------------------------.
		$wp_customize->add_setting(
			'colors-footer-message',
			array(
				'sanitize_callback' => 'wp_kses_post',
			)
		);
		$wp_customize->add_control(
			new Osixthreeo_Content_Area(
				$wp_customize,
				'colors-footer-message',
				array(
					'section'  => 'colors',
					'label'    => esc_html__( 'Footer', 'osixthreeo' ),
					'priority' => 90,
				)
			)
		);
		// bg.
		$wp_customize->add_setting(
			'osixthreeo_settings[footer_background_color]',
			array(
				'default'           => $defaults['footer_background_color'],
				'type'              => 'option',
				'sanitize_callback' => 'sanitize_hex_color',
				'transport'         => 'postMessage',
			)
		);
		$wp_customize->add_control(
			new WP_Customize_Color_Control(
				$wp_customize,
				'osixthreeo_settings[footer_background_color]',
				array(
					'label'    => esc_html__( 'Background', 'osixthreeo' ),
					'section'  => 'colors',
					'settings' => 'osixthreeo_settings[footer_background_color]',
					'priority' => 91,
				)
			)
		);
		// title.
		$wp_customize->add_setting(
			'osixthreeo_settings[footer_title_color]',
			array(
				'default'           => $defaults['footer_title_color'],
				'type'              => 'option',
				'sanitize_callback' => 'sanitize_hex_color',
				'transport'         => 'postMessage',
			)
		);
		$wp_customize->add_control(
			new WP_Customize_Color_Control(
				$wp_customize,
				'osixthreeo_settings[footer_title_color]',
				array(
					'label'    => esc_html__( 'Title', 'osixthreeo' ),
					'section'  => 'colors',
					'settings' => 'osixthreeo_settings[footer_title_color]',
					'priority' => 92,
				)
			)
		);
		// text.
		$wp_customize->add_setting(
			'osixthreeo_settings[footer_text_color]',
			array(
				'default'           => $defaults['footer_text_color'],
				'type'              => 'option',
				'sanitize_callback' => 'sanitize_hex_color',
				'transport'         => 'postMessage',
			)
		);
		$wp_customize->add_control(
			new WP_Customize_Color_Control(
				$wp_customize,
				'osixthreeo_settings[footer_text_color]',
				array(
					'label'    => esc_html__( 'Text', 'osixthreeo' ),
					'section'  => 'colors',
					'settings' => 'osixthreeo_settings[footer_text_color]',
					'priority' => 93,
				)
			)
		);
		// links.
		$wp_customize->add_setting(
			'osixthreeo_settings[footer_link_color]',
			array(
				'default'           => $defaults['footer_link_color'],
				'type'              => 'option',
				'sanitize_callback' => 'sanitize_hex_color',
				'transport'         => 'postMessage',
			)
		);
		$wp_customize->add_control(
			new WP_Customize_Color_Control(
				$wp_customize,
				'osixthreeo_settings[footer_link_color]',
				array(
					'label'    => esc_html__( 'Links', 'osixthreeo' ),
					'section'  => 'colors',
					'settings' => 'osixthreeo_settings[footer_link_color]',
					'priority' => 94,
				)
			)
		);
		// links hover.
		$wp_customize->add_setting(
			'osixthreeo_settings[footer_link_color_hover]',
			array(
				'default'           => $defaults['footer_link_color_hover'],
				'type'              => 'option',
				'sanitize_callback' => 'sanitize_hex_color',
				'transport'         => 'postMessage',
			)
		);
		$wp_customize->add_control(
			new WP_Customize_Color_Control(
				$wp_customize,
				'osixthreeo_settings[footer_link_color_hover]',
				array(
					'label'    => esc_html__( 'Hover links', 'osixthreeo' ),
					'section'  => 'colors',
					'settings' => 'osixthreeo_settings[footer_link_color_hover]',
					'priority' => 95,
				)
			)
		);

		// GET EXTENSIONS.
		if ( ! OSTO_XTRAS ) :
			$wp_customize->add_setting(
				'colors-pro-callout',
				array(
					'sanitize_callback' => 'wp_kses_post',
				)
			);
			$wp_customize->add_control(
				new Osixthreeo_Content_Area(
					$wp_customize,
					'colors-pro-callout',
					array(
						'section'  => 'colors',
						'label'    => esc_html__( 'Get more color controls with an OsixthreeO Extension', 'osixthreeo' ),
						'content'  => '<a href="' . OSIXTHREEO_THEME_LINK . '" class="probtn" target="_blank" rel="noopener">OsixthreeO.com</a>',
						'priority' => 200,
					)
				)
			);
		endif;

		/*
		 * TYPOGRAPHY ----------------------------------------------------------------------
		 * tab -----------------------------------------------------------------------------
		 * ---------------------------------------------------------------------------------
		 * ---------------------------------------------------------------------------------
		 */
		$wp_customize->add_section(
			'osixthreeo_typography',
			array(
				'title'    => esc_html__( 'Typography', 'osixthreeo' ),
				'priority' => 40,
			)
		);

		// 3 FONTS.
		$wp_customize->add_setting(
			'typography-fonts-message',
			array(
				'sanitize_callback' => 'wp_kses_post',
			)
		);
		$wp_customize->add_control(
			new Osixthreeo_Content_Area(
				$wp_customize,
				'typography-fonts-message',
				array(
					'section'  => 'osixthreeo_typography',
					'label'    => esc_html__( '3 Fonts', 'osixthreeo' ),
					'priority' => 1,
				)
			)
		);

		// base font.
		$wp_customize->add_setting(
			'osixthreeo_settings[base_font]',
			array(
				'default'           => $defaults['base_font'],
				'type'              => 'option',
				'sanitize_callback' => 'osixthreeo_sanitize_choices',
			)
		);
		$wp_customize->add_control(
			'osixthreeo_settings[base_font]',
			array(
				'type'     => 'select',
				'label'    => esc_html__( 'Base Font', 'osixthreeo' ),
				'section'  => 'osixthreeo_typography',
				'choices'  => array(
					''                     => esc_html__( 'Arial - default', 'osixthreeo' ),
					'georgia'              => esc_html__( 'Georgia', 'osixthreeo' ),
					'verdana'              => esc_html__( 'Verdana', 'osixthreeo' ),
					'trebuchet'            => esc_html__( 'Trebuchet', 'osixthreeo' ),
					'palatino'             => esc_html__( 'Palatino', 'osixthreeo' ),
					'tahoma'               => esc_html__( 'Tahoma', 'osixthreeo' ),
					'times'                => esc_html__( 'Times', 'osixthreeo' ),
					'arialblack'           => esc_html__( 'Arial Black', 'osixthreeo' ),
					'impact'               => esc_html__( 'Impact', 'osixthreeo' ),
					'copperplate'          => esc_html__( 'Copperplate', 'osixthreeo' ),
					'papyrus'              => esc_html__( 'Papyrus', 'osixthreeo' ),
					'courier'              => esc_html__( 'Courier', 'osixthreeo' ),
					'lucidatypewritter'    => esc_html__( 'Lucida Typewritter', 'osixthreeo' ),
					'comicsans'            => esc_html__( 'Comic Sans', 'osixthreeo' ),
					'alegreya'             => esc_html__( 'Alegreya', 'osixthreeo' ),
					'alegreyasc'           => esc_html__( 'Alegreya SC', 'osixthreeo' ),
					'alegreyasans'         => esc_html__( 'Alegreya Sans', 'osixthreeo' ),
					'alegreyasanssc'       => esc_html__( 'Alegreya Sans SC', 'osixthreeo' ),
					'archivo'              => esc_html__( 'Archivo', 'osixthreeo' ),
					'archivonarrow'        => esc_html__( 'Archivo Narrow', 'osixthreeo' ),
					'arvo'                 => esc_html__( 'Arvo', 'osixthreeo' ),
					'abrilfatface'         => esc_html__( 'Abril Fatface', 'osixthreeo' ),
					'alfaslabone'          => esc_html__( 'Alfa Slab One', 'osixthreeo' ),
					'b612'                 => esc_html__( 'B612', 'osixthreeo' ),
					'biothyme'             => esc_html__( 'BioRhyme', 'osixthreeo' ),
					'baloo'                => esc_html__( 'Baloo', 'osixthreeo' ),
					'barrio'               => esc_html__( 'Barrio', 'osixthreeo' ),
					'blackopsone'          => esc_html__( 'Black Ops One', 'osixthreeo' ),
					'cabin'                => esc_html__( 'Cabin', 'osixthreeo' ),
					'cairo'                => esc_html__( 'Cairo', 'osixthreeo' ),
					'chivo'                => esc_html__( 'Chivo', 'osixthreeo' ),
					'cardo'                => esc_html__( 'Cardo', 'osixthreeo' ),
					'cormorant'            => esc_html__( 'Cormorant', 'osixthreeo' ),
					'crimsontext'          => esc_html__( 'Crimson Text', 'osixthreeo' ),
					'cabinsketch'          => esc_html__( 'Cabin Sketch', 'osixthreeo' ),
					'chelaone'             => esc_html__( 'Chela One', 'osixthreeo' ),
					'concertone'           => esc_html__( 'Concert One', 'osixthreeo' ),
					'domine'               => esc_html__( 'Domine', 'osixthreeo' ),
					'exo2'                 => esc_html__( 'Exo 2', 'osixthreeo' ),
					'eczar'                => esc_html__( 'Eczar', 'osixthreeo' ),
					'ericaone'             => esc_html__( 'Erica One', 'osixthreeo' ),
					'fjallaone'            => esc_html__( 'Fjalla One', 'osixthreeo' ),
					'firasans'             => esc_html__( 'Fira Sans', 'osixthreeo' ),
					'frankruhllibre'       => esc_html__( 'Frank Ruhl Libre', 'osixthreeo' ),
					'fascinate'            => esc_html__( 'Fascinate', 'osixthreeo' ),
					'flamenco'             => esc_html__( 'Flamenco', 'osixthreeo' ),
					'frederickathegreat'   => esc_html__( 'Fredericka the Great', 'osixthreeo' ),
					'ibmplexsans'          => esc_html__( 'IBM Plex Sans', 'osixthreeo' ),
					'ibmplexserif'         => esc_html__( 'IBM Plex Serif', 'osixthreeo' ),
					'inknutantiqua'        => esc_html__( 'Inknut Antiqua', 'osixthreeo' ),
					'inconsolata'          => esc_html__( 'Inconsolata', 'osixthreeo' ),
					'karla'                => esc_html__( 'Karla', 'osixthreeo' ),
					'lato'                 => esc_html__( 'Lato', 'osixthreeo' ),
					'librefranklin'        => esc_html__( 'Libre Franklin', 'osixthreeo' ),
					'librebaskerville'     => esc_html__( 'Libre Baskerville', 'osixthreeo' ),
					'lora'                 => esc_html__( 'Lora', 'osixthreeo' ),
					'lilyscriptone'        => esc_html__( 'Lily Script One', 'osixthreeo' ),
					'lobster'              => esc_html__( 'Lobster', 'osixthreeo' ),
					'lobstertwo'           => esc_html__( 'Lobster Two', 'osixthreeo' ),
					'montserrat'           => esc_html__( 'Montserrat', 'osixthreeo' ),
					'montserratalternates' => esc_html__( 'Montserrat Alternates', 'osixthreeo' ),
					'muli'                 => esc_html__( 'Muli', 'osixthreeo' ),
					'merriweather'         => esc_html__( 'Merriweather', 'osixthreeo' ),
					'monoton'              => esc_html__( 'Monoton', 'osixthreeo' ),
					'notosans'             => esc_html__( 'Noto Sans', 'osixthreeo' ),
					'nunito'               => esc_html__( 'Nunito', 'osixthreeo' ),
					'neuton'               => esc_html__( 'Neuton', 'osixthreeo' ),
					'nixieone'             => esc_html__( 'Nixie One', 'osixthreeo' ),
					'opensans'             => esc_html__( 'Open Sans', 'osixthreeo' ),
					'oswald'               => esc_html__( 'Oswald', 'osixthreeo' ),
					'oxygen'               => esc_html__( 'Oxygen', 'osixthreeo' ),
					'oldstandardtt'        => esc_html__( 'Old Standard TT', 'osixthreeo' ),
					'oleoscript'           => esc_html__( 'Oleo Script', 'osixthreeo' ),
					'oleoscriptswashcaps'  => esc_html__( 'Oleo Script Swash Caps', 'osixthreeo' ),
					'poppins'              => esc_html__( 'Poppins', 'osixthreeo' ),
					'prozalibre'           => esc_html__( 'Proza Libre', 'osixthreeo' ),
					'ptsans'               => esc_html__( 'PT Sans', 'osixthreeo' ),
					'playfairdisplay'      => esc_html__( 'Playfair Display', 'osixthreeo' ),
					'ptserif'              => esc_html__( 'PT Serif', 'osixthreeo' ),
					'raleway'              => esc_html__( 'Raleway', 'osixthreeo' ),
					'roboto'               => esc_html__( 'Roboto', 'osixthreeo' ),
					'rubik'                => esc_html__( 'Rubik', 'osixthreeo' ),
					'robotoslab'           => esc_html__( 'Roboto Slab', 'osixthreeo' ),
					'rokkitt'              => esc_html__( 'Rokkitt', 'osixthreeo' ),
					'ranchers'             => esc_html__( 'Ranchers', 'osixthreeo' ),
					'rakkas'               => esc_html__( 'Rakkas', 'osixthreeo' ),
					'sourcesanspro'        => esc_html__( 'Source Sans Pro', 'osixthreeo' ),
					'sourceserifpro'       => esc_html__( 'Source Serif Pro', 'osixthreeo' ),
					'spectral'             => esc_html__( 'Spectral', 'osixthreeo' ),
					'specialelite'         => esc_html__( 'Special Elite', 'osixthreeo' ),
					'spacemono'            => esc_html__( 'Space Mono', 'osixthreeo' ),
					'titilliumweb'         => esc_html__( 'Titillium Web', 'osixthreeo' ),
					'ubuntu'               => esc_html__( 'Ubuntu', 'osixthreeo' ),
					'varela'               => esc_html__( 'Varela', 'osixthreeo' ),
					'varelaround'          => esc_html__( 'Varela Round', 'osixthreeo' ),
					'vollkorn'             => esc_html__( 'Vollkorn', 'osixthreeo' ),
					'vollkornsc'           => esc_html__( 'Vollkorn SC', 'osixthreeo' ),
					'worksans'             => esc_html__( 'Work Sans', 'osixthreeo' ),
					'yatraone'             => esc_html__( 'Yatra One', 'osixthreeo' ),
				),
				'settings' => 'osixthreeo_settings[base_font]',
				'priority' => 2,
			)
		);

		// header font.
		$wp_customize->add_setting(
			'osixthreeo_settings[header_font]',
			array(
				'default'           => $defaults['header_font'],
				'type'              => 'option',
				'sanitize_callback' => 'osixthreeo_sanitize_choices',
			)
		);
		$wp_customize->add_control(
			'osixthreeo_settings[header_font]',
			array(
				'type'     => 'select',
				'label'    => esc_html__( 'Header Font', 'osixthreeo' ),
				'section'  => 'osixthreeo_typography',
				'choices'  => array(
					''                     => esc_html__( 'Arial - default', 'osixthreeo' ),
					'georgia'              => esc_html__( 'Georgia', 'osixthreeo' ),
					'verdana'              => esc_html__( 'Verdana', 'osixthreeo' ),
					'trebuchet'            => esc_html__( 'Trebuchet', 'osixthreeo' ),
					'palatino'             => esc_html__( 'Palatino', 'osixthreeo' ),
					'tahoma'               => esc_html__( 'Tahoma', 'osixthreeo' ),
					'times'                => esc_html__( 'Times', 'osixthreeo' ),
					'arialblack'           => esc_html__( 'Arial Black', 'osixthreeo' ),
					'impact'               => esc_html__( 'Impact', 'osixthreeo' ),
					'copperplate'          => esc_html__( 'Copperplate', 'osixthreeo' ),
					'papyrus'              => esc_html__( 'Papyrus', 'osixthreeo' ),
					'courier'              => esc_html__( 'Courier', 'osixthreeo' ),
					'lucidatypewritter'    => esc_html__( 'Lucida Typewritter', 'osixthreeo' ),
					'comicsans'            => esc_html__( 'Comic Sans', 'osixthreeo' ),
					'alegreya'             => esc_html__( 'Alegreya', 'osixthreeo' ),
					'alegreyasc'           => esc_html__( 'Alegreya SC', 'osixthreeo' ),
					'alegreyasans'         => esc_html__( 'Alegreya Sans', 'osixthreeo' ),
					'alegreyasanssc'       => esc_html__( 'Alegreya Sans SC', 'osixthreeo' ),
					'archivo'              => esc_html__( 'Archivo', 'osixthreeo' ),
					'archivonarrow'        => esc_html__( 'Archivo Narrow', 'osixthreeo' ),
					'arvo'                 => esc_html__( 'Arvo', 'osixthreeo' ),
					'abrilfatface'         => esc_html__( 'Abril Fatface', 'osixthreeo' ),
					'alfaslabone'          => esc_html__( 'Alfa Slab One', 'osixthreeo' ),
					'b612'                 => esc_html__( 'B612', 'osixthreeo' ),
					'biothyme'             => esc_html__( 'BioRhyme', 'osixthreeo' ),
					'baloo'                => esc_html__( 'Baloo', 'osixthreeo' ),
					'barrio'               => esc_html__( 'Barrio', 'osixthreeo' ),
					'blackopsone'          => esc_html__( 'Black Ops One', 'osixthreeo' ),
					'cabin'                => esc_html__( 'Cabin', 'osixthreeo' ),
					'cairo'                => esc_html__( 'Cairo', 'osixthreeo' ),
					'chivo'                => esc_html__( 'Chivo', 'osixthreeo' ),
					'cardo'                => esc_html__( 'Cardo', 'osixthreeo' ),
					'cormorant'            => esc_html__( 'Cormorant', 'osixthreeo' ),
					'crimsontext'          => esc_html__( 'Crimson Text', 'osixthreeo' ),
					'cabinsketch'          => esc_html__( 'Cabin Sketch', 'osixthreeo' ),
					'chelaone'             => esc_html__( 'Chela One', 'osixthreeo' ),
					'concertone'           => esc_html__( 'Concert One', 'osixthreeo' ),
					'domine'               => esc_html__( 'Domine', 'osixthreeo' ),
					'exo2'                 => esc_html__( 'Exo 2', 'osixthreeo' ),
					'eczar'                => esc_html__( 'Eczar', 'osixthreeo' ),
					'ericaone'             => esc_html__( 'Erica One', 'osixthreeo' ),
					'fjallaone'            => esc_html__( 'Fjalla One', 'osixthreeo' ),
					'firasans'             => esc_html__( 'Fira Sans', 'osixthreeo' ),
					'frankruhllibre'       => esc_html__( 'Frank Ruhl Libre', 'osixthreeo' ),
					'fascinate'            => esc_html__( 'Fascinate', 'osixthreeo' ),
					'flamenco'             => esc_html__( 'Flamenco', 'osixthreeo' ),
					'frederickathegreat'   => esc_html__( 'Fredericka the Great', 'osixthreeo' ),
					'ibmplexsans'          => esc_html__( 'IBM Plex Sans', 'osixthreeo' ),
					'ibmplexserif'         => esc_html__( 'IBM Plex Serif', 'osixthreeo' ),
					'inknutantiqua'        => esc_html__( 'Inknut Antiqua', 'osixthreeo' ),
					'inconsolata'          => esc_html__( 'Inconsolata', 'osixthreeo' ),
					'karla'                => esc_html__( 'Karla', 'osixthreeo' ),
					'lato'                 => esc_html__( 'Lato', 'osixthreeo' ),
					'librefranklin'        => esc_html__( 'Libre Franklin', 'osixthreeo' ),
					'librebaskerville'     => esc_html__( 'Libre Baskerville', 'osixthreeo' ),
					'lora'                 => esc_html__( 'Lora', 'osixthreeo' ),
					'lilyscriptone'        => esc_html__( 'Lily Script One', 'osixthreeo' ),
					'lobster'              => esc_html__( 'Lobster', 'osixthreeo' ),
					'lobstertwo'           => esc_html__( 'Lobster Two', 'osixthreeo' ),
					'montserrat'           => esc_html__( 'Montserrat', 'osixthreeo' ),
					'montserratalternates' => esc_html__( 'Montserrat Alternates', 'osixthreeo' ),
					'muli'                 => esc_html__( 'Muli', 'osixthreeo' ),
					'merriweather'         => esc_html__( 'Merriweather', 'osixthreeo' ),
					'monoton'              => esc_html__( 'Monoton', 'osixthreeo' ),
					'notosans'             => esc_html__( 'Noto Sans', 'osixthreeo' ),
					'nunito'               => esc_html__( 'Nunito', 'osixthreeo' ),
					'neuton'               => esc_html__( 'Neuton', 'osixthreeo' ),
					'nixieone'             => esc_html__( 'Nixie One', 'osixthreeo' ),
					'opensans'             => esc_html__( 'Open Sans', 'osixthreeo' ),
					'oswald'               => esc_html__( 'Oswald', 'osixthreeo' ),
					'oxygen'               => esc_html__( 'Oxygen', 'osixthreeo' ),
					'oldstandardtt'        => esc_html__( 'Old Standard TT', 'osixthreeo' ),
					'oleoscript'           => esc_html__( 'Oleo Script', 'osixthreeo' ),
					'oleoscriptswashcaps'  => esc_html__( 'Oleo Script Swash Caps', 'osixthreeo' ),
					'poppins'              => esc_html__( 'Poppins', 'osixthreeo' ),
					'prozalibre'           => esc_html__( 'Proza Libre', 'osixthreeo' ),
					'ptsans'               => esc_html__( 'PT Sans', 'osixthreeo' ),
					'playfairdisplay'      => esc_html__( 'Playfair Display', 'osixthreeo' ),
					'ptserif'              => esc_html__( 'PT Serif', 'osixthreeo' ),
					'raleway'              => esc_html__( 'Raleway', 'osixthreeo' ),
					'roboto'               => esc_html__( 'Roboto', 'osixthreeo' ),
					'rubik'                => esc_html__( 'Rubik', 'osixthreeo' ),
					'robotoslab'           => esc_html__( 'Roboto Slab', 'osixthreeo' ),
					'rokkitt'              => esc_html__( 'Rokkitt', 'osixthreeo' ),
					'ranchers'             => esc_html__( 'Ranchers', 'osixthreeo' ),
					'rakkas'               => esc_html__( 'Rakkas', 'osixthreeo' ),
					'sourcesanspro'        => esc_html__( 'Source Sans Pro', 'osixthreeo' ),
					'sourceserifpro'       => esc_html__( 'Source Serif Pro', 'osixthreeo' ),
					'spectral'             => esc_html__( 'Spectral', 'osixthreeo' ),
					'specialelite'         => esc_html__( 'Special Elite', 'osixthreeo' ),
					'spacemono'            => esc_html__( 'Space Mono', 'osixthreeo' ),
					'titilliumweb'         => esc_html__( 'Titillium Web', 'osixthreeo' ),
					'ubuntu'               => esc_html__( 'Ubuntu', 'osixthreeo' ),
					'varela'               => esc_html__( 'Varela', 'osixthreeo' ),
					'varelaround'          => esc_html__( 'Varela Round', 'osixthreeo' ),
					'vollkorn'             => esc_html__( 'Vollkorn', 'osixthreeo' ),
					'vollkornsc'           => esc_html__( 'Vollkorn SC', 'osixthreeo' ),
					'worksans'             => esc_html__( 'Work Sans', 'osixthreeo' ),
					'yatraone'             => esc_html__( 'Yatra One', 'osixthreeo' ),
				),
				'settings' => 'osixthreeo_settings[header_font]',
				'priority' => 3,
			)
		);

		// highlite font.
		$wp_customize->add_setting(
			'osixthreeo_settings[highlite_font]',
			array(
				'default'           => $defaults['highlite_font'],
				'type'              => 'option',
				'sanitize_callback' => 'osixthreeo_sanitize_choices',
			)
		);
		$wp_customize->add_control(
			'osixthreeo_settings[highlite_font]',
			array(
				'type'     => 'select',
				'label'    => esc_html__( 'Highlite Font', 'osixthreeo' ),
				'section'  => 'osixthreeo_typography',
				'choices'  => array(
					''                     => esc_html__( 'Arial - default', 'osixthreeo' ),
					'georgia'              => esc_html__( 'Georgia', 'osixthreeo' ),
					'verdana'              => esc_html__( 'Verdana', 'osixthreeo' ),
					'trebuchet'            => esc_html__( 'Trebuchet', 'osixthreeo' ),
					'palatino'             => esc_html__( 'Palatino', 'osixthreeo' ),
					'tahoma'               => esc_html__( 'Tahoma', 'osixthreeo' ),
					'times'                => esc_html__( 'Times', 'osixthreeo' ),
					'arialblack'           => esc_html__( 'Arial Black', 'osixthreeo' ),
					'impact'               => esc_html__( 'Impact', 'osixthreeo' ),
					'copperplate'          => esc_html__( 'Copperplate', 'osixthreeo' ),
					'papyrus'              => esc_html__( 'Papyrus', 'osixthreeo' ),
					'courier'              => esc_html__( 'Courier', 'osixthreeo' ),
					'lucidatypewritter'    => esc_html__( 'Lucida Typewritter', 'osixthreeo' ),
					'comicsans'            => esc_html__( 'Comic Sans', 'osixthreeo' ),
					'alegreya'             => esc_html__( 'Alegreya', 'osixthreeo' ),
					'alegreyasc'           => esc_html__( 'Alegreya SC', 'osixthreeo' ),
					'alegreyasans'         => esc_html__( 'Alegreya Sans', 'osixthreeo' ),
					'alegreyasanssc'       => esc_html__( 'Alegreya Sans SC', 'osixthreeo' ),
					'archivo'              => esc_html__( 'Archivo', 'osixthreeo' ),
					'archivonarrow'        => esc_html__( 'Archivo Narrow', 'osixthreeo' ),
					'arvo'                 => esc_html__( 'Arvo', 'osixthreeo' ),
					'abrilfatface'         => esc_html__( 'Abril Fatface', 'osixthreeo' ),
					'alfaslabone'          => esc_html__( 'Alfa Slab One', 'osixthreeo' ),
					'b612'                 => esc_html__( 'B612', 'osixthreeo' ),
					'biothyme'             => esc_html__( 'BioRhyme', 'osixthreeo' ),
					'baloo'                => esc_html__( 'Baloo', 'osixthreeo' ),
					'barrio'               => esc_html__( 'Barrio', 'osixthreeo' ),
					'blackopsone'          => esc_html__( 'Black Ops One', 'osixthreeo' ),
					'cabin'                => esc_html__( 'Cabin', 'osixthreeo' ),
					'cairo'                => esc_html__( 'Cairo', 'osixthreeo' ),
					'chivo'                => esc_html__( 'Chivo', 'osixthreeo' ),
					'cardo'                => esc_html__( 'Cardo', 'osixthreeo' ),
					'cormorant'            => esc_html__( 'Cormorant', 'osixthreeo' ),
					'crimsontext'          => esc_html__( 'Crimson Text', 'osixthreeo' ),
					'cabinsketch'          => esc_html__( 'Cabin Sketch', 'osixthreeo' ),
					'chelaone'             => esc_html__( 'Chela One', 'osixthreeo' ),
					'concertone'           => esc_html__( 'Concert One', 'osixthreeo' ),
					'domine'               => esc_html__( 'Domine', 'osixthreeo' ),
					'exo2'                 => esc_html__( 'Exo 2', 'osixthreeo' ),
					'eczar'                => esc_html__( 'Eczar', 'osixthreeo' ),
					'ericaone'             => esc_html__( 'Erica One', 'osixthreeo' ),
					'fjallaone'            => esc_html__( 'Fjalla One', 'osixthreeo' ),
					'firasans'             => esc_html__( 'Fira Sans', 'osixthreeo' ),
					'frankruhllibre'       => esc_html__( 'Frank Ruhl Libre', 'osixthreeo' ),
					'fascinate'            => esc_html__( 'Fascinate', 'osixthreeo' ),
					'flamenco'             => esc_html__( 'Flamenco', 'osixthreeo' ),
					'frederickathegreat'   => esc_html__( 'Fredericka the Great', 'osixthreeo' ),
					'ibmplexsans'          => esc_html__( 'IBM Plex Sans', 'osixthreeo' ),
					'ibmplexserif'         => esc_html__( 'IBM Plex Serif', 'osixthreeo' ),
					'inknutantiqua'        => esc_html__( 'Inknut Antiqua', 'osixthreeo' ),
					'inconsolata'          => esc_html__( 'Inconsolata', 'osixthreeo' ),
					'karla'                => esc_html__( 'Karla', 'osixthreeo' ),
					'lato'                 => esc_html__( 'Lato', 'osixthreeo' ),
					'librefranklin'        => esc_html__( 'Libre Franklin', 'osixthreeo' ),
					'librebaskerville'     => esc_html__( 'Libre Baskerville', 'osixthreeo' ),
					'lora'                 => esc_html__( 'Lora', 'osixthreeo' ),
					'lilyscriptone'        => esc_html__( 'Lily Script One', 'osixthreeo' ),
					'lobster'              => esc_html__( 'Lobster', 'osixthreeo' ),
					'lobstertwo'           => esc_html__( 'Lobster Two', 'osixthreeo' ),
					'montserrat'           => esc_html__( 'Montserrat', 'osixthreeo' ),
					'montserratalternates' => esc_html__( 'Montserrat Alternates', 'osixthreeo' ),
					'muli'                 => esc_html__( 'Muli', 'osixthreeo' ),
					'merriweather'         => esc_html__( 'Merriweather', 'osixthreeo' ),
					'monoton'              => esc_html__( 'Monoton', 'osixthreeo' ),
					'notosans'             => esc_html__( 'Noto Sans', 'osixthreeo' ),
					'nunito'               => esc_html__( 'Nunito', 'osixthreeo' ),
					'neuton'               => esc_html__( 'Neuton', 'osixthreeo' ),
					'nixieone'             => esc_html__( 'Nixie One', 'osixthreeo' ),
					'opensans'             => esc_html__( 'Open Sans', 'osixthreeo' ),
					'oswald'               => esc_html__( 'Oswald', 'osixthreeo' ),
					'oxygen'               => esc_html__( 'Oxygen', 'osixthreeo' ),
					'oldstandardtt'        => esc_html__( 'Old Standard TT', 'osixthreeo' ),
					'oleoscript'           => esc_html__( 'Oleo Script', 'osixthreeo' ),
					'oleoscriptswashcaps'  => esc_html__( 'Oleo Script Swash Caps', 'osixthreeo' ),
					'poppins'              => esc_html__( 'Poppins', 'osixthreeo' ),
					'prozalibre'           => esc_html__( 'Proza Libre', 'osixthreeo' ),
					'ptsans'               => esc_html__( 'PT Sans', 'osixthreeo' ),
					'playfairdisplay'      => esc_html__( 'Playfair Display', 'osixthreeo' ),
					'ptserif'              => esc_html__( 'PT Serif', 'osixthreeo' ),
					'raleway'              => esc_html__( 'Raleway', 'osixthreeo' ),
					'roboto'               => esc_html__( 'Roboto', 'osixthreeo' ),
					'rubik'                => esc_html__( 'Rubik', 'osixthreeo' ),
					'robotoslab'           => esc_html__( 'Roboto Slab', 'osixthreeo' ),
					'rokkitt'              => esc_html__( 'Rokkitt', 'osixthreeo' ),
					'ranchers'             => esc_html__( 'Ranchers', 'osixthreeo' ),
					'rakkas'               => esc_html__( 'Rakkas', 'osixthreeo' ),
					'sourcesanspro'        => esc_html__( 'Source Sans Pro', 'osixthreeo' ),
					'sourceserifpro'       => esc_html__( 'Source Serif Pro', 'osixthreeo' ),
					'spectral'             => esc_html__( 'Spectral', 'osixthreeo' ),
					'specialelite'         => esc_html__( 'Special Elite', 'osixthreeo' ),
					'spacemono'            => esc_html__( 'Space Mono', 'osixthreeo' ),
					'titilliumweb'         => esc_html__( 'Titillium Web', 'osixthreeo' ),
					'ubuntu'               => esc_html__( 'Ubuntu', 'osixthreeo' ),
					'varela'               => esc_html__( 'Varela', 'osixthreeo' ),
					'varelaround'          => esc_html__( 'Varela Round', 'osixthreeo' ),
					'vollkorn'             => esc_html__( 'Vollkorn', 'osixthreeo' ),
					'vollkornsc'           => esc_html__( 'Vollkorn SC', 'osixthreeo' ),
					'worksans'             => esc_html__( 'Work Sans', 'osixthreeo' ),
					'yatraone'             => esc_html__( 'Yatra One', 'osixthreeo' ),
				),
				'settings' => 'osixthreeo_settings[highlite_font]',
				'priority' => 4,
			)
		);

		// section message.
		$wp_customize->add_setting(
			'typography-global-message',
			array(
				'sanitize_callback' => 'wp_kses_post',
			)
		);
		$wp_customize->add_control(
			new Osixthreeo_Content_Area(
				$wp_customize,
				'typography-global-message',
				array(
					'section'  => 'osixthreeo_typography',
					'label'    => esc_html__( 'Global Settings', 'osixthreeo' ),
					'priority' => 5,
				)
			)
		);

		// base font size.
		$wp_customize->add_setting(
			'osixthreeo_settings[base_font_size]',
			array(
				'default'           => $defaults['base_font_size'],
				'type'              => 'option',
				'sanitize_callback' => 'osixthreeo_sanitize_integer',
				'transport'         => 'postMessage',
			)
		);
		$wp_customize->add_control(
			new Osixthreeo_Range_Control(
				$wp_customize,
				'osixthreeo_settings[base_font_size]',
				array(
					'type'        => 'range',
					'label'       => esc_html__( 'Content font size', 'osixthreeo' ),
					'section'     => 'osixthreeo_typography',
					'settings'    => 'osixthreeo_settings[base_font_size]',
					'input_attrs' => array(
						'min'  => 12,
						'max'  => 24,
						'step' => 1,
					),
					'priority'    => 6,
				)
			)
		);

		// headers font weight.
		$wp_customize->add_setting(
			'osixthreeo_settings[header_font_weight]',
			array(
				'default'           => $defaults['header_font_weight'],
				'type'              => 'option',
				'sanitize_callback' => 'osixthreeo_sanitize_choices',
				'transport'         => 'postMessage',
			)
		);
		$wp_customize->add_control(
			'osixthreeo_settings[header_font_weight]',
			array(
				'type'        => 'select',
				'label'       => esc_html__( 'Header font weight', 'osixthreeo' ),
				'description' => esc_html__( 'h1 - h6 header size options coming soon', 'osixthreeo' ),
				'section'     => 'osixthreeo_typography',
				'choices'     => array(
					''    => esc_html__( 'Default', 'osixthreeo' ),
					'100' => esc_html__( 'Thin: 100', 'osixthreeo' ),
					'200' => esc_html__( 'Light: 200', 'osixthreeo' ),
					'300' => esc_html__( 'Book: 300', 'osixthreeo' ),
					'400' => esc_html__( 'Normal: 400', 'osixthreeo' ),
					'500' => esc_html__( 'Medium: 500', 'osixthreeo' ),
					'600' => esc_html__( 'Semibold: 600', 'osixthreeo' ),
					'700' => esc_html__( 'Bold: 700', 'osixthreeo' ),
					'800' => esc_html__( 'Extra Bold: 800', 'osixthreeo' ),
					'900' => esc_html__( 'Black: 900', 'osixthreeo' ),
				),
				'settings'    => 'osixthreeo_settings[header_font_weight]',
				'priority'    => 7,
			)
		);

		// section message.
		$wp_customize->add_setting(
			'typographu-fonts-message',
			array(
				'sanitize_callback' => 'wp_kses_post',
			)
		);
		$wp_customize->add_control(
			new Osixthreeo_Content_Area(
				$wp_customize,
				'typographu-fonts-message',
				array(
					'section'  => 'osixthreeo_typography',
					'content'  => esc_html__( 'Using the controls below the 3 fonts selected above can be assigned to various areas of the site.', 'osixthreeo' ) . '</p>',
					'priority' => 8,
				)
			)
		);

		// TITLE section message.
		$wp_customize->add_setting(
			'typography-title-message',
			array(
				'sanitize_callback' => 'wp_kses_post',
			)
		);
		$wp_customize->add_control(
			new Osixthreeo_Content_Area(
				$wp_customize,
				'typography-title-message',
				array(
					'section'  => 'osixthreeo_typography',
					'label'    => esc_html__( 'Site Title', 'osixthreeo' ),
					'priority' => 9,
				)
			)
		);
		// site title font family.
		$wp_customize->add_setting(
			'osixthreeo_settings[sitetitle_font]',
			array(
				'default'           => $defaults['sitetitle_font'],
				'type'              => 'option',
				'sanitize_callback' => 'osixthreeo_sanitize_choices',
			)
		);
		$wp_customize->add_control(
			'osixthreeo_settings[sitetitle_font]',
			array(
				'type'     => 'select',
				'label'    => esc_html__( 'Font family', 'osixthreeo' ),
				'section'  => 'osixthreeo_typography',
				'choices'  => array(
					''         => esc_html__( 'Base font', 'osixthreeo' ),
					'header'   => esc_html__( 'Header font', 'osixthreeo' ),
					'highlite' => esc_html__( 'Highlite font', 'osixthreeo' ),
				),
				'settings' => 'osixthreeo_settings[sitetitle_font]',
				'priority' => 10,
			)
		);
		// site title font size.
		$wp_customize->add_setting(
			'osixthreeo_settings[sitetitle_font_size]',
			array(
				'default'           => $defaults['sitetitle_font_size'],
				'type'              => 'option',
				'sanitize_callback' => 'osixthreeo_sanitize_integer',
				'transport'         => 'postMessage',
			)
		);
		$wp_customize->add_control(
			new Osixthreeo_Range_Control(
				$wp_customize,
				'osixthreeo_settings[sitetitle_font_size]',
				array(
					'type'        => 'range',
					'label'       => esc_html__( 'Font size', 'osixthreeo' ),
					'section'     => 'osixthreeo_typography',
					'settings'    => 'osixthreeo_settings[sitetitle_font_size]',
					'input_attrs' => array(
						'min'  => 24,
						'max'  => 72,
						'step' => 1,
					),
					'priority'    => 11,
				)
			)
		);
		// site title font weight.
		$wp_customize->add_setting(
			'osixthreeo_settings[sitetitle_font_weight]',
			array(
				'default'           => $defaults['sitetitle_font_weight'],
				'type'              => 'option',
				'sanitize_callback' => 'osixthreeo_sanitize_choices',
				'transport'         => 'postMessage',
			)
		);
		$wp_customize->add_control(
			'osixthreeo_settings[sitetitle_font_weight]',
			array(
				'type'     => 'select',
				'label'    => esc_html__( 'Font weight', 'osixthreeo' ),
				'section'  => 'osixthreeo_typography',
				'choices'  => array(
					''    => esc_html__( 'Default', 'osixthreeo' ),
					'100' => esc_html__( 'Thin: 100', 'osixthreeo' ),
					'200' => esc_html__( 'Light: 200', 'osixthreeo' ),
					'300' => esc_html__( 'Book: 300', 'osixthreeo' ),
					'400' => esc_html__( 'Normal: 400', 'osixthreeo' ),
					'500' => esc_html__( 'Medium: 500', 'osixthreeo' ),
					'600' => esc_html__( 'Semibold: 600', 'osixthreeo' ),
					'700' => esc_html__( 'Bold: 700', 'osixthreeo' ),
					'800' => esc_html__( 'Extra Bold: 800', 'osixthreeo' ),
					'900' => esc_html__( 'Black: 900', 'osixthreeo' ),
				),
				'settings' => 'osixthreeo_settings[sitetitle_font_weight]',
				'priority' => 12,
			)
		);

		// DESCRIPTION section message.
		$wp_customize->add_setting(
			'typography-description-message',
			array(
				'sanitize_callback' => 'wp_kses_post',
			)
		);
		$wp_customize->add_control(
			new Osixthreeo_Content_Area(
				$wp_customize,
				'typography-description-message',
				array(
					'section'  => 'osixthreeo_typography',
					'label'    => esc_html__( 'Site Description', 'osixthreeo' ),
					'priority' => 13,
				)
			)
		);
		// site description font family.
		$wp_customize->add_setting(
			'osixthreeo_settings[sitedescription_font]',
			array(
				'default'           => $defaults['sitedescription_font'],
				'type'              => 'option',
				'sanitize_callback' => 'osixthreeo_sanitize_choices',
			)
		);
		$wp_customize->add_control(
			'osixthreeo_settings[sitedescription_font]',
			array(
				'type'     => 'select',
				'label'    => esc_html__( 'Font family', 'osixthreeo' ),
				'section'  => 'osixthreeo_typography',
				'choices'  => array(
					''         => esc_html__( 'Base font', 'osixthreeo' ),
					'header'   => esc_html__( 'Header font', 'osixthreeo' ),
					'highlite' => esc_html__( 'Highlite font', 'osixthreeo' ),
				),
				'settings' => 'osixthreeo_settings[sitedescription_font]',
				'priority' => 14,
			)
		);
		// site description font size.
		$wp_customize->add_setting(
			'osixthreeo_settings[sitedescription_font_size]',
			array(
				'default'           => $defaults['sitedescription_font_size'],
				'type'              => 'option',
				'sanitize_callback' => 'osixthreeo_sanitize_integer',
				'transport'         => 'postMessage',
			)
		);
		$wp_customize->add_control(
			new Osixthreeo_Range_Control(
				$wp_customize,
				'osixthreeo_settings[sitedescription_font_size]',
				array(
					'type'        => 'range',
					'label'       => esc_html__( 'Font size', 'osixthreeo' ),
					'section'     => 'osixthreeo_typography',
					'settings'    => 'osixthreeo_settings[sitedescription_font_size]',
					'input_attrs' => array(
						'min'  => 12,
						'max'  => 20,
						'step' => 1,
					),
					'priority'    => 15,
				)
			)
		);
		// site description font weight.
		$wp_customize->add_setting(
			'osixthreeo_settings[sitedescription_font_weight]',
			array(
				'default'           => $defaults['sitedescription_font_weight'],
				'type'              => 'option',
				'sanitize_callback' => 'osixthreeo_sanitize_choices',
				'transport'         => 'postMessage',
			)
		);
		$wp_customize->add_control(
			'osixthreeo_settings[sitedescription_font_weight]',
			array(
				'type'     => 'select',
				'label'    => esc_html__( 'Font weight', 'osixthreeo' ),
				'section'  => 'osixthreeo_typography',
				'choices'  => array(
					''    => esc_html__( 'Default', 'osixthreeo' ),
					'100' => esc_html__( 'Thin: 100', 'osixthreeo' ),
					'200' => esc_html__( 'Light: 200', 'osixthreeo' ),
					'300' => esc_html__( 'Book: 300', 'osixthreeo' ),
					'400' => esc_html__( 'Normal: 400', 'osixthreeo' ),
					'500' => esc_html__( 'Medium: 500', 'osixthreeo' ),
					'600' => esc_html__( 'Semibold: 600', 'osixthreeo' ),
					'700' => esc_html__( 'Bold: 700', 'osixthreeo' ),
					'800' => esc_html__( 'Extra Bold: 800', 'osixthreeo' ),
					'900' => esc_html__( 'Black: 900', 'osixthreeo' ),
				),
				'settings' => 'osixthreeo_settings[sitedescription_font_weight]',
				'priority' => 16,
			)
		);

		// MENU section message.
		$wp_customize->add_setting(
			'typography-menu-message',
			array(
				'sanitize_callback' => 'wp_kses_post',
			)
		);
		$wp_customize->add_control(
			new Osixthreeo_Content_Area(
				$wp_customize,
				'typography-menu-message',
				array(
					'section'  => 'osixthreeo_typography',
					'label'    => esc_html__( 'Menu', 'osixthreeo' ),
					'priority' => 17,
				)
			)
		);

		// menu font family --------------------------------.
		$wp_customize->add_setting(
			'osixthreeo_settings[menu_font]',
			array(
				'default'           => $defaults['menu_font'],
				'type'              => 'option',
				'sanitize_callback' => 'osixthreeo_sanitize_choices',
			)
		);
		$wp_customize->add_control(
			'osixthreeo_settings[menu_font]',
			array(
				'type'     => 'select',
				'label'    => esc_html__( 'Font family', 'osixthreeo' ),
				'section'  => 'osixthreeo_typography',
				'choices'  => array(
					''         => esc_html__( 'Base font', 'osixthreeo' ),
					'header'   => esc_html__( 'Header font', 'osixthreeo' ),
					'highlite' => esc_html__( 'Highlite font', 'osixthreeo' ),
				),
				'settings' => 'osixthreeo_settings[menu_font]',
				'priority' => 18,
			)
		);
		// menu font size.
		$wp_customize->add_setting(
			'osixthreeo_settings[menu_font_size]',
			array(
				'default'           => $defaults['menu_font_size'],
				'type'              => 'option',
				'sanitize_callback' => 'osixthreeo_sanitize_integer',
				'transport'         => 'postMessage',
			)
		);
		$wp_customize->add_control(
			new Osixthreeo_Range_Control(
				$wp_customize,
				'osixthreeo_settings[menu_font_size]',
				array(
					'type'        => 'range',
					'label'       => esc_html__( 'Font size', 'osixthreeo' ),
					'section'     => 'osixthreeo_typography',
					'settings'    => 'osixthreeo_settings[menu_font_size]',
					'input_attrs' => array(
						'min'  => 12,
						'max'  => 24,
						'step' => 1,
					),
					'priority'    => 19,
				)
			)
		);
		// menu font weight.
		$wp_customize->add_setting(
			'osixthreeo_settings[menu_font_weight]',
			array(
				'default'           => $defaults['menu_font_weight'],
				'type'              => 'option',
				'sanitize_callback' => 'osixthreeo_sanitize_choices',
				'transport'         => 'postMessage',
			)
		);
		$wp_customize->add_control(
			'osixthreeo_settings[menu_font_weight]',
			array(
				'type'     => 'select',
				'label'    => esc_html__( 'Font weight', 'osixthreeo' ),
				'section'  => 'osixthreeo_typography',
				'choices'  => array(
					''    => esc_html__( 'Default', 'osixthreeo' ),
					'100' => esc_html__( 'Thin: 100', 'osixthreeo' ),
					'200' => esc_html__( 'Light: 200', 'osixthreeo' ),
					'300' => esc_html__( 'Book: 300', 'osixthreeo' ),
					'400' => esc_html__( 'Normal: 400', 'osixthreeo' ),
					'500' => esc_html__( 'Medium: 500', 'osixthreeo' ),
					'600' => esc_html__( 'Semibold: 600', 'osixthreeo' ),
					'700' => esc_html__( 'Bold: 700', 'osixthreeo' ),
					'800' => esc_html__( 'Extra Bold: 800', 'osixthreeo' ),
					'900' => esc_html__( 'Black: 900', 'osixthreeo' ),
				),
				'settings' => 'osixthreeo_settings[menu_font_weight]',
				'priority' => 20,
			)
		);

		/*
		 * META
		 * ------------------------------------------------------------
		 */

		// section message.
		$wp_customize->add_setting(
			'typography-meta-message',
			array(
				'sanitize_callback' => 'wp_kses_post',
			)
		);
		$wp_customize->add_control(
			new Osixthreeo_Content_Area(
				$wp_customize,
				'typography-meta-message',
				array(
					'section'  => 'osixthreeo_typography',
					'label'    => esc_html__( 'Post Meta', 'osixthreeo' ),
					'priority' => 21,
				)
			)
		);
		// font family --------------------------------.
		$wp_customize->add_setting(
			'osixthreeo_settings[meta_font]',
			array(
				'default'           => $defaults['meta_font'],
				'type'              => 'option',
				'sanitize_callback' => 'osixthreeo_sanitize_choices',
			)
		);
		$wp_customize->add_control(
			'osixthreeo_settings[meta_font]',
			array(
				'type'     => 'select',
				'label'    => esc_html__( 'Font family', 'osixthreeo' ),
				'section'  => 'osixthreeo_typography',
				'choices'  => array(
					''         => esc_html__( 'Base font', 'osixthreeo' ),
					'header'   => esc_html__( 'Header font', 'osixthreeo' ),
					'highlite' => esc_html__( 'Highlite font', 'osixthreeo' ),
				),
				'settings' => 'osixthreeo_settings[meta_font]',
				'priority' => 22,
			)
		);
		// font size.
		$wp_customize->add_setting(
			'osixthreeo_settings[meta_font_size]',
			array(
				'default'           => $defaults['meta_font_size'],
				'type'              => 'option',
				'sanitize_callback' => 'osixthreeo_sanitize_integer',
				'transport'         => 'postMessage',
			)
		);
		$wp_customize->add_control(
			new Osixthreeo_Range_Control(
				$wp_customize,
				'osixthreeo_settings[meta_font_size]',
				array(
					'type'        => 'range',
					'label'       => esc_html__( 'Font size', 'osixthreeo' ),
					'section'     => 'osixthreeo_typography',
					'settings'    => 'osixthreeo_settings[meta_font_size]',
					'input_attrs' => array(
						'min'  => 12,
						'max'  => 20,
						'step' => 1,
					),
					'priority'    => 23,
				)
			)
		);
		// font weight.
		$wp_customize->add_setting(
			'osixthreeo_settings[meta_font_weight]',
			array(
				'default'           => $defaults['meta_font_weight'],
				'type'              => 'option',
				'sanitize_callback' => 'osixthreeo_sanitize_choices',
				'transport'         => 'postMessage',
			)
		);
		$wp_customize->add_control(
			'osixthreeo_settings[meta_font_weight]',
			array(
				'type'     => 'select',
				'label'    => esc_html__( 'Font weight', 'osixthreeo' ),
				'section'  => 'osixthreeo_typography',
				'choices'  => array(
					''    => esc_html__( 'Default', 'osixthreeo' ),
					'100' => esc_html__( 'Thin: 100', 'osixthreeo' ),
					'200' => esc_html__( 'Light: 200', 'osixthreeo' ),
					'300' => esc_html__( 'Book: 300', 'osixthreeo' ),
					'400' => esc_html__( 'Normal: 400', 'osixthreeo' ),
					'500' => esc_html__( 'Medium: 500', 'osixthreeo' ),
					'600' => esc_html__( 'Semibold: 600', 'osixthreeo' ),
					'700' => esc_html__( 'Bold: 700', 'osixthreeo' ),
					'800' => esc_html__( 'Extra Bold: 800', 'osixthreeo' ),
					'900' => esc_html__( 'Black: 900', 'osixthreeo' ),
				),
				'settings' => 'osixthreeo_settings[meta_font_weight]',
				'priority' => 24,
			)
		);

		// GET EXTENSIONS.
		if ( ! OSTO_XTRAS ) :
			$wp_customize->add_setting(
				'typography-pro-callout',
				array(
					'sanitize_callback' => 'wp_kses_post',
				)
			);
			$wp_customize->add_control(
				new Osixthreeo_Content_Area(
					$wp_customize,
					'typography-pro-callout',
					array(
						'section'  => 'osixthreeo_typography',
						'label'    => esc_html__( 'Get more controls with an OsixthreeO Extension', 'osixthreeo' ),
						'content'  => '<a href="' . OSIXTHREEO_THEME_LINK . '" class="probtn" target="_blank" rel="noopener">OsixthreeO.com</a>',
						'priority' => 100,
					)
				)
			);
		endif;

		/*
		 * CUSTOM HEADER -------------------------------------------------------------------
		 * tab -----------------------------------------------------------------------------
		 * ---------------------------------------------------------------------------------
		 * ---------------------------------------------------------------------------------
		 */

		if ( class_exists( 'WP_Customize_Panel' ) ) {
			if ( ! $wp_customize->get_panel( 'osixthreeo_header_panel' ) ) {
				$wp_customize->add_panel(
					'osixthreeo_header_panel',
					array(
						'priority' => 50,
						'title'    => esc_html__( 'Custom Header', 'osixthreeo' ),
					)
				);
			}
		}

		// SUB PANEL ---------------------------------- .
		$wp_customize->add_section(
			'osixthreeo_ch_bgcolor',
			array(
				'title'    => esc_html__( 'Background Colors', 'osixthreeo' ),
				'panel'    => 'osixthreeo_header_panel',
				'priority' => 10,
			)
		);

		// gradient - left.
		$wp_customize->add_setting(
			'osixthreeo_settings[header_bg_color_left]',
			array(
				'default'           => $defaults['header_bg_color_left'],
				'type'              => 'option',
				'sanitize_callback' => 'sanitize_hex_color',
			)
		);
		$wp_customize->add_control(
			new WP_Customize_Color_Control(
				$wp_customize,
				'osixthreeo_settings[header_bg_color_left]',
				array(
					'label'    => esc_html__( 'Color left', 'osixthreeo' ),
					'section'  => 'osixthreeo_ch_bgcolor',
					'settings' => 'osixthreeo_settings[header_bg_color_left]',
					'priority' => 10,
				)
			)
		);

		// gradient - right.
		$wp_customize->add_setting(
			'osixthreeo_settings[header_bg_color_right]',
			array(
				'default'           => $defaults['header_bg_color_right'],
				'type'              => 'option',
				'sanitize_callback' => 'sanitize_hex_color',
			)
		);
		$wp_customize->add_control(
			new WP_Customize_Color_Control(
				$wp_customize,
				'osixthreeo_settings[header_bg_color_right]',
				array(
					'label'    => esc_html__( 'Color right', 'osixthreeo' ),
					'section'  => 'osixthreeo_ch_bgcolor',
					'settings' => 'osixthreeo_settings[header_bg_color_right]',
					'priority' => 20,
				)
			)
		);

		// gradient angle.
		$wp_customize->add_setting(
			'osixthreeo_settings[header_gradient_angle]',
			array(
				'default'           => $defaults['header_gradient_angle'],
				'type'              => 'option',
				'sanitize_callback' => 'osixthreeo_sanitize_integer',
			)
		);
		$wp_customize->add_control(
			new Osixthreeo_Range_Control(
				$wp_customize,
				'osixthreeo_settings[header_gradient_angle]',
				array(
					'type'        => 'range',
					'label'       => esc_html__( 'Gradient angle (0-180&deg;)', 'osixthreeo' ),
					'section'     => 'osixthreeo_ch_bgcolor',
					'settings'    => 'osixthreeo_settings[header_gradient_angle]',
					'input_attrs' => array(
						'min'  => 0,
						'max'  => 180,
						'step' => 5,
					),
					'priority'    => 30,
				)
			)
		);

		// gradient left stop point.
		$wp_customize->add_setting(
			'osixthreeo_settings[header_left_stop]',
			array(
				'default'           => $defaults['header_left_stop'],
				'type'              => 'option',
				'sanitize_callback' => 'osixthreeo_sanitize_integer',
			)
		);
		$wp_customize->add_control(
			new Osixthreeo_Range_Control(
				$wp_customize,
				'osixthreeo_settings[header_left_stop]',
				array(
					'type'        => 'range',
					'label'       => esc_html__( 'Gradient left blend point', 'osixthreeo' ),
					'section'     => 'osixthreeo_ch_bgcolor',
					'settings'    => 'osixthreeo_settings[header_left_stop]',
					'input_attrs' => array(
						'min'  => 0,
						'max'  => 100,
						'step' => 5,
					),
					'priority'    => 40,
				)
			)
		);

		// gradient right stop point.
		$wp_customize->add_setting(
			'osixthreeo_settings[header_right_stop]',
			array(
				'default'           => $defaults['header_right_stop'],
				'type'              => 'option',
				'sanitize_callback' => 'osixthreeo_sanitize_integer',
			)
		);
		$wp_customize->add_control(
			new Osixthreeo_Range_Control(
				$wp_customize,
				'osixthreeo_settings[header_right_stop]',
				array(
					'type'        => 'range',
					'label'       => esc_html__( 'Gradient right blend point', 'osixthreeo' ),
					'section'     => 'osixthreeo_ch_bgcolor',
					'settings'    => 'osixthreeo_settings[header_right_stop]',
					'input_attrs' => array(
						'min'  => 10,
						'max'  => 100,
						'step' => 5,
					),
					'priority'    => 50,
				)
			)
		);

		// SUB PANEL ---------------------------------- .
		$wp_customize->add_section(
			'header_image',
			array(
				'title'    => esc_html__( 'Background Image/Video', 'osixthreeo' ),
				'panel'    => 'osixthreeo_header_panel',
				'priority' => 20,
			)
		);

		// BG Size.
		$wp_customize->add_setting(
			'osixthreeo_settings[header_bg_size]',
			array(
				'default'           => $defaults['header_bg_size'],
				'type'              => 'option',
				'sanitize_callback' => 'osixthreeo_sanitize_choices',
				'transport'         => 'postMessage',
			)
		);
		$wp_customize->add_control(
			'osixthreeo_settings[header_bg_size]',
			array(
				'type'     => 'select',
				'label'    => esc_html__( 'Background image size', 'osixthreeo' ),
				'section'  => 'header_image',
				'choices'  => array(
					'cover'   => esc_html__( 'Cover (default)', 'osixthreeo' ),
					'contain' => esc_html__( 'Contain', 'osixthreeo' ),
					'auto'    => esc_html__( 'Auto', 'osixthreeo' ),
				),
				'settings' => 'osixthreeo_settings[header_bg_size]',
				'priority' => 70,
			)
		);

		// BG Image Position.
		$wp_customize->add_setting(
			'osixthreeo_settings[header_bg_position]',
			array(
				'default'           => $defaults['header_bg_position'],
				'type'              => 'option',
				'sanitize_callback' => 'osixthreeo_sanitize_choices',
				'transport'         => 'postMessage',
			)
		);
		$wp_customize->add_control(
			'osixthreeo_settings[header_bg_position]',
			array(
				'type'     => 'select',
				'label'    => esc_html__( 'Background image position', 'osixthreeo' ),
				'section'  => 'header_image',
				'choices'  => array(
					'left-top'      => esc_html__( 'Left Top', 'osixthreeo' ),
					'left-center'   => esc_html__( 'Left Center', 'osixthreeo' ),
					'left-bottom'   => esc_html__( 'Left Bottom', 'osixthreeo' ),
					'right-top'     => esc_html__( 'Right Top', 'osixthreeo' ),
					'right-center'  => esc_html__( 'Right Center', 'osixthreeo' ),
					'right-bottom'  => esc_html__( 'Right Bottom', 'osixthreeo' ),
					'center-top'    => esc_html__( 'Center Top', 'osixthreeo' ),
					'center-center' => esc_html__( 'Center Center (default)', 'osixthreeo' ),
					'center-bottom' => esc_html__( 'Center Bottom', 'osixthreeo' ),
				),
				'settings' => 'osixthreeo_settings[header_bg_position]',
				'priority' => 71,
			)
		);
		// BG Repeat.
		$wp_customize->add_setting(
			'osixthreeo_settings[header_bg_repeat]',
			array(
				'default'           => $defaults['header_bg_repeat'],
				'type'              => 'option',
				'sanitize_callback' => 'osixthreeo_sanitize_choices',
				'transport'         => 'postMessage',
			)
		);
		$wp_customize->add_control(
			'osixthreeo_settings[header_bg_repeat]',
			array(
				'type'     => 'select',
				'label'    => esc_html__( 'Background image repeat', 'osixthreeo' ),
				'section'  => 'header_image',
				'choices'  => array(
					'no-repeat' => esc_html__( 'No Repeat (default)', 'osixthreeo' ),
					'repeat'    => esc_html__( 'Tile', 'osixthreeo' ),
					'repeat-x'  => esc_html__( 'Tile Horizontally', 'osixthreeo' ),
					'repeat-y'  => esc_html__( 'Tile Vertically', 'osixthreeo' ),
				),
				'settings' => 'osixthreeo_settings[header_bg_repeat]',
				'priority' => 72,
			)
		);

		// Parallax Headers --------------------------------------------------- .
		$wp_customize->add_setting(
			'osixthreeo_settings[parallax_header]',
			array(
				'default'           => $defaults['parallax_header'],
				'type'              => 'option',
				'sanitize_callback' => 'osixthreeo_sanitize_checkbox',
			)
		);
		$wp_customize->add_control(
			'osixthreeo_settings[parallax_header]',
			array(
				'type'        => 'checkbox',
				'label'       => esc_html__( 'APPLY PARALLAX', 'osixthreeo' ),
				'description' => esc_html__( 'Apply a parallax effect to images in the custom header', 'osixthreeo' ),
				'section'     => 'header_image',
				'settings'    => 'osixthreeo_settings[parallax_header]',
				'priority'    => 80,
			)
		);

		// SUB PANEL ---------------------------------- .
		$wp_customize->add_section(
			'osixthreeo_ch_text',
			array(
				'title'    => esc_html__( 'Homepage Overlay Text', 'osixthreeo' ),
				'panel'    => 'osixthreeo_header_panel',
				'priority' => 30,
			)
		);

		// Primary Text (message).
		$wp_customize->add_setting(
			'primary-text-message',
			array(
				'sanitize_callback' => 'wp_kses_post',
			)
		);
		$wp_customize->add_control(
			new Osixthreeo_Content_Area(
				$wp_customize,
				'primary-text-message',
				array(
					'section'  => 'osixthreeo_ch_text',
					'priority' => 5,
					'label'    => esc_html__( 'Primary text', 'osixthreeo' ),
				)
			)
		);

		// Primary Text.
		$wp_customize->add_setting(
			'osixthreeo_settings[hero_text_primary]',
			array(
				'default'           => $defaults['hero_text_primary'],
				'type'              => 'option',
				'sanitize_callback' => 'wp_kses_post',
			)
		);
		$wp_customize->add_control(
			'osixthreeo_settings[hero_text_primary]',
			array(
				'type'     => 'textarea',
				'section'  => 'osixthreeo_ch_text',
				'priority' => 10,
			)
		);

		// Primary Text font family.
		$wp_customize->add_setting(
			'osixthreeo_settings[hero_text_primary_font]',
			array(
				'default'           => $defaults['hero_text_primary_font'],
				'type'              => 'option',
				'sanitize_callback' => 'osixthreeo_sanitize_choices',
			)
		);
		$wp_customize->add_control(
			'osixthreeo_settings[hero_text_primary_font]',
			array(
				'type'     => 'select',
				'label'    => esc_html__( 'Font family', 'osixthreeo' ),
				'section'  => 'osixthreeo_ch_text',
				'choices'  => array(
					''         => esc_html__( 'Base font', 'osixthreeo' ),
					'header'   => esc_html__( 'Header font', 'osixthreeo' ),
					'highlite' => esc_html__( 'Highlite font', 'osixthreeo' ),
				),
				'settings' => 'osixthreeo_settings[hero_text_primary_font]',
				'priority' => 11,
			)
		);

		// Primary Text color.
		$wp_customize->add_setting(
			'osixthreeo_settings[hero_text_primary_color]',
			array(
				'default'           => $defaults['hero_text_primary_color'],
				'type'              => 'option',
				'sanitize_callback' => 'osixthreeo_sanitize_rgba',
				'transport'         => 'postMessage',
			)
		);
		$wp_customize->add_control(
			new Osixthreeo_Alpha_Color_Control(
				$wp_customize,
				'osixthreeo_settings[hero_text_primary_color]',
				array(
					'label'    => esc_html__( 'Color', 'osixthreeo' ),
					'section'  => 'osixthreeo_ch_text',
					'settings' => 'osixthreeo_settings[hero_text_primary_color]',
					'priority' => 12,
				)
			)
		);

		// Primary Text font size - Desktop.
		$wp_customize->add_setting(
			'osixthreeo_settings[hero_text_primary_font_size]',
			array(
				'default'           => $defaults['hero_text_primary_font_size'],
				'type'              => 'option',
				'sanitize_callback' => 'osixthreeo_sanitize_integer',
				'transport'         => 'postMessage',
			)
		);
		$wp_customize->add_control(
			new Osixthreeo_Range_Control(
				$wp_customize,
				'osixthreeo_settings[hero_text_primary_font_size]',
				array(
					'type'        => 'range',
					'label'       => esc_html__( 'Font size - Desktop', 'osixthreeo' ),
					'section'     => 'osixthreeo_ch_text',
					'settings'    => 'osixthreeo_settings[hero_text_primary_font_size]',
					'input_attrs' => array(
						'min'  => 16,
						'max'  => 120,
						'step' => 1,
					),
					'priority'    => 13,
				)
			)
		);

		// Primary Text font size - Mobile.
		$wp_customize->add_setting(
			'osixthreeo_settings[hero_text_primary_font_size_mobile]',
			array(
				'default'           => $defaults['hero_text_primary_font_size_mobile'],
				'type'              => 'option',
				'sanitize_callback' => 'osixthreeo_sanitize_integer',
			)
		);
		$wp_customize->add_control(
			new Osixthreeo_Range_Control(
				$wp_customize,
				'osixthreeo_settings[hero_text_primary_font_size_mobile]',
				array(
					'type'        => 'range',
					'label'       => esc_html__( 'Font size - Mobile', 'osixthreeo' ),
					'section'     => 'osixthreeo_ch_text',
					'settings'    => 'osixthreeo_settings[hero_text_primary_font_size_mobile]',
					'input_attrs' => array(
						'min'  => 16,
						'max'  => 80,
						'step' => 1,
					),
					'priority'    => 14,
				)
			)
		);

		// Primary Text alignment.
		$wp_customize->add_setting(
			'osixthreeo_settings[hero_text_primary_alignment]',
			array(
				'default'           => $defaults['hero_text_primary_alignment'],
				'type'              => 'option',
				'sanitize_callback' => 'osixthreeo_sanitize_choices',
				'transport'         => 'postMessage',
			)
		);
		$wp_customize->add_control(
			'osixthreeo_settings[hero_text_primary_alignment]',
			array(
				'type'     => 'select',
				'label'    => esc_html__( 'Alignment', 'osixthreeo' ),
				'section'  => 'osixthreeo_ch_text',
				'choices'  => array(
					'left'   => esc_html__( 'Left', 'osixthreeo' ),
					'right'  => esc_html__( 'Right', 'osixthreeo' ),
					'center' => esc_html__( 'Centered', 'osixthreeo' ),
				),
				'settings' => 'osixthreeo_settings[hero_text_primary_alignment]',
				'priority' => 15,
			)
		);

		// Primary Text Shadow (message).
		$wp_customize->add_setting(
			'h-ot-primary-shadow-message',
			array(
				'sanitize_callback' => 'wp_kses_post',
			)
		);
		$wp_customize->add_control(
			new Osixthreeo_Content_Area(
				$wp_customize,
				'h-ot-primary-shadow-message',
				array(
					'section'  => 'osixthreeo_ch_text',
					'content'  => esc_html__( 'Text Shadow', 'osixthreeo' ),
					'priority' => 16,
				)
			)
		);
		// Primary Text Shadow color.
		$wp_customize->add_setting(
			'osixthreeo_settings[hero_text_primary_shadow_color]',
			array(
				'default'           => $defaults['hero_text_primary_shadow_color'],
				'type'              => 'option',
				'sanitize_callback' => 'osixthreeo_sanitize_rgba',
			)
		);
		$wp_customize->add_control(
			new Osixthreeo_Alpha_Color_Control(
				$wp_customize,
				'osixthreeo_settings[hero_text_primary_shadow_color]',
				array(
					'label'    => esc_html__( 'Color', 'osixthreeo' ),
					'section'  => 'osixthreeo_ch_text',
					'settings' => 'osixthreeo_settings[hero_text_primary_shadow_color]',
					'priority' => 17,
				)
			)
		);
		// Primary Text Shadow X-offset.
		$wp_customize->add_setting(
			'osixthreeo_settings[hero_text_primary_shadow_x]',
			array(
				'default'           => $defaults['hero_text_primary_shadow_x'],
				'type'              => 'option',
				'sanitize_callback' => 'osixthreeo_sanitize_intval',
			)
		);
		$wp_customize->add_control(
			'osixthreeo_settings[hero_text_primary_shadow_x]',
			array(
				'type'     => 'number',
				'label'    => esc_html__( 'x offset', 'osixthreeo' ),
				'section'  => 'osixthreeo_ch_text',
				'settings' => 'osixthreeo_settings[hero_text_primary_shadow_x]',
				'priority' => 18,
			)
		);
		// Primary Text Shadow Y-offset.
		$wp_customize->add_setting(
			'osixthreeo_settings[hero_text_primary_shadow_y]',
			array(
				'default'           => $defaults['hero_text_primary_shadow_y'],
				'type'              => 'option',
				'sanitize_callback' => 'osixthreeo_sanitize_intval',
			)
		);
		$wp_customize->add_control(
			'osixthreeo_settings[hero_text_primary_shadow_y]',
			array(
				'type'     => 'number',
				'label'    => esc_html__( 'y offset', 'osixthreeo' ),
				'section'  => 'osixthreeo_ch_text',
				'settings' => 'osixthreeo_settings[hero_text_primary_shadow_y]',
				'priority' => 19,
			)
		);
		// Primary Text Shadow blur.
		$wp_customize->add_setting(
			'osixthreeo_settings[hero_text_primary_shadow_blur]',
			array(
				'default'           => $defaults['hero_text_primary_shadow_blur'],
				'type'              => 'option',
				'sanitize_callback' => 'osixthreeo_sanitize_integer',
			)
		);
		$wp_customize->add_control(
			'osixthreeo_settings[hero_text_primary_shadow_blur]',
			array(
				'type'        => 'number',
				'label'       => esc_html__( 'Blur', 'osixthreeo' ),
				'section'     => 'osixthreeo_ch_text',
				'settings'    => 'osixthreeo_settings[hero_text_primary_shadow_blur]',
				'input_attrs' => array(
					'min'  => 0,
					'max'  => 100,
					'step' => 1,
				),
				'priority'    => 20,
			)
		);

		// Secondary Text (message).
		$wp_customize->add_setting(
			'secondary-text-message',
			array(
				'sanitize_callback' => 'wp_kses_post',
			)
		);
		$wp_customize->add_control(
			new Osixthreeo_Content_Area(
				$wp_customize,
				'secondary-text-message',
				array(
					'section'  => 'osixthreeo_ch_text',
					'label'    => esc_html__( 'Secondary text', 'osixthreeo' ),
					'priority' => 30,
				)
			)
		);

		// Secondary Text.
		$wp_customize->add_setting(
			'osixthreeo_settings[hero_text_secondary]',
			array(
				'default'           => $defaults['hero_text_secondary'],
				'type'              => 'option',
				'sanitize_callback' => 'wp_kses_post',
			)
		);
		$wp_customize->add_control(
			'osixthreeo_settings[hero_text_secondary]',
			array(
				'type'     => 'textarea',
				'section'  => 'osixthreeo_ch_text',
				'priority' => 31,
			)
		);

		// Secondary Text font family.
		$wp_customize->add_setting(
			'osixthreeo_settings[hero_text_secondary_font]',
			array(
				'default'           => $defaults['hero_text_secondary_font'],
				'type'              => 'option',
				'sanitize_callback' => 'osixthreeo_sanitize_choices',
			)
		);
		$wp_customize->add_control(
			'osixthreeo_settings[hero_text_secondary_font]',
			array(
				'type'     => 'select',
				'label'    => esc_html__( 'Font family', 'osixthreeo' ),
				'section'  => 'osixthreeo_ch_text',
				'choices'  => array(
					''         => esc_html__( 'Base font', 'osixthreeo' ),
					'header'   => esc_html__( 'Header font', 'osixthreeo' ),
					'highlite' => esc_html__( 'Highlite font', 'osixthreeo' ),
				),
				'settings' => 'osixthreeo_settings[hero_text_secondary_font]',
				'priority' => 32,
			)
		);

		// Secondary Text color.
		$wp_customize->add_setting(
			'osixthreeo_settings[hero_text_secondary_color]',
			array(
				'default'           => $defaults['hero_text_secondary_color'],
				'type'              => 'option',
				'sanitize_callback' => 'osixthreeo_sanitize_rgba',
				'transport'         => 'postMessage',
			)
		);
		$wp_customize->add_control(
			new Osixthreeo_Alpha_Color_Control(
				$wp_customize,
				'osixthreeo_settings[hero_text_secondary_color]',
				array(
					'label'    => esc_html__( 'Color', 'osixthreeo' ),
					'section'  => 'osixthreeo_ch_text',
					'settings' => 'osixthreeo_settings[hero_text_secondary_color]',
					'priority' => 33,
				)
			)
		);

		// Secondary Text font size - Desktop.
		$wp_customize->add_setting(
			'osixthreeo_settings[hero_text_secondary_font_size]',
			array(
				'default'           => $defaults['hero_text_secondary_font_size'],
				'type'              => 'option',
				'sanitize_callback' => 'osixthreeo_sanitize_integer',
				'transport'         => 'postMessage',
			)
		);
		$wp_customize->add_control(
			new Osixthreeo_Range_Control(
				$wp_customize,
				'osixthreeo_settings[hero_text_secondary_font_size]',
				array(
					'type'        => 'range',
					'label'       => esc_html__( 'Font size - Desktop', 'osixthreeo' ),
					'section'     => 'osixthreeo_ch_text',
					'settings'    => 'osixthreeo_settings[hero_text_secondary_font_size]',
					'input_attrs' => array(
						'min'  => 14,
						'max'  => 80,
						'step' => 1,
					),
					'priority'    => 34,
				)
			)
		);
		// Secondary Text font size - Mobile.
		$wp_customize->add_setting(
			'osixthreeo_settings[hero_text_secondary_font_size_mobile]',
			array(
				'default'           => $defaults['hero_text_secondary_font_size_mobile'],
				'type'              => 'option',
				'sanitize_callback' => 'osixthreeo_sanitize_integer',
			)
		);
		$wp_customize->add_control(
			new Osixthreeo_Range_Control(
				$wp_customize,
				'osixthreeo_settings[hero_text_secondary_font_size_mobile]',
				array(
					'type'        => 'range',
					'label'       => esc_html__( 'Font size - Mobile', 'osixthreeo' ),
					'section'     => 'osixthreeo_ch_text',
					'settings'    => 'osixthreeo_settings[hero_text_secondary_font_size_mobile]',
					'input_attrs' => array(
						'min'  => 14,
						'max'  => 48,
						'step' => 1,
					),
					'priority'    => 35,
				)
			)
		);
		// Secondary Text alignment.
		$wp_customize->add_setting(
			'osixthreeo_settings[hero_text_secondary_alignment]',
			array(
				'default'           => $defaults['hero_text_secondary_alignment'],
				'type'              => 'option',
				'sanitize_callback' => 'osixthreeo_sanitize_choices',
				'transport'         => 'postMessage',
			)
		);
		$wp_customize->add_control(
			'osixthreeo_settings[hero_text_secondary_alignment]',
			array(
				'type'     => 'select',
				'label'    => esc_html__( 'Alignment', 'osixthreeo' ),
				'section'  => 'osixthreeo_ch_text',
				'choices'  => array(
					'left'   => esc_html__( 'Left', 'osixthreeo' ),
					'right'  => esc_html__( 'Right', 'osixthreeo' ),
					'center' => esc_html__( 'Centered', 'osixthreeo' ),
				),
				'settings' => 'osixthreeo_settings[hero_text_secondary_alignment]',
				'priority' => 36,
			)
		);

		// Secondary Text Shadow.
		$wp_customize->add_setting(
			'h-ot-secondary-shadow-message',
			array(
				'sanitize_callback' => 'wp_kses_post',
			)
		);
		$wp_customize->add_control(
			new Osixthreeo_Content_Area(
				$wp_customize,
				'h-ot-secondary-shadow-message',
				array(
					'section'  => 'osixthreeo_ch_text',
					'content'  => esc_html__( 'Text Shadow', 'osixthreeo' ),
					'priority' => 37,
				)
			)
		);
		// Secondary Text Shadow color.
		$wp_customize->add_setting(
			'osixthreeo_settings[hero_text_secondary_shadow_color]',
			array(
				'default'           => $defaults['hero_text_secondary_shadow_color'],
				'type'              => 'option',
				'sanitize_callback' => 'osixthreeo_sanitize_rgba',
			)
		);
		$wp_customize->add_control(
			new Osixthreeo_Alpha_Color_Control(
				$wp_customize,
				'osixthreeo_settings[hero_text_secondary_shadow_color]',
				array(
					'label'    => esc_html__( 'Color', 'osixthreeo' ),
					'section'  => 'osixthreeo_ch_text',
					'settings' => 'osixthreeo_settings[hero_text_secondary_shadow_color]',
					'priority' => 38,
				)
			)
		);
		// Secondary Text Shadow X-offset.
		$wp_customize->add_setting(
			'osixthreeo_settings[hero_text_secondary_shadow_x]',
			array(
				'default'           => $defaults['hero_text_secondary_shadow_x'],
				'type'              => 'option',
				'sanitize_callback' => 'osixthreeo_sanitize_intval',
			)
		);
		$wp_customize->add_control(
			'osixthreeo_settings[hero_text_secondary_shadow_x]',
			array(
				'type'     => 'number',
				'label'    => esc_html__( 'x offset', 'osixthreeo' ),
				'section'  => 'osixthreeo_ch_text',
				'settings' => 'osixthreeo_settings[hero_text_secondary_shadow_x]',
				'priority' => 39,
			)
		);
		// Secondary Text Shadow Y-offset.
		$wp_customize->add_setting(
			'osixthreeo_settings[hero_text_secondary_shadow_y]',
			array(
				'default'           => $defaults['hero_text_secondary_shadow_y'],
				'type'              => 'option',
				'sanitize_callback' => 'osixthreeo_sanitize_intval',
			)
		);
		$wp_customize->add_control(
			'osixthreeo_settings[hero_text_secondary_shadow_y]',
			array(
				'type'     => 'number',
				'label'    => esc_html__( 'y offset', 'osixthreeo' ),
				'section'  => 'osixthreeo_ch_text',
				'settings' => 'osixthreeo_settings[hero_text_secondary_shadow_y]',
				'priority' => 40,
			)
		);
		// Secondary Text Shadow blur.
		$wp_customize->add_setting(
			'osixthreeo_settings[hero_text_secondary_shadow_blur]',
			array(
				'default'           => $defaults['hero_text_secondary_shadow_blur'],
				'type'              => 'option',
				'sanitize_callback' => 'osixthreeo_sanitize_integer',
			)
		);
		$wp_customize->add_control(
			'osixthreeo_settings[hero_text_secondary_shadow_blur]',
			array(
				'type'        => 'number',
				'label'       => esc_html__( 'Blur', 'osixthreeo' ),
				'section'     => 'osixthreeo_ch_text',
				'settings'    => 'osixthreeo_settings[hero_text_secondary_shadow_blur]',
				'input_attrs' => array(
					'min'  => 0,
					'max'  => 100,
					'step' => 1,
				),
				'priority'    => 41,
			)
		);

		// Scroll Button (message).
		$wp_customize->add_setting(
			'scroll-button-message',
			array(
				'sanitize_callback' => 'wp_kses_post',
			)
		);
		$wp_customize->add_control(
			new Osixthreeo_Content_Area(
				$wp_customize,
				'scroll-button-message',
				array(
					'section'  => 'osixthreeo_ch_text',
					'label'    => esc_html__( 'Scroll-to-content button', 'osixthreeo' ),
					'priority' => 50,
				)
			)
		);
		// Scroll Button show/hide.
		$wp_customize->add_setting(
			'osixthreeo_settings[hero_scroll_button]',
			array(
				'default'           => $defaults['hero_scroll_button'],
				'type'              => 'option',
				'sanitize_callback' => 'osixthreeo_sanitize_checkbox',
			)
		);
		$wp_customize->add_control(
			'osixthreeo_settings[hero_scroll_button]',
			array(
				'type'     => 'checkbox',
				'label'    => esc_html__( 'Display button', 'osixthreeo' ),
				'section'  => 'osixthreeo_ch_text',
				'settings' => 'osixthreeo_settings[hero_scroll_button]',
				'priority' => 51,
			)
		);
		// Scroll Button alignment.
		$wp_customize->add_setting(
			'osixthreeo_settings[hero_scroll_button_alignment]',
			array(
				'default'           => $defaults['hero_scroll_button_alignment'],
				'type'              => 'option',
				'sanitize_callback' => 'osixthreeo_sanitize_choices',
				'transport'         => 'postMessage',
			)
		);
		$wp_customize->add_control(
			'osixthreeo_settings[hero_scroll_button_alignment]',
			array(
				'type'     => 'select',
				'label'    => esc_html__( 'Alignment', 'osixthreeo' ),
				'section'  => 'osixthreeo_ch_text',
				'choices'  => array(
					'left'   => esc_html__( 'Left', 'osixthreeo' ),
					'right'  => esc_html__( 'Right', 'osixthreeo' ),
					'center' => esc_html__( 'Centered', 'osixthreeo' ),
				),
				'settings' => 'osixthreeo_settings[hero_scroll_button_alignment]',
				'priority' => 52,
			)
		);

		// Note (message).
		$wp_customize->add_setting(
			'hometext-message',
			array(
				'sanitize_callback' => 'wp_kses_post',
			)
		);
		$wp_customize->add_control(
			new Osixthreeo_Content_Area(
				$wp_customize,
				'hometext-message',
				array(
					'section'  => 'osixthreeo_ch_text',
					'label'    => esc_html__( 'Note:', 'osixthreeo' ),
					'content'  => esc_html__( 'Text above only displays on the homepage.', 'osixthreeo' ) . '</p>',
					'priority' => 53,
				)
			)
		);

		/*
		 * THEME OPTIONS -------------------------------------------------------------------
		 * tab -----------------------------------------------------------------------------
		 * ---------------------------------------------------------------------------------
		 * ---------------------------------------------------------------------------------
		 */

		// PANEL - THEME OPTIONS ------------------------------------------.
		$wp_customize->add_panel(
			'osixthreeo_themeops',
			array(
				'title'    => esc_html__( 'Theme Options', 'osixthreeo' ),
				'priority' => 70,
			)
		);

		// SUBPANEL - SITE HEADER --------------------------------------- .
		// -------------------------------------------------------------- .
		$wp_customize->add_section(
			'osixthreeo_to_header',
			array(
				'title'    => esc_html__( 'Site Header', 'osixthreeo' ),
				'panel'    => 'osixthreeo_themeops',
				'priority' => 10,
			)
		);

		// Append Search to Nav -------------------- .
		$wp_customize->add_setting(
			'themeops-appendsearch-message',
			array(
				'sanitize_callback' => 'wp_kses_post',
			)
		);
		$wp_customize->add_control(
			new Osixthreeo_Content_Area(
				$wp_customize,
				'themeops-appendsearch-message',
				array(
					'section'  => 'osixthreeo_to_header',
					'label'    => esc_html__( 'Menu', 'osixthreeo' ),
					'priority' => 10,
				)
			)
		);

		$wp_customize->add_setting(
			'osixthreeo_settings[nav_search]',
			array(
				'default'           => $defaults['nav_search'],
				'type'              => 'option',
				'sanitize_callback' => 'osixthreeo_sanitize_checkbox',
			)
		);
		$wp_customize->add_control(
			'osixthreeo_settings[nav_search]',
			array(
				'type'        => 'checkbox',
				'label'       => esc_html__( 'MENU SEARCH', 'osixthreeo' ),
				'description' => esc_html__( 'Append search functionality to the menu.', 'osixthreeo' ),
				'section'     => 'osixthreeo_to_header',
				'settings'    => 'osixthreeo_settings[nav_search]',
				'priority'    => 11,
			)
		);

		// SUBPANEL - POST/PAGE ENTRIES --------------------------------- .
		// -------------------------------------------------------------- .
		$wp_customize->add_section(
			'osixthreeo_to_content',
			array(
				'title'    => esc_html__( 'Post/Page Entries', 'osixthreeo' ),
				'panel'    => 'osixthreeo_themeops',
				'priority' => 20,
			)
		);

		// Meta Data ------------------------- .
		$wp_customize->add_setting(
			'themeops-meta-message',
			array(
				'sanitize_callback' => 'wp_kses_post',
			)
		);
		$wp_customize->add_control(
			new Osixthreeo_Content_Area(
				$wp_customize,
				'themeops-meta-message',
				array(
					'section'  => 'osixthreeo_to_content',
					'label'    => esc_html__( 'Meta Data', 'osixthreeo' ),
					'priority' => 30,
				)
			)
		);
		// Post Header.
		$wp_customize->add_setting(
			'themeops-metaheader-message',
			array(
				'sanitize_callback' => 'wp_kses_post',
			)
		);
		$wp_customize->add_control(
			new Osixthreeo_Content_Area(
				$wp_customize,
				'themeops-metaheader-message',
				array(
					'section'  => 'osixthreeo_to_content',
					'content'  => esc_html__( 'Post header', 'osixthreeo' ),
					'priority' => 31,
				)
			)
		);
		// date.
		$wp_customize->add_setting(
			'osixthreeo_settings[meta_date]',
			array(
				'default'           => $defaults['meta_date'],
				'type'              => 'option',
				'sanitize_callback' => 'osixthreeo_sanitize_checkbox',
			)
		);
		$wp_customize->add_control(
			'osixthreeo_settings[meta_date]',
			array(
				'type'     => 'checkbox',
				'label'    => esc_html__( 'Publish Date', 'osixthreeo' ),
				'section'  => 'osixthreeo_to_content',
				'settings' => 'osixthreeo_settings[meta_date]',
				'priority' => 32,
			)
		);
		// author.
		$wp_customize->add_setting(
			'osixthreeo_settings[meta_author]',
			array(
				'default'           => $defaults['meta_author'],
				'type'              => 'option',
				'sanitize_callback' => 'osixthreeo_sanitize_checkbox',
			)
		);
		$wp_customize->add_control(
			'osixthreeo_settings[meta_author]',
			array(
				'type'     => 'checkbox',
				'label'    => esc_html__( 'Author', 'osixthreeo' ),
				'section'  => 'osixthreeo_to_content',
				'settings' => 'osixthreeo_settings[meta_author]',
				'priority' => 33,
			)
		);
		// comments.
		$wp_customize->add_setting(
			'osixthreeo_settings[meta_comments]',
			array(
				'default'           => $defaults['meta_comments'],
				'type'              => 'option',
				'sanitize_callback' => 'osixthreeo_sanitize_checkbox',
			)
		);
		$wp_customize->add_control(
			'osixthreeo_settings[meta_comments]',
			array(
				'type'     => 'checkbox',
				'label'    => esc_html__( 'Comments', 'osixthreeo' ),
				'section'  => 'osixthreeo_to_content',
				'settings' => 'osixthreeo_settings[meta_comments]',
				'priority' => 34,
			)
		);
		// updated.
		$wp_customize->add_setting(
			'osixthreeo_settings[meta_updated]',
			array(
				'default'           => $defaults['meta_updated'],
				'type'              => 'option',
				'sanitize_callback' => 'osixthreeo_sanitize_checkbox',
			)
		);
		$wp_customize->add_control(
			'osixthreeo_settings[meta_updated]',
			array(
				'type'     => 'checkbox',
				'label'    => esc_html__( 'Updated', 'osixthreeo' ),
				'section'  => 'osixthreeo_to_content',
				'settings' => 'osixthreeo_settings[meta_updated]',
				'priority' => 35,
			)
		);
		// Post Footer.
		$wp_customize->add_setting(
			'themeops-metafooter-message',
			array(
				'sanitize_callback' => 'wp_kses_post',
			)
		);
		$wp_customize->add_control(
			new Osixthreeo_Content_Area(
				$wp_customize,
				'themeops-metafooter-message',
				array(
					'section'  => 'osixthreeo_to_content',
					'content'  => esc_html__( 'Post footer', 'osixthreeo' ),
					'priority' => 36,
				)
			)
		);
		// show footer meta.
		$wp_customize->add_setting(
			'osixthreeo_settings[meta_footer]',
			array(
				'default'           => $defaults['meta_footer'],
				'type'              => 'option',
				'sanitize_callback' => 'osixthreeo_sanitize_checkbox',
			)
		);
		$wp_customize->add_control(
			'osixthreeo_settings[meta_footer]',
			array(
				'type'     => 'checkbox',
				'label'    => esc_html__( 'Categories & Tags', 'osixthreeo' ),
				'section'  => 'osixthreeo_to_content',
				'settings' => 'osixthreeo_settings[meta_footer]',
				'priority' => 37,
			)
		);
		// show post navigation.
		$wp_customize->add_setting(
			'osixthreeo_settings[post_nav]',
			array(
				'default'           => $defaults['post_nav'],
				'type'              => 'option',
				'sanitize_callback' => 'osixthreeo_sanitize_checkbox',
			)
		);
		$wp_customize->add_control(
			'osixthreeo_settings[post_nav]',
			array(
				'type'     => 'checkbox',
				'label'    => esc_html__( 'Post Navigation (prev, next)', 'osixthreeo' ),
				'section'  => 'osixthreeo_to_content',
				'settings' => 'osixthreeo_settings[post_nav]',
				'priority' => 38,
			)
		);

		// GET EXTENSIONS.
		if ( ! OSTO_XTRAS ) :
			$wp_customize->add_setting(
				'themeops-pro-callout',
				array(
					'sanitize_callback' => 'wp_kses_post',
				)
			);
			$wp_customize->add_control(
				new Osixthreeo_Content_Area(
					$wp_customize,
					'themeops-pro-callout',
					array(
						'section'  => 'osixthreeo_to_content',
						'priority' => 100,
						'label'    => esc_html__( 'Get more options with an OsixthreeO Extension', 'osixthreeo' ),
						'content'  => '<a href="' . OSIXTHREEO_THEME_LINK . '" class="probtn" target="_blank" rel="noopener">OsixthreeO.com</a>',
					)
				)
			);
		endif;

		// SUBPANEL - ARCHIVE ENTRIES ----------------------------------- .
		// -------------------------------------------------------------- .
		$wp_customize->add_section(
			'osixthreeo_to_archives',
			array(
				'title'    => esc_html__( 'Archive Entries', 'osixthreeo' ),
				'priority' => 30,
				'panel'    => 'osixthreeo_themeops',
			)
		);

		// Entry Elements.
		$wp_customize->add_setting(
			'to-a-elements-message',
			array(
				'sanitize_callback' => 'wp_kses_post',
			)
		);
		$wp_customize->add_control(
			new Osixthreeo_Content_Area(
				$wp_customize,
				'to-a-elements-message',
				array(
					'section'  => 'osixthreeo_to_archives',
					'label'    => esc_html__( 'Entry Elements', 'osixthreeo' ),
					'priority' => 10,
				)
			)
		);
		// Hide featured images.
		$wp_customize->add_setting(
			'osixthreeo_settings[archives_hide_featuredimage]',
			array(
				'default'           => $defaults['archives_hide_featuredimage'],
				'type'              => 'option',
				'sanitize_callback' => 'osixthreeo_sanitize_checkbox',
				'transport'         => 'postMessage',
			)
		);
		$wp_customize->add_control(
			'osixthreeo_settings[archives_hide_featuredimage]',
			array(
				'type'     => 'checkbox',
				'label'    => esc_html__( 'Hide the featured image', 'osixthreeo' ),
				'section'  => 'osixthreeo_to_archives',
				'settings' => 'osixthreeo_settings[archives_hide_featuredimage]',
				'priority' => 11,
			)
		);
		// Hide excerpt.
		$wp_customize->add_setting(
			'osixthreeo_settings[archives_hide_meta]',
			array(
				'default'           => $defaults['archives_hide_meta'],
				'type'              => 'option',
				'sanitize_callback' => 'osixthreeo_sanitize_checkbox',
				'transport'         => 'postMessage',
			)
		);
		$wp_customize->add_control(
			'osixthreeo_settings[archives_hide_meta]',
			array(
				'type'     => 'checkbox',
				'label'    => esc_html__( 'Hide the meta data', 'osixthreeo' ),
				'section'  => 'osixthreeo_to_archives',
				'settings' => 'osixthreeo_settings[archives_hide_meta]',
				'priority' => 12,
			)
		);
		// Hide excerpt.
		$wp_customize->add_setting(
			'osixthreeo_settings[archives_hide_excerpt]',
			array(
				'default'           => $defaults['archives_hide_excerpt'],
				'type'              => 'option',
				'sanitize_callback' => 'osixthreeo_sanitize_checkbox',
				'transport'         => 'postMessage',
			)
		);
		$wp_customize->add_control(
			'osixthreeo_settings[archives_hide_excerpt]',
			array(
				'type'     => 'checkbox',
				'label'    => esc_html__( 'Hide the excerpt', 'osixthreeo' ),
				'section'  => 'osixthreeo_to_archives',
				'settings' => 'osixthreeo_settings[archives_hide_excerpt]',
				'priority' => 13,
			)
		);
		// Hide readmore.
		$wp_customize->add_setting(
			'osixthreeo_settings[archives_hide_readmore]',
			array(
				'default'           => $defaults['archives_hide_readmore'],
				'type'              => 'option',
				'sanitize_callback' => 'osixthreeo_sanitize_checkbox',
				'transport'         => 'postMessage',
			)
		);
		$wp_customize->add_control(
			'osixthreeo_settings[archives_hide_readmore]',
			array(
				'type'     => 'checkbox',
				'label'    => esc_html__( 'Hide the Continue button', 'osixthreeo' ),
				'section'  => 'osixthreeo_to_archives',
				'settings' => 'osixthreeo_settings[archives_hide_readmore]',
				'priority' => 14,
			)
		);

		// Padding.
		$wp_customize->add_setting(
			'to-a-padding-message',
			array(
				'sanitize_callback' => 'wp_kses_post',
			)
		);
		$wp_customize->add_control(
			new Osixthreeo_Content_Area(
				$wp_customize,
				'to-a-padding-message',
				array(
					'section'  => 'osixthreeo_to_archives',
					'label'    => esc_html__( 'Padding', 'osixthreeo' ),
					'priority' => 20,
				)
			)
		);
		// Padding - Left.
		$wp_customize->add_setting(
			'osixthreeo_settings[archives_pad_left]',
			array(
				'default'           => $defaults['archives_pad_left'],
				'type'              => 'option',
				'sanitize_callback' => 'osixthreeo_sanitize_integer',
				'transport'         => 'postMessage',
			)
		);
		$wp_customize->add_control(
			new Osixthreeo_Number_Control(
				$wp_customize,
				'osixthreeo_settings[archives_pad_left]',
				array(
					'type'        => 'number',
					'label'       => esc_html__( 'Left', 'osixthreeo' ),
					'section'     => 'osixthreeo_to_archives',
					'input_attrs' => array(
						'min'  => 0,
						'max'  => 24,
						'step' => 1,
					),
					'settings'    => 'osixthreeo_settings[archives_pad_left]',
					'priority'    => 21,
				)
			)
		);
		// Padding - Right.
		$wp_customize->add_setting(
			'osixthreeo_settings[archives_pad_right]',
			array(
				'default'           => $defaults['archives_pad_right'],
				'type'              => 'option',
				'sanitize_callback' => 'osixthreeo_sanitize_integer',
				'transport'         => 'postMessage',
			)
		);
		$wp_customize->add_control(
			new Osixthreeo_Number_Control(
				$wp_customize,
				'osixthreeo_settings[archives_pad_right]',
				array(
					'type'        => 'number',
					'label'       => esc_html__( 'Right', 'osixthreeo' ),
					'section'     => 'osixthreeo_to_archives',
					'input_attrs' => array(
						'min'  => 0,
						'max'  => 24,
						'step' => 1,
					),
					'settings'    => 'osixthreeo_settings[archives_pad_right]',
					'priority'    => 22,
				)
			)
		);
		// Padding - Top.
		$wp_customize->add_setting(
			'osixthreeo_settings[archives_pad_top]',
			array(
				'default'           => $defaults['archives_pad_top'],
				'type'              => 'option',
				'sanitize_callback' => 'osixthreeo_sanitize_integer',
				'transport'         => 'postMessage',
			)
		);
		$wp_customize->add_control(
			new Osixthreeo_Number_Control(
				$wp_customize,
				'osixthreeo_settings[archives_pad_top]',
				array(
					'type'        => 'number',
					'label'       => esc_html__( 'Top', 'osixthreeo' ),
					'section'     => 'osixthreeo_to_archives',
					'input_attrs' => array(
						'min'  => 0,
						'max'  => 24,
						'step' => 1,
					),
					'settings'    => 'osixthreeo_settings[archives_pad_top]',
					'priority'    => 23,
				)
			)
		);
		// Padding - Bottom.
		$wp_customize->add_setting(
			'osixthreeo_settings[archives_pad_bottom]',
			array(
				'default'           => $defaults['archives_pad_bottom'],
				'type'              => 'option',
				'sanitize_callback' => 'osixthreeo_sanitize_integer',
				'transport'         => 'postMessage',
			)
		);
		$wp_customize->add_control(
			new Osixthreeo_Number_Control(
				$wp_customize,
				'osixthreeo_settings[archives_pad_bottom]',
				array(
					'type'        => 'number',
					'label'       => esc_html__( 'Bottom', 'osixthreeo' ),
					'section'     => 'osixthreeo_to_archives',
					'input_attrs' => array(
						'min'  => 0,
						'max'  => 24,
						'step' => 1,
					),
					'settings'    => 'osixthreeo_settings[archives_pad_bottom]',
					'priority'    => 24,
				)
			)
		);

		// BORDER.
		$wp_customize->add_setting(
			'to-a-border-message',
			array(
				'sanitize_callback' => 'wp_kses_post',
			)
		);
		$wp_customize->add_control(
			new Osixthreeo_Content_Area(
				$wp_customize,
				'to-a-border-message',
				array(
					'section'  => 'osixthreeo_to_archives',
					'label'    => esc_html__( 'Border', 'osixthreeo' ),
					'priority' => 30,
				)
			)
		);
		// Border - Color.
		$wp_customize->add_setting(
			'osixthreeo_settings[archives_border_color]',
			array(
				'default'           => $defaults['archives_border_color'],
				'type'              => 'option',
				'sanitize_callback' => 'osixthreeo_sanitize_rgba',
			)
		);
		$wp_customize->add_control(
			new Osixthreeo_Alpha_Color_Control(
				$wp_customize,
				'osixthreeo_settings[archives_border_color]',
				array(
					'label'    => esc_html__( 'Color', 'osixthreeo' ),
					'section'  => 'osixthreeo_to_archives',
					'settings' => 'osixthreeo_settings[archives_border_color]',
					'priority' => 31,
				)
			)
		);
		// Border - width.
		$wp_customize->add_setting(
			'osixthreeo_settings[archives_border_width]',
			array(
				'default'           => $defaults['archives_border_width'],
				'type'              => 'option',
				'sanitize_callback' => 'osixthreeo_sanitize_integer',
			)
		);
		$wp_customize->add_control(
			'osixthreeo_settings[archives_border_width]',
			array(
				'type'        => 'number',
				'label'       => esc_html__( 'Width', 'osixthreeo' ),
				'section'     => 'osixthreeo_to_archives',
				'input_attrs' => array(
					'min'  => 0,
					'max'  => 10,
					'step' => 1,
				),
				'settings'    => 'osixthreeo_settings[archives_border_width]',
				'priority'    => 32,
			)
		);
		// Border - Radius.
		$wp_customize->add_setting(
			'osixthreeo_settings[archives_border_radius]',
			array(
				'default'           => $defaults['archives_border_radius'],
				'type'              => 'option',
				'sanitize_callback' => 'osixthreeo_sanitize_integer',
				'transport'         => 'postMessage',
			)
		);
		$wp_customize->add_control(
			'osixthreeo_settings[archives_border_radius]',
			array(
				'type'        => 'number',
				'label'       => esc_html__( 'Border radius', 'osixthreeo' ),
				'section'     => 'osixthreeo_to_archives',
				'input_attrs' => array(
					'min'  => 0,
					'max'  => 120,
					'step' => 1,
				),
				'settings'    => 'osixthreeo_settings[archives_border_radius]',
				'priority'    => 33,
			)
		);

		// BOX SHADOW.
		$wp_customize->add_setting(
			'to-a-shadow-message',
			array(
				'sanitize_callback' => 'wp_kses_post',
			)
		);
		$wp_customize->add_control(
			new Osixthreeo_Content_Area(
				$wp_customize,
				'to-a-shadow-message',
				array(
					'section'  => 'osixthreeo_to_archives',
					'label'    => esc_html__( 'Box Shadow', 'osixthreeo' ),
					'priority' => 40,
				)
			)
		);
		// Shadow - Color.
		$wp_customize->add_setting(
			'osixthreeo_settings[archives_box_shadow_color]',
			array(
				'default'           => $defaults['archives_box_shadow_color'],
				'type'              => 'option',
				'sanitize_callback' => 'osixthreeo_sanitize_rgba',
			)
		);
		$wp_customize->add_control(
			new Osixthreeo_Alpha_Color_Control(
				$wp_customize,
				'osixthreeo_settings[archives_box_shadow_color]',
				array(
					'label'        => esc_html__( 'Color', 'osixthreeo' ),
					'section'      => 'osixthreeo_to_archives',
					'settings'     => 'osixthreeo_settings[archives_box_shadow_color]',
					'show_opacity' => true,
					'priority'     => 41,
				)
			)
		);

		// SHADOW - X.
		$wp_customize->add_setting(
			'osixthreeo_settings[archives_box_shadow_x]',
			array(
				'default'           => $defaults['archives_box_shadow_x'],
				'type'              => 'option',
				'sanitize_callback' => 'osixthreeo_sanitize_integer',
			)
		);
		$wp_customize->add_control(
			'osixthreeo_settings[archives_box_shadow_x]',
			array(
				'type'     => 'number',
				'label'    => esc_html__( 'x offset', 'osixthreeo' ),
				'section'  => 'osixthreeo_to_archives',
				'settings' => 'osixthreeo_settings[archives_box_shadow_x]',
				'priority' => 42,
			)
		);
		// SHADOW - Y.
		$wp_customize->add_setting(
			'osixthreeo_settings[archives_box_shadow_y]',
			array(
				'default'           => $defaults['archives_box_shadow_y'],
				'type'              => 'option',
				'sanitize_callback' => 'osixthreeo_sanitize_integer',
			)
		);
		$wp_customize->add_control(
			'osixthreeo_settings[archives_box_shadow_y]',
			array(
				'type'     => 'number',
				'label'    => esc_html__( 'y offset', 'osixthreeo' ),
				'section'  => 'osixthreeo_to_archives',
				'settings' => 'osixthreeo_settings[archives_box_shadow_y]',
				'priority' => 43,
			)
		);
		// SHADOW - Blur.
		$wp_customize->add_setting(
			'osixthreeo_settings[archives_box_shadow_blur]',
			array(
				'default'           => $defaults['archives_box_shadow_blur'],
				'type'              => 'option',
				'sanitize_callback' => 'osixthreeo_sanitize_integer',
			)
		);
		$wp_customize->add_control(
			'osixthreeo_settings[archives_box_shadow_blur]',
			array(
				'type'        => 'number',
				'label'       => esc_html__( 'Blur', 'osixthreeo' ),
				'section'     => 'osixthreeo_to_archives',
				'settings'    => 'osixthreeo_settings[archives_box_shadow_blur]',
				'input_attrs' => array(
					'min'  => 0,
					'max'  => 100,
					'step' => 1,
				),
				'priority'    => 44,
			)
		);
		// Shadow - Spread.
		$wp_customize->add_setting(
			'osixthreeo_settings[archives_box_shadow_spread]',
			array(
				'default'           => $defaults['archives_box_shadow_spread'],
				'type'              => 'option',
				'sanitize_callback' => 'osixthreeo_sanitize_integer',
			)
		);
		$wp_customize->add_control(
			'osixthreeo_settings[archives_box_shadow_spread]',
			array(
				'type'        => 'number',
				'label'       => esc_html__( 'Spread', 'osixthreeo' ),
				'section'     => 'osixthreeo_to_archives',
				'settings'    => 'osixthreeo_settings[archives_box_shadow_spread]',
				'input_attrs' => array(
					'min'  => 0,
					'max'  => 100,
					'step' => 1,
				),
				'priority'    => 45,
			)
		);

		// GET EXTENSIONS.
		if ( ! OSTO_XTRAS ) :
			$wp_customize->add_setting(
				'themeops-a-pro-callout',
				array(
					'sanitize_callback' => 'wp_kses_post',
				)
			);
			$wp_customize->add_control(
				new Osixthreeo_Content_Area(
					$wp_customize,
					'themeops-a-pro-callout',
					array(
						'section'  => 'osixthreeo_to_archives',
						'label'    => esc_html__( 'Get more options with an OsixthreeO Extension', 'osixthreeo' ),
						'content'  => '<a href="' . OSIXTHREEO_THEME_LINK . '" class="probtn" target="_blank" rel="noopener">OsixthreeO.com</a>',
						'priority' => 100,
					)
				)
			);
		endif;

		// SUBPANEL - SITE FOOTER --------------------------------------- .
		// -------------------------------------------------------------- .
		$wp_customize->add_section(
			'osixthreeo_to_footer',
			array(
				'title'    => esc_html__( 'Site Footer', 'osixthreeo' ),
				'panel'    => 'osixthreeo_themeops',
				'priority' => 40,
			)
		);

		// Back To Top.
		$wp_customize->add_setting(
			'to-f-backtotop-message',
			array(
				'sanitize_callback' => 'wp_kses_post',
			)
		);
		$wp_customize->add_control(
			new Osixthreeo_Content_Area(
				$wp_customize,
				'to-f-backtotop-message',
				array(
					'section'  => 'osixthreeo_to_footer',
					'label'    => esc_html__( 'Back To Top', 'osixthreeo' ),
					'priority' => 10,
				)
			)
		);
		$wp_customize->add_setting(
			'osixthreeo_settings[back_to_top]',
			array(
				'default'           => $defaults['back_to_top'],
				'type'              => 'option',
				'sanitize_callback' => 'osixthreeo_sanitize_checkbox',
			)
		);
		$wp_customize->add_control(
			'osixthreeo_settings[back_to_top]',
			array(
				'type'        => 'checkbox',
				'label'       => esc_html__( 'Add a Back To Top button', 'osixthreeo' ),
				'description' => esc_html__( 'Appears on the right side of the site footer.', 'osixthreeo' ),
				'section'     => 'osixthreeo_to_footer',
				'settings'    => 'osixthreeo_settings[back_to_top]',
				'priority'    => 11,
			)
		);

		// Footer Columns.
		$wp_customize->add_setting(
			'to-f-columns-message',
			array(
				'sanitize_callback' => 'wp_kses_post',
			)
		);
		$wp_customize->add_control(
			new Osixthreeo_Content_Area(
				$wp_customize,
				'to-f-columns-message',
				array(
					'section'  => 'osixthreeo_to_footer',
					'label'    => esc_html__( 'Widget Columns', 'osixthreeo' ),
					'priority' => 12,
				)
			)
		);
		$wp_customize->add_setting(
			'osixthreeo_settings[footer_columns]',
			array(
				'default'           => $defaults['footer_columns'],
				'type'              => 'option',
				'sanitize_callback' => 'osixthreeo_sanitize_checkbox',
			)
		);
		$wp_customize->add_control(
			'osixthreeo_settings[footer_columns]',
			array(
				'type'     => 'checkbox',
				'label'    => esc_html__( 'Display multiple widgets as responsive columns.', 'osixthreeo' ),
				'section'  => 'osixthreeo_to_footer',
				'settings' => 'osixthreeo_settings[footer_columns]',
				'priority' => 13,
			)
		);
	}
}

/**
 * Binds JS handlers to make Theme Customizer preview reload changes asynchronously.
 *
 * @since 0.1
 */
function osixthreeo_customizer_live_preview() {
	wp_enqueue_script( 'osixthreeo-themecustomizer', trailingslashit( get_template_directory_uri() ) . 'assets/js/customizer-min.js', array( 'jquery', 'customize-preview' ), OSIXTHREEO_VERSION, true );
}
add_action( 'customize_preview_init', 'osixthreeo_customizer_live_preview' );

/**
 * Custom contextual controls
 *
 * @since 1.0.0
 */
function osixthreeo_customizer_panel() {
	wp_enqueue_script( 'osixthreeo-customizer-panel', trailingslashit( get_template_directory_uri() ) . 'assets/js/customizer-panel-min.js', array( 'customize-controls' ), OSIXTHREEO_VERSION, false );
}
add_action( 'customize_controls_enqueue_scripts', 'osixthreeo_customizer_panel' );
