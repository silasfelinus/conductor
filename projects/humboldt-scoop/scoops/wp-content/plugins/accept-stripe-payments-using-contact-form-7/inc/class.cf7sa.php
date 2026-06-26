<?php
/**
 * CF7SA Class
 *
 * Handles the plugin functionality.
 *
 * @package WordPress
 * @subpackage Contact Form 7 - Stripe Add-on
 * @since 1.0
 */

// Exit if accessed directly
if ( !defined( 'ABSPATH' ) ) exit;

if ( !class_exists( 'CF7SA' ) ) {

	/**
	 * The main CF7SA class
	 */
	class CF7SA {

		private static $_instance = null;
		/*private static $private_data = null;*/

		var $admin = null,
		    $front = null,
		    $lib   = null;

		public static function instance() {

			if ( is_null( self::$_instance ) )
				self::$_instance = new self();

			return self::$_instance;
		}

		function __construct() {
			add_action( 'plugins_loaded', array( $this, 'action__plugins_loaded' ), 1 );
			add_action( 'setup_theme', array( $this, 'action__setup_theme' ) );
		}

		function action__plugins_loaded() {
			include_once( ABSPATH . 'wp-admin/includes/plugin.php' );
			if ( !is_plugin_active( 'contact-form-7/wp-contact-form-7.php' ) ) {
				add_action( 'admin_notices', array( $this, 'action__admin_notices_deactive' ) );
				deactivate_plugins( CF7SA_PLUGIN_BASENAME );
			}
			
			// Action to load plugin text domain
			add_action( 'init', array( $this, 'action__init' ) );

			/* Initialize backend tags */
			add_action( 'wpcf7_admin_init', array( $this, 'action__wpcf7_admin_init' ), 15, 0 );

		}

		function action__setup_theme() {

			if ( is_admin() ) {
				CF7SA()->admin = new CF7SA_Admin;
				CF7SA()->admin->action = new CF7SA_Admin_Action;
				CF7SA()->admin->filter = new CF7SA_Admin_Filter;
			} else {
				CF7SA()->front = new CF7SA_Front;
				CF7SA()->front->action = new CF7SA_Front_Action;
				CF7SA()->front->filter = new CF7SA_Front_Filter;
			}
			CF7SA()->lib = new CF7SA_Lib;
		
		}

		function action__wpcf7_admin_init() {
			$tag_generator = WPCF7_TagGenerator::get_instance();
			$tag_generator->add(
				'stripe',
				__( 'Stripe', 'accept-stripe-payments-using-contact-form-7' ),
				array( $this, 'wpcf7_tag_generator_stripe_net' )
			);
		}

		/**
		 * Load Text Domain
		 * This gets the plugin ready for translation
		 */
		function action__init() {

			add_rewrite_rule( '^cf7sa-webhook(/(.*))?/?$', 'index.php?cf7sa-webhook=$matches[2]', 'top' );
			flush_rewrite_rules();

			// Since WordPress 4.6, translations are automatically loaded from WordPress.org
			// This custom loading is only needed for custom translation files in wp-content/languages/plugins/
			// phpcs:ignore WordPress.NamingConventions.PrefixAllGlobals.NonPrefixedHooknameFound -- 'plugin_locale' is a WordPress core filter
			$locale = apply_filters( 'plugin_locale', determine_locale(), 'accept-stripe-payments-using-contact-form-7' );
			$mofile = sprintf( '%1$s-%2$s.mo', 'accept-stripe-payments-using-contact-form-7', $locale );
			$mofile_global = WP_LANG_DIR . '/plugins/' . $mofile;

			if ( file_exists( $mofile_global ) ) {
				// Load custom translation file if it exists in global languages folder
				load_textdomain( 'accept-stripe-payments-using-contact-form-7', $mofile_global );
			}
			// Note: WordPress automatically loads translations from WordPress.org for plugins

			/**
			 * Post Type: Stripe Add-on.
			 */

			$labels = array(
				'name'          => __( 'Stripe Add-on', 'accept-stripe-payments-using-contact-form-7' ),
				'singular_name' => __( 'Stripe Add-on', 'accept-stripe-payments-using-contact-form-7' ),
				'not_found'     => __( 'No Transactions Found.', 'accept-stripe-payments-using-contact-form-7' ),
			);

			$args = array(
				'label' => __( 'Stripe Add-on', 'accept-stripe-payments-using-contact-form-7' ),
				'labels' => $labels,
				'description' => '',
				'public' => false,
				'publicly_queryable' => false,
				'show_ui' => true,
				'delete_with_user' => false,
				'show_in_rest' => false,
				'rest_base' => '',
				'has_archive' => false,
				'show_in_menu' => 'wpcf7',
				'show_in_nav_menus' => false,
				'exclude_from_search' => true,
				'capability_type' => 'post',
				'capabilities' => array(
					'read' => true,
					'create_posts'  => false,
					'publish_posts' => false,
				),
				'map_meta_cap' => true,
				'hierarchical' => false,
				'rewrite' => false,
				'query_var' => false,
				'supports' => array( 'title' ),
			);

			register_post_type( 'cf7sa_data', $args );
		}

		function action__admin_notices_deactive() {
			$allowed_html = array(
				'strong' => array(),
				'a' => array( 'href' => array(), 'target' => array() )
			);
			echo '<div class="error"><p>';
			echo wp_kses(
				sprintf(
					/* translators: 1: Link to Contact Form 7 plugin, 2: Plugin name */
					__( '%1$s is required to use %2$s.', 'accept-stripe-payments-using-contact-form-7' ),
					'<strong><a href="https://wordpress.org/plugins/contact-form-7/" target="_blank">' . __( 'Contact Form 7', 'accept-stripe-payments-using-contact-form-7' ) . '</a></strong>',
					'<strong>' . __( 'Contact Form 7 - Stripe Add-on', 'accept-stripe-payments-using-contact-form-7' ) . '</strong>'
				),
				$allowed_html
			);
			echo '</p></div>';
		}

		/*
		######## #### ##       ######## ######## ########   ######
		##        ##  ##          ##    ##       ##     ## ##    ##
		##        ##  ##          ##    ##       ##     ## ##
		######    ##  ##          ##    ######   ########   ######
		##        ##  ##          ##    ##       ##   ##         ##
		##        ##  ##          ##    ##       ##    ##  ##    ##
		##       #### ########    ##    ######## ##     ##  ######
		*/



		/*
		######## ##     ## ##    ##  ######  ######## ####  #######  ##    ##  ######
		##       ##     ## ###   ## ##    ##    ##     ##  ##     ## ###   ## ##    ##
		##       ##     ## ####  ## ##          ##     ##  ##     ## ####  ## ##
		######   ##     ## ## ## ## ##          ##     ##  ##     ## ## ## ##  ######
		##       ##     ## ##  #### ##          ##     ##  ##     ## ##  ####       ##
		##       ##     ## ##   ### ##    ##    ##     ##  ##     ## ##   ### ##    ##
		##        #######  ##    ##  ######     ##    ####  #######  ##    ##  ######
		*/

		/**
		 * -Render CF7 Shortcode settings into backend.
		 *
		 * @method wpcf7_tag_generator_stripe_net
		 *
		 * @param  object $contact_form
		 * @param  array  $args
		 */
		function wpcf7_tag_generator_stripe_net( $contact_form, $args = '' ) {

			$args = wp_parse_args( $args, array() );
			$type = $args['id'];

			$description = __( 'Generate a form-tag to display Stripe payment form', 'accept-stripe-payments-using-contact-form-7' );
			?>
			<div class="control-box">
				<fieldset>
					<legend><?php echo esc_html( $description ); ?></legend>

					<table class="form-table">
						<tbody>
							<tr>
							<th scope="row"><label for="<?php echo esc_attr( $args['content'] . '-name' ); ?>"><?php echo esc_html__( 'Name', 'accept-stripe-payments-using-contact-form-7' ); ?></label></th>
							<td>
								<legend class="screen-reader-text"><input type="checkbox" name="required" value="on" checked="checked" /></legend>
								<input type="text" name="name" class="tg-name oneline" id="<?php echo esc_attr( $args['content'] . '-name' ); ?>" /></td>
							</tr>

							<tr>
								<th scope="row"><label for="<?php echo esc_attr( $args['content'] . '-values' ); ?>"><?php esc_html_e( 'Button Name', 'accept-stripe-payments-using-contact-form-7' ); ?></label></th>
								<td><input type="text" name="values" class="oneline" id="<?php echo esc_attr( $args['content'] . '-values' ); ?>" value="<?php esc_attr_e( 'Make Payment', 'accept-stripe-payments-using-contact-form-7' ); ?>" /></td>
							</tr>

						</tbody>
					</table>
				</fieldset>
			</div>

			<div class="insert-box">
				<input type="text" name="<?php echo esc_attr( $type ); ?>" class="tag code" readonly="readonly" onfocus="this.select()" />

				<div class="submitbox">
					<input type="button" class="button button-primary insert-tag" value="<?php echo esc_attr__( 'Insert Tag', 'accept-stripe-payments-using-contact-form-7' ); ?>" />
				</div>

				<br class="clear" />

				<p class="description mail-tag">
					<label for="<?php echo esc_attr( $args['content'] . '-mailtag' ); ?>">
						<?php
						/* translators: %s: mail-tag placeholder */
						printf( esc_html__( 'To use the value input through this field in a mail field, you need to insert the corresponding mail-tag (%s) into the field on the Mail tab.', 'accept-stripe-payments-using-contact-form-7' ), '<strong><span class="mail-tag"></span></strong>' );
						?><input type="text" class="mail-tag code hidden" readonly="readonly" id="<?php echo esc_attr( $args['content'] . '-mailtag' ); ?>" />
					</label>
				</p>
			</div>
			<?php

		}

	}
}

function CF7SA() {
	return CF7SA::instance();
}

CF7SA();
