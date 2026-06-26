<?php
/**
 * REST endpoints: checkout, billing portal, profile, quote, Stripe webhook.
 * @package hss-portal
 */
if ( ! defined( 'ABSPATH' ) ) { exit; }

class HSS_Rest {

	const NS = 'hss/v1';

	public static function init() {
		add_action( 'rest_api_init', [ __CLASS__, 'routes' ] );
	}

	public static function routes() {
		register_rest_route( self::NS, '/checkout', [
			'methods'             => 'POST',
			'callback'            => [ __CLASS__, 'checkout' ],
			'permission_callback' => [ __CLASS__, 'logged_in' ],
		] );
		register_rest_route( self::NS, '/billing-portal', [
			'methods'             => 'POST',
			'callback'            => [ __CLASS__, 'billing_portal' ],
			'permission_callback' => [ __CLASS__, 'logged_in' ],
		] );
		register_rest_route( self::NS, '/profile', [
			'methods'             => 'POST',
			'callback'            => [ __CLASS__, 'save_profile' ],
			'permission_callback' => [ __CLASS__, 'logged_in' ],
		] );
		register_rest_route( self::NS, '/quote', [
			'methods'             => 'POST',
			'callback'            => [ __CLASS__, 'quote' ],
			'permission_callback' => '__return_true',
		] );
		register_rest_route( self::NS, '/webhook', [
			'methods'             => 'POST',
			'callback'            => [ __CLASS__, 'webhook' ],
			'permission_callback' => '__return_true',
		] );
	}

	public static function logged_in() {
		return is_user_logged_in();
	}

	/* ── Checkout: subscription or one-time ───────────────────────────── */
	public static function checkout( WP_REST_Request $req ) {
		if ( ! HSS_Config::is_configured() ) {
			return new WP_Error( 'hss_unconfigured', 'Online payments are not set up yet. Please contact us to get started.', [ 'status' => 503 ] );
		}

		$user = wp_get_current_user();
		$cust = HSS_Customers::get_or_create( $user->ID );
		$stripe_customer = HSS_Customers::ensure_stripe_customer( $cust );
		if ( is_wp_error( $stripe_customer ) ) {
			return new WP_Error( 'hss_customer', 'Could not start checkout: ' . $stripe_customer->get_error_message(), [ 'status' => 502 ] );
		}

		$plan = sanitize_text_field( $req->get_param( 'plan' ) );
		$dogs = max( 1, min( 3, (int) $req->get_param( 'dogs' ) ) );
		$portal = HSS_Portal::portal_url();

		$common = [
			'customer'                  => $stripe_customer,
			'success_url'               => add_query_arg( 'checkout', 'success', $portal ),
			'cancel_url'                => add_query_arg( 'checkout', 'cancel', $portal ),
			'client_reference_id'       => $user->ID,
			'allow_promotion_codes'     => 'true',
			'metadata[hss_user_id]'     => $user->ID,
			'metadata[plan_key]'        => $plan,
			'metadata[dog_count]'       => $dogs,
		];

		if ( 'onetime' === $plan ) {
			$args = $common + [
				'mode'                                        => 'payment',
				'line_items[0][quantity]'                     => 1,
				'line_items[0][price_data][currency]'         => HSS_Config::CURRENCY,
				'line_items[0][price_data][unit_amount]'      => HSS_Config::onetime_cents(),
				'line_items[0][price_data][product_data][name]' => 'One-Time Cleanup (per half hour)',
				'payment_intent_data[metadata][hss_user_id]'  => $user->ID,
				'invoice_creation[enabled]'                   => 'true',
			];
		} else {
			$amount = HSS_Config::amount_cents( $plan, $dogs );
			if ( ! $amount ) {
				return new WP_Error( 'hss_bad_plan', 'Unknown plan selected.', [ 'status' => 400 ] );
			}
			$args = $common + [
				'mode'                                                 => 'subscription',
				'line_items[0][quantity]'                              => 1,
				'line_items[0][price_data][currency]'                  => HSS_Config::CURRENCY,
				'line_items[0][price_data][unit_amount]'               => $amount,
				'line_items[0][price_data][recurring][interval]'       => HSS_Config::INTERVAL,
				'line_items[0][price_data][product_data][name]'        => 'HSS ' . HSS_Config::plan_label( $plan, $dogs ),
				'subscription_data[metadata][hss_user_id]'             => $user->ID,
				'subscription_data[metadata][plan_key]'                => $plan,
				'subscription_data[metadata][dog_count]'               => $dogs,
			];
		}

		$session = HSS_Stripe::create_checkout_session( $args );
		if ( is_wp_error( $session ) ) {
			return new WP_Error( 'hss_checkout', 'Could not start checkout: ' . $session->get_error_message(), [ 'status' => 502 ] );
		}
		return [ 'url' => $session['url'] ];
	}

	/* ── Hosted billing portal (manage / cancel / update card) ────────── */
	public static function billing_portal( WP_REST_Request $req ) {
		$user = wp_get_current_user();
		$cust = HSS_Customers::get_or_create( $user->ID );
		if ( empty( $cust->stripe_customer_id ) ) {
			return new WP_Error( 'hss_no_billing', 'No billing account found yet.', [ 'status' => 400 ] );
		}
		$session = HSS_Stripe::create_billing_portal_session( [
			'customer'   => $cust->stripe_customer_id,
			'return_url' => HSS_Portal::portal_url(),
		] );
		if ( is_wp_error( $session ) ) {
			return new WP_Error( 'hss_billing', 'Could not open billing portal: ' . $session->get_error_message(), [ 'status' => 502 ] );
		}
		return [ 'url' => $session['url'] ];
	}

	/* ── Save service details ─────────────────────────────────────────── */
	public static function save_profile( WP_REST_Request $req ) {
		$user = wp_get_current_user();
		$cust = HSS_Customers::get_or_create( $user->ID );
		HSS_Customers::update( $cust->id, [
			'address'    => sanitize_text_field( $req->get_param( 'address' ) ),
			'city'       => sanitize_text_field( $req->get_param( 'city' ) ),
			'phone'      => sanitize_text_field( $req->get_param( 'phone' ) ),
			'dog_count'  => max( 1, min( 6, (int) $req->get_param( 'dog_count' ) ) ),
			'gate_notes' => sanitize_textarea_field( $req->get_param( 'gate_notes' ) ),
			'yard_notes' => sanitize_textarea_field( $req->get_param( 'yard_notes' ) ),
			'pet_notes'  => sanitize_textarea_field( $req->get_param( 'pet_notes' ) ),
			'sms_opt_in' => $req->get_param( 'sms_opt_in' ) ? 1 : 0,
		] );
		return [ 'ok' => true ];
	}

	/* ── Quote request ────────────────────────────────────────────────── */
	public static function quote( WP_REST_Request $req ) {
		// Honeypot
		if ( $req->get_param( 'hss_hp' ) ) {
			return [ 'ok' => true ];
		}
		$name  = sanitize_text_field( $req->get_param( 'name' ) );
		$email = sanitize_email( $req->get_param( 'email' ) );
		if ( ! $name || ! is_email( $email ) ) {
			return new WP_Error( 'hss_bad_quote', 'Please provide your name and a valid email.', [ 'status' => 400 ] );
		}

		global $wpdb;
		$data = [
			'name'     => $name,
			'email'    => $email,
			'phone'    => sanitize_text_field( $req->get_param( 'phone' ) ),
			'city'     => sanitize_text_field( $req->get_param( 'city' ) ),
			'dogs'     => sanitize_text_field( $req->get_param( 'dogs' ) ),
			'interest' => sanitize_text_field( $req->get_param( 'interest' ) ),
			'message'  => sanitize_textarea_field( $req->get_param( 'message' ) ),
		];
		$wpdb->insert( HSS_DB::t( 'quote_requests' ), $data );

		$to      = get_option( 'admin_email' );
		$subject = 'New quote request — ' . $name;
		$body    = "New quote request from the website:\n\n"
			. "Name: {$data['name']}\nEmail: {$data['email']}\nPhone: {$data['phone']}\n"
			. "City: {$data['city']}\nDogs: {$data['dogs']}\nInterested in: {$data['interest']}\n\n"
			. "Message:\n{$data['message']}\n";
		wp_mail( $to, $subject, $body, [ 'Reply-To: ' . $name . ' <' . $email . '>' ] );

		return [ 'ok' => true, 'message' => 'Thanks! We\'ll be in touch soon.' ];
	}

	/* ── Stripe webhook ───────────────────────────────────────────────── */
	public static function webhook( WP_REST_Request $req ) {
		$payload = $req->get_body();
		$sig     = $req->get_header( 'stripe_signature' );
		$secret  = HSS_Config::webhook_secret();

		$event = HSS_Stripe::construct_event( $payload, $sig, $secret );
		if ( is_wp_error( $event ) ) {
			return new WP_REST_Response( [ 'error' => $event->get_error_message() ], 400 );
		}

		$type = $event['type'] ?? '';
		$obj  = $event['data']['object'] ?? [];

		switch ( $type ) {
			case 'checkout.session.completed':
				self::on_checkout_completed( $obj );
				break;
			case 'customer.subscription.created':
			case 'customer.subscription.updated':
			case 'customer.subscription.deleted':
				self::upsert_subscription( $obj );
				break;
			case 'invoice.paid':
			case 'invoice.payment_succeeded':
			case 'invoice.payment_failed':
			case 'invoice.finalized':
				self::upsert_invoice( $obj );
				break;
		}

		return new WP_REST_Response( [ 'received' => true ], 200 );
	}

	protected static function resolve_user( $obj ) {
		// Try metadata, then client_reference_id, then map by stripe customer.
		if ( ! empty( $obj['metadata']['hss_user_id'] ) ) { return (int) $obj['metadata']['hss_user_id']; }
		if ( ! empty( $obj['client_reference_id'] ) ) { return (int) $obj['client_reference_id']; }
		$customer_id = is_array( $obj['customer'] ?? null ) ? ( $obj['customer']['id'] ?? '' ) : ( $obj['customer'] ?? '' );
		if ( $customer_id ) {
			$row = HSS_Customers::get_by_stripe_id( $customer_id );
			if ( $row ) { return (int) $row->user_id; }
		}
		return 0;
	}

	protected static function on_checkout_completed( $session ) {
		$user_id     = self::resolve_user( $session );
		$customer_id = $session['customer'] ?? '';

		// Make sure the Stripe customer id is linked to the user.
		if ( $user_id && $customer_id ) {
			$cust = HSS_Customers::get_by_user( $user_id );
			if ( $cust && empty( $cust->stripe_customer_id ) ) {
				HSS_Customers::update( $cust->id, [ 'stripe_customer_id' => $customer_id ] );
			}
		}

		// Pull the subscription so the dashboard reflects it immediately.
		if ( ( $session['mode'] ?? '' ) === 'subscription' && ! empty( $session['subscription'] ) ) {
			$sub = HSS_Stripe::get_subscription( $session['subscription'] );
			if ( ! is_wp_error( $sub ) ) { self::upsert_subscription( $sub ); }
		}
	}

	protected static function upsert_subscription( $sub ) {
		global $wpdb;
		$user_id     = self::resolve_user( $sub );
		$customer_id = is_array( $sub['customer'] ?? null ) ? ( $sub['customer']['id'] ?? '' ) : ( $sub['customer'] ?? '' );
		$cust        = $user_id ? HSS_Customers::get_by_user( $user_id ) : HSS_Customers::get_by_stripe_id( $customer_id );

		$item   = $sub['items']['data'][0] ?? [];
		$amount = (int) ( $item['price']['unit_amount'] ?? 0 );
		$row = [
			'user_id'                => $user_id,
			'customer_id'            => $cust ? (int) $cust->id : 0,
			'stripe_subscription_id' => $sub['id'] ?? '',
			'plan_key'               => $sub['metadata']['plan_key'] ?? '',
			'dog_count'              => (int) ( $sub['metadata']['dog_count'] ?? 1 ),
			'amount_cents'           => $amount,
			'status'                 => $sub['status'] ?? '',
			'current_period_end'     => ! empty( $sub['current_period_end'] ) ? gmdate( 'Y-m-d H:i:s', (int) $sub['current_period_end'] ) : null,
			'updated_at'             => current_time( 'mysql' ),
		];

		$t = HSS_DB::t( 'subscriptions' );
		$exists = $wpdb->get_var( $wpdb->prepare( "SELECT id FROM $t WHERE stripe_subscription_id = %s", $row['stripe_subscription_id'] ) );
		if ( $exists ) {
			$wpdb->update( $t, $row, [ 'id' => $exists ] );
		} else {
			$wpdb->insert( $t, $row );
		}
	}

	protected static function upsert_invoice( $inv ) {
		global $wpdb;
		$user_id     = self::resolve_user( $inv );
		$customer_id = is_array( $inv['customer'] ?? null ) ? ( $inv['customer']['id'] ?? '' ) : ( $inv['customer'] ?? '' );
		$cust        = $user_id ? HSS_Customers::get_by_user( $user_id ) : HSS_Customers::get_by_stripe_id( $customer_id );
		if ( ! $user_id && $cust ) { $user_id = (int) $cust->user_id; }

		$desc = '';
		if ( ! empty( $inv['lines']['data'][0]['description'] ) ) {
			$desc = $inv['lines']['data'][0]['description'];
		}

		$row = [
			'user_id'           => $user_id,
			'customer_id'       => $cust ? (int) $cust->id : 0,
			'stripe_invoice_id' => $inv['id'] ?? '',
			'number'            => $inv['number'] ?? '',
			'amount_cents'      => (int) ( $inv['amount_paid'] ?? $inv['amount_due'] ?? $inv['total'] ?? 0 ),
			'status'            => $inv['status'] ?? '',
			'description'       => $desc,
			'hosted_url'        => $inv['hosted_invoice_url'] ?? '',
			'pdf_url'           => $inv['invoice_pdf'] ?? '',
		];

		$t = HSS_DB::t( 'invoices' );
		$exists = $wpdb->get_var( $wpdb->prepare( "SELECT id FROM $t WHERE stripe_invoice_id = %s", $row['stripe_invoice_id'] ) );
		if ( $exists ) {
			$wpdb->update( $t, $row, [ 'id' => $exists ] );
		} else {
			$wpdb->insert( $t, $row );
		}
	}
}
