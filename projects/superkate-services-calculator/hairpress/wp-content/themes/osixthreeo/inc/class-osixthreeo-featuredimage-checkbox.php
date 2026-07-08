<?php
/**
 * Display Featured Image checkbox.
 *
 * @package    osixthreeo
 * @subpackage osixthreeo/inc
 * @author     Chip Sheppard
 * @since      1.0.0
 * @license    GPL-2.0+
 *
 * @link https://developer.wordpress.org/reference/functions/add_meta_box/
 * @link https://www.billerickson.net/code/add-checkbox-to-featured-image-metabox/
 */

/**
 * Calls the class on the post edit screen.
 */
function osixthreeo_fi_checkbox() {
	new Osixthreeo_Featuredimage_Checkbox();
}

if ( is_admin() ) {
	add_action( 'load-post.php', 'osixthreeo_fi_checkbox' );
	add_action( 'load-post-new.php', 'osixthreeo_fi_checkbox' );
}

/**
 * The Class.
 */
class Osixthreeo_Featuredimage_Checkbox {

	/**
	 * Hook into the appropriate actions when the class is constructed.
	 */
	public function __construct() {
		add_action( 'add_meta_boxes', array( $this, 'add_fi_checkbox' ) );
		add_action( 'save_post', array( $this, 'save_fi_checkbox' ) );
	}

	/**
	 * Adds a checkbox.
	 *
	 * @link https://developer.wordpress.org/reference/functions/add_meta_box/
	 * @link https://wordpress.org/ideas/topic/add-meta-box-to-multiple-post-types
	 * @param Array $post_type Post Types to target.
	 */
	public function add_fi_checkbox( $post_type ) {
		$types = array( 'post', 'page' );
		if ( in_array( $post_type, $types, true ) ) {
			add_meta_box(
				'fi_checkbox_id',
				__( 'Featured Image Display', 'osixthreeo' ),
				array( $this, 'render_fi_checkbox' ),
				$post_type,
				'side',
				'high'
			);
		}
	}

	/**
	 * Saving the meta box.
	 *
	 * @param int $post_id Post ID.
	 */
	public function save_fi_checkbox( $post_id ) {
		// Check if our nonce is set.
		if ( ! isset( $_POST['osixthreeo_nonce'] ) ) {
			return $post_id;
		}

		$nonce = sanitize_text_field( wp_unslash( $_POST['osixthreeo_nonce'] ) );

		// Verify that the nonce is valid.
		if ( ! wp_verify_nonce( $nonce, 'osixthreeo_nonce_action' ) ) {
			return $post_id;
		}

		// Check if not an autosave.
		if ( defined( 'DOING_AUTOSAVE' ) && DOING_AUTOSAVE ) {
			return $post_id;
		}

		// Check the user's permissions.
		if ( ! current_user_can( 'edit_post', $post_id ) ) {
			return $post_id;
		}

		// Check if not a revision.
		if ( wp_is_post_revision( $post_id ) ) {
			return $post_id;
		}

		// check if there was a multisite switch before.
		if ( is_multisite() && ms_is_switched() ) {
			return $post_id;
		}

		/* OK, it's safe for us to save the data now. */
		$field_id    = 'osixthreeo_show_featured_image';
		$field_value = isset( $_REQUEST[ $field_id ] ) ? 'yes' : '';

		// Update the meta field.
		update_post_meta( $post_id, '_osixthreeo_show_featured_image', $field_value );

	}

	/**
	 * Callback.
	 *
	 * @param WP_Post $post The post object.
	 */
	public function render_fi_checkbox( $post ) {
		// Add an nonce field so we can check for it later - $action, $name.
		wp_nonce_field( 'osixthreeo_nonce_action', 'osixthreeo_nonce' );

		// Use get_post_meta to retrieve an existing value from the database.
		$isfeatured = get_post_meta( $post->ID, '_osixthreeo_show_featured_image', true );
		?>
		<label><input type="checkbox" name="osixthreeo_show_featured_image" value="yes" <?php echo ( ( 'yes' === $isfeatured ) ? 'checked="checked"' : '' ); ?>/> <?php esc_html_e( 'Display in the custom header.', 'osixthreeo' ); ?><label>
		<?php
	}
}
