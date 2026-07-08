<?php
/**
 * Sets all of our customizer defaults.
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

if ( ! function_exists( 'osixthreeo_get_defaults' ) ) {
	/**
	 * Set default options
	 *
	 * @since 1.0
	 */
	function osixthreeo_get_defaults() {
		$osixthreeo_defaults = array(
			'tagline_align'                        => '',
			'background_color'                     => '#f3f5f7',
			'containment_setting'                  => 'full',
			'max_width'                            => '1280',
			'header_layout'                        => '',
			'header_padding'                       => '16',
			'home_layout_setting'                  => 'layout-ns',
			'page_layout_setting'                  => 'layout-ns',
			'single_layout_setting'                => 'layout-ns',
			'search_layout_setting'                => 'layout-ns',
			'archive_layout_setting'               => 'layout-ns',
			'header_bg_color_left'                 => '#4169e1',
			'header_bg_color_right'                => '#ba55d3',
			'header_gradient_angle'                => '145',
			'header_left_stop'                     => '0',
			'header_right_stop'                    => '100',
			'home_header_fullheight'               => 'adjustable',
			'home_header_height'                   => '600',
			'home_mobile_header_height'            => '400',
			'subpage_header_height'                => '200',
			'subpage_mobile_header_height'         => '120',
			'header_bg_position'                   => 'center-center',
			'header_bg_repeat'                     => 'no-repeat',
			'header_bg_size'                       => 'cover',
			'meta_date'                            => true,
			'meta_author'                          => true,
			'meta_comments'                        => true,
			'meta_updated'                         => true,
			'meta_footer'                          => true,
			'post_nav'                             => true,
			'content_title_lift'                   => false,
			'content_title_color'                  => '',
			'header_background_color'              => '',
			'header_background_color_home'         => '',
			'nav_link_color'                       => '#ffffff',
			'subnav_text_color'                    => '#222222',
			'subnav_bg_color'                      => '#ffffff',
			'subnav_border_color'                  => '#dcdcdc',
			'subnav_hover_text_color'              => '',
			'subnav_hover_bg_color'                => '#f3f3f3',
			'content_bgcolor'                      => '',
			'text_color'                           => '#222222',
			'link_color'                           => '#4169e1',
			'link_color_hover'                     => '#ba55d3',
			'footer_background_color'              => '#000000',
			'footer_title_color'                   => '#ffffff',
			'footer_text_color'                    => '#f5f5f5',
			'footer_link_color'                    => '#dcdcdc',
			'footer_link_color_hover'              => '#ffffff',
			'meta_color'                           => '#808080',
			'base_font'                            => '',
			'header_font'                          => '',
			'highlite_font'                        => '',
			'sitetitle_font'                       => '',
			'sitedescription_font'                 => '',
			'menu_font'                            => '',
			'meta_font'                            => '',
			'base_font_size'                       => '16',
			'sitetitle_font_size'                  => '48',
			'sitedescription_font_size'            => '16',
			'menu_font_size'                       => '16',
			'meta_font_size'                       => '14',
			'header_font_weight'                   => '',
			'sitetitle_font_weight'                => '',
			'sitedescription_font_weight'          => '',
			'menu_font_weight'                     => '',
			'meta_font_weight'                     => '',
			'hero_text_primary'                    => '',
			'hero_text_secondary'                  => '',
			'hero_text_primary_font'               => '',
			'hero_text_secondary_font'             => '',
			'hero_text_primary_font_size'          => '48',
			'hero_text_primary_font_size_mobile'   => '32',
			'hero_text_secondary_font_size'        => '24',
			'hero_text_secondary_font_size_mobile' => '18',
			'hero_text_primary_color'              => '#ffffff',
			'hero_text_secondary_color'            => '#ffffff',
			'hero_text_primary_alignment'          => 'left',
			'hero_text_secondary_alignment'        => 'left',
			'hero_text_primary_shadow_color'       => '',
			'hero_text_secondary_shadow_color'     => '',
			'hero_text_primary_shadow_x'           => '0',
			'hero_text_secondary_shadow_x'         => '0',
			'hero_text_primary_shadow_y'           => '0',
			'hero_text_secondary_shadow_y'         => '0',
			'hero_text_primary_shadow_blur'        => '0',
			'hero_text_secondary_shadow_blur'      => '0',
			'hero_scroll_button'                   => '',
			'hero_scroll_button_alignment'         => 'left',
			'nav_search'                           => '',
			'parallax_header'                      => '',
			'back_to_top'                          => '',
			'footer_columns'                       => '',
			'archives_background_color'            => '#ffffff',
			'archives_text_color'                  => '',
			'archives_title_color'                 => '',
			'archives_meta_color'                  => '',
			'archives_link_color'                  => '',
			'archives_link_color_hover'            => '',
			'archives_hide_featuredimage'          => '',
			'archives_hide_excerpt'                => '',
			'archives_hide_readmore'               => '',
			'archives_hide_meta'                   => '',
			'archives_pad_left'                    => '16',
			'archives_pad_right'                   => '16',
			'archives_pad_top'                     => '16',
			'archives_pad_bottom'                  => '0',
			'archives_box_shadow_color'            => '',
			'archives_box_shadow_x'                => '0',
			'archives_box_shadow_y'                => '0',
			'archives_box_shadow_blur'             => '0',
			'archives_box_shadow_spread'           => '0',
			'archives_border_color'                => '#e3e3e3',
			'archives_border_width'                => '1',
			'archives_border_radius'               => '0',
		);

		return apply_filters( 'osixthreeo_option_defaults', $osixthreeo_defaults );
	}
}
