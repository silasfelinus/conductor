<?php
/**
 * Customize Range Slider.
 *
 * @package    osixthreeo
 * @subpackage osixthreeo/inc/customizer/controls
 * @author     Chip Sheppard
 * @since      1.2.0
 * @license    GPL-2.0+
 */

if ( ! defined( 'ABSPATH' ) ) {
	exit;
}

if ( class_exists( 'WP_Customize_Control' ) && ! class_exists( 'Osixthreeo_Range_Control' ) ) :
	/**
	 * Creates HTML section in customizer.
	 */
	class Osixthreeo_Range_Control extends WP_Customize_Control {

		/**
		 * Official control name.
		 *
		 * @var $type string.
		 */
		public $type = 'custom_range';

		/**
		 * Enqueue the JS.
		 */
		public function enqueue() {
			wp_enqueue_script( 'custom_range', get_template_directory_uri() . '/assets/js/customize-range-control-min.js', array( 'jquery', 'customize-base' ), OSIXTHREEO_VERSION, true );
			wp_enqueue_style( 'custom_range', get_template_directory_uri() . '/assets/css/customize-range-control-min.css', array(), OSIXTHREEO_VERSION );
		}

		/**
		 * Write the HTML.
		 */
		protected function render_content() {

			$default = $this->setting->default;
			?>
			<label>
				<?php if ( ! empty( $this->label ) ) : ?>
					<span class="customize-control-title"><?php echo esc_html( $this->label ); ?></span>
				<?php endif; ?>
				<?php if ( ! empty( $this->description ) ) : ?>
					<span class="description customize-control-description"><?php echo esc_html( $this->description ); ?></span>
				<?php endif; ?>
				<input data-input-type="range" type="range" <?php $this->input_attrs(); ?> value="<?php echo esc_attr( $this->value() ); ?>" <?php $this->link(); ?> data-reset_value="<?php echo esc_attr( $default ); ?>" />
				<input data-input-type="number" type="number" <?php $this->input_attrs(); ?> class="osixthreeo-range-value" value="<?php echo esc_attr( $this->value() ); ?>" <?php $this->link(); ?> />
				<span class="osixthreeo-reset-slider"><span class="dashicons dashicons-image-rotate"></span></span>
			</label>
			<?php
		}
	}
endif;
