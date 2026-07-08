<?php
/**
 * Output all of our dynamic CSS.
 *
 * @package    osixthreeo
 * @subpackage osixthreeo/inc/customizer
 * @author     Chip Sheppard
 * @since      1.0.0
 * @license    GPL-2.0+
 */

if ( ! defined( 'ABSPATH' ) ) {
	exit; // Exit if accessed directly.
}

if ( ! function_exists( 'osixthreeo_base_css' ) ) {
	/**
	 * Generate the CSS in the <head> section using the Theme Customizer.
	 *
	 * @param null $css an array.
	 * @since 0.1
	 */
	function osixthreeo_base_css( $css = null ) {
		$saved               = (array) get_option( 'osixthreeo_settings' );
		$defaults            = osixthreeo_get_defaults();
		$osixthreeo_settings = wp_parse_args( $saved, $defaults );
		$osixthreeo_settings = array_intersect_key( $osixthreeo_settings, $defaults );

		$tagline_align                                = $osixthreeo_settings['tagline_align'];
		$default_tagline_align                        = $defaults['tagline_align'];
		$max_width                                    = $osixthreeo_settings['max_width'];
		$default_max_width                            = $defaults['max_width'];
		$header_bg_color_left                         = $osixthreeo_settings['header_bg_color_left'];
		$header_bg_color_right                        = $osixthreeo_settings['header_bg_color_right'];
		$header_gradient_angle                        = $osixthreeo_settings['header_gradient_angle'];
		$header_left_stop                             = $osixthreeo_settings['header_left_stop'];
		$header_right_stop                            = $osixthreeo_settings['header_right_stop'];
		$default_header_bg_color_left                 = $defaults['header_bg_color_left'];
		$default_header_bg_color_right                = $defaults['header_bg_color_right'];
		$default_header_gradient_angle                = $defaults['header_gradient_angle'];
		$default_header_left_stop                     = $defaults['header_left_stop'];
		$default_header_right_stop                    = $defaults['header_right_stop'];
		$home_header_height                           = $osixthreeo_settings['home_header_height'];
		$subpage_header_height                        = $osixthreeo_settings['subpage_header_height'];
		$home_mobile_header_height                    = $osixthreeo_settings['home_mobile_header_height'];
		$subpage_mobile_header_height                 = $osixthreeo_settings['subpage_mobile_header_height'];
		$default_home_header_height                   = $defaults['home_header_height'];
		$default_subpage_header_height                = $defaults['subpage_header_height'];
		$default_home_mobile_header_height            = $defaults['home_mobile_header_height'];
		$default_subpage_mobile_header_height         = $defaults['subpage_mobile_header_height'];
		$header_bg_color                              = $osixthreeo_settings['header_background_color'];
		$default_header_bg_color                      = $defaults['header_background_color'];
		$header_bg_color_home                         = $osixthreeo_settings['header_background_color_home'];
		$default_header_bg_color_home                 = $defaults['header_background_color_home'];
		$header_padding                               = $osixthreeo_settings['header_padding'];
		$default_header_padding                       = $defaults['header_padding'];
		$header_bg_position                           = $osixthreeo_settings['header_bg_position'];
		$header_bg_repeat                             = $osixthreeo_settings['header_bg_repeat'];
		$header_bg_size                               = $osixthreeo_settings['header_bg_size'];
		$default_header_bg_position                   = $defaults['header_bg_position'];
		$default_header_bg_repeat                     = $defaults['header_bg_repeat'];
		$default_header_bg_size                       = $defaults['header_bg_size'];
		$nav_link_color                               = $osixthreeo_settings['nav_link_color'];
		$default_nav_link_color                       = $defaults['nav_link_color'];
		$subnav_text_color                            = $osixthreeo_settings['subnav_text_color'];
		$subnav_bg_color                              = $osixthreeo_settings['subnav_bg_color'];
		$subnav_border_color                          = $osixthreeo_settings['subnav_border_color'];
		$subnav_hover_text_color                      = $osixthreeo_settings['subnav_hover_text_color'];
		$subnav_hover_bg_color                        = $osixthreeo_settings['subnav_hover_bg_color'];
		$default_subnav_text_color                    = $defaults['subnav_text_color'];
		$default_subnav_bg_color                      = $defaults['subnav_bg_color'];
		$default_subnav_border_color                  = $defaults['subnav_border_color'];
		$default_subnav_hover_text_color              = $defaults['subnav_hover_text_color'];
		$default_subnav_hover_bg_color                = $defaults['subnav_hover_bg_color'];
		$content_title_color                          = $osixthreeo_settings['content_title_color'];
		$content_bgcolor                              = $osixthreeo_settings['content_bgcolor'];
		$text_color                                   = $osixthreeo_settings['text_color'];
		$link_color                                   = $osixthreeo_settings['link_color'];
		$link_color_hover                             = $osixthreeo_settings['link_color_hover'];
		$default_content_title_color                  = $defaults['content_title_color'];
		$default_content_bgcolor                      = $defaults['content_bgcolor'];
		$default_text_color                           = $defaults['text_color'];
		$default_link_color                           = $defaults['link_color'];
		$default_link_color_hover                     = $defaults['link_color_hover'];
		$footer_bg_color                              = $osixthreeo_settings['footer_background_color'];
		$footer_title_color                           = $osixthreeo_settings['footer_title_color'];
		$footer_text_color                            = $osixthreeo_settings['footer_text_color'];
		$footer_link_color                            = $osixthreeo_settings['footer_link_color'];
		$footer_link_color_hover                      = $osixthreeo_settings['footer_link_color_hover'];
		$default_footer_bg_color                      = $defaults['footer_background_color'];
		$default_footer_title_color                   = $defaults['footer_title_color'];
		$default_footer_text_color                    = $defaults['footer_text_color'];
		$default_footer_link_color                    = $defaults['footer_link_color'];
		$default_footer_link_color_hover              = $defaults['footer_link_color_hover'];
		$base_font                                    = $osixthreeo_settings['base_font'];
		$header_font                                  = $osixthreeo_settings['header_font'];
		$highlite_font                                = $osixthreeo_settings['highlite_font'];
		$default_base_font                            = $defaults['base_font'];
		$default_header_font                          = $defaults['header_font'];
		$default_highlite_font                        = $defaults['highlite_font'];
		$sitetitle_font                               = $osixthreeo_settings['sitetitle_font'];
		$sitedescription_font                         = $osixthreeo_settings['sitedescription_font'];
		$menu_font                                    = $osixthreeo_settings['menu_font'];
		$default_sitetitle_font                       = $defaults['sitetitle_font'];
		$default_sitedescription_font                 = $defaults['sitedescription_font'];
		$default_menu_font                            = $defaults['menu_font'];
		$header_font_weight                           = $osixthreeo_settings['header_font_weight'];
		$sitetitle_font_weight                        = $osixthreeo_settings['sitetitle_font_weight'];
		$sitedescription_font_weight                  = $osixthreeo_settings['sitedescription_font_weight'];
		$menu_font_weight                             = $osixthreeo_settings['menu_font_weight'];
		$default_header_font_weight                   = $defaults['header_font_weight'];
		$default_sitetitle_font_weight                = $defaults['sitetitle_font_weight'];
		$default_sitedescription_font_weight          = $defaults['sitedescription_font_weight'];
		$default_menu_font_weight                     = $defaults['menu_font_weight'];
		$base_font_size                               = $osixthreeo_settings['base_font_size'];
		$sitetitle_font_size                          = $osixthreeo_settings['sitetitle_font_size'];
		$sitedescription_font_size                    = $osixthreeo_settings['sitedescription_font_size'];
		$menu_font_size                               = $osixthreeo_settings['menu_font_size'];
		$default_base_font_size                       = $defaults['base_font_size'];
		$default_sitetitle_font_size                  = $defaults['sitetitle_font_size'];
		$default_sitedescription_font_size            = $defaults['sitedescription_font_size'];
		$default_menu_font_size                       = $defaults['menu_font_size'];
		$hero_text_primary                            = $osixthreeo_settings['hero_text_primary'];
		$hero_text_secondary                          = $osixthreeo_settings['hero_text_secondary'];
		$hero_text_primary_font                       = $osixthreeo_settings['hero_text_primary_font'];
		$hero_text_secondary_font                     = $osixthreeo_settings['hero_text_secondary_font'];
		$hero_text_primary_font_size                  = $osixthreeo_settings['hero_text_primary_font_size'];
		$hero_text_primary_font_size_mobile           = $osixthreeo_settings['hero_text_primary_font_size_mobile'];
		$hero_text_primary_color                      = $osixthreeo_settings['hero_text_primary_color'];
		$hero_text_primary_alignment                  = $osixthreeo_settings['hero_text_primary_alignment'];
		$hero_text_primary_shadow_color               = $osixthreeo_settings['hero_text_primary_shadow_color'];
		$hero_text_primary_shadow_x                   = $osixthreeo_settings['hero_text_primary_shadow_x'];
		$hero_text_primary_shadow_y                   = $osixthreeo_settings['hero_text_primary_shadow_y'];
		$hero_text_primary_shadow_blur                = $osixthreeo_settings['hero_text_primary_shadow_blur'];
		$default_hero_text_primary                    = $defaults['hero_text_primary'];
		$default_hero_text_secondary                  = $defaults['hero_text_secondary'];
		$default_hero_text_primary_font               = $defaults['hero_text_primary_font'];
		$default_hero_text_secondary_font             = $defaults['hero_text_secondary_font'];
		$default_hero_text_primary_font_size          = $defaults['hero_text_primary_font_size'];
		$default_hero_text_primary_font_size_mobile   = $defaults['hero_text_primary_font_size_mobile'];
		$default_hero_text_primary_color              = $defaults['hero_text_primary_color'];
		$default_hero_text_primary_alignment          = $defaults['hero_text_primary_alignment'];
		$default_hero_text_primary_shadow_color       = $defaults['hero_text_primary_shadow_color'];
		$default_hero_text_primary_shadow_x           = $defaults['hero_text_primary_shadow_x'];
		$default_hero_text_primary_shadow_y           = $defaults['hero_text_primary_shadow_y'];
		$default_hero_text_primary_shadow_blur        = $defaults['hero_text_primary_shadow_blur'];
		$hero_text_secondary_font_size                = $osixthreeo_settings['hero_text_secondary_font_size'];
		$hero_text_secondary_font_size_mobile         = $osixthreeo_settings['hero_text_secondary_font_size_mobile'];
		$hero_text_secondary_color                    = $osixthreeo_settings['hero_text_secondary_color'];
		$hero_text_secondary_alignment                = $osixthreeo_settings['hero_text_secondary_alignment'];
		$hero_text_secondary_shadow_color             = $osixthreeo_settings['hero_text_secondary_shadow_color'];
		$hero_text_secondary_shadow_x                 = $osixthreeo_settings['hero_text_secondary_shadow_x'];
		$hero_text_secondary_shadow_y                 = $osixthreeo_settings['hero_text_secondary_shadow_y'];
		$hero_text_secondary_shadow_blur              = $osixthreeo_settings['hero_text_secondary_shadow_blur'];
		$default_hero_text_secondary_font_size        = $defaults['hero_text_secondary_font_size'];
		$default_hero_text_secondary_font_size_mobile = $defaults['hero_text_secondary_font_size_mobile'];
		$default_hero_text_secondary_color            = $defaults['hero_text_secondary_color'];
		$default_hero_text_secondary_alignment        = $defaults['hero_text_secondary_alignment'];
		$default_hero_text_secondary_shadow_color     = $defaults['hero_text_secondary_shadow_color'];
		$default_hero_text_secondary_shadow_x         = $defaults['hero_text_secondary_shadow_x'];
		$default_hero_text_secondary_shadow_y         = $defaults['hero_text_secondary_shadow_y'];
		$default_hero_text_secondary_shadow_blur      = $defaults['hero_text_secondary_shadow_blur'];
		$hero_scroll_button                           = $osixthreeo_settings['hero_scroll_button'];
		$hero_scroll_button_alignment                 = $osixthreeo_settings['hero_scroll_button_alignment'];
		$default_hero_scroll_button                   = $defaults['hero_scroll_button'];
		$default_hero_scroll_button_alignment         = $defaults['hero_scroll_button_alignment'];
		$meta_date                                    = $osixthreeo_settings['meta_date'];
		$meta_author                                  = $osixthreeo_settings['meta_author'];
		$meta_comments                                = $osixthreeo_settings['meta_comments'];
		$meta_updated                                 = $osixthreeo_settings['meta_updated'];
		$meta_footer                                  = $osixthreeo_settings['meta_footer'];
		$default_meta_date                            = $defaults['meta_date'];
		$default_meta_author                          = $defaults['meta_author'];
		$default_meta_comments                        = $defaults['meta_comments'];
		$default_meta_updated                         = $defaults['meta_updated'];
		$default_meta_footer                          = $defaults['meta_footer'];
		$meta_font                                    = $osixthreeo_settings['meta_font'];
		$meta_font_size                               = $osixthreeo_settings['meta_font_size'];
		$meta_font_weight                             = $osixthreeo_settings['meta_font_weight'];
		$meta_color                                   = $osixthreeo_settings['meta_color'];
		$default_meta_font                            = $defaults['meta_font'];
		$default_meta_font_size                       = $defaults['meta_font_size'];
		$default_meta_font_weight                     = $defaults['meta_font_weight'];
		$default_meta_color                           = $defaults['meta_color'];
		$archives_text_color                          = $osixthreeo_settings['archives_text_color'];
		$archives_title_color                         = $osixthreeo_settings['archives_title_color'];
		$archives_meta_color                          = $osixthreeo_settings['archives_meta_color'];
		$archives_link_color                          = $osixthreeo_settings['archives_link_color'];
		$archives_link_color_hover                    = $osixthreeo_settings['archives_link_color_hover'];
		$default_archives_text_color                  = $defaults['archives_text_color'];
		$default_archives_title_color                 = $defaults['archives_title_color'];
		$default_archives_meta_color                  = $defaults['archives_meta_color'];
		$default_archives_link_color                  = $defaults['archives_link_color'];
		$default_archives_link_color_hover            = $defaults['archives_link_color_hover'];
		$archives_bg_color                            = $osixthreeo_settings['archives_background_color'];
		$archives_pad_left                            = $osixthreeo_settings['archives_pad_left'];
		$archives_pad_right                           = $osixthreeo_settings['archives_pad_right'];
		$archives_pad_top                             = $osixthreeo_settings['archives_pad_top'];
		$archives_pad_bottom                          = $osixthreeo_settings['archives_pad_bottom'];
		$archives_box_shadow_color                    = $osixthreeo_settings['archives_box_shadow_color'];
		$archives_box_shadow_x                        = $osixthreeo_settings['archives_box_shadow_x'];
		$archives_box_shadow_y                        = $osixthreeo_settings['archives_box_shadow_y'];
		$archives_box_shadow_blur                     = $osixthreeo_settings['archives_box_shadow_blur'];
		$archives_box_shadow_spread                   = $osixthreeo_settings['archives_box_shadow_spread'];
		$archives_border_color                        = $osixthreeo_settings['archives_border_color'];
		$archives_border_width                        = $osixthreeo_settings['archives_border_width'];
		$archives_border_radius                       = $osixthreeo_settings['archives_border_radius'];
		$default_archives_bg_color                    = $defaults['archives_background_color'];
		$default_archives_pad_left                    = $defaults['archives_pad_left'];
		$default_archives_pad_right                   = $defaults['archives_pad_right'];
		$default_archives_pad_top                     = $defaults['archives_pad_top'];
		$default_archives_pad_bottom                  = $defaults['archives_pad_bottom'];
		$default_archives_box_shadow_color            = $defaults['archives_box_shadow_color'];
		$default_archives_box_shadow_x                = $defaults['archives_box_shadow_x'];
		$default_archives_box_shadow_y                = $defaults['archives_box_shadow_y'];
		$default_archives_box_shadow_blur             = $defaults['archives_box_shadow_blur'];
		$default_archives_box_shadow_spread           = $defaults['archives_box_shadow_spread'];
		$default_archives_border_color                = $defaults['archives_border_color'];
		$default_archives_border_width                = $defaults['archives_border_width'];
		$default_archives_border_radius               = $defaults['archives_border_radius'];

		// Initiate our class.
		$css = new Osixthreeo_Customizer_CSS();

		/*
		 * get_header_textcolor() options: Any hex value, 'blank' to hide text. Default: HEADER_TEXTCOLOR.
		 */
		$title_text_color = get_header_textcolor();

		if ( get_theme_support( 'custom-header', 'default-text-color' ) !== $title_text_color ) :
			$ht_color = ( '#' . $title_text_color );
			if ( ! display_header_text() ) :
				$css->set_selector( '.site-title,.site-description' );
				$css->add_property( 'position', 'absolute' );
				$css->add_property( 'clip', 'rect(1px, 1px, 1px, 1px)' );
			else :
				$css->set_selector( '.site-title,.site-title a,.site-description' );
				$css->add_property( 'color', esc_attr( $ht_color ) );
			endif;
		endif;

		/*
		 * Site Width --------------------------------
		 */
		if ( absint( $default_max_width ) !== absint( $max_width ) ) :
			$css->set_selector( 'body.contained .site' );
			$css->add_property( 'max-width', esc_attr( $osixthreeo_settings['max_width'] . 'px' ) );
		endif;

		/*
		 * Custom Header --------------------------------
		 */
		if ( $default_header_bg_color_left !== $header_bg_color_left ||
		$default_header_bg_color_right !== $header_bg_color_right ||
		absint( $default_header_gradient_angle ) !== absint( $header_gradient_angle ) ||
		absint( $default_header_left_stop ) !== absint( $header_left_stop ) ||
		absint( $default_header_right_stop ) !== absint( $header_right_stop ) ) :
			$clr1      = $osixthreeo_settings['header_bg_color_left'];
			$clr2      = $osixthreeo_settings['header_bg_color_right'];
			$angle     = absint( $osixthreeo_settings['header_gradient_angle'] );
			$stopleft  = absint( $osixthreeo_settings['header_left_stop'] );
			$stopright = absint( $osixthreeo_settings['header_right_stop'] );
			$prop      = sprintf( 'linear-gradient(%1$sdeg, %2$s %3$s%%, %4$s %5$s%%)', $angle, $clr1, $stopleft, $clr2, $stopright );
			$css->set_selector( '.custom-header' );
			$css->add_property( 'background', $prop );
		endif;

		if ( absint( $default_subpage_header_height ) !== absint( $subpage_header_height ) ) :
			$css->set_selector( '.site-header' );
			$css->add_property( 'min-height', esc_attr( $osixthreeo_settings['subpage_header_height'] . 'px' ) );
		endif;
		if ( absint( $default_home_header_height ) !== absint( $home_header_height ) ) :
			$css->set_selector( '.home .site-header' );
			$css->add_property( 'min-height', esc_attr( $osixthreeo_settings['home_header_height'] . 'px' ) );
		endif;
		if ( absint( $default_subpage_mobile_header_height ) !== absint( $subpage_mobile_header_height ) ) :
			$css->start_media_query( apply_filters( 'osixthreeo_mobile_media_query', '(max-width:768px)' ) );
				$css->set_selector( '.site-header' );
				$css->add_property( 'min-height', esc_attr( $osixthreeo_settings['subpage_mobile_header_height'] . 'px' ) );
			$css->stop_media_query();
		endif;
		if ( absint( $default_home_mobile_header_height ) !== absint( $home_mobile_header_height ) ) :
			$css->start_media_query( apply_filters( 'osixthreeo_mobile_media_query', '(max-width:768px)' ) );
				$css->set_selector( '.home .site-header' );
				$css->add_property( 'min-height', esc_attr( $osixthreeo_settings['home_mobile_header_height'] . 'px' ) );
			$css->stop_media_query();
		endif;

		if ( $default_header_bg_position !== $header_bg_position ) :
			if ( 'left-top' === $header_bg_position ) :
				$lcr = 'left';
				$tcb = 'top';
			elseif ( 'left-center' === $header_bg_position ) :
				$lcr = 'left';
				$tcb = 'center';
			elseif ( 'left-bottom' === $header_bg_position ) :
				$lcr = 'left';
				$tcb = 'bottom';
			elseif ( 'right-top' === $header_bg_position ) :
				$lcr = 'right';
				$tcb = 'top';
			elseif ( 'right-center' === $header_bg_position ) :
				$lcr = 'right';
				$tcb = 'center';
			elseif ( 'right-bottom' === $header_bg_position ) :
				$lcr = 'right';
				$tcb = 'bottom';
			elseif ( 'center-top' === $header_bg_position ) :
				$lcr = 'center';
				$tcb = 'top';
			elseif ( 'center-bottom' === $header_bg_position ) :
				$lcr = 'center';
				$tcb = 'bottom';
			endif;
			$prop = sprintf( '%1$s %2$s', $lcr, $tcb );
			$css->set_selector( '.custom-header .custom-header-image' );
			$css->add_property( 'background-position', $prop );
		endif;
		if ( $default_header_bg_repeat !== $header_bg_repeat ) :
			$css->set_selector( '.custom-header .custom-header-image' );
			$css->add_property( 'background-repeat', esc_attr( $osixthreeo_settings['header_bg_repeat'] ) );
		endif;
		if ( $default_header_bg_size !== $header_bg_size ) :
			$css->set_selector( '.custom-header .custom-header-image' );
			$css->add_property( 'background-size', esc_attr( $osixthreeo_settings['header_bg_size'] ) );
		endif;

		/*
		 * Header background color --------------------------------
		 */
		if ( $default_header_bg_color !== $header_bg_color ) :
			$css->set_selector( '.header-wrap' );
			$css->add_property( 'background-color', esc_attr( $osixthreeo_settings['header_background_color'] ) );
		endif;

		/*
		 * Header background color HOME --------------------------------
		 */
		if ( $default_header_bg_color_home !== $header_bg_color_home ) :
			$css->set_selector( '.home .header-wrap' );
			$css->add_property( 'background-color', esc_attr( $osixthreeo_settings['header_background_color_home'] ) );
		endif;

		/*
		 * Header top/bottom padding --------------------------------
		 */
		if ( absint( $default_header_padding ) !== absint( $header_padding ) ) :
			$css->set_selector( '.header-wrap' );
			$css->add_property( 'padding-top', esc_attr( $osixthreeo_settings['header_padding'] . 'px' ) );
			$css->add_property( 'padding-bottom', esc_attr( $osixthreeo_settings['header_padding'] . 'px' ) );
			$css->set_selector( 'responsive-menu-icon' );
			$css->add_property( 'margin-top', esc_attr( $osixthreeo_settings['header_padding'] . 'px' ) );
		endif;

		/*
		 * Navigation link colors --------------------------------
		 */
		if ( $default_nav_link_color !== $nav_link_color ) :
			// Text.
			$css->set_selector( '.site-navigation a, button.dropdown-toggle' );
			$css->add_property( 'color', esc_attr( $osixthreeo_settings['nav_link_color'] ) );
			// Background.
			$css->set_selector( '.responsive-menu-icon .menu-icon,.responsive-menu-icon .menu-icon::before,.responsive-menu-icon .menu-icon::after, .site-navigation li.search-icon .theicon:before' );
			$css->add_property( 'background-color', esc_attr( $osixthreeo_settings['nav_link_color'] ) );
			// Borders.
			$css->set_selector( '.site-navigation li.search-icon .theicon,.site-navigation li.search-icon:hover,.site-navigation .sub-menu,.topbar-widget.widget_nav_menu .sub-menu' );
			$css->add_property( 'border-color', esc_attr( $osixthreeo_settings['nav_link_color'] ) );

		endif;

		/*
		 * SubNav/Mobile colors --------------------------------
		 */

		// text.
		if ( $default_subnav_text_color !== $subnav_text_color ) :
			$css->set_selector( '.site-navigation .sub-menu a,.sub-menu button.dropdown-toggle' );
			$css->add_property( 'color', esc_attr( $osixthreeo_settings['subnav_text_color'] ) );
			$css->start_media_query( apply_filters( 'osixthreeo_mobile_media_query', '(max-width:768px)' ) );
				$css->set_selector( '.site-navigation a, button.dropdown-toggle' );
				$css->add_property( 'color', esc_attr( $osixthreeo_settings['subnav_text_color'] ) . '!important' );
			$css->stop_media_query();
		endif;

		// hover text.
		if ( $default_subnav_hover_text_color !== $subnav_hover_text_color ) :
			$css->set_selector( '.site-navigation .sub-menu a:hover,.site-navigation .sub-menu .current_page_item > a,.site-navigation .sub-menu .current-menu-item > a' );
			$css->add_property( 'color', esc_attr( $osixthreeo_settings['subnav_hover_text_color'] ) );
			$css->start_media_query( apply_filters( 'osixthreeo_mobile_media_query', '(max-width:768px)' ) );
				$css->set_selector( '.site-navigation a:hover' );
				$css->add_property( 'color', esc_attr( $osixthreeo_settings['subnav_hover_text_color'] ) . '!important' );
			$css->stop_media_query();
		endif;

		// bg.
		if ( $default_subnav_bg_color !== $subnav_bg_color ) :
			$css->set_selector( '.site-navigation .sub-menu a' );
			$css->add_property( 'background', esc_attr( $osixthreeo_settings['subnav_bg_color'] ) );
			$css->start_media_query( apply_filters( 'osixthreeo_mobile_media_query', '(max-width:768px)' ) );
				$css->set_selector( '.site-navigation a' );
				$css->add_property( 'background-color', esc_attr( $osixthreeo_settings['subnav_bg_color'] ) );
			$css->stop_media_query();
		endif;

		// hover bg.
		if ( $default_subnav_hover_bg_color !== $subnav_hover_bg_color ) :
			$css->set_selector( '.site-navigation .sub-menu a:hover,.site-navigation .sub-menu .current_page_item > a,.site-navigation .sub-menu .current-menu-item > a' );
			$css->add_property( 'background', esc_attr( $osixthreeo_settings['subnav_hover_bg_color'] ) );
			$css->start_media_query( apply_filters( 'osixthreeo_mobile_media_query', '(max-width:768px)' ) );
				$css->set_selector( '.site-navigation a:hover,.site-navigation .current_page_item > a,.site-navigation .current-menu-item > a' );
				$css->add_property( 'background-color', esc_attr( $osixthreeo_settings['subnav_hover_bg_color'] ) );
			$css->stop_media_query();
		endif;

		// border.
		if ( $default_subnav_border_color !== $subnav_border_color ) :
			$css->set_selector( '.site-navigation .sub-menu li,.site-navigation .sub-menu li:first-of-type' );
			$css->add_property( 'border-color', esc_attr( $osixthreeo_settings['subnav_border_color'] ) );
			$css->start_media_query( apply_filters( 'osixthreeo_mobile_media_query', '(max-width:768px)' ) );
				$css->set_selector( '.site-navigation li' );
				$css->add_property( 'border-color', esc_attr( $osixthreeo_settings['subnav_border_color'] ) . '!important' );
			$css->stop_media_query();
		endif;

		/*
		 * Content Area colors --------------------------------
		 */
		if ( $default_content_bgcolor !== $content_bgcolor ) :
			$css->set_selector( '.site-content' );
			$css->add_property( 'background-color', esc_attr( $osixthreeo_settings['content_bgcolor'] ) );
		endif;
		if ( $default_text_color !== $text_color ) :
			$css->set_selector( 'body,button,input,select,textarea,.sidebar-widget ul a,.sidebar-widget .menu a,.comment-navigation .nav-previous a,.posts-navigation .nav-previous a,.post-navigation .nav-previous a,.comment-navigation .nav-next a,.posts-navigation .nav-next a,.post-navigation .nav-next a' );
			$css->add_property( 'color', esc_attr( $osixthreeo_settings['text_color'] ) );
		endif;

		if ( $default_link_color !== $link_color ) :
			$css->set_selector( 'a,.sidebar-widget ul a:hover,.sidebar-widget menu a:hover,.comment-navigation .nav-previous a:hover,.posts-navigation .nav-previous a:hover,.post-navigation .nav-previous a:hover,.comment-navigation .nav-next a:hover,.posts-navigation .nav-next a:hover,.post-navigation .nav-next a:hover,.link-more' );
			$css->add_property( 'color', esc_attr( $osixthreeo_settings['link_color'] ) );
			// button bg.
			$css->set_selector( 'input[type="button"],input[type="reset"],input[type="submit"],.btn,.woocommerce a.button,.woocommerce button.button,.woocommerce a.button:hover,.woocommerce button.button:hover,.woocommerce input.button,.woocommerce #respond input#submit' );
			$css->add_property( 'background-color', esc_attr( $osixthreeo_settings['link_color'] ) );
			// borders.
			$css->set_selector( '.sticky .entry-header,.blog .hentry.sticky,.archive .hentry.sticky' );
			$css->add_property( 'border-top-color', esc_attr( $osixthreeo_settings['link_color'] ) );
		endif;

		if ( $default_link_color_hover !== $link_color_hover ) :
			$css->set_selector( '.site-content a:not(.btn):not(.button):not(.meta-link):not(.wp-block-button__link):hover,.site-content a:not(.btn):not(.button):not(.meta-link):not(.wp-block-button__link):focus,.site-content a:not(.btn):not(.button):not(.meta-link):not(.wp-block-button__link):active' );
			$css->add_property( 'color', esc_attr( $osixthreeo_settings['link_color_hover'] ) );
			$css->set_selector( 'input[type="button"]:hover,input[type="reset"]:hover,input[type="submit"]:hover,.btn.secondary,.footer-widgets input[type="submit"],.woocommerce a.button.alt,.woocommerce button.button.alt,.woocommerce #respond input#submit.alt,.woocommerce input.button.alt,.woocommerce input.button:hover,.woocommerce #respond input#submit:hover' );
			$css->add_property( 'background-color', esc_attr( $osixthreeo_settings['link_color_hover'] ) );
		endif;

		/*
		 * Site Footer colors --------------------------------
		 */
		if ( $default_footer_bg_color !== $footer_bg_color ) :
			$css->set_selector( '.site-footer' );
			$css->add_property( 'background-color', esc_attr( $osixthreeo_settings['footer_background_color'] ) );
		endif;
		if ( $default_footer_title_color !== $footer_title_color ) :
			$css->set_selector( '.site-info .widget-title' );
			$css->add_property( 'color', esc_attr( $osixthreeo_settings['footer_title_color'] ) );
		endif;
		if ( $default_footer_text_color !== $footer_text_color ) :
			$css->set_selector( '.site-info' );
			$css->add_property( 'color', esc_attr( $osixthreeo_settings['footer_text_color'] ) );
		endif;
		if ( $default_footer_link_color !== $footer_link_color ) :
			$css->set_selector( '.site-info a' );
			$css->add_property( 'color', esc_attr( $osixthreeo_settings['footer_link_color'] ) );
		endif;
		if ( $default_footer_link_color_hover !== $footer_link_color_hover ) :
			$css->set_selector( '.site-info a:hover' );
			$css->add_property( 'color', esc_attr( $osixthreeo_settings['footer_link_color_hover'] ) );
		endif;

		/*
		 * Post Title colors (+ lifted entry meta) --------------------------------
		 */
		if ( $default_content_title_color !== $content_title_color ) :
			$css->set_selector( 'body.page .entry-title,body.single .entry-title,body.blog .page-title,body.archive .page-title,body.search .page-title,body.error404 .page-title,.woocommerce-products-header,.product_title.entry-title,body.page.titlelift .entry-title,body.single.titlelift .entry-title,body.blog.titlelift .page-title,body.archive.titlelift .page-title,body.search.titlelift .page-title,body.error404.titlelift .page-title,.single.titlelift .entry-meta a,.single.titlelift .entry-meta,.titlelift .archive-description,.titlelift .woocommerce-products-header,.titlelift .product_title.entry-title' );
			$css->add_property( 'color', esc_attr( $osixthreeo_settings['content_title_color'] ) );
		endif;

		/*
		 * Fonts --------------------------------
		 */
		if ( $default_base_font !== $base_font ) :
			$css->set_selector( 'body,button,input,select,textarea,blockquote,.search .page-title span' );
			if ( 'arialblack' === $base_font ) {
				$basefont = 'Arial Black, Gadget, sans-serif';
			} elseif ( 'impact' === $base_font ) {
				$basefont = 'Impact, Charcoal, sans-serif';
			} elseif ( 'trebuchet' === $base_font ) {
				$basefont = 'Trebuchet MS, sans-serif';
			} elseif ( 'verdana' === $base_font ) {
				$basefont = 'Verdana, sans-serif';
			} elseif ( 'georgia' === $base_font ) {
				$basefont = 'Georgia, serif';
			} elseif ( 'palatino' === $base_font ) {
				$basefont = 'Palatino, Palatino Linotype, serif';
			} elseif ( 'tahoma' === $base_font ) {
				$basefont = 'Tahoma, sans-serif';
			} elseif ( 'times' === $base_font ) {
				$basefont = 'Times New Roman, Times, serif';
			} elseif ( 'comicsans' === $base_font ) {
				$basefont = 'Comic Sans MS, cursive';
			} elseif ( 'copperplate' === $base_font ) {
				$basefont = 'Copperplate, "Copperplate Gothic Light", fantasy';
			} elseif ( 'papyrus' === $base_font ) {
				$basefont = 'Papyrus, cursive';
			} elseif ( 'courier' === $base_font ) {
				$basefont = 'Courier, monospace';
			} elseif ( 'lucidatypewritter' === $base_font ) {
				$basefont = '"Lucida Sans Typewriter", monaco, monospace';
			} elseif ( 'alegreyasans' === $base_font ) {
				$basefont = '"Alegreya Sans", sans-serif';
			} elseif ( 'alegreyasanssc' === $base_font ) {
				$basefont = '"Alegreya Sans SC", sans-serif';
			} elseif ( 'archivo' === $base_font ) {
				$basefont = '"Archivo", sans-serif';
			} elseif ( 'archivonarrow' === $base_font ) {
				$basefont = '"Archivo Narrow", sans-serif';
			} elseif ( 'b612' === $base_font ) {
				$basefont = '"B612", sans-serif';
			} elseif ( 'cabin' === $base_font ) {
				$basefont = '"Cabin", sans-serif';
			} elseif ( 'cairo' === $base_font ) {
				$basefont = '"Cairo", sans-serif';
			} elseif ( 'chivo' === $base_font ) {
				$basefont = '"Chivo", sans-serif';
			} elseif ( 'exo2' === $base_font ) {
				$basefont = '"Exo 2", sans-serif';
			} elseif ( 'fjallaone' === $base_font ) {
				$basefont = '"Fjalla One", sans-serif';
			} elseif ( 'firasans' === $base_font ) {
				$basefont = '"Fira Sans", sans-serif';
			} elseif ( 'ibmplexsans' === $base_font ) {
				$basefont = '"IBM Plex Sans", sans-serif';
			} elseif ( 'karla' === $base_font ) {
				$basefont = '"Karla", sans-serif';
			} elseif ( 'lato' === $base_font ) {
				$basefont = '"Lato", sans-serif';
			} elseif ( 'librefranklin' === $base_font ) {
				$basefont = '"Libre Franklin", sans-serif';
			} elseif ( 'montserrat' === $base_font ) {
				$basefont = '"Montserrat", sans-serif';
			} elseif ( 'montserratalternates' === $base_font ) {
				$basefont = '"Montserrat Alternates", sans-serif';
			} elseif ( 'muli' === $base_font ) {
				$basefont = '"Muli", sans-serif';
			} elseif ( 'notosans' === $base_font ) {
				$basefont = '"Noto Sans", sans-serif';
			} elseif ( 'nunito' === $base_font ) {
				$basefont = '"Nunito", sans-serif';
			} elseif ( 'opensans' === $base_font ) {
				$basefont = '"Open Sans", sans-serif';
			} elseif ( 'oswald' === $base_font ) {
				$basefont = '"Oswald", sans-serif';
			} elseif ( 'oxygen' === $base_font ) {
				$basefont = '"Oxygen", sans-serif';
			} elseif ( 'poppins' === $base_font ) {
				$basefont = '"Poppins", sans-serif';
			} elseif ( 'prozalibre' === $base_font ) {
				$basefont = '"Proza Libre", sans-serif';
			} elseif ( 'ptsans' === $base_font ) {
				$basefont = '"PT Sans", sans-serif';
			} elseif ( 'raleway' === $base_font ) {
				$basefont = '"Raleway", sans-serif';
			} elseif ( 'roboto' === $base_font ) {
				$basefont = '"Roboto", sans-serif';
			} elseif ( 'rubik' === $base_font ) {
				$basefont = '"Rubik", sans-serif';
			} elseif ( 'sourcesanspro' === $base_font ) {
				$basefont = '"Source Sans Pro", sans-serif';
			} elseif ( 'titilliumweb' === $base_font ) {
				$basefont = '"Titillium Web", sans-serif';
			} elseif ( 'ubuntu' === $base_font ) {
				$basefont = '"Ubuntu", sans-serif';
			} elseif ( 'varela' === $base_font ) {
				$basefont = '"Varela", sans-serif';
			} elseif ( 'varelaround' === $base_font ) {
				$basefont = '"Varela Round", sans-serif';
			} elseif ( 'worksans' === $base_font ) {
				$basefont = '"Work Sans", sans-serif';
			} elseif ( 'alegreya' === $base_font ) {
				$basefont = '"Alegreya", serif';
			} elseif ( 'alegreyasc' === $base_font ) {
				$basefont = '"Alegreya SC", serif';
			} elseif ( 'arvo' === $base_font ) {
				$basefont = '"Arvo", serif';
			} elseif ( 'biothyme' === $base_font ) {
				$basefont = '"BioRhyme", serif';
			} elseif ( 'cardo' === $base_font ) {
				$basefont = '"Cardo", serif';
			} elseif ( 'cormorant' === $base_font ) {
				$basefont = '"Cormorant", serif';
			} elseif ( 'crimsontext' === $base_font ) {
				$basefont = '"Crimson Text", serif';
			} elseif ( 'domine' === $base_font ) {
				$basefont = '"Domine", serif';
			} elseif ( 'eczar' === $base_font ) {
				$basefont = '"Eczar", serif';
			} elseif ( 'frankruhllibre' === $base_font ) {
				$basefont = '"Frank Ruhl Libre", serif';
			} elseif ( 'ibmplexserif' === $base_font ) {
				$basefont = '"IBM Plex Serif", serif';
			} elseif ( 'inknutantiqua' === $base_font ) {
				$basefont = '"Inknut Antiqua", serif';
			} elseif ( 'librebaskerville' === $base_font ) {
				$basefont = '"Libre Baskerville", serif';
			} elseif ( 'lora' === $base_font ) {
				$basefont = '"Lora", serif';
			} elseif ( 'merriweather' === $base_font ) {
				$basefont = '"Merriweather", serif';
			} elseif ( 'neuton' === $base_font ) {
				$basefont = '"Neuton", serif';
			} elseif ( 'oldstandardtt' === $base_font ) {
				$basefont = '"Old Standard TT", serif';
			} elseif ( 'playfairdisplay' === $base_font ) {
				$basefont = '"Playfair Display", serif';
			} elseif ( 'ptserif' === $base_font ) {
				$basefont = '"PT Serif", serif';
			} elseif ( 'robotoslab' === $base_font ) {
				$basefont = '"Roboto Slab", serif';
			} elseif ( 'rokkitt' === $base_font ) {
				$basefont = '"Rokkitt", serif';
			} elseif ( 'sourceserifpro' === $base_font ) {
				$basefont = '"Source Serif Pro", serif';
			} elseif ( 'spectral' === $base_font ) {
				$basefont = '"Spectral", serif';
			} elseif ( 'vollkorn' === $base_font ) {
				$basefont = '"Vollkorn", serif';
			} elseif ( 'vollkornsc' === $base_font ) {
				$basefont = '"Vollkorn SC", serif';
			} elseif ( 'abrilfatface' === $base_font ) {
				$basefont = '"Abril Fatface", cursive';
			} elseif ( 'alfaslabone' === $base_font ) {
				$basefont = '"Alfa Slab One", cursive';
			} elseif ( 'baloo' === $base_font ) {
				$basefont = '"Baloo", cursive';
			} elseif ( 'barrio' === $base_font ) {
				$basefont = '"Barrio", cursive';
			} elseif ( 'blackopsone' === $base_font ) {
				$basefont = '"Black Ops One", cursive';
			} elseif ( 'cabinsketch' === $base_font ) {
				$basefont = '"Cabin Sketch", cursive';
			} elseif ( 'chelaone' === $base_font ) {
				$basefont = '"Chela One", cursive';
			} elseif ( 'concertone' === $base_font ) {
				$basefont = '"Concert One", cursive';
			} elseif ( 'ericaone' === $base_font ) {
				$basefont = '"Erica One", cursive';
			} elseif ( 'fascinate' === $base_font ) {
				$basefont = '"Fascinate", cursive';
			} elseif ( 'flamenco' === $base_font ) {
				$basefont = '"Flamenco", cursive';
			} elseif ( 'frederickathegreat' === $base_font ) {
				$basefont = '"Fredericka the Great", cursive';
			} elseif ( 'lilyscriptone' === $base_font ) {
				$basefont = '"Lily Script One", cursive';
			} elseif ( 'lobster' === $base_font ) {
				$basefont = '"Lobster", cursive';
			} elseif ( 'lobstertwo' === $base_font ) {
				$basefont = '"Lobster Two", cursive';
			} elseif ( 'monoton' === $base_font ) {
				$basefont = '"Monoton", cursive';
			} elseif ( 'nixieone' === $base_font ) {
				$basefont = '"Nixie One", cursive';
			} elseif ( 'oleoscript' === $base_font ) {
				$basefont = '"Oleo Script", cursive';
			} elseif ( 'oleoscriptswashcaps' === $base_font ) {
				$basefont = '"Oleo Script Swash Caps", cursive';
			} elseif ( 'ranchers' === $base_font ) {
				$basefont = '"Ranchers", cursive';
			} elseif ( 'rakkas' === $base_font ) {
				$basefont = '"Rakkas", cursive';
			} elseif ( 'specialelite' === $base_font ) {
				$basefont = '"Special Elite", cursive';
			} elseif ( 'yatraone' === $base_font ) {
				$basefont = '"Yatra One", cursive';
			} elseif ( 'inconsolata' === $base_font ) {
				$basefont = '"Inconsolata", monospace';
			} elseif ( 'spacemono' === $base_font ) {
				$basefont = '"Space Mono", monospace';
			}
			$css->add_property( 'font-family', $basefont );
		endif;

		if ( $default_header_font !== $header_font ) :
			$css->set_selector( 'h1:not(.site-title),h2,h3,h4,h5,h6' );
			if ( 'arialblack' === $header_font ) {
				$headerfont = 'Arial Black, Gadget, sans-serif';
			} elseif ( 'impact' === $header_font ) {
				$headerfont = 'Impact, Charcoal, sans-serif';
			} elseif ( 'trebuchet' === $header_font ) {
				$headerfont = 'Trebuchet MS, sans-serif';
			} elseif ( 'verdana' === $header_font ) {
				$headerfont = 'Verdana, sans-serif';
			} elseif ( 'georgia' === $header_font ) {
				$headerfont = 'Georgia, serif';
			} elseif ( 'palatino' === $header_font ) {
				$headerfont = 'Palatino, Palatino Linotype, serif';
			} elseif ( 'tahoma' === $header_font ) {
				$headerfont = 'Tahoma, sans-serif';
			} elseif ( 'times' === $header_font ) {
				$headerfont = 'Times New Roman, Times, serif';
			} elseif ( 'comicsans' === $header_font ) {
				$headerfont = 'Comic Sans MS, cursive';
			} elseif ( 'copperplate' === $header_font ) {
				$headerfont = 'Copperplate, "Copperplate Gothic Light", fantasy';
			} elseif ( 'papyrus' === $header_font ) {
				$headerfont = 'Papyrus, cursive';
			} elseif ( 'courier' === $header_font ) {
				$headerfont = 'Courier, monospace';
			} elseif ( 'lucidatypewritter' === $header_font ) {
				$headerfont = '"Lucida Sans Typewriter", monaco, monospace';
			} elseif ( 'alegreyasans' === $header_font ) {
				$headerfont = '"Alegreya Sans", sans-serif';
			} elseif ( 'alegreyasanssc' === $header_font ) {
				$headerfont = '"Alegreya Sans SC", sans-serif';
			} elseif ( 'archivo' === $header_font ) {
				$headerfont = '"Archivo", sans-serif';
			} elseif ( 'archivonarrow' === $header_font ) {
				$headerfont = '"Archivo Narrow", sans-serif';
			} elseif ( 'b612' === $header_font ) {
				$headerfont = '"B612", sans-serif';
			} elseif ( 'cabin' === $header_font ) {
				$headerfont = '"Cabin", sans-serif';
			} elseif ( 'cairo' === $header_font ) {
				$headerfont = '"Cairo", sans-serif';
			} elseif ( 'chivo' === $header_font ) {
				$headerfont = '"Chivo", sans-serif';
			} elseif ( 'exo2' === $header_font ) {
				$headerfont = '"Exo 2", sans-serif';
			} elseif ( 'fjallaone' === $header_font ) {
				$headerfont = '"Fjalla One", sans-serif';
			} elseif ( 'firasans' === $header_font ) {
				$headerfont = '"Fira Sans", sans-serif';
			} elseif ( 'ibmplexsans' === $header_font ) {
				$headerfont = '"IBM Plex Sans", sans-serif';
			} elseif ( 'karla' === $header_font ) {
				$headerfont = '"Karla", sans-serif';
			} elseif ( 'lato' === $header_font ) {
				$headerfont = '"Lato", sans-serif';
			} elseif ( 'librefranklin' === $header_font ) {
				$headerfont = '"Libre Franklin", sans-serif';
			} elseif ( 'montserrat' === $header_font ) {
				$headerfont = '"Montserrat", sans-serif';
			} elseif ( 'montserratalternates' === $header_font ) {
				$headerfont = '"Montserrat Alternates", sans-serif';
			} elseif ( 'muli' === $header_font ) {
				$headerfont = '"Muli", sans-serif';
			} elseif ( 'notosans' === $header_font ) {
				$headerfont = '"Noto Sans", sans-serif';
			} elseif ( 'nunito' === $header_font ) {
				$headerfont = '"Nunito", sans-serif';
			} elseif ( 'opensans' === $header_font ) {
				$headerfont = '"Open Sans", sans-serif';
			} elseif ( 'oswald' === $header_font ) {
				$headerfont = '"Oswald", sans-serif';
			} elseif ( 'oxygen' === $header_font ) {
				$headerfont = '"Oxygen", sans-serif';
			} elseif ( 'poppins' === $header_font ) {
				$headerfont = '"Poppins", sans-serif';
			} elseif ( 'prozalibre' === $header_font ) {
				$headerfont = '"Proza Libre", sans-serif';
			} elseif ( 'ptsans' === $header_font ) {
				$headerfont = '"PT Sans", sans-serif';
			} elseif ( 'raleway' === $header_font ) {
				$headerfont = '"Raleway", sans-serif';
			} elseif ( 'roboto' === $header_font ) {
				$headerfont = '"Roboto", sans-serif';
			} elseif ( 'rubik' === $header_font ) {
				$headerfont = '"Rubik", sans-serif';
			} elseif ( 'sourcesanspro' === $header_font ) {
				$headerfont = '"Source Sans Pro", sans-serif';
			} elseif ( 'titilliumweb' === $header_font ) {
				$headerfont = '"Titillium Web", sans-serif';
			} elseif ( 'ubuntu' === $header_font ) {
				$headerfont = '"Ubuntu", sans-serif';
			} elseif ( 'varela' === $header_font ) {
				$headerfont = '"Varela", sans-serif';
			} elseif ( 'varelaround' === $header_font ) {
				$headerfont = '"Varela Round", sans-serif';
			} elseif ( 'worksans' === $header_font ) {
				$headerfont = '"Work Sans", sans-serif';
			} elseif ( 'alegreya' === $header_font ) {
				$headerfont = '"Alegreya", serif';
			} elseif ( 'alegreyasc' === $header_font ) {
				$headerfont = '"Alegreya SC", serif';
			} elseif ( 'arvo' === $header_font ) {
				$headerfont = '"Arvo", serif';
			} elseif ( 'biothyme' === $header_font ) {
				$headerfont = '"BioRhyme", serif';
			} elseif ( 'cardo' === $header_font ) {
				$headerfont = '"Cardo", serif';
			} elseif ( 'cormorant' === $header_font ) {
				$headerfont = '"Cormorant", serif';
			} elseif ( 'crimsontext' === $header_font ) {
				$headerfont = '"Crimson Text", serif';
			} elseif ( 'domine' === $header_font ) {
				$headerfont = '"Domine", serif';
			} elseif ( 'eczar' === $header_font ) {
				$headerfont = '"Eczar", serif';
			} elseif ( 'frankruhllibre' === $header_font ) {
				$headerfont = '"Frank Ruhl Libre", serif';
			} elseif ( 'ibmplexserif' === $header_font ) {
				$headerfont = '"IBM Plex Serif", serif';
			} elseif ( 'inknutantiqua' === $header_font ) {
				$headerfont = '"Inknut Antiqua", serif';
			} elseif ( 'librebaskerville' === $header_font ) {
				$headerfont = '"Libre Baskerville", serif';
			} elseif ( 'lora' === $header_font ) {
				$headerfont = '"Lora", serif';
			} elseif ( 'merriweather' === $header_font ) {
				$headerfont = '"Merriweather", serif';
			} elseif ( 'neuton' === $header_font ) {
				$headerfont = '"Neuton", serif';
			} elseif ( 'oldstandardtt' === $header_font ) {
				$headerfont = '"Old Standard TT", serif';
			} elseif ( 'playfairdisplay' === $header_font ) {
				$headerfont = '"Playfair Display", serif';
			} elseif ( 'ptserif' === $header_font ) {
				$headerfont = '"PT Serif", serif';
			} elseif ( 'robotoslab' === $header_font ) {
				$headerfont = '"Roboto Slab", serif';
			} elseif ( 'rokkitt' === $header_font ) {
				$headerfont = '"Rokkitt", serif';
			} elseif ( 'sourceserifpro' === $header_font ) {
				$headerfont = '"Source Serif Pro", serif';
			} elseif ( 'spectral' === $header_font ) {
				$headerfont = '"Spectral", serif';
			} elseif ( 'vollkorn' === $header_font ) {
				$headerfont = '"Vollkorn", serif';
			} elseif ( 'vollkornsc' === $header_font ) {
				$headerfont = '"Vollkorn SC", serif';
			} elseif ( 'abrilfatface' === $header_font ) {
				$headerfont = '"Abril Fatface", cursive';
			} elseif ( 'alfaslabone' === $header_font ) {
				$headerfont = '"Alfa Slab One", cursive';
			} elseif ( 'baloo' === $header_font ) {
				$headerfont = '"Baloo", cursive';
			} elseif ( 'barrio' === $header_font ) {
				$headerfont = '"Barrio", cursive';
			} elseif ( 'blackopsone' === $header_font ) {
				$headerfont = '"Black Ops One", cursive';
			} elseif ( 'cabinsketch' === $header_font ) {
				$headerfont = '"Cabin Sketch", cursive';
			} elseif ( 'chelaone' === $header_font ) {
				$headerfont = '"Chela One", cursive';
			} elseif ( 'concertone' === $header_font ) {
				$headerfont = '"Concert One", cursive';
			} elseif ( 'ericaone' === $header_font ) {
				$headerfont = '"Erica One", cursive';
			} elseif ( 'fascinate' === $header_font ) {
				$headerfont = '"Fascinate", cursive';
			} elseif ( 'flamenco' === $header_font ) {
				$headerfont = '"Flamenco", cursive';
			} elseif ( 'frederickathegreat' === $header_font ) {
				$headerfont = '"Fredericka the Great", cursive';
			} elseif ( 'lilyscriptone' === $header_font ) {
				$headerfont = '"Lily Script One", cursive';
			} elseif ( 'lobster' === $header_font ) {
				$headerfont = '"Lobster", cursive';
			} elseif ( 'lobstertwo' === $header_font ) {
				$headerfont = '"Lobster Two", cursive';
			} elseif ( 'monoton' === $header_font ) {
				$headerfont = '"Monoton", cursive';
			} elseif ( 'nixieone' === $header_font ) {
				$headerfont = '"Nixie One", cursive';
			} elseif ( 'oleoscript' === $header_font ) {
				$headerfont = '"Oleo Script", cursive';
			} elseif ( 'oleoscriptswashcaps' === $header_font ) {
				$headerfont = '"Oleo Script Swash Caps", cursive';
			} elseif ( 'ranchers' === $header_font ) {
				$headerfont = '"Ranchers", cursive';
			} elseif ( 'rakkas' === $header_font ) {
				$headerfont = '"Rakkas", cursive';
			} elseif ( 'specialelite' === $header_font ) {
				$headerfont = '"Special Elite", cursive';
			} elseif ( 'yatraone' === $header_font ) {
				$headerfont = '"Yatra One", cursive';
			} elseif ( 'inconsolata' === $header_font ) {
				$headerfont = '"Inconsolata", monospace';
			} elseif ( 'spacemono' === $header_font ) {
				$headerfont = '"Space Mono", monospace';
			}
			$css->add_property( 'font-family', $headerfont );
		endif;

		if ( $default_highlite_font !== $highlite_font ) :
			if ( 'arialblack' === $highlite_font ) {
				$highlitefont = 'Arial Black, Gadget, sans-serif';
			} elseif ( 'impact' === $highlite_font ) {
				$highlitefont = 'Impact, Charcoal, sans-serif';
			} elseif ( 'trebuchet' === $highlite_font ) {
				$highlitefont = 'Trebuchet MS, sans-serif';
			} elseif ( 'verdana' === $highlite_font ) {
				$highlitefont = 'Verdana, sans-serif';
			} elseif ( 'georgia' === $highlite_font ) {
				$highlitefont = 'Georgia, serif';
			} elseif ( 'palatino' === $highlite_font ) {
				$highlitefont = 'Palatino, Palatino Linotype, serif';
			} elseif ( 'tahoma' === $highlite_font ) {
				$highlitefont = 'Tahoma, sans-serif';
			} elseif ( 'times' === $highlite_font ) {
				$highlitefont = 'Times New Roman, Times, serif';
			} elseif ( 'comicsans' === $highlite_font ) {
				$highlitefont = 'Comic Sans MS, cursive';
			} elseif ( 'copperplate' === $highlite_font ) {
				$highlitefont = 'Copperplate, "Copperplate Gothic Light", fantasy';
			} elseif ( 'papyrus' === $highlite_font ) {
				$highlitefont = 'Papyrus, cursive';
			} elseif ( 'courier' === $highlite_font ) {
				$highlitefont = 'Courier, monospace';
			} elseif ( 'lucidatypewritter' === $highlite_font ) {
				$highlitefont = '"Lucida Sans Typewriter", monaco, monospace';
			} elseif ( 'alegreyasans' === $highlite_font ) {
				$highlitefont = '"Alegreya Sans", sans-serif';
			} elseif ( 'alegreyasanssc' === $highlite_font ) {
				$highlitefont = '"Alegreya Sans SC", sans-serif';
			} elseif ( 'archivo' === $highlite_font ) {
				$highlitefont = '"Archivo", sans-serif';
			} elseif ( 'archivonarrow' === $highlite_font ) {
				$highlitefont = '"Archivo Narrow", sans-serif';
			} elseif ( 'b612' === $highlite_font ) {
				$highlitefont = '"B612", sans-serif';
			} elseif ( 'cabin' === $highlite_font ) {
				$highlitefont = '"Cabin", sans-serif';
			} elseif ( 'cairo' === $highlite_font ) {
				$highlitefont = '"Cairo", sans-serif';
			} elseif ( 'chivo' === $highlite_font ) {
				$highlitefont = '"Chivo", sans-serif';
			} elseif ( 'exo2' === $highlite_font ) {
				$highlitefont = '"Exo 2", sans-serif';
			} elseif ( 'fjallaone' === $highlite_font ) {
				$highlitefont = '"Fjalla One", sans-serif';
			} elseif ( 'firasans' === $highlite_font ) {
				$highlitefont = '"Fira Sans", sans-serif';
			} elseif ( 'ibmplexsans' === $highlite_font ) {
				$highlitefont = '"IBM Plex Sans", sans-serif';
			} elseif ( 'karla' === $highlite_font ) {
				$highlitefont = '"Karla", sans-serif';
			} elseif ( 'lato' === $highlite_font ) {
				$highlitefont = '"Lato", sans-serif';
			} elseif ( 'librefranklin' === $highlite_font ) {
				$highlitefont = '"Libre Franklin", sans-serif';
			} elseif ( 'montserrat' === $highlite_font ) {
				$highlitefont = '"Montserrat", sans-serif';
			} elseif ( 'montserratalternates' === $highlite_font ) {
				$highlitefont = '"Montserrat Alternates", sans-serif';
			} elseif ( 'muli' === $highlite_font ) {
				$highlitefont = '"Muli", sans-serif';
			} elseif ( 'notosans' === $highlite_font ) {
				$highlitefont = '"Noto Sans", sans-serif';
			} elseif ( 'nunito' === $highlite_font ) {
				$highlitefont = '"Nunito", sans-serif';
			} elseif ( 'opensans' === $highlite_font ) {
				$highlitefont = '"Open Sans", sans-serif';
			} elseif ( 'oswald' === $highlite_font ) {
				$highlitefont = '"Oswald", sans-serif';
			} elseif ( 'oxygen' === $highlite_font ) {
				$highlitefont = '"Oxygen", sans-serif';
			} elseif ( 'poppins' === $highlite_font ) {
				$highlitefont = '"Poppins", sans-serif';
			} elseif ( 'prozalibre' === $highlite_font ) {
				$highlitefont = '"Proza Libre", sans-serif';
			} elseif ( 'ptsans' === $highlite_font ) {
				$highlitefont = '"PT Sans", sans-serif';
			} elseif ( 'raleway' === $highlite_font ) {
				$highlitefont = '"Raleway", sans-serif';
			} elseif ( 'roboto' === $highlite_font ) {
				$highlitefont = '"Roboto", sans-serif';
			} elseif ( 'rubik' === $highlite_font ) {
				$highlitefont = '"Rubik", sans-serif';
			} elseif ( 'sourcesanspro' === $highlite_font ) {
				$highlitefont = '"Source Sans Pro", sans-serif';
			} elseif ( 'titilliumweb' === $highlite_font ) {
				$highlitefont = '"Titillium Web", sans-serif';
			} elseif ( 'ubuntu' === $highlite_font ) {
				$highlitefont = '"Ubuntu", sans-serif';
			} elseif ( 'varela' === $highlite_font ) {
				$highlitefont = '"Varela", sans-serif';
			} elseif ( 'varelaround' === $highlite_font ) {
				$highlitefont = '"Varela Round", sans-serif';
			} elseif ( 'worksans' === $highlite_font ) {
				$highlitefont = '"Work Sans", sans-serif';
			} elseif ( 'alegreya' === $highlite_font ) {
				$highlitefont = '"Alegreya", serif';
			} elseif ( 'alegreyasc' === $highlite_font ) {
				$highlitefont = '"Alegreya SC", serif';
			} elseif ( 'arvo' === $highlite_font ) {
				$highlitefont = '"Arvo", serif';
			} elseif ( 'biothyme' === $highlite_font ) {
				$highlitefont = '"BioRhyme", serif';
			} elseif ( 'cardo' === $highlite_font ) {
				$highlitefont = '"Cardo", serif';
			} elseif ( 'cormorant' === $highlite_font ) {
				$highlitefont = '"Cormorant", serif';
			} elseif ( 'crimsontext' === $highlite_font ) {
				$highlitefont = '"Crimson Text", serif';
			} elseif ( 'domine' === $highlite_font ) {
				$highlitefont = '"Domine", serif';
			} elseif ( 'eczar' === $highlite_font ) {
				$highlitefont = '"Eczar", serif';
			} elseif ( 'frankruhllibre' === $highlite_font ) {
				$highlitefont = '"Frank Ruhl Libre", serif';
			} elseif ( 'ibmplexserif' === $highlite_font ) {
				$highlitefont = '"IBM Plex Serif", serif';
			} elseif ( 'inknutantiqua' === $highlite_font ) {
				$highlitefont = '"Inknut Antiqua", serif';
			} elseif ( 'librebaskerville' === $highlite_font ) {
				$highlitefont = '"Libre Baskerville", serif';
			} elseif ( 'lora' === $highlite_font ) {
				$highlitefont = '"Lora", serif';
			} elseif ( 'merriweather' === $highlite_font ) {
				$highlitefont = '"Merriweather", serif';
			} elseif ( 'neuton' === $highlite_font ) {
				$highlitefont = '"Neuton", serif';
			} elseif ( 'oldstandardtt' === $highlite_font ) {
				$highlitefont = '"Old Standard TT", serif';
			} elseif ( 'playfairdisplay' === $highlite_font ) {
				$highlitefont = '"Playfair Display", serif';
			} elseif ( 'ptserif' === $highlite_font ) {
				$highlitefont = '"PT Serif", serif';
			} elseif ( 'robotoslab' === $highlite_font ) {
				$highlitefont = '"Roboto Slab", serif';
			} elseif ( 'rokkitt' === $highlite_font ) {
				$highlitefont = '"Rokkitt", serif';
			} elseif ( 'sourceserifpro' === $highlite_font ) {
				$highlitefont = '"Source Serif Pro", serif';
			} elseif ( 'spectral' === $highlite_font ) {
				$highlitefont = '"Spectral", serif';
			} elseif ( 'vollkorn' === $highlite_font ) {
				$highlitefont = '"Vollkorn", serif';
			} elseif ( 'vollkornsc' === $highlite_font ) {
				$highlitefont = '"Vollkorn SC", serif';
			} elseif ( 'abrilfatface' === $highlite_font ) {
				$highlitefont = '"Abril Fatface", cursive';
			} elseif ( 'alfaslabone' === $highlite_font ) {
				$highlitefont = '"Alfa Slab One", cursive';
			} elseif ( 'baloo' === $highlite_font ) {
				$highlitefont = '"Baloo", cursive';
			} elseif ( 'barrio' === $highlite_font ) {
				$highlitefont = '"Barrio", cursive';
			} elseif ( 'blackopsone' === $highlite_font ) {
				$highlitefont = '"Black Ops One", cursive';
			} elseif ( 'cabinsketch' === $highlite_font ) {
				$highlitefont = '"Cabin Sketch", cursive';
			} elseif ( 'chelaone' === $highlite_font ) {
				$highlitefont = '"Chela One", cursive';
			} elseif ( 'concertone' === $highlite_font ) {
				$highlitefont = '"Concert One", cursive';
			} elseif ( 'ericaone' === $highlite_font ) {
				$highlitefont = '"Erica One", cursive';
			} elseif ( 'fascinate' === $highlite_font ) {
				$highlitefont = '"Fascinate", cursive';
			} elseif ( 'flamenco' === $highlite_font ) {
				$highlitefont = '"Flamenco", cursive';
			} elseif ( 'frederickathegreat' === $highlite_font ) {
				$highlitefont = '"Fredericka the Great", cursive';
			} elseif ( 'lilyscriptone' === $highlite_font ) {
				$highlitefont = '"Lily Script One", cursive';
			} elseif ( 'lobster' === $highlite_font ) {
				$highlitefont = '"Lobster", cursive';
			} elseif ( 'lobstertwo' === $highlite_font ) {
				$highlitefont = '"Lobster Two", cursive';
			} elseif ( 'monoton' === $highlite_font ) {
				$highlitefont = '"Monoton", cursive';
			} elseif ( 'nixieone' === $highlite_font ) {
				$highlitefont = '"Nixie One", cursive';
			} elseif ( 'oleoscript' === $highlite_font ) {
				$highlitefont = '"Oleo Script", cursive';
			} elseif ( 'oleoscriptswashcaps' === $highlite_font ) {
				$highlitefont = '"Oleo Script Swash Caps", cursive';
			} elseif ( 'ranchers' === $highlite_font ) {
				$highlitefont = '"Ranchers", cursive';
			} elseif ( 'rakkas' === $highlite_font ) {
				$highlitefont = '"Rakkas", cursive';
			} elseif ( 'specialelite' === $highlite_font ) {
				$highlitefont = '"Special Elite", cursive';
			} elseif ( 'yatraone' === $highlite_font ) {
				$highlitefont = '"Yatra One", cursive';
			} elseif ( 'inconsolata' === $highlite_font ) {
				$highlitefont = '"Inconsolata", monospace';
			} elseif ( 'spacemono' === $highlite_font ) {
				$highlitefont = '"Space Mono", monospace';
			}
		endif;

		if ( $default_sitetitle_font !== $sitetitle_font ) :
			$css->set_selector( '.site-title' );
			if ( 'header' === $sitetitle_font && $default_header_font !== $header_font ) {
				$css->add_property( 'font-family', $headerfont );
			} elseif ( 'highlite' === $sitetitle_font && $default_highlite_font !== $highlite_font ) {
				$css->add_property( 'font-family', $highlitefont );
			}
		endif;
		if ( $default_sitedescription_font !== $sitedescription_font ) :
			$css->set_selector( '.site-description' );
			if ( 'header' === $sitedescription_font && $default_header_font !== $header_font ) {
				$css->add_property( 'font-family', $headerfont );
			} elseif ( 'highlite' === $sitedescription_font && $default_highlite_font !== $highlite_font ) {
				$css->add_property( 'font-family', $highlitefont );
			}
		endif;
		if ( $default_menu_font !== $menu_font ) :
			$css->set_selector( '.site-navigation' );
			if ( 'header' === $menu_font && $default_header_font !== $header_font ) {
				$css->add_property( 'font-family', $headerfont );
			} elseif ( 'highlite' === $menu_font && $default_highlite_font !== $highlite_font ) {
				$css->add_property( 'font-family', $highlitefont );
			}
		endif;

		if ( $default_header_font_weight !== $header_font_weight ) :
			$css->set_selector( 'h1:not(.site-title), h2, h3, h4, h5, h6' );
			$css->add_property( 'font-weight', $header_font_weight );
		endif;
		if ( $default_sitetitle_font_weight !== $sitetitle_font_weight ) :
			$css->set_selector( '.site-title' );
			$css->add_property( 'font-weight', $sitetitle_font_weight );
		endif;
		if ( $default_sitedescription_font_weight !== $sitedescription_font_weight ) :
			$css->set_selector( '.site-description' );
			$css->add_property( 'font-weight', $sitedescription_font_weight );
		endif;
		if ( $default_menu_font_weight !== $menu_font_weight ) :
			$css->set_selector( '.site-navigation a' );
			$css->add_property( 'font-weight', $menu_font_weight );
		endif;

		if ( absint( $default_base_font_size ) !== absint( $base_font_size ) ) :
			$css->set_selector( '.content-inner-wrap' );
			$css->add_property( 'font-size', esc_attr( $osixthreeo_settings['base_font_size'] . 'px' ) );
		endif;
		if ( absint( $default_sitetitle_font_size ) !== absint( $sitetitle_font_size ) ) :
			$css->set_selector( '.site-title' );
			$css->add_property( 'font-size', esc_attr( $osixthreeo_settings['sitetitle_font_size'] . 'px' ) );
		endif;
		if ( absint( $default_sitedescription_font_size ) !== absint( $sitedescription_font_size ) ) :
			$css->set_selector( '.site-description' );
			$css->add_property( 'font-size', esc_attr( $osixthreeo_settings['sitedescription_font_size'] . 'px' ) );
		endif;
		if ( absint( $default_menu_font_size ) !== absint( $menu_font_size ) ) :
			$css->set_selector( '#primary-navigation' );
			$css->add_property( 'font-size', esc_attr( $osixthreeo_settings['menu_font_size'] . 'px' ) );
		endif;

		/*
		 * Post Meta --------------------------------
		 */
		// Header/Footer colors.
		if ( $default_meta_date === $meta_date || $default_meta_author === $meta_author || $default_meta_comments === $meta_comments || $default_meta_updated === $meta_updated ) :
			if ( $default_meta_color !== $meta_color ) :
				$css->set_selector( '.entry-meta, .entry-meta a' );
				$css->add_property( 'color', esc_attr( $osixthreeo_settings['meta_color'] ) );
			endif;
			if ( $default_archives_meta_color !== $archives_meta_color ) :
				$css->set_selector( '.blog article .entry-meta,.archive article .entry-meta,.search article .entry-meta, .blog article .entry-meta a,.archive article .entry-meta a,.search article .entry-meta a' );
				$css->add_property( 'color', esc_attr( $osixthreeo_settings['archives_meta_color'] ) );
			endif;
		endif;
		if ( $default_meta_footer === $meta_footer ) :
			if ( $default_meta_color !== $meta_color ) :
				$css->set_selector( '.entry-footer, .entry-footer a' );
				$css->add_property( 'color', esc_attr( $osixthreeo_settings['meta_color'] ) );
			endif;
		endif;
		// Header meta.
		if ( $default_meta_date === $meta_date || $default_meta_author === $meta_author || $default_meta_comments === $meta_comments || $default_meta_updated === $meta_updated ) :
			if ( $default_meta_font !== $meta_font ) :
				$css->set_selector( '.entry-meta' );
				if ( 'header' === $meta_font && $default_header_font !== $header_font ) {
					$css->add_property( 'font-family', $headerfont );
				} elseif ( 'highlite' === $meta_font && $default_highlite_font !== $highlite_font ) {
					$css->add_property( 'font-family', $highlitefont );
				}
			endif;
			if ( $default_meta_font_weight !== $meta_font_weight ) :
				$css->set_selector( '.entry-meta' );
				$css->add_property( 'font-weight', $meta_font_weight );
			endif;
			if ( absint( $default_meta_font_size ) !== absint( $meta_font_size ) ) :
				$css->set_selector( '.entry-meta' );
				$css->add_property( 'font-size', esc_attr( $osixthreeo_settings['meta_font_size'] . 'px' ) );
			endif;
		endif;
		// Footer meta.
		if ( $default_meta_footer === $meta_footer ) :
			if ( $default_meta_font !== $meta_font ) :
				$css->set_selector( '.entry-footer' );
				if ( 'header' === $meta_font && $default_header_font !== $header_font ) {
					$css->add_property( 'font-family', $headerfont );
				} elseif ( 'highlite' === $meta_font && $default_highlite_font !== $highlite_font ) {
					$css->add_property( 'font-family', $highlitefont );
				}
			endif;
			if ( $default_meta_font_weight !== $meta_font_weight ) :
				$css->set_selector( '.entry-footer' );
				$css->add_property( 'font-weight', $meta_font_weight );
			endif;
			if ( absint( $default_meta_font_size ) !== absint( $meta_font_size ) ) :
				$css->set_selector( '.entry-footer' );
				$css->add_property( 'font-size', esc_attr( $osixthreeo_settings['meta_font_size'] . 'px' ) );
			endif;
		endif;

		// PRIMARY HERO TEXT.
		if ( $default_hero_text_primary !== $hero_text_primary ) :

			if ( $default_hero_text_primary_font !== $hero_text_primary_font ) :
					$css->set_selector( '.hero-primary' );
				if ( 'header' === $hero_text_primary_font && $default_header_font !== $header_font ) {
					$css->add_property( 'font-family', $headerfont );
				} elseif ( 'highlite' === $hero_text_primary_font && $default_highlite_font !== $highlite_font ) {
					$css->add_property( 'font-family', $highlitefont );
				}
			endif;

			if ( absint( $default_hero_text_primary_font_size ) !== absint( $hero_text_primary_font_size ) ) :
				$css->set_selector( '.hero-primary' );
				$css->add_property( 'font-size', esc_attr( $osixthreeo_settings['hero_text_primary_font_size'] . 'px' ) );
			endif;
			if ( absint( $default_hero_text_primary_font_size_mobile ) !== absint( $hero_text_primary_font_size_mobile ) ) :
				$css->start_media_query( apply_filters( 'osixthreeo_mobile_media_query', '(max-width:768px)' ) );
					$css->set_selector( '.hero-primary' );
					$css->add_property( 'font-size', esc_attr( $osixthreeo_settings['hero_text_primary_font_size_mobile'] . 'px' ) );
				$css->stop_media_query();
			endif;

			if ( $default_hero_text_primary_color !== $hero_text_primary_color ) :
				$css->set_selector( '.hero-primary' );
				$css->add_property( 'color', esc_attr( $osixthreeo_settings['hero_text_primary_color'] ) );
			endif;

			if ( $default_hero_text_primary_alignment !== $hero_text_primary_alignment ) :
				$css->set_selector( '.hero-primary' );
				$css->add_property( 'text-align', $hero_text_primary_alignment );
			endif;

			if ( $default_hero_text_primary_shadow_color !== $hero_text_primary_shadow_color ||
				intval( $default_hero_text_primary_shadow_x ) !== intval( $hero_text_primary_shadow_x ) ||
				intval( $default_hero_text_primary_shadow_y ) !== intval( $hero_text_primary_shadow_y ) ||
				absint( $default_hero_text_primary_shadow_blur ) !== absint( $hero_text_primary_shadow_blur ) ) :
				$p_bgcolor = $osixthreeo_settings['hero_text_primary_shadow_color'];
				$p_bgx     = intval( $osixthreeo_settings['hero_text_primary_shadow_x'] );
				$p_bgy     = intval( $osixthreeo_settings['hero_text_primary_shadow_y'] );
				$p_bgblur  = absint( $osixthreeo_settings['hero_text_primary_shadow_blur'] );
				$prop_p    = sprintf( '%1$spx %2$spx %3$spx %4$s', $p_bgx, $p_bgy, $p_bgblur, $p_bgcolor );
				$css->set_selector( '.hero-primary' );
				$css->add_property( 'text-shadow', $prop_p );
			endif;

		endif;

		// SECONDARY HERO TEXT.
		if ( $default_hero_text_secondary !== $hero_text_secondary ) :

			if ( $default_hero_text_secondary_font !== $hero_text_secondary_font ) :
					$css->set_selector( '.hero-secondary' );
				if ( 'header' === $hero_text_secondary_font && $default_header_font !== $header_font ) {
					$css->add_property( 'font-family', $headerfont );
				} elseif ( 'highlite' === $hero_text_secondary_font && $default_highlite_font !== $highlite_font ) {
					$css->add_property( 'font-family', $highlitefont );
				}
			endif;

			if ( absint( $default_hero_text_secondary_font_size ) !== absint( $hero_text_secondary_font_size ) ) :
				$css->set_selector( '.hero-secondary' );
				$css->add_property( 'font-size', esc_attr( $osixthreeo_settings['hero_text_secondary_font_size'] . 'px' ) );
			endif;
			if ( absint( $default_hero_text_secondary_font_size_mobile ) !== absint( $hero_text_secondary_font_size_mobile ) ) :
				$css->start_media_query( apply_filters( 'osixthreeo_mobile_media_query', '(max-width:768px)' ) );
					$css->set_selector( '.hero-secondary' );
					$css->add_property( 'font-size', esc_attr( $osixthreeo_settings['hero_text_secondary_font_size_mobile'] . 'px' ) );
				$css->stop_media_query();
			endif;

			if ( $default_hero_text_secondary_color !== $hero_text_secondary_color ) :
				$css->set_selector( '.hero-secondary' );
				$css->add_property( 'color', esc_attr( $osixthreeo_settings['hero_text_secondary_color'] ) );
			endif;

			if ( $default_hero_text_secondary_alignment !== $hero_text_secondary_alignment ) :
				$css->set_selector( '.hero-secondary' );
				$css->add_property( 'text-align', $hero_text_secondary_alignment );
			endif;

			if ( $default_hero_text_secondary_shadow_color !== $hero_text_secondary_shadow_color ||
				intval( $default_hero_text_secondary_shadow_x ) !== intval( $hero_text_secondary_shadow_x ) ||
				intval( $default_hero_text_secondary_shadow_y ) !== intval( $hero_text_secondary_shadow_y ) ||
				absint( $default_hero_text_secondary_shadow_blur ) !== absint( $hero_text_secondary_shadow_blur ) ) :
				$p_bgcolor = $osixthreeo_settings['hero_text_secondary_shadow_color'];
				$p_bgx     = intval( $osixthreeo_settings['hero_text_secondary_shadow_x'] );
				$p_bgy     = intval( $osixthreeo_settings['hero_text_secondary_shadow_y'] );
				$p_bgblur  = absint( $osixthreeo_settings['hero_text_secondary_shadow_blur'] );
				$prop_p    = sprintf( '%1$spx %2$spx %3$spx %4$s', $p_bgx, $p_bgy, $p_bgblur, $p_bgcolor );
				$css->set_selector( '.hero-secondary' );
				$css->add_property( 'text-shadow', $prop_p );
			endif;
		endif;

		if ( $default_hero_scroll_button_alignment !== $hero_scroll_button_alignment ) :
			$css->set_selector( '.hero-scroll-button' );
			$css->add_property( 'text-align', $hero_scroll_button_alignment );
		endif;

		// ARCHIVES ------------------------------------------ .
		if ( $default_archives_bg_color !== $archives_bg_color ) :
			$css->set_selector( '.blog article,.archive article,.search article' );
			$css->add_property( 'background-color', esc_attr( $osixthreeo_settings['archives_background_color'] ) );
		endif;

		if ( $default_archives_text_color !== $archives_text_color ) :
			$css->set_selector( '.blog article,.archive article,.search article' );
			$css->add_property( 'color', esc_attr( $osixthreeo_settings['archives_text_color'] ) );
		endif;
		if ( $default_archives_title_color !== $archives_title_color ) :
			$css->set_selector( '.blog article .entry-title,.archive article .entry-title,.search article .entry-title,.blog article .entry-title a,.archive article .entry-title a,.search article .entry-title a' );
			$css->add_property( 'color', esc_attr( $osixthreeo_settings['archives_title_color'] ) );
		endif;
		if ( $default_archives_link_color !== $archives_link_color ) :
			$css->set_selector( '.blog article .entry-content a,.archive article .entry-content a,.search article .entry-content a,.link-more' );
			$css->add_property( 'color', esc_attr( $osixthreeo_settings['archives_link_color'] ) );
		endif;
		if ( $default_archives_link_color_hover !== $archives_link_color_hover ) :
			$css->set_selector( '.blog article .entry-content a:hover,.archive article .entry-content a:hover,.search article .entry-content a:hover' );
			$css->add_property( 'color', esc_attr( $osixthreeo_settings['archives_link_color_hover'] ) );
		endif;

		if ( absint( $default_archives_pad_left ) !== absint( $archives_pad_left ) ) :
			$css->set_selector( '.blog article .entry-header,.archive article .entry-header,.search article .entry-header,.blog article .entry-content,.archive article .entry-content,.search article .entry-content,.link-more' );
			$css->add_property( 'padding-left', esc_attr( $osixthreeo_settings['archives_pad_left'] . 'px' ) );
		endif;
		if ( absint( $default_archives_pad_right ) !== absint( $archives_pad_right ) ) :
			$css->set_selector( '.blog article .entry-header,.archive article .entry-header,.search article .entry-header,.blog article .entry-content,.archive article .entry-content,.search article .entry-content,.link-more' );
			$css->add_property( 'padding-right', esc_attr( $osixthreeo_settings['archives_pad_right'] . 'px' ) );
		endif;

		if ( absint( $default_archives_pad_top ) !== absint( $archives_pad_top ) ) :
			$css->set_selector( '.blog article .entry-header,.archive article .entry-header,.search article .entry-header,.archive article.format-aside .entry-content,.blog article.format-aside .entry-content,.search article.format-aside .entry-content,.archive article.format-status .entry-content,.blog article.format-status .entry-content,.search article.format-status .entry-content' );
			$css->add_property( 'padding-top', esc_attr( $osixthreeo_settings['archives_pad_top'] . 'px' ) );
		endif;

		if ( absint( $default_archives_pad_bottom ) !== absint( $archives_pad_bottom ) ) :
			$css->set_selector( '.link-more' );
			$css->add_property( 'padding-bottom', esc_attr( $osixthreeo_settings['archives_pad_bottom'] . 'px' ) );
		endif;

		// Border.
		if ( $default_archives_border_color !== $archives_border_color ||
			absint( $default_archives_border_width ) !== absint( $archives_border_width ) ) :
			$a_bgcolor = $osixthreeo_settings['archives_border_color'];
			$a_bgwidth = absint( $osixthreeo_settings['archives_border_width'] );
			$prop      = sprintf( '%1$spx solid %2$s', $a_bgwidth, $a_bgcolor );
			$css->set_selector( '.blog article,.archive article,.search article' );
			$css->add_property( 'border', $prop );
		endif;
		// Border Radius.
		if ( absint( $default_archives_border_radius ) !== absint( $archives_border_radius ) ) :
			$rad = absint( $osixthreeo_settings['archives_border_radius'] );
			$css->set_selector( '.blog article,.archive article,.search article' );
			$css->add_property( 'border-radius', esc_attr( $osixthreeo_settings['archives_border_radius'] . 'px' ) );
		endif;

		if ( $default_archives_box_shadow_color !== $archives_box_shadow_color &&
			intval( $default_archives_box_shadow_x ) !== intval( $archives_box_shadow_x ) ||
			intval( $default_archives_box_shadow_y ) !== intval( $archives_box_shadow_y ) ||
			absint( $default_archives_box_shadow_blur ) !== absint( $archives_box_shadow_blur ) ||
			absint( $default_archives_box_shadow_spread ) !== absint( $archives_box_shadow_spread ) ) :
			$a_bgcolor  = $osixthreeo_settings['archives_box_shadow_color'];
			$a_bgx      = intval( $osixthreeo_settings['archives_box_shadow_x'] );
			$a_bgy      = intval( $osixthreeo_settings['archives_box_shadow_y'] );
			$a_bgblur   = absint( $osixthreeo_settings['archives_box_shadow_blur'] );
			$a_bgspread = absint( $osixthreeo_settings['archives_box_shadow_spread'] );
			$prop       = sprintf( '%1$spx %2$spx %3$spx %4$spx %5$s', $a_bgx, $a_bgy, $a_bgblur, $a_bgspread, $a_bgcolor );
			$css->set_selector( '.blog article,.archive article,.search article' );
			$css->add_property( 'box-shadow', $prop );
		endif;

		// Allow us to hook CSS into our output - where we would hook our "Pro" features?
		do_action( 'osixthreeo_base_css', $css );

		if ( null !== $css ) {
			return apply_filters( 'osixthreeo_settings', $css->css_output() );
		}

		return $osixthreeo_settings;
	}
}


/**
 * Enqueue our customizer CSS.
 *
 * @since 1.0.0
 */
function osixthreeo_enqueue_customizer_css() {
	$css = osixthreeo_base_css();
	// If there are no settings set Or if we're in the customizer.
	if ( '' === $css || is_customize_preview() ) {
		$css = osixthreeo_base_css();
	} else {
		$css = osixthreeo_base_css() . '/* OsixthreeO customizer CSS */';
	}
	wp_add_inline_style( 'osixthreeo-style', $css );
}
add_action( 'wp_enqueue_scripts', 'osixthreeo_enqueue_customizer_css', 50 );
