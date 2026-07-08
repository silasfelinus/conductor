<?php
/**
 * Customizer Osixthreeo_Content_Area.
 *
 * @package    osixthreeo
 * @subpackage osixthreeo/inc/customizer/controls
 * @author     Chip Sheppard
 * @since      1.2.0
 * @license    GPL-2.0+
 */

if ( ! defined( 'ABSPATH' ) ) {
	exit; // Exit if accessed directly.
}

if ( class_exists( 'WP_Customize_Control' ) && ! class_exists( 'Osixthreeo_Content_Area' ) ) :
	/**
	 * Creates HTML section in customizer.
	 */
	class Osixthreeo_Content_Area extends WP_Customize_Control {

		/**
		 * Whitelist content parameter
		 *
		 * @access public
		 * @var string
		 */
		public $content = '';

		/**
		 * Render the control's content.
		 *
		 * Allows the content to be overridden without having to rewrite the wrapper.
		 *
		 * @since   1.0.0
		 * @return  void
		 */
		public function render_content() {
			if ( isset( $this->label ) ) {
				echo '<span class="customize-control-title">' . wp_kses_post( $this->label ) . '</span>';
			}
			if ( isset( $this->content ) ) {
				echo wp_kses_post( $this->content );
			}
			if ( isset( $this->description ) ) {
				echo '<span class="description customize-control-description">' . wp_kses_post( $this->description ) . '</span>';
			}
		}
	}
endif;
