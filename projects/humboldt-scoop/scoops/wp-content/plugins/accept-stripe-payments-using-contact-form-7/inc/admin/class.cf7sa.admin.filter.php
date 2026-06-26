<?php
/**
 * CF7SA_Admin_Filter Class
 *
 * Handles the admin functionality.
 *
 * @package WordPress
 * @subpackage Contact Form 7 - Stripe Add-on
 * @since 1.0
 */

// Exit if accessed directly
if ( !defined( 'ABSPATH' ) ) exit;

if ( !class_exists( 'CF7SA_Admin_Filter' ) ) {

	/**
	 *  The CF7SA_Admin_Filter Class
	 */
	class CF7SA_Admin_Filter {

		function __construct() {

			// Adding Stripe setting tab
			add_filter( 'wpcf7_editor_panels', array( $this, 'filter__wpcf7_editor_panels' ), 10, 3 );
			add_filter( 'post_row_actions',    array( $this, 'filter__post_row_actions' ), 10, 3 );

			add_filter( 'manage_edit-cf7sa_data_sortable_columns', array( $this, 'filter__manage_cf7sa_data_sortable_columns' ), 10, 3 );
			add_filter( 'manage_cf7sa_data_posts_columns',         array( $this, 'filter__manage_cf7sa_data_posts_columns' ), 10, 3 );
			add_filter( 'bulk_actions-edit-cf7sa_data',            array( $this, 'filter__bulk_actions_edit_cf7sa_data' ) );
			add_filter( 'plugin_action_links', array( $this,'filter__admin_plugin_links'), 10, 2 ); 

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
		/**
		 * Stripe tab
		 * Adding tab in contact form 7
		 *
		 * @param $panels
		 *
		 * @return array
		 */
		public function filter__wpcf7_editor_panels( $panels ) {

			$panels[ 'stripe-add-on' ] = array(
				'title'    => __( 'Stripe', 'accept-stripe-payments-using-contact-form-7' ),
				'callback' => array( $this, 'wpcf7_admin_after_additional_settings' )
			);

			return $panels;
		}

		/**
		 * Filter: post_row_actions
		 *
		 * - Used to modify the post list action buttons.
		 *
		 * @method filter__post_row_actions
		 *
		 * @param  array $actions
		 *
		 * @return array
		 */
		function filter__post_row_actions( $actions ) {

			if ( get_post_type() === 'cf7sa_data' ) {
				unset( $actions['view'] );
				unset( $actions['inline hide-if-no-js'] );
			}

			return $actions;
		}

		/**
		 * Filter: manage_edit-cf7sa_data_sortable_columns
		 *
		 * - Used to add the sortable fields into "cf7sa_data" CPT
		 *
		 * @method filter__manage_cf7sa_data_sortable_columns
		 *
		 * @param  array $columns
		 *
		 * @return array
		 */
		function filter__manage_cf7sa_data_sortable_columns( $columns ) {
			$columns['form_id'] = '_form_id';
			$columns['transaction_status'] = '_transaction_status';
			$columns['total'] = '_total';
			return $columns;
		}

		/**
		 * Filter: manage_cf7sa_data_posts_columns
		 *
		 * - Used to add new column fields for the "cf7sa_data" CPT
		 *
		 * @method filter__manage_cf7sa_data_posts_columns
		 *
		 * @param  array $columns
		 *
		 * @return array
		 */
		function filter__manage_cf7sa_data_posts_columns( $columns ) {
			unset( $columns['date'] );
			$columns['form_id'] = __( 'Form ID', 'accept-stripe-payments-using-contact-form-7' );
			$columns['transaction_status'] = __( 'Transaction Status', 'accept-stripe-payments-using-contact-form-7' );
			$columns['total'] = __( 'Total Amount', 'accept-stripe-payments-using-contact-form-7' );
			$columns['date'] = __( 'Submitted Date', 'accept-stripe-payments-using-contact-form-7' );
			return $columns;
		}

		/**
		 * Filter: bulk_actions-edit-cf7sa_data
		 *
		 * - Add/Remove bulk actions for "cf7sa_data" CPT
		 *
		 * @method filter__bulk_actions_edit_cf7sa_data
		 *
		 * @param  array $actions
		 *
		 * @return array
		 */
		function filter__bulk_actions_edit_cf7sa_data( $actions ) {
			unset( $actions['edit'] );
			return $actions;
		}


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
		 * Adding Stripe fields in Stripe tab
		 *
		 * @param $cf7
		 */
		public function wpcf7_admin_after_additional_settings( $cf7 ) {

			wp_enqueue_script( CF7SA_PREFIX . '_admin_js' );

			require_once( CF7SA_DIR . '/inc/admin/template/' . CF7SA_PREFIX . '.template.php' );

		}
		 /**
        * add documentation link in plugins
        */

        function filter__admin_plugin_links( $links, $file ) {
            if ( $file != CF7SA_PLUGIN_BASENAME ) {
                return $links;
            }
        
            if ( ! current_user_can( 'wpcf7_read_contact_forms' ) ) {
                return $links;
            }
			// Add your donation link
			$documentLink = '<a target="_blank" href="https://store.zealousweb.com/accept-stripe-payments-using-contact-form-7-pro">' . __( 'Document Link', 'accept-stripe-payments-using-contact-form-7' ) . '</a>';
			$donateLink = '<a target="_blank" href="http://www.zealousweb.com/payment/">' . __( 'Donate', 'accept-stripe-payments-using-contact-form-7' ) . '</a>';
            array_unshift( $links ,$documentLink,$donateLink);
        
            return $links;
        }

	}

}
