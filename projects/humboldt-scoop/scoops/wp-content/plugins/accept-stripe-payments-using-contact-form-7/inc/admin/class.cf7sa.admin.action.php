<?php
/**
 * CF7SA_Admin_Action Class
 *
 * Handles the admin functionality.
 *
 * @package WordPress
 * @subpackage Contact Form 7 - Stripe Add-on
 * @since 1.0
 */

// Exit if accessed directly
if ( !defined( 'ABSPATH' ) ) exit;

if ( !class_exists( 'CF7SA_Admin_Action' ) ){

	/**
	 *  The CF7SA_Admin_Action Class
	 */
	class CF7SA_Admin_Action {

		function __construct()  {

			add_action( 'init',           array( $this, 'action__init' ) );
			add_action( 'init',           array( $this, 'action__init_99' ), 99 );
			add_action( 'add_meta_boxes', array( $this, 'action__add_meta_boxes' ) );

			// Save settings of contact form 7 admin
			add_action( 'wpcf7_save_contact_form',            array( $this, 'action__wpcf7_save_contact_form' ), 20, 2 );

			add_action( 'manage_cf7sa_data_posts_custom_column', array( $this, 'action__manage_cf7sa_data_posts_custom_column' ), 10, 2 );

			add_action( 'pre_get_posts',         array( $this, 'action__pre_get_posts' ) );
			add_action( 'restrict_manage_posts', array( $this, 'action__restrict_manage_posts' ) );
			add_action( 'parse_query',           array( $this, 'action__parse_query' ) );
            add_action( CF7SA_PREFIX . '/postbox', array( $this, 'action__acf7sa_postbox' ) );			

		}

		/*
		   ###     ######  ######## ####  #######  ##    ##  ######
		  ## ##   ##    ##    ##     ##  ##     ## ###   ## ##    ##
		 ##   ##  ##          ##     ##  ##     ## ####  ## ##
		##     ## ##          ##     ##  ##     ## ## ## ##  ######
		######### ##          ##     ##  ##     ## ##  ####       ##
		##     ## ##    ##    ##     ##  ##     ## ##   ### ##    ##
		##     ##  ######     ##    ####  #######  ##    ##  ######
		*/

		/**
		 * Action: init
		 *
		 * - Register neccessary assets for backend.
		 *
		 * @method action__init
		 */
		function action__init() {
			wp_register_style( CF7SA_PREFIX . '_admin_css', CF7SA_URL . 'assets/css/admin.min.css', array(), CF7SA_VERSION );
			wp_register_script( CF7SA_PREFIX . '_admin_js', CF7SA_URL . 'assets/js/admin.min.js', array( 'jquery-core' ), CF7SA_VERSION, true );

			wp_register_style( 'select2', CF7SA_URL . 'assets/css/select2.min.css', array(), '4.0.7' );
			wp_register_script( 'select2', CF7SA_URL . 'assets/js/select2.min.js', array( 'jquery-core' ), '4.0.7', true );

			if(!get_option('_exceed_cfsazw_l')){
				add_option('_exceed_cfsazw_l', 'cfsazw10');
			}
		}

		/**
		 * Action: init 99
		 *
		 * - Used to perform the CSV export functionality.
		 *
		 */
		function action__init_99() {
			if (
				isset( $_REQUEST['cf7sa_export_csv'] )
				&& isset( $_REQUEST['form-id'] )
				&& !empty( $_REQUEST['form-id'] )
			) {
				// Security: Verify user has permission to read contact forms and export data
				if ( ! current_user_can( 'wpcf7_read_contact_forms' ) ) {
					wp_die( esc_html__( 'You do not have permission to export data.', 'accept-stripe-payments-using-contact-form-7' ) );
				}

				// Security: Verify admin referer for CSRF protection
				check_admin_referer( 'bulk-posts' );

				$form_id = sanitize_text_field( wp_unslash( $_REQUEST['form-id'] ) );

				if ( 'all' == $form_id ) {
					add_action( 'admin_notices', array( $this, 'action__admin_notices_export' ) );
					return;
				}

				$args = array(
					'post_type' => 'cf7sa_data',
					'posts_per_page' => -1,
					'post_status' => 'publish',
					'order'          => 'ASC',  // ASC for descending order
				);

				$exported_data = get_posts( $args );

				if ( empty( $exported_data ) )
					return;

				/** CSV Export **/
				$filename = 'cf7sa-' . $form_id . '-' . time() . '.csv';

				$header_row = array(
					'_form_id'            => 'Form ID/Name',
					'_email'              => 'Email Address',
					'_transaction_id'     => 'Transaction ID',
					'_invoice_no'         => 'Invoice ID',
					'_amount'             => 'Amount',
					'_quantity'           => 'Quantity',
					'_total'              => 'Total',
					'_currency'           => 'Currency code',
					'_submit_time'        => 'Submit Time',
					'_request_Ip'         => 'Request IP',
					'_transaction_status' => 'Transaction status'
				);

				$data_rows = array();
				$special_row_cf7sa = false;
				if ( !empty( $exported_data ) ) {
					foreach ( $exported_data as $entry ) {

						$row = array();

						if ( !empty( $header_row ) ) {
							foreach ( $header_row as $key => $value ) {

								if (
									   $key != '_transaction_status'
									&& $key != '_submit_time'
								) {

									$row[$key] = (
										(
											'_form_id' == $key
											&& !empty( get_the_title( get_post_meta( $entry->ID, $key, true ) ) )
										)
										? get_the_title( get_post_meta( $entry->ID, $key, true ) )
										: get_post_meta( $entry->ID, $key, true )
									);

								} else if ( $key == '_transaction_status' ) {

									$row[$key] = get_post_meta( $entry->ID , $key, true );

								} else if ( '_submit_time' == $key ) {
									$row[$key] = get_the_date( 'd, M Y H:i:s', $entry->ID );
								}
							}
						}

						/* form_data */
						// Security: Use maybe_unserialize to safely handle serialized data
						$data = maybe_unserialize( get_post_meta( $entry->ID, '_form_data', true ) );
						$hide_data = apply_filters( CF7SA_PREFIX . '/hide-display', array( '_wpcf7', '_wpcf7_version', '_wpcf7_locale', '_wpcf7_unit_tag', '_wpcf7_container_post' ) );
						foreach ( $hide_data as $key => $value ) {
							if ( array_key_exists( $value, $data ) ) {
								unset( $data[$value] );
							}
						}

						// Check for _exceed_num_cfsazw and handle it
						if (array_key_exists('_exceed_num_cfsazw', $data) && !$special_row_cf7sa) {
							$special_row = array_fill_keys(array_keys($header_row), '');
							$special_row['_transaction_id'] = "To unlock more export data, consider upgrading to PRO. Visit: " . esc_url(CFSAZW_PRODUCT);
							$data_rows[] = $special_row;
							
							// Set the flag to true to prevent adding the special row again
							$special_row_cf7sa = true;
							// Skip adding other data for this entry
							break;
						}

						if ( !empty( $data ) ) {
							foreach ( $data as $key => $value ) {
								if ( strpos( $key, 'stripe-' ) === false ) {

									if ( !in_array( $key, $header_row ) ) {
										$header_row[$key] = $key;
									}

									$row[$key] = is_array( $value ) ? implode( ', ', $value ) : $value;

								}
							}
						}

						$data_rows[] = $row;

					}
				}

				ob_start();

				$fh = @fopen( 'php://output', 'w' );
				fprintf( $fh, chr(0xEF) . chr(0xBB) . chr(0xBF) );
				header( 'Cache-Control: must-revalidate, post-check=0, pre-check=0' );
				header( 'Content-Description: File Transfer' );
				header( 'Content-type: text/csv' );
				header( "Content-Disposition: attachment; filename={$filename}" );
				header( 'Expires: 0' );
				header( 'Pragma: public' );
				fputcsv( $fh, $header_row ); // phpcs:ignore WordPress.WP.AlternativeFunctions.file_system_operations_fputcsv -- Writing to php://output stream
				foreach ( $data_rows as $data_row ) {
					fputcsv( $fh, $data_row ); // phpcs:ignore WordPress.WP.AlternativeFunctions.file_system_operations_fputcsv -- Writing to php://output stream
				}
				fclose( $fh ); // phpcs:ignore WordPress.WP.AlternativeFunctions.file_system_operations_fclose -- Closing php://output stream

				ob_end_flush();
				die();

			}
		}

		/**
		 * Action: add_meta_boxes
		 *
		 * - Add mes boxes for the CPT "cf7sa_data"
		 */
		function action__add_meta_boxes() {
			add_meta_box( 'cfsa-data', __( 'From Data', 'accept-stripe-payments-using-contact-form-7' ), array( $this, 'cfsa_show_from_data' ), 'cf7sa_data', 'normal', 'high' );
			add_meta_box( 'cfsa-help', __( 'Do you need help for configuration?', 'accept-stripe-payments-using-contact-form-7' ), array( $this, 'cfsa_show_help_data' ), 'cf7sa_data', 'side', 'high' );
		}

		/**
		 * Action: wpcf7_save_contact_form
		 *
		 * - Save setting fields data.
		 *
		 * @param object $WPCF7_form
		 */
		public function action__wpcf7_save_contact_form( $WPCF7_form ) {

			// Security: Verify user has permission to edit contact forms
			if ( ! current_user_can( 'wpcf7_edit_contact_form' ) ) {
				return;
			}

			$wpcf7 = WPCF7_ContactForm::get_current();

			if ( !empty( $wpcf7 ) ) {
				$post_id = $wpcf7->id;
			}

			// Checkbox fields - these need special handling since unchecked checkboxes don't send data
			$checkbox_fields = array(
				CF7SA_META_PREFIX . 'use_stripe',
				CF7SA_META_PREFIX . 'debug',
				CF7SA_META_PREFIX . 'enable_test_mode',
				CF7SA_META_PREFIX . 'enable_postal_code',
				CF7SA_META_PREFIX . 'customer_details',
			);

			// Text/select fields
			$form_fields = array(
				CF7SA_META_PREFIX . 'test_publishable_key',
				CF7SA_META_PREFIX . 'test_secret_key',
				CF7SA_META_PREFIX . 'live_publishable_key',
				CF7SA_META_PREFIX . 'live_secret_key',
				CF7SA_META_PREFIX . 'webhook_secret', // Security: For webhook signature verification
				CF7SA_META_PREFIX . 'amount',
				CF7SA_META_PREFIX . 'quantity',
				CF7SA_META_PREFIX . 'email',
				CF7SA_META_PREFIX . 'description',
				CF7SA_META_PREFIX . 'currency',
				CF7SA_META_PREFIX . 'success_returnurl',
				CF7SA_META_PREFIX . 'cancel_returnurl',
				CF7SA_META_PREFIX . 'payment-success-msg',

				// Customer Details fields
				CF7SA_META_PREFIX . 'first_name',
				CF7SA_META_PREFIX . 'last_name',
				CF7SA_META_PREFIX . 'company_name',
				CF7SA_META_PREFIX . 'address',
				CF7SA_META_PREFIX . 'city',
				CF7SA_META_PREFIX . 'state',
				CF7SA_META_PREFIX . 'zip_code',
				CF7SA_META_PREFIX . 'country',
			);

			/**
			 * Save custom form setting fields
			 *
			 * @var array $form_fields
			 * @var array $checkbox_fields
			 */
			$form_fields = apply_filters( CF7SA_PREFIX . '/save_fields', $form_fields );
			$checkbox_fields = apply_filters( CF7SA_PREFIX . '/save_checkbox_fields', $checkbox_fields );

			if(!get_option('_exceed_cfsazw_l')){
				add_option('_exceed_cfsazw_l', 'cfsazw10');
			}

			// Note: Nonce verification is handled by Contact Form 7 before this hook fires
			// phpcs:disable WordPress.Security.NonceVerification.Recommended -- Nonce verified by CF7

			// Save checkbox fields - set to '1' if checked, '' if unchecked
			if ( ! empty( $checkbox_fields ) ) {
				foreach ( $checkbox_fields as $key ) {
					if ( isset( $_REQUEST[ $key ] ) ) {
						update_post_meta( $post_id, $key, '1' );
					} else {
						update_post_meta( $post_id, $key, '' );
					}
				}
			}

			// Save text/select fields
			if ( ! empty( $form_fields ) ) {
				foreach ( $form_fields as $key ) {
					if ( isset( $_REQUEST[ $key ] ) ) {
						$keyval = sanitize_text_field( wp_unslash( $_REQUEST[ $key ] ) );
						update_post_meta( $post_id, $key, $keyval );
					}
				}
			}

			// phpcs:enable WordPress.Security.NonceVerification.Recommended

		}

		/**
		 * Action: manage_cf7sa_data_posts_custom_column
		 *
		 * @method action__manage_cf7sa_data_posts_custom_column
		 *
		 * @param  string  $column
		 * @param  int     $post_id
		 *
		 * @return string
		 */
		function action__manage_cf7sa_data_posts_custom_column( $column, $post_id ) {
			$data_ct = $this->cfsazw_check_data_ct( sanitize_text_field( $post_id ) );
			switch ( $column ) {

				case 'form_id' :
					if( $data_ct ){
							echo '<a href="' . esc_url( CFSAZW_PRODUCT ) . '" target="_blank">' . esc_html__( 'To unlock more features consider upgrading to PRO.', 'accept-stripe-payments-using-contact-form-7' ) . '</a>';
					}else{
						$form_id_meta = get_post_meta( $post_id , '_form_id', true );
						if ( ! empty( $form_id_meta ) ) {
							$form_title = get_the_title( $form_id_meta );
							echo esc_html( ! empty( $form_title ) ? $form_title : $form_id_meta );
						}
					}					
				break;

				case 'transaction_status' :
					if( $data_ct ){
							echo '<a href="' . esc_url( CFSAZW_PRODUCT ) . '" target="_blank">' . esc_html__( 'To unlock more features consider upgrading to PRO.', 'accept-stripe-payments-using-contact-form-7' ) . '</a>';
					}else{
						$status = get_post_meta( $post_id , '_transaction_status', true );
						echo esc_html( ! empty( $status ) ? ucfirst( $status ) : '' );
					}
				break;

				case 'total' :
					if( $data_ct ){
							echo '<a href="' . esc_url( CFSAZW_PRODUCT ) . '" target="_blank">' . esc_html__( 'To unlock more features consider upgrading to PRO.', 'accept-stripe-payments-using-contact-form-7' ) . '</a>';
					}else{
						$total = get_post_meta( $post_id , '_total', true );
						$currency = get_post_meta( $post_id , '_currency', true );
						echo esc_html( ( ! empty( $total ) ? $total : '' ) . ' ' . ( ! empty( $currency ) ? strtoupper( $currency ) : '' ) );
					}
				break;

			}
		}

		/**
		 * Action: pre_get_posts
		 *
		 * - Used to perform order by into CPT List.
		 *
		 * @method action__pre_get_posts
		 *
		 * @param  object $query WP_Query
		 */
		function action__pre_get_posts( $query ) {

			if (
				! is_admin()
				|| !in_array ( $query->get( 'post_type' ), array( 'cf7sa_data' ) )
			)
				return;

			$orderby = $query->get( 'orderby' );

			if ( '_transaction_status' == $orderby ) {
				$query->set( 'meta_key', '_transaction_status' );
				$query->set( 'orderby', 'meta_value_num' );
			}

			if ( '_form_id' == $orderby ) {
				$query->set( 'meta_key', '_form_id' );
				$query->set( 'orderby', 'meta_value_num' );
			}

			if ( '_total' == $orderby ) {
				$query->set( 'meta_key', '_total' );
				$query->set( 'orderby', 'meta_value_num' );
			}
		}

		/**
		 * Action: restrict_manage_posts
		 *
		 * - Used to creat filter by form and export functionality.
		 *
		 * @method action__restrict_manage_posts
		 *
		 * @param  string $post_type
		 */
		function action__restrict_manage_posts( $post_type ) {

			if ( 'cf7sa_data' != $post_type ) {
				return;
			}

			$posts = get_posts(
				array(
					'post_type'        => 'wpcf7_contact_form',
					'post_status'      => 'publish',
					'suppress_filters' => false,
					'posts_per_page'   => -1
				)
			);

			if ( empty( $posts ) ) {
				return;
			}

			// phpcs:ignore WordPress.Security.NonceVerification.Recommended -- This is a filter dropdown, no data modification
			$selected = ( isset( $_GET['form-id'] ) ? sanitize_text_field( wp_unslash( $_GET['form-id'] ) ) : '' );

			echo '<select name="form-id" id="form-id">';
			echo '<option value="all">' . esc_html__( 'All Forms', 'accept-stripe-payments-using-contact-form-7' ) . '</option>';
			foreach ( $posts as $post ) {
				echo '<option value="' . esc_attr( $post->ID ) . '" ' . selected( $selected, $post->ID, false ) . '>' . esc_html($post->post_title) . '</option>';
			}
			echo '</select>';

			echo '<input type="submit" id="cf7sa_export_csv" name="cf7sa_export_csv" class="button action" value="' . esc_attr__( 'Export CSV', 'accept-stripe-payments-using-contact-form-7' ) . '"> ';

		}

		/**
		 * Action: parse_query
		 *
		 * - Filter data by form id.
		 *
		 * @method action__parse_query
		 *
		 * @param  object $query WP_Query
		 */
		function action__parse_query( $query ) {
			if (
				! is_admin()
				|| !in_array ( $query->get( 'post_type' ), array( 'cf7sa_data' ) )
			)
				return;

			// phpcs:disable WordPress.Security.NonceVerification.Recommended -- This is a filter query, no data modification
			if (
				is_admin()
				&& isset( $_GET['form-id'] )
				&& 'all' != sanitize_text_field( wp_unslash( $_GET['form-id'] ) )
			) {
				// phpcs:disable WordPress.DB.SlowDBQuery.slow_db_query_meta_key, WordPress.DB.SlowDBQuery.slow_db_query_meta_value -- Required for filtering by form ID
				$query->query_vars['meta_key']     = '_form_id';
				$query->query_vars['meta_value']   = sanitize_text_field( wp_unslash( $_GET['form-id'] ) );
				$query->query_vars['meta_compare'] = '=';
				// phpcs:enable WordPress.DB.SlowDBQuery.slow_db_query_meta_key, WordPress.DB.SlowDBQuery.slow_db_query_meta_value
			} elseif ( isset( $_GET['form-id'] ) && 'all' == sanitize_text_field( wp_unslash( $_GET['form-id'] ) ) && ! isset( $_REQUEST['cf7sa_export_csv'] ) ) {
				add_action( 'admin_notices', array( $this, 'action__admin_notices_export_not_found' ) );
				return;
			}
			// phpcs:enable WordPress.Security.NonceVerification.Recommended

		}

		/**
		 * Action: admin_notices
		 *
		 * - Added use notice when trying to export without selecting the form.
		 *
		 * @method action__admin_notices_export
		 */
		function action__admin_notices_export() {
			echo '<div class="error">' .
				'<p>' .
					esc_html__( 'Please select Form to export.', 'accept-stripe-payments-using-contact-form-7' ) .
				'</p>' .
			'</div>';
		}

		/**
		 * Action: admin_notices
		 *
		 * - Added use notice when trying to export without selecting the form.
		 *
		 * @method action__admin_notices_export_not_found
		 */
		function action__admin_notices_export_not_found() {
			echo '<div class="error">' .
				'<p>' .
				esc_html__( 'Please Select to Form.', 'accept-stripe-payments-using-contact-form-7' ) .
				'</p>' .
			'</div>';
		}

		/**
		 * Action: CF7SA_PREFIX /postbox
		 *
		 * - Added metabox for the setting fields in backend.
		 *
		 * @method action__acf7sa_postbox
		 */
		function action__acf7sa_postbox() {

			echo '<div id="configuration-help" class="postbox">' .
				wp_kses_post(
					apply_filters(
						CF7SA_PREFIX . '/help/postbox',
						'<h3>' . esc_html__( 'Do you need help for configuration?', 'accept-stripe-payments-using-contact-form-7' ) . '</h3>' .
						'<p></p>' .
						'<ol>' .
							'<li><a href="https://store.zealousweb.com/accept-stripe-payments-using-contact-form-7-pro" target="_blank">' . esc_html__( 'Refer the document.', 'accept-stripe-payments-using-contact-form-7' ) . '</a></li>' .
							'<li><a href="https://www.zealousweb.com/contact/" target="_blank">' . esc_html__( 'Contact Us', 'accept-stripe-payments-using-contact-form-7' ) . '</a></li>' .
							'<li><a href="mailto:support@zealousweb.com">' . esc_html__( 'Email us', 'accept-stripe-payments-using-contact-form-7' ) . '</a></li>' .
						'</ol>'
					)
				) .
			'</div>';
		}


		// define the wp_print_footer_scripts callback



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
		 * - Used to display the form data in CPT detail page.
		 *
		 * @method cfsa_show_from_data
		 *
		 * @param  object $post WP_Post
		 */
		function cfsa_show_from_data( $post ) {

			$fields = CF7SA()->lib->data_fields;

			$form_id = get_post_meta( $post->ID, '_form_id', true );
			$data_ct = $this->cfsazw_check_data_ct( sanitize_text_field( $post->ID ) );
			

			echo '<table class="cf7sa-box-data form-table">' .
				'<style>.inside-field td, .inside-field th{ padding-top: 5px; padding-bottom: 5px;} .postbox table.form-table{ word-break: break-all; }</style>';

				if ( !empty( $fields ) ) {

					if( $data_ct ){

						echo'<tr class="inside-field"><th scope="row">You are using Accept Stripe Payments Using Contact Form 7 - no license needed. Enjoy! 🙂</th></tr>';
							echo'<tr class="inside-field"><th scope="row"><a href="https://store.zealousweb.com/accept-stripe-payments-using-contact-form-7-pro" target="_blank">To unlock more features consider upgrading to PRO.</a></th></tr>';

					}else{

						if ( array_key_exists( '_transaction_response', $fields ) && empty( get_post_meta( $form_id, CF7SA_META_PREFIX . 'debug', true ) ) ) {
							unset( $fields['_transaction_response'] );
						}

						// Security: Use maybe_unserialize to safely handle serialized data
						$attachment = ( !empty( get_post_meta( $post->ID, '_attachment', true ) ) ? maybe_unserialize( get_post_meta( $post->ID, '_attachment', true ) ) : '' );
						$root_path = get_home_path();

						foreach ( $fields as $key => $value ) {

							if (
								!empty( get_post_meta( $post->ID, $key, true ) )
								&& $key != '_form_data'
								&& $key != '_transaction_response'
								&& $key != '_transaction_status'
							) {

								$val = get_post_meta( $post->ID, $key, true );

								echo '<tr class="form-field">' .
									'<th scope="row">' .
										'<label for="hcf_author">' . esc_html( $value ) . '</label>' .
									'</th>' .
									'<td>' .
										esc_html(
											(
												'_form_id' == $key
												&& !empty( get_the_title( get_post_meta( $post->ID, $key, true ) ) )
											)
											? get_the_title( get_post_meta( $post->ID, $key, true ) )
											: get_post_meta( $post->ID, $key, true )
										) .
									'</td>' .
								'</tr>';

							} else if (
								!empty( get_post_meta( $post->ID, $key, true ) )
								&& $key == '_transaction_status'
							) {

								echo '<tr class="form-field">' .
									'<th scope="row">' .
										'<label for="hcf_author">' . esc_html( $value ) . '</label>' .
									'</th>' .
									'<td>' .
										esc_html( ucfirst( get_post_meta( $post->ID , $key, true ) ) ) .
									'</td>' .
								'</tr>';

							} else if (
								!empty( get_post_meta( $post->ID, $key, true ) )
								&& $key == '_form_data'
							) {

								echo '<tr class="form-field">' .
									'<th scope="row">' .
										'<label for="hcf_author">' . esc_html( $value ) . '</label>' .
									'</th>' .
									'<td>' .
										'<table>';

											// Security: Use maybe_unserialize to safely handle serialized data
											$data = maybe_unserialize( get_post_meta( $post->ID, $key, true ) );
											$hide_data = apply_filters( CF7SA_PREFIX . '/hide-display', array( '_wpcf7', '_wpcf7_version', '_wpcf7_locale', '_wpcf7_unit_tag', '_wpcf7_container_post' ) );
											foreach ( $hide_data as $key => $value ) {
												if ( array_key_exists( $value, $data ) ) {
													unset( $data[$value] );
												}
											}

											if ( !empty( $data ) ) {
												foreach ( $data as $key => $value ) {
													if ( strpos( $key, 'stripe-' ) === false ) {
														echo '<tr class="inside-field">' .
															'<th scope="row">' .
																esc_html( $key ) .
															'</th>' .
															'<td>' .
																(
																	(
																		!empty( $attachment )
																		&& array_key_exists( $key, $attachment )
																	)
																	? '<a href="' . esc_url( home_url( str_replace( $root_path, '/', $attachment[$key] ) ) ) . '" target="_blank" download>' . esc_html( $value ) . '</a>'
																	: esc_html( is_array( $value ) ? implode( ', ', $value ) : $value )
																) .
															'</td>' .
														'</tr>';
													}
												}
											}

										echo '</table>' .
									'</td>
								</tr>';

							} else if (
								!empty( get_post_meta( $post->ID, $key, true ) )
								&& $key == '_transaction_response'
							) {

								echo '<tr class="form-field">' .
									'<th scope="row">' .
										'<label for="hcf_author">' . esc_html( $value ) . '</label>' .
									'</th>' .
									'<td>' .
										'<code style="word-break: break-all;">' .
											esc_html( get_post_meta( $post->ID , $key, true ) ) .
										'</code>' .
									'</td>' .
								'</tr>';

							}


						}

					}

					
				}

			echo '</table>';
		}

		/**
		* check data ct
		*/
		function cfsazw_check_data_ct( $post_id ){
			// Security: Use maybe_unserialize to safely handle serialized data
			$data = maybe_unserialize( get_post_meta( $post_id, '_form_data', true ) );			
			if( !empty( get_post_meta( $post_id, '_form_data', true ) ) && is_array( $data ) && isset( $data['_exceed_num_cfsazw'] ) && !empty( $data['_exceed_num_cfsazw'] ) ){
				return $data['_exceed_num_cfsazw'];
			}else{
				return '';
			}

		}

		/**
		 * - Used to add meta box in CPT detail page.
		 */
		function cfsa_show_help_data() {
			echo '<div id="cf7sa-data-help">' .
				wp_kses_post(
					apply_filters(
						CF7SA_PREFIX . '/help/cf7sa_data/postbox',
						'<ol>' .
							'<li><a href="https://store.zealousweb.com/accept-stripe-payments-using-contact-form-7-pro" target="_blank">' . esc_html__( 'Refer the document.', 'accept-stripe-payments-using-contact-form-7' ) . '</a></li>' .
							'<li><a href="https://www.zealousweb.com/contact/" target="_blank">' . esc_html__( 'Contact Us', 'accept-stripe-payments-using-contact-form-7' ) . '</a></li>' .
							'<li><a href="mailto:support@zealousweb.com">' . esc_html__( 'Email us', 'accept-stripe-payments-using-contact-form-7' ) . '</a></li>' .
						'</ol>'
					)
				) .
			'</div>';
		}
	}
}
