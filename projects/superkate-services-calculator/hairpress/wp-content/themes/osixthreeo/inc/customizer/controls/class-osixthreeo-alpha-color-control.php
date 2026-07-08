<?php
/**
 * Alpha Color Picker Customizer Control
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

/**
 * Color control with alpha slider.
 */
class Osixthreeo_Alpha_Color_Control extends WP_Customize_Control {

	/**
	 * Official control name.
	 *
	 * @var $type string.
	 */
	public $type = 'alpha-color';

	/**
	 * Add support for palettes to be passed in.
	 *
	 * @var $palette Supported palette values are true, false, or an array of RGBa and Hex colors.
	 */
	public $palette;

	/**
	 * Add support for showing the opacity value on the slider handle.
	 *
	 * @var $show_opacity The opacity control object.
	 */
	public $show_opacity;

	/**
	 * Render the control.
	 */
	public function render_content() {

		// Process the palette.
		if ( is_array( $this->palette ) ) {
			$palette = implode( '|', $this->palette );
		} else {
			// Default to true.
			$palette = ( false === $this->palette || 'false' === $this->palette ) ? 'false' : 'true';
		}

		// Support passing show_opacity as string or boolean. Default to true.
		$show_opacity = ( false === $this->show_opacity || 'false' === $this->show_opacity ) ? 'false' : 'true';

		// Begin the output.
		if ( isset( $this->label ) && '' !== $this->label ) {
			echo '<span class="customize-control-title">' . esc_html( $this->label ) . '</span>';
		}
		if ( isset( $this->description ) && '' !== $this->description ) {
			echo '<span class="description customize-control-description">' . esc_html( $this->description ) . '</span>';
		}
		?>
		<label>
			<input class="alpha-color-control" type="text" data-show-opacity="<?php echo esc_html( $show_opacity ); ?>" data-palette="<?php echo esc_attr( $palette ); ?>" data-default-color="<?php echo esc_attr( $this->settings['default']->default ); ?>" <?php $this->link(); ?>  />
		</label>

		<?php
	}

	/**
	 * Loads our custom styles in.
	 *
	 * @access public
	 * @return void
	 */
	public function enqueue() {
		wp_enqueue_script(
			'osixthreeo-alpha-color-control-js',
			get_template_directory_uri() . '/assets/js/customize-alpha-color-control-min.js',
			array( 'jquery', 'wp-color-picker' ),
			OSIXTHREEO_VERSION,
			true
		);
		wp_enqueue_style(
			'osixthreeo-alpha-color-control-css',
			get_template_directory_uri() . '/assets/css/customize-alpha-color-control-min.css',
			array( 'wp-color-picker' ),
			OSIXTHREEO_VERSION
		);
	}
}
