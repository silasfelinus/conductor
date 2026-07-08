<?php
/**
 * Customize Number Slider.
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

if ( class_exists( 'WP_Customize_Control' ) && ! class_exists( 'Osixthreeo_Number_Control' ) ) :
	/**
	 * Creates HTML section in customizer.
	 */
	class Osixthreeo_Number_Control extends WP_Customize_Control {

		/**
		 * Official control name.
		 *
		 * @var $type string.
		 */
		public $type = 'custom_number';

		/**
		 * Enqueue the JS.
		 */
		public function enqueue() {
			wp_enqueue_script( 'custom_number', get_template_directory_uri() . '/assets/js/customize-number-control-min.js', array( 'jquery', 'customize-base' ), OSIXTHREEO_VERSION, true );
			wp_enqueue_style( 'custom_number', get_template_directory_uri() . '/assets/css/customize-number-control-min.css', array(), OSIXTHREEO_VERSION );
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
				<input data-input-type="number" type="number" <?php $this->input_attrs(); ?> class="osixthreeo-number-value" value="<?php echo esc_attr( $this->value() ); ?>" <?php $this->link(); ?> data-reset_value="<?php echo esc_attr( $default ); ?>" />
				<span class="osixthreeo-reset-number"><span class="dashicons dashicons-image-rotate"></span></span>
			</label>
			<?php
		}
	}
endif;
