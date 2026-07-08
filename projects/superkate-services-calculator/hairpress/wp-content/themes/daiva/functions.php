<?php
// Exit if accessed directly
if ( !defined( 'ABSPATH' ) ) exit;

// Overwrite parent theme background defaults and registers support for WordPress features.
add_action( 'after_setup_theme', 'lalita_background_setup' );
function lalita_background_setup() {
	add_theme_support( "custom-background",
		array(
			'default-color' 		 => '222222',
			'default-image'          => '',
			'default-repeat'         => 'repeat',
			'default-position-x'     => 'left',
			'default-position-y'     => 'top',
			'default-size'           => 'auto',
			'default-attachment'     => '',
			'wp-head-callback'       => '_custom_background_cb',
			'admin-head-callback'    => '',
			'admin-preview-callback' => ''
		)
	);
}

// Overwrite theme URL
function lalita_theme_uri_link() {
	return 'https://wpkoi.com/daiva-wpkoi-wordpress-theme/';
}

// Overwrite parent theme's blog header function
add_action( 'lalita_after_header', 'lalita_blog_header_image', 11 );
function lalita_blog_header_image() {

	if ( ( is_front_page() && is_home() ) || ( is_home() ) ) { 
		$blog_header_image 			=  lalita_get_setting( 'blog_header_image' ); 
		$blog_header_title 			=  lalita_get_setting( 'blog_header_title' ); 
		$blog_header_text 			=  lalita_get_setting( 'blog_header_text' ); 
		$blog_header_button_text 	=  lalita_get_setting( 'blog_header_button_text' ); 
		$blog_header_button_url 	=  lalita_get_setting( 'blog_header_button_url' ); 
		if ( $blog_header_image != '' ) { ?>
		<div class="page-header-image grid-parent page-header-blog" style="background-image: url('<?php echo esc_url($blog_header_image); ?>') !important;">
        	<div class="page-header-noiseoverlay"></div>
        	<div class="page-header-blog-inner">
                <div class="page-header-blog-content-h grid-container">
                    <div class="page-header-blog-content">
                    <?php if ( $blog_header_title != '' ) { ?>
                        <div class="page-header-blog-text">
                            <?php if ( $blog_header_title != '' ) { ?>
                            <h2><?php echo wp_kses_post( $blog_header_title ); ?></h2>
                            <div class="clearfix"></div>
                            <?php } ?>
                        </div>
                    <?php } ?>
                    </div>
                </div>
                <div class="page-header-blog-content page-header-blog-content-b">
                	<?php if ( $blog_header_text != '' ) { ?>
                	<div class="page-header-blog-text">
						<?php if ( $blog_header_title != '' ) { ?>
                        <p><?php echo wp_kses_post( $blog_header_text ); ?></p>
                        <div class="clearfix"></div>
                        <?php } ?>
                    </div>
                    <?php } ?>
                    <div class="page-header-blog-button">
                        <?php if ( $blog_header_button_text != '' ) { ?>
                        <a class="read-more button" href="<?php echo esc_url( $blog_header_button_url ); ?>"><?php echo esc_html( $blog_header_button_text ); ?></a>
                        <?php } ?>
                    </div>
                </div>
            </div>
		</div>
		<?php
		}
	}
}

// Extra cutomizer functions
if ( ! function_exists( 'daiva_customize_register' ) ) {
	add_action( 'customize_register', 'daiva_customize_register' );
	function daiva_customize_register( $wp_customize ) {
				
		// Add Daiva customizer section
		$wp_customize->add_section(
			'daiva_layout_effects',
			array(
				'title' => __( 'Daiva Effects', 'daiva' ),
				'priority' => 24,
			)
		);
		
		
		// Color frame
		$wp_customize->add_setting(
			'daiva_settings[color_frame]',
			array(
				'default' => 'enable',
				'type' => 'option',
				'sanitize_callback' => 'daiva_sanitize_choices'
			)
		);

		$wp_customize->add_control(
			'daiva_settings[color_frame]',
			array(
				'type' => 'select',
				'label' => __( 'Color frame', 'daiva' ),
				'choices' => array(
					'enable' => __( 'Enable', 'daiva' ),
					'disable' => __( 'Disable', 'daiva' )
				),
				'settings' => 'daiva_settings[color_frame]',
				'section' => 'daiva_layout_effects',
				'priority' => 1
			)
		);
		
		// Color logo
		$wp_customize->add_setting(
			'daiva_settings[color_logo]',
			array(
				'default' => 'enable',
				'type' => 'option',
				'sanitize_callback' => 'daiva_sanitize_choices'
			)
		);

		$wp_customize->add_control(
			'daiva_settings[color_logo]',
			array(
				'type' => 'select',
				'label' => __( 'Color logo', 'daiva' ),
				'choices' => array(
					'enable' => __( 'Enable', 'daiva' ),
					'disable' => __( 'Disable', 'daiva' )
				),
				'settings' => 'daiva_settings[color_logo]',
				'section' => 'daiva_layout_effects',
				'priority' => 2
			)
		);
		
		// Menu colors
		$wp_customize->add_setting(
			'daiva_settings[menu_colors]',
			array(
				'default' => 'enable',
				'type' => 'option',
				'sanitize_callback' => 'daiva_sanitize_choices'
			)
		);

		$wp_customize->add_control(
			'daiva_settings[menu_colors]',
			array(
				'type' => 'select',
				'label' => __( 'Menu colors', 'daiva' ),
				'choices' => array(
					'enable' => __( 'Enable', 'daiva' ),
					'disable' => __( 'Disable', 'daiva' )
				),
				'settings' => 'daiva_settings[menu_colors]',
				'section' => 'daiva_layout_effects',
				'priority' => 3
			)
		);
		
		// Blog posts border
		$wp_customize->add_setting(
			'daiva_settings[blog_posts_effect]',
			array(
				'default' => 'enable',
				'type' => 'option',
				'sanitize_callback' => 'daiva_sanitize_choices'
			)
		);

		$wp_customize->add_control(
			'daiva_settings[blog_posts_effect]',
			array(
				'type' => 'select',
				'label' => __( 'Blog posts effect', 'daiva' ),
				'choices' => array(
					'enable' => __( 'Enable', 'daiva' ),
					'disable' => __( 'Disable', 'daiva' )
				),
				'settings' => 'daiva_settings[blog_posts_effect]',
				'section' => 'daiva_layout_effects',
				'priority' => 4
			)
		);
		
		// Daiva effect colors
		$wp_customize->add_setting(
			'daiva_settings[daiva_color_1]', array(
				'default' => '#FFB001',
				'type' => 'option',
				'sanitize_callback' => 'daiva_sanitize_hex_color',
			)
		);

		$wp_customize->add_control(
			new WP_Customize_Color_Control(
				$wp_customize,
				'daiva_settings[daiva_color_1]',
				array(
					'label' => __( 'Color 1 for Daiva effects', 'daiva' ),
					'section' => 'colors',
					'settings' => 'daiva_settings[daiva_color_1]',
					'priority' => 31
				)
			)
		);
		
		$wp_customize->add_setting(
			'daiva_settings[daiva_color_2]', array(
				'default' => '#44EE77',
				'type' => 'option',
				'sanitize_callback' => 'daiva_sanitize_hex_color',
			)
		);

		$wp_customize->add_control(
			new WP_Customize_Color_Control(
				$wp_customize,
				'daiva_settings[daiva_color_2]',
				array(
					'label' => __( 'Color 2 for Daiva effects', 'daiva' ),
					'section' => 'colors',
					'settings' => 'daiva_settings[daiva_color_2]',
					'priority' => 32
				)
			)
		);
		
		$wp_customize->add_setting(
			'daiva_settings[daiva_color_3]', array(
				'default' => '#019992',
				'type' => 'option',
				'sanitize_callback' => 'daiva_sanitize_hex_color',
			)
		);

		$wp_customize->add_control(
			new WP_Customize_Color_Control(
				$wp_customize,
				'daiva_settings[daiva_color_3]',
				array(
					'label' => __( 'Color 3 for Daiva effects', 'daiva' ),
					'section' => 'colors',
					'settings' => 'daiva_settings[daiva_color_3]',
					'priority' => 33
				)
			)
		);
		
		$wp_customize->add_setting(
			'daiva_settings[daiva_color_4]', array(
				'default' => '#FB475E',
				'type' => 'option',
				'sanitize_callback' => 'daiva_sanitize_hex_color',
			)
		);

		$wp_customize->add_control(
			new WP_Customize_Color_Control(
				$wp_customize,
				'daiva_settings[daiva_color_4]',
				array(
					'label' => __( 'Color 4 for Daiva effects', 'daiva' ),
					'section' => 'colors',
					'settings' => 'daiva_settings[daiva_color_4]',
					'priority' => 34
				)
			)
		);
		
	}
}

//Sanitize choices.
if ( ! function_exists( 'daiva_sanitize_choices' ) ) {
	function daiva_sanitize_choices( $input, $setting ) {
		// Ensure input is a slug
		$input = sanitize_key( $input );

		// Get list of choices from the control
		// associated with the setting
		$choices = $setting->manager->get_control( $setting->id )->choices;

		// If the input is a valid key, return it;
		// otherwise, return the default
		return ( array_key_exists( $input, $choices ) ? $input : $setting->default );
	}
}

// Sanitize colors. Allow blank value.
if ( ! function_exists( 'daiva_sanitize_hex_color' ) ) {
	function daiva_sanitize_hex_color( $color ) {
	    if ( '' === $color ) {
	        return '';
		}

	    // 3 or 6 hex digits, or the empty string.
	    if ( preg_match('|^#([A-Fa-f0-9]{3}){1,2}$|', $color ) ) {
	        return $color;
		}

	    return '';
	}
}

// Daiva effects colors css
if ( ! function_exists( 'daiva_effect_colors_css' ) ) {
	function daiva_effect_colors_css() {
		// Get Customizer settings
		$daiva_settings = get_option( 'daiva_settings' );
		
		$daiva_color_1  	 = '#FFB001';
		$daiva_color_2  	 = '#44EE77';
		$daiva_color_3  	 = '#019992';
		$daiva_color_4  	 = '#FB475E';
		if ( isset( $daiva_settings['daiva_color_1'] ) ) {
			$daiva_color_1 = $daiva_settings['daiva_color_1'];
		}
		if ( isset( $daiva_settings['daiva_color_2'] ) ) {
			$daiva_color_2 = $daiva_settings['daiva_color_2'];
		}
		if ( isset( $daiva_settings['daiva_color_3'] ) ) {
			$daiva_color_3 = $daiva_settings['daiva_color_3'];
		}
		if ( isset( $daiva_settings['daiva_color_4'] ) ) {
			$daiva_color_4 = $daiva_settings['daiva_color_4'];
		}
		
		$lalita_settings = wp_parse_args(
			get_option( 'lalita_settings', array() ),
			lalita_get_color_defaults()
		);
		
		$daiva_extracolors = '.daiva-frame-top {border-color: ' . esc_attr( $daiva_color_2 ) . ' transparent transparent transparent;}.daiva-frame-right {border-color: transparent ' . esc_attr( $daiva_color_3 ) . ' transparent transparent;}.daiva-frame-bottom {border-color: transparent transparent ' . esc_attr( $daiva_color_4 ) . ' transparent;}.daiva-frame-left {border-color: transparent transparent transparent ' . esc_attr( $daiva_color_1 ) . ';}.daiva-color-logo-style .main-title a .word span, .daiva-color-logo-style .main-title a .word span:nth-child(5), .daiva-color-logo-style .main-title a .word span:nth-child(9) {color: ' . esc_attr( $daiva_color_1 ) . '}.daiva-color-logo-style .main-title a .word span:nth-child(2), .daiva-color-logo-style .main-title a .word span:nth-child(6), .daiva-color-logo-style .main-title a .word span:nth-child(10), .daiva-menu-style .top-bar .lalita-socials-list li:nth-child(2) a, .daiva-menu-style .top-bar .lalita-socials-list li:nth-child(6) a {color: ' . esc_attr( $daiva_color_2 ) . '}.daiva-color-logo-style .main-title a .word span:nth-child(3), .daiva-color-logo-style .main-title a .word span:nth-child(7), .daiva-color-logo-style .main-title a .word span:nth-child(11), .daiva-menu-style .top-bar .lalita-socials-list li:nth-child(3) a, .daiva-menu-style .top-bar .lalita-socials-list li:nth-child(7) a {color: ' . esc_attr( $daiva_color_3 ) . '}.daiva-color-logo-style .main-title a .word span:nth-child(4), .daiva-color-logo-style .main-title a .word span:nth-child(8), .daiva-color-logo-style .main-title a .word span:nth-child(12), .daiva-menu-style .top-bar .lalita-socials-list li:nth-child(4) a, .daiva-menu-style .top-bar .lalita-socials-list li:nth-child(8) a {color: ' . esc_attr( $daiva_color_4 ) . '}.daiva-menu-style .main-navigation .main-nav ul li a, .daiva-menu-style .main-navigation .main-nav ul li:nth-child(5) a, .daiva-menu-style .main-navigation .main-nav ul li:nth-child(9) a {color: ' . esc_attr( $daiva_color_2 ) . '}.daiva-menu-style .main-navigation .main-nav ul li:nth-child(2) a, .daiva-menu-style .main-navigation .main-nav ul li:nth-child(6) a, .daiva-menu-style .main-navigation .main-nav ul li:nth-child(10) a {color: ' . esc_attr( $daiva_color_3 ) . '}.daiva-menu-style .main-navigation .main-nav ul li:nth-child(3) a, .daiva-menu-style .main-navigation .main-nav ul li:nth-child(7) a, .daiva-menu-style .main-navigation .main-nav ul li:nth-child(11) a {color: ' . esc_attr( $daiva_color_4 ) . '}.daiva-menu-style .main-navigation .main-nav ul li:nth-child(4) a, .daiva-menu-style .main-navigation .main-nav ul li:nth-child(8) a, .daiva-menu-style .main-navigation .main-nav ul li:nth-child(12) a {color: ' . esc_attr( $daiva_color_1 ) . '}.daiva-menu-style .top-bar .lalita-socials-list li a:hover{color: ' . esc_attr( $lalita_settings[ 'top_bar_link_color_hover' ] ) . '}.daiva-menu-style .main-navigation .main-nav ul li:hover > a {color: ' . esc_attr( $lalita_settings[ 'navigation_text_hover_color' ] ) . '}.daiva-menu-style .main-navigation .main-nav ul ul li a {color: ' . esc_attr( $lalita_settings[ 'subnavigation_text_color' ] ) . ' !important}.daiva-menu-style .main-navigation .main-nav ul ul li:hover > a {color: ' . esc_attr( $lalita_settings[ 'subnavigation_text_hover_color' ] ) . ' !important}.daiva-blog-title-effect article .entry-header .entry-title a {background-image: linear-gradient(transparent calc(65% - 5px), ' . esc_attr( $daiva_color_1 ) . ' 5px);color: ' . esc_attr( $daiva_color_1 ) . ';}';
		
		return $daiva_extracolors;
	}
}


// The dynamic styles of the parent theme added inline to the parent stylesheet.
// For the customizer functions it is better to enqueue after the child theme stylesheet.
if ( ! function_exists( 'daiva_remove_parent_dynamic_css' ) ) {
	add_action( 'init', 'daiva_remove_parent_dynamic_css' );
	function daiva_remove_parent_dynamic_css() {
		remove_action( 'wp_enqueue_scripts', 'lalita_enqueue_dynamic_css', 50 );
	}
}

// Enqueue this CSS after the child stylesheet, not after the parent stylesheet.
if ( ! function_exists( 'daiva_enqueue_parent_dynamic_css' ) ) {
	add_action( 'wp_enqueue_scripts', 'daiva_enqueue_parent_dynamic_css', 50 );
	function daiva_enqueue_parent_dynamic_css() {
		$css = lalita_base_css() . lalita_font_css() . lalita_advanced_css() . lalita_spacing_css() . lalita_no_cache_dynamic_css() .daiva_effect_colors_css();

		// escaped secure before in parent theme
		wp_add_inline_style( 'lalita-child', $css );
	}
}

//Adds custom classes to the array of body classes.
if ( ! function_exists( 'daiva_body_classes' ) ) {
	add_filter( 'body_class', 'daiva_body_classes' );
	function daiva_body_classes( $classes ) {
		// Get Customizer settings
		$daiva_settings = get_option( 'daiva_settings' );
		
		$color_frame 	   = 'enable';
		$blog_posts_effect = 'enable';
		$color_logo  	   = 'enable';
		$menu_colors  	   = 'enable';
		
		if ( isset( $daiva_settings['color_frame'] ) ) {
			$color_frame = $daiva_settings['color_frame'];
		}
		
		if ( isset( $daiva_settings['blog_posts_effect'] ) ) {
			$blog_posts_effect = $daiva_settings['blog_posts_effect'];
		}
		
		if ( isset( $daiva_settings['color_logo'] ) ) {
			$color_logo = $daiva_settings['color_logo'];
		}
		
		if ( isset( $daiva_settings['menu_colors'] ) ) {
			$menu_colors = $daiva_settings['menu_colors'];
		}
		
		// Color frame
		if ( $color_frame != 'disable' ) {
			$classes[] = 'daiva-color-frame';
		}
		
		// Blog posts border
		if ( $blog_posts_effect != 'disable' ) {
			$classes[] = 'daiva-blog-title-effect';
		}
		
		// Color logo
		if ( $color_logo != 'disable' ) {
			$classes[] = 'daiva-color-logo-style';
		}
		
		// Menu colors
		if ( $menu_colors != 'disable' ) {
			$classes[] = 'daiva-menu-style';
		}
		
		return $classes;
	}
}

if ( ! function_exists( 'daiva_scripts' ) ) {
	add_action( 'wp_enqueue_scripts', 'daiva_scripts' );
	/**
	 * Enqueue script
	 */
	function daiva_scripts() {
		
		$daiva_settings = get_option( 'daiva_settings' );
		
		$color_logo		 = 'enable';
		if ( isset( $daiva_settings['color_logo'] ) ) {
			$color_logo = $daiva_settings['color_logo'];
		}
		
		if ( $color_logo != 'disable' ) {
			wp_enqueue_style( 'daiva-splitting', esc_url( get_stylesheet_directory_uri() ) . "/css/splitting.min.css", false, LALITA_VERSION, 'all' );
			wp_enqueue_script( 'daiva-splitting', esc_url( get_stylesheet_directory_uri() ) . "/js/splitting.min.js", array( 'jquery'), LALITA_VERSION, true );
		}

	}
}

if ( ! function_exists( 'daiva_frame_html' ) ) {
	add_action( 'lalita_after_footer_content', 'daiva_frame_html' );
	/**
	 * HTML for the color frame
	 */
	function daiva_frame_html() {
		$daiva_settings = get_option( 'daiva_settings' );
		
		$color_frame 	   = 'enable';
		if ( isset( $daiva_settings['color_frame'] ) ) {
			$color_frame = $daiva_settings['color_frame'];
		}
		
		if ( $color_frame != 'disable' ) {
	?>
    <div class="daiva-frame daiva-frame-top"></div>
    <div class="daiva-frame daiva-frame-right"></div>
    <div class="daiva-frame daiva-frame-bottom"></div>
    <div class="daiva-frame daiva-frame-left"></div>
    <?php
		}
	}
}