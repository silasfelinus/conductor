<?php
// phpcs:disable WordPress.NamingConventions.PrefixAllGlobals.NonPrefixedVariableFound -- Template variables are scoped to inclusion context, not truly global
// phpcs:ignore WordPress.Security.NonceVerification.Recommended -- This template is loaded within CF7 admin which handles nonce verification
$post_id = ( isset( $_REQUEST[ 'post' ] ) ? sanitize_text_field( wp_unslash( $_REQUEST[ 'post' ] ) ) : '' );

	if ( empty( $post_id ) ) {
		$wpcf7 = WPCF7_ContactForm::get_current();
		$post_id = $wpcf7->id();
	}

	if ( !function_exists( 'cf7sa_inlineScript_select2' ) ) {
		function cf7sa_inlineScript_select2() {
			ob_start();
			?>
			( function($) {
				jQuery('#cf7sa_currency, #cf7sa_success_returnurl, #cf7sa_cancel_returnurl' ).select2();
			} )( jQuery );
			<?php
			return ob_get_clean();
		}
	}

	wp_enqueue_style( 'wp-pointer' );
	wp_enqueue_script( 'wp-pointer' );

	wp_enqueue_style( 'select2' );
	wp_enqueue_script( 'select2' );
	wp_add_inline_script( 'select2', cf7sa_inlineScript_select2() );

	wp_enqueue_style( CF7SA_PREFIX . '_admin_css' );

	$use_stripe              = get_post_meta( $post_id, CF7SA_META_PREFIX . 'use_stripe', true );
	$debug_stripe            = get_post_meta( $post_id, CF7SA_META_PREFIX . 'debug', true );
	$enable_test_mode        = get_post_meta( $post_id, CF7SA_META_PREFIX . 'enable_test_mode', true );
	$test_publishable_key    = get_post_meta( $post_id, CF7SA_META_PREFIX . 'test_publishable_key', true );
	$test_secret_key         = get_post_meta( $post_id, CF7SA_META_PREFIX . 'test_secret_key', true );
	$live_publishable_key    = get_post_meta( $post_id, CF7SA_META_PREFIX . 'live_publishable_key', true );
	$live_secret_key         = get_post_meta( $post_id, CF7SA_META_PREFIX . 'live_secret_key', true );
	$webhook_secret          = get_post_meta( $post_id, CF7SA_META_PREFIX . 'webhook_secret', true );
	$amount                  = get_post_meta( $post_id, CF7SA_META_PREFIX . 'amount', true );
	$quantity                = get_post_meta( $post_id, CF7SA_META_PREFIX . 'quantity', true );
	$email                   = get_post_meta( $post_id, CF7SA_META_PREFIX . 'email', true );
	$description             = get_post_meta( $post_id, CF7SA_META_PREFIX . 'description', true );
	$success_returnURL       = get_post_meta( $post_id, CF7SA_META_PREFIX . 'success_returnurl', true );
	$cancel_returnURL        = get_post_meta( $post_id, CF7SA_META_PREFIX . 'cancel_returnurl', true );
	$message                 = get_post_meta( $post_id, CF7SA_META_PREFIX . 'message', true );
	$currency                = get_post_meta( $post_id, CF7SA_META_PREFIX . 'currency', true );
	$customer_details        = get_post_meta( $post_id, CF7SA_META_PREFIX . 'customer_details', true );
	$first_name              = get_post_meta( $post_id, CF7SA_META_PREFIX . 'first_name', true );
	$last_name               = get_post_meta( $post_id, CF7SA_META_PREFIX . 'last_name', true );
	$company_name            = get_post_meta( $post_id, CF7SA_META_PREFIX . 'company_name', true );
	$address                 = get_post_meta( $post_id, CF7SA_META_PREFIX . 'address', true );
	$city                    = get_post_meta( $post_id, CF7SA_META_PREFIX . 'city', true );
	$state                   = get_post_meta( $post_id, CF7SA_META_PREFIX . 'state', true );
	$zip_code                = get_post_meta( $post_id, CF7SA_META_PREFIX . 'zip_code', true );
	$country                 = get_post_meta( $post_id, CF7SA_META_PREFIX . 'country', true );
	$enable_postal_code      = get_post_meta( $post_id, CF7SA_META_PREFIX . 'enable_postal_code', true );
	$payment_success_msg     = get_post_meta( $post_id, CF7SA_META_PREFIX . 'payment-success-msg', true );

	$currency_code = array(
		'AUD' => 'Australian Dollar',
		'BRL' => 'Brazilian Real',
		'CAD' => 'Canadian Dollar',
		'CHF' => 'Swiss Franc',
		'DKK' => 'Danish Krone',
		'EUR' => 'Euro',
		'GBP' => 'Pound Sterling',
		'HKD' => 'Hong Kong Dollar',
		'INR' => 'Indian Rupee',
		'JPY' => 'Japanese Yen',
		'MXN' => 'Mexican Peso',
		'MYR' => 'Malaysian Ringgit',
		'NOK' => 'Norwegian Krone',
		'NZD' => 'New Zealand Dollar',
		'SEK' => 'Swedish Krona',
		'SGD' => 'Singapore Dollar',
		'USD' => 'U.S. Dollar'
	);

	$selected = '';

	$args = array(
			'post_type'      => array( 'page' ),
			'orderby'        => 'title',
			'posts_per_page' => -1
	);

	$pages = get_posts( $args );
	$all_pages = array();

	if ( !empty( $pages ) ) {
		foreach ( $pages as $page ) {
			$all_pages[$page->ID] = $page->post_title;
		}
	}
?>
<div class="cf7sa-settings">
	<div class="left-box postbox">
		<input style="display: none;" id="<?php echo esc_attr( CF7SA_META_PREFIX . 'customer_details' ); ?>" name="<?php echo esc_attr( CF7SA_META_PREFIX . 'customer_details' ); ?>" type="checkbox" value="1" <?php checked( $customer_details, 1 ); ?> />
		<table class="form-table">
			<tbody>
				<tr class="form-field">
					<th scope="row">
						<label for="<?php echo esc_attr( CF7SA_META_PREFIX . 'use_stripe' ); ?>">
							<?php esc_html_e( 'Enable Stripe Payment Form', 'accept-stripe-payments-using-contact-form-7' ); ?>
						</label>
					</th>
					<td>
						<input id="<?php echo esc_attr( CF7SA_META_PREFIX . 'use_stripe' ); ?>" name="<?php echo esc_attr( CF7SA_META_PREFIX . 'use_stripe' ); ?>" type="checkbox" class="enable_required" value="1" <?php checked( $use_stripe, 1 ); ?>/>
					</td>
				</tr>
				<tr class="form-field">
					<th scope="row">
						<label for="<?php echo esc_attr( CF7SA_META_PREFIX . 'debug' ); ?>">
							<?php esc_html_e( 'Enable Debug Mode', 'accept-stripe-payments-using-contact-form-7' ); ?>
						</label>
					</th>
					<td>
						<input id="<?php echo esc_attr( CF7SA_META_PREFIX . 'debug' ); ?>" name="<?php echo esc_attr( CF7SA_META_PREFIX . 'debug' ); ?>" type="checkbox" value="1" <?php checked( $debug_stripe, 1 ); ?>/>
					</td>
				</tr>
				<tr class="form-field">
					<th scope="row">
						<label for="<?php echo esc_attr( CF7SA_META_PREFIX . 'enable_test_mode' ); ?>">
							<?php esc_html_e( 'Enable Test Mode', 'accept-stripe-payments-using-contact-form-7' ); ?>
						</label>
					</th>
					<td>
						<input id="<?php echo esc_attr( CF7SA_META_PREFIX . 'enable_test_mode' ); ?>" name="<?php echo esc_attr( CF7SA_META_PREFIX . 'enable_test_mode' ); ?>" type="checkbox" class="enable_required" value="1" <?php checked( $enable_test_mode, 1 ); ?>/>
					</td>
				</tr>
				<tr class="form-field">
					<th>
						<label for="<?php echo esc_attr( CF7SA_META_PREFIX . 'test_publishable_key' ); ?>">
							<?php esc_html_e( 'Test Publishable key (Required)', 'accept-stripe-payments-using-contact-form-7' ); ?>
						</label>
						<span class="cf7sa-tooltip hide-if-no-js" id="cf7sa-test-publishable-key"></span>
					</th>
					<td>
						<input id="<?php echo esc_attr( CF7SA_META_PREFIX . 'test_publishable_key' ); ?>" name="<?php echo esc_attr( CF7SA_META_PREFIX . 'test_publishable_key' ); ?>" type="text" class="large-text cf7sa_cus_css" value="<?php echo esc_attr( $test_publishable_key ); ?>" <?php echo ( ( !empty( $enable_test_mode ) && !empty( $use_stripe ) ) ? 'required' : '' ); ?> />
					</td>
				</tr>
				<tr class="form-field">
					<th>
						<label for="<?php echo esc_attr( CF7SA_META_PREFIX . 'test_secret_key' ); ?>">
							<?php esc_html_e( 'Test Secret key (Required)', 'accept-stripe-payments-using-contact-form-7' ); ?>
						</label>
						<span class="cf7sa-tooltip hide-if-no-js" id="cf7sa-test-secret-key"></span>
					</th>
					<td>
						<input id="<?php echo esc_attr( CF7SA_META_PREFIX . 'test_secret_key' ); ?>" name="<?php echo esc_attr( CF7SA_META_PREFIX . 'test_secret_key' ); ?>" type="text" class="large-text cf7sa_cus_css" value="<?php echo esc_attr( $test_secret_key ); ?>" <?php echo ( ( !empty( $enable_test_mode ) && !empty( $use_stripe ) ) ? 'required' : '' ); ?> />
					</td>
				</tr>
				<tr class="form-field">
					<th>
						<label for="<?php echo esc_attr( CF7SA_META_PREFIX . 'live_publishable_key' ); ?>">
							<?php esc_html_e( 'Live Publishable key (Required)', 'accept-stripe-payments-using-contact-form-7' ); ?>
						</label>
						<span class="cf7sa-tooltip hide-if-no-js" id="cf7sa-live-publishable-key"></span>
					</th>
					<td>
						<input id="<?php echo esc_attr( CF7SA_META_PREFIX . 'live_publishable_key' ); ?>" name="<?php echo esc_attr( CF7SA_META_PREFIX . 'live_publishable_key' ); ?>" type="text" class="large-text cf7sa_cus_css" value="<?php echo esc_attr( $live_publishable_key ); ?>" <?php echo ( ( empty( $enable_test_mode ) && !empty( $use_stripe ) ) ? 'required' : '' ); ?> />
					</td>
				</tr>
				<tr class="form-field">
					<th>
						<label for="<?php echo esc_attr( CF7SA_META_PREFIX . 'live_secret_key' ); ?>">
							<?php esc_html_e( 'Live Secret key (Required)', 'accept-stripe-payments-using-contact-form-7' ); ?>
						</label>
						<span class="cf7sa-tooltip hide-if-no-js" id="cf7sa-live-secret-key"></span>
					</th>
					<td>
						<input id="<?php echo esc_attr( CF7SA_META_PREFIX . 'live_secret_key' ); ?>" name="<?php echo esc_attr( CF7SA_META_PREFIX . 'live_secret_key' ); ?>" type="text" class="large-text cf7sa_cus_css" value="<?php echo esc_attr( $live_secret_key ); ?>" <?php echo ( ( empty( $enable_test_mode ) && !empty( $use_stripe ) ) ? 'required' : '' ); ?> />
					</td>
				</tr>
				<tr class="form-field">
					<th>
						<label for="<?php echo esc_attr( CF7SA_META_PREFIX . 'email' ); ?>">
							<?php esc_html_e( 'Customer Email Field Name (Required)', 'accept-stripe-payments-using-contact-form-7' ); ?>
						</label>
					</th>
					<td>
						<input class="cf7sa_cus_css" id="<?php echo esc_attr( CF7SA_META_PREFIX . 'email' ); ?>" name="<?php echo esc_attr( CF7SA_META_PREFIX . 'email' ); ?>" type="text" value="<?php echo esc_attr( $email ); ?>" <?php echo ( !empty( $email ) ? 'required' : '' ); ?> />
					</td>
				</tr>
				<tr class="form-field">
					<th>
						<label for="<?php echo esc_attr( CF7SA_META_PREFIX . 'amount' ); ?>">
							<?php esc_html_e( 'Amount Field Name (Required)', 'accept-stripe-payments-using-contact-form-7' ); ?>
						</label>
						<span class="cf7sa-tooltip hide-if-no-js" id="cf7sa-amount-field"></span>
					</th>
					<td>
						<input class="cf7sa_cus_css" id="<?php echo esc_attr( CF7SA_META_PREFIX . 'amount' ); ?>" name="<?php echo esc_attr( CF7SA_META_PREFIX . 'amount' ); ?>" type="text" value="<?php echo esc_attr( $amount ); ?>" <?php echo ( !empty( $use_stripe ) ? 'required' : '' ); ?> />
					</td>
				</tr>
				<tr class="form-field">
					<th>
						<label for="<?php echo esc_attr( CF7SA_META_PREFIX . 'quantity' ); ?>">
							<?php esc_html_e( 'Quantity Field Name (Optional)', 'accept-stripe-payments-using-contact-form-7' ); ?>
						</label>
					</th>
					<td>
						<input class="cf7sa_cus_css" id="<?php echo esc_attr( CF7SA_META_PREFIX . 'quantity' ); ?>" name="<?php echo esc_attr( CF7SA_META_PREFIX . 'quantity' ); ?>" type="text" value="<?php echo esc_attr( $quantity ); ?>" />
					</td>
				</tr>
				<tr class="form-field">
					<th>
						<label for="<?php echo esc_attr( CF7SA_META_PREFIX . 'description' ); ?>">
							<?php esc_html_e( 'Description Field Name (Optional)', 'accept-stripe-payments-using-contact-form-7' ); ?>
						</label>
					</th>
					<td>
						<input class="cf7sa_cus_css" id="<?php echo esc_attr( CF7SA_META_PREFIX . 'description' ); ?>" name="<?php echo esc_attr( CF7SA_META_PREFIX . 'description' ); ?>" type="text" value="<?php echo esc_attr( $description ); ?>" />
					</td>
				</tr>
				<tr class="form-field">
					<th>
						<label for="<?php echo esc_attr( CF7SA_META_PREFIX . 'currency' ); ?>">
							<?php esc_html_e( 'Select Currency', 'accept-stripe-payments-using-contact-form-7' ); ?>
						</label>
						<span class="cf7sa-tooltip hide-if-no-js" id="cf7sa-select-currency"></span>
					</th>
					<td>
						<select id="<?php echo esc_attr( CF7SA_META_PREFIX . 'currency' ); ?>" name="<?php echo esc_attr( CF7SA_META_PREFIX . 'currency' ); ?>">
							<?php
							if ( !empty( $currency_code ) ) {
								foreach ( $currency_code as $key => $value ) {
									echo '<option value="' . esc_attr( $key ) . '" ' . selected( $currency, $key, false ) . '>' . esc_html( $value ) . '</option>';
								}
							}
							?>
						</select>
					</td>
				</tr>
				<tr class="form-field">
					<th>
						<label for="<?php echo esc_attr( CF7SA_META_PREFIX . 'success_returnurl' ); ?>">
							<?php esc_html_e( 'Success Return URL (Optional)', 'accept-stripe-payments-using-contact-form-7' ); ?>
						</label>
					</th>
					<td>
						<select id="<?php echo esc_attr( CF7SA_META_PREFIX . 'success_returnurl' ); ?>" name="<?php echo esc_attr( CF7SA_META_PREFIX . 'success_returnurl' ); ?>">
							<option><?php esc_html_e( 'Select page', 'accept-stripe-payments-using-contact-form-7' ); ?></option>
							<?php
							if( !empty( $all_pages ) ) {
								foreach ( $all_pages as $page_id => $title ) {
									echo '<option value="' . esc_attr( $page_id ) . '" ' . selected( $success_returnURL, $page_id, false ) . '>' . esc_html( $title ) . '</option>';
								}
							}
							?>
						</select>
					</td>
				</tr>
				<tr class="form-field">
					<th>
						<label for="<?php echo esc_attr( CF7SA_META_PREFIX . 'cancel_returnurl' ); ?>">
							<?php esc_html_e( 'Cancel Return URL (Optional)', 'accept-stripe-payments-using-contact-form-7' ); ?>
						</label>
					</th>
					<td>
						<select id="<?php echo esc_attr( CF7SA_META_PREFIX . 'cancel_returnurl' ); ?>" name="<?php echo esc_attr( CF7SA_META_PREFIX . 'cancel_returnurl' ); ?>">
							<option><?php esc_html_e( 'Select page', 'accept-stripe-payments-using-contact-form-7' ); ?></option>
							<?php
							if( !empty( $all_pages ) ) {
								foreach ( $all_pages as $page_id => $title ) {
									echo '<option value="' . esc_attr( $page_id ) . '" ' . selected( $cancel_returnURL, $page_id, false ) . '>' . esc_html( $title ) . '</option>';
								}
							}
							?>
						</select>
					</td>
				</tr>
				<tr class="form-field">
					<th scope="row">
						<label for="<?php echo esc_attr( CF7SA_META_PREFIX . 'enable_postal_code' ); ?>">
							<?php esc_html_e( 'Enable Postal Code field on the Card.', 'accept-stripe-payments-using-contact-form-7' ); ?>
						</label>
						<span class="cf7sa-tooltip hide-if-no-js" id="cf7sa-enable-postal-code"></span>
					</th>
					<td>
						<input id="<?php echo esc_attr( CF7SA_META_PREFIX . 'enable_postal_code' ); ?>" name="<?php echo esc_attr( CF7SA_META_PREFIX . 'enable_postal_code' ); ?>" type="checkbox" class="enable_required" value="1" <?php checked( $enable_postal_code, 1 ); ?>/>
					</td>
				</tr>
				<tr class="form-field">
					<th>
						<label for="<?php echo esc_attr( CF7SA_META_PREFIX . 'payment-success-msg' ); ?>">
							<?php esc_html_e( 'Payment Successful Message', 'accept-stripe-payments-using-contact-form-7' ); ?>
						</label>
						<span class="cf7sa-tooltip hide-if-no-js" id="cf7sa-payment-success-msg"></span>
					</th>
					<td>
						<textarea class="cf7sa_cus_css" id="<?php echo esc_attr( CF7SA_META_PREFIX . 'payment-success-msg' ); ?>" name="<?php echo esc_attr( CF7SA_META_PREFIX . 'payment-success-msg' ); ?>"><?php echo esc_textarea( $payment_success_msg ); ?></textarea>
					</td>
				</tr>
				<?php
				/**
				 * - Add new field at the middle.
				 *
				 * @var int $post_id
				 */
				do_action( CF7SA_PREFIX . '/add/fields/middle', $post_id );
				?>
				<tr class="form-field">
					<th colspan="2">
						<label for="<?php echo esc_attr( CF7SA_META_PREFIX . 'customer_details' ); ?>">
							<h3 style="margin: 0;">
								<?php esc_html_e( 'Customer Details', 'accept-stripe-payments-using-contact-form-7' ); ?>
								<span class="arrow-switch"></span>
							</h3>
						</label>
					</th>
				</tr>
				<tr class="form-field hide-show">
					<th>
						<label for="<?php echo esc_attr( CF7SA_META_PREFIX . 'first_name' ); ?>">
							<?php esc_html_e( 'First Name', 'accept-stripe-payments-using-contact-form-7' ); ?>
						</label>
					</th>
					<td>
						<input id="<?php echo esc_attr( CF7SA_META_PREFIX . 'first_name' ); ?>" name="<?php echo esc_attr( CF7SA_META_PREFIX . 'first_name' ); ?>" type="text" class="regular-text" value="<?php echo esc_attr( $first_name ); ?>" />
					</td>
				</tr>
				<tr class="form-field hide-show">
					<th>
						<label for="<?php echo esc_attr( CF7SA_META_PREFIX . 'last_name' ); ?>">
							<?php esc_html_e( 'Last Name', 'accept-stripe-payments-using-contact-form-7' ); ?>
						</label>
					</th>
					<td>
						<input id="<?php echo esc_attr( CF7SA_META_PREFIX . 'last_name' ); ?>" name="<?php echo esc_attr( CF7SA_META_PREFIX . 'last_name' ); ?>" type="text" class="regular-text" value="<?php echo esc_attr( $last_name ); ?>" />
					</td>
				</tr>
				<tr class="form-field hide-show">
					<th>
						<label for="<?php echo esc_attr( CF7SA_META_PREFIX . 'company_name' ); ?>">
							<?php esc_html_e( 'Company Name', 'accept-stripe-payments-using-contact-form-7' ); ?>
						</label>
					</th>
					<td>
						<input id="<?php echo esc_attr( CF7SA_META_PREFIX . 'company_name' ); ?>" name="<?php echo esc_attr( CF7SA_META_PREFIX . 'company_name' ); ?>" type="text" class="regular-text" value="<?php echo esc_attr( $company_name ); ?>" />
					</td>
				</tr>
				<tr class="form-field hide-show">
					<th>
						<label for="<?php echo esc_attr( CF7SA_META_PREFIX . 'address' ); ?>">
							<?php esc_html_e( 'Address', 'accept-stripe-payments-using-contact-form-7' ); ?>
						</label>
					</th>
					<td>
						<input id="<?php echo esc_attr( CF7SA_META_PREFIX . 'address' ); ?>" name="<?php echo esc_attr( CF7SA_META_PREFIX . 'address' ); ?>" type="text" class="regular-text" value="<?php echo esc_attr( $address ); ?>" />
					</td>
				</tr>
				<tr class="form-field hide-show">
					<th>
						<label for="<?php echo esc_attr( CF7SA_META_PREFIX . 'city' ); ?>">
							<?php esc_html_e( 'City', 'accept-stripe-payments-using-contact-form-7' ); ?>
						</label>
					</th>
					<td>
						<input id="<?php echo esc_attr( CF7SA_META_PREFIX . 'city' ); ?>" name="<?php echo esc_attr( CF7SA_META_PREFIX . 'city' ); ?>" type="text" class="regular-text" value="<?php echo esc_attr( $city ); ?>" />
					</td>
				</tr>
				<tr class="form-field hide-show">
					<th>
						<label for="<?php echo esc_attr( CF7SA_META_PREFIX . 'state' ); ?>">
							<?php esc_html_e( 'State', 'accept-stripe-payments-using-contact-form-7' ); ?>
						</label>
					</th>
					<td>
						<input id="<?php echo esc_attr( CF7SA_META_PREFIX . 'state' ); ?>" name="<?php echo esc_attr( CF7SA_META_PREFIX . 'state' ); ?>" type="text" class="regular-text" value="<?php echo esc_attr( $state ); ?>" />
					</td>
				</tr>
				<tr class="form-field hide-show">
					<th>
						<label for="<?php echo esc_attr( CF7SA_META_PREFIX . 'zip_code' ); ?>">
							<?php esc_html_e( 'Zip Code', 'accept-stripe-payments-using-contact-form-7' ); ?>
						</label>
					</th>
					<td>
						<input id="<?php echo esc_attr( CF7SA_META_PREFIX . 'zip_code' ); ?>" name="<?php echo esc_attr( CF7SA_META_PREFIX . 'zip_code' ); ?>" type="text" class="regular-text" value="<?php echo esc_attr( $zip_code ); ?>" />
					</td>
				</tr>
				<tr class="form-field hide-show">
					<th>
						<label for="<?php echo esc_attr( CF7SA_META_PREFIX . 'country' ); ?>">
							<?php esc_html_e( 'Country', 'accept-stripe-payments-using-contact-form-7' ); ?>
						</label>
					</th>
					<td>
						<input id="<?php echo esc_attr( CF7SA_META_PREFIX . 'country' ); ?>" name="<?php echo esc_attr( CF7SA_META_PREFIX . 'country' ); ?>" type="text" class="regular-text" value="<?php echo esc_attr( $country ); ?>" />
					</td>
				</tr>
				<?php
				/**
				 * - Add new field at the end.
				 *
				 * @var int $post_id
				 */
				do_action( CF7SA_PREFIX . '/add/fields/end', $post_id );
				?>
				<input type="hidden" name="post" value="<?php echo esc_attr( $post_id ); ?>">
			</tbody>
		</table>
	</div>
	<div class="right-box">
		<?php
		/**
		 * Add new post box to display the information.
		 */
		do_action( CF7SA_PREFIX . '/postbox' );
		?>
	</div>
</div>
<?php
add_action('admin_print_footer_scripts', function() {
	$allowed_html = array(
		'h3' => array(),
		'p' => array(),
		'a' => array( 'href' => array(), 'target' => array() ),
		'strong' => array(),
		'br' => array()
	);
	?>
	<script type="text/javascript">
		//<![CDATA[
		jQuery(document).ready( function($) {
			jQuery( '#cf7sa-test-publishable-key' ).on( 'hover click', function() {
				jQuery( 'body .wp-pointer-buttons .close' ).trigger( 'click' );
				jQuery( '#cf7sa-test-publishable-key' ).pointer({
					pointerClass: 'wp-pointer cf7sa-pointer',
					content: '<?php echo wp_kses( __( '<h3>Get Your Publishable Key</h3><p>Get it from <a href="https://dashboard.stripe.com/" target="_blank">Stripe</a> then <strong>Developers > API Keys</strong> page in your Stripe account.</p>', 'accept-stripe-payments-using-contact-form-7' ), $allowed_html ); ?>',
					position: 'left center',
				} ).pointer('open');
			} );

			jQuery( '#cf7sa-live-publishable-key' ).on( 'hover click', function() {
				jQuery( 'body .wp-pointer-buttons .close' ).trigger( 'click' );
				jQuery( '#cf7sa-live-publishable-key' ).pointer({
					pointerClass: 'wp-pointer cf7sa-pointer',
					content: '<?php echo wp_kses( __( '<h3>Get Your Publishable Key</h3><p>Get it from <a href="https://dashboard.stripe.com/" target="_blank">Stripe</a> then <strong>Developers > API Keys</strong> page in your Stripe account.</p>', 'accept-stripe-payments-using-contact-form-7' ), $allowed_html ); ?>',
					position: 'left center',
				} ).pointer('open');
			} );

			jQuery( '#cf7sa-test-secret-key' ).on( 'hover click', function() {
				jQuery( 'body .wp-pointer-buttons .close' ).trigger( 'click' );
				jQuery( '#cf7sa-test-secret-key' ).pointer({
					pointerClass: 'wp-pointer cf7sa-pointer',
					content: '<?php echo wp_kses( __( '<h3>Get Your Secret Key</h3><p>Get it from <a href="https://dashboard.stripe.com/" target="_blank">Stripe</a> then <strong>Developers > API Keys</strong> page in your Stripe account.</p>', 'accept-stripe-payments-using-contact-form-7' ), $allowed_html ); ?>',
					position: 'left center',
				} ).pointer('open');
			} );

			jQuery( '#cf7sa-amount-field' ).on( 'hover click', function() {
				jQuery( 'body .wp-pointer-buttons .close' ).trigger( 'click' );
				jQuery( '#cf7sa-amount-field' ).pointer({
					pointerClass: 'wp-pointer cf7sa-pointer',
					content: '<?php echo wp_kses( __( '<h3>Add Amount Name</h3><p>Add here the Name of amount field</p>', 'accept-stripe-payments-using-contact-form-7' ), $allowed_html ); ?>',
					position: 'left center',
				} ).pointer('open');
			} );

			jQuery( '#cf7sa-select-currency' ).on( 'hover click', function() {
				jQuery( 'body .wp-pointer-buttons .close' ).trigger( 'click' );
				jQuery( '#cf7sa-select-currency' ).pointer({
					pointerClass: 'wp-pointer cf7sa-pointer',
					content: '<?php echo wp_kses( __( '<h3>Select Currency</h3><p>Select the currency which is selected from your stripe.net merchant account.<br/><strong>Note:</strong>Stripe does not provide multiple currencies for single account</p>', 'accept-stripe-payments-using-contact-form-7' ), $allowed_html ); ?>',
					position: 'left center',
				} ).pointer('open');
			} );

			jQuery( '#cf7sa-enable-postal-code' ).on( 'hover click', function() {
				jQuery( 'body .wp-pointer-buttons .close' ).trigger( 'click' );
				jQuery( '#cf7sa-enable-postal-code' ).pointer({
					pointerClass: 'wp-pointer cf7sa-pointer',
					content: '<?php echo wp_kses( __( '<h3>Enable Postal Code field on the Card.</h3><p>Enable the Postal Code field on the card for each form individually.</p>', 'accept-stripe-payments-using-contact-form-7' ), $allowed_html ); ?>',
					position: 'left center',
				} ).pointer('open');
			} );

			jQuery( '#cf7sa-payment-success-msg' ).on( 'hover click', function() {
				jQuery( 'body .wp-pointer-buttons .close' ).trigger( 'click' );
				jQuery( '#cf7sa-payment-success-msg' ).pointer({
					pointerClass: 'wp-pointer cf7sa-pointer',
					content: '<?php echo wp_kses( __( '<h3>Payment Successful Message.</h3><p>Message Displayed After Form Submission and Successful Payment</p>', 'accept-stripe-payments-using-contact-form-7' ), $allowed_html ); ?>',
					position: 'left center',
				} ).pointer('open');
			} );

			jQuery( '#cf7sa-webhook-secret' ).on( 'hover click', function() {
				jQuery( 'body .wp-pointer-buttons .close' ).trigger( 'click' );
				jQuery( '#cf7sa-webhook-secret' ).pointer({
					pointerClass: 'wp-pointer cf7sa-pointer',
					content: '<?php echo wp_kses( __( '<h3>Webhook Signing Secret</h3><p>For security, configure webhook signature verification. Get this from Stripe Dashboard > Developers > Webhooks.</p>', 'accept-stripe-payments-using-contact-form-7' ), $allowed_html ); ?>',
					position: 'left center',
				} ).pointer('open');
			} );
		} );
		//]]>
	</script>
	<?php
} );
