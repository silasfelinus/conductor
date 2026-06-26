<?php
/**
 * Minimal Stripe REST client built on the WordPress HTTP API.
 * No Composer, no SDK, no plugin dependencies — just direct HTTPS calls.
 * @package hss-portal
 */
if ( ! defined( 'ABSPATH' ) ) { exit; }

class HSS_Stripe {

	const API     = 'https://api.stripe.com/v1/';
	const VERSION = '2024-06-20';

	/**
	 * Perform a Stripe API request.
	 * @return array|WP_Error decoded JSON body, or WP_Error on failure.
	 */
	protected static function request( $method, $path, $params = [] ) {
		$key = HSS_Config::stripe_secret();
		if ( ! $key ) {
			return new WP_Error( 'hss_stripe_unconfigured', 'Stripe is not configured. Add HSS_STRIPE_SECRET_KEY.' );
		}

		$url  = self::API . $path;
		$args = [
			'method'  => $method,
			'timeout' => 30,
			'headers' => [
				'Authorization'  => 'Bearer ' . $key,
				'Content-Type'   => 'application/x-www-form-urlencoded',
				'Stripe-Version' => self::VERSION,
			],
		];

		if ( 'GET' === $method ) {
			if ( $params ) { $url .= '?' . self::encode( $params ); }
		} elseif ( $params ) {
			$args['body'] = self::encode( $params );
		}

		$res = wp_remote_request( $url, $args );
		if ( is_wp_error( $res ) ) { return $res; }

		$code = wp_remote_retrieve_response_code( $res );
		$body = json_decode( wp_remote_retrieve_body( $res ), true );

		if ( $code >= 200 && $code < 300 ) {
			return is_array( $body ) ? $body : [];
		}

		$msg = isset( $body['error']['message'] ) ? $body['error']['message'] : 'Stripe API error (HTTP ' . $code . ').';
		return new WP_Error( 'hss_stripe_error', $msg, [ 'status' => $code, 'body' => $body ] );
	}

	/** Encode params with PHP bracket syntax, which Stripe accepts. */
	protected static function encode( $params ) {
		return http_build_query( $params, '', '&', PHP_QUERY_RFC3986 );
	}

	/* ── Customers ────────────────────────────────────────────────────── */
	public static function create_customer( $args ) {
		return self::request( 'POST', 'customers', $args );
	}
	public static function get_customer( $id ) {
		return self::request( 'GET', 'customers/' . rawurlencode( $id ) );
	}

	/* ── Checkout ─────────────────────────────────────────────────────── */
	public static function create_checkout_session( $args ) {
		return self::request( 'POST', 'checkout/sessions', $args );
	}

	/* ── Billing portal (hosted self-service: cancel, pause, update card) ─ */
	public static function create_billing_portal_session( $args ) {
		return self::request( 'POST', 'billing_portal/sessions', $args );
	}

	/* ── Reads for the dashboard / admin ──────────────────────────────── */
	public static function list_invoices( $customer_id, $limit = 12 ) {
		return self::request( 'GET', 'invoices', [ 'customer' => $customer_id, 'limit' => $limit ] );
	}
	public static function list_subscriptions( $customer_id ) {
		return self::request( 'GET', 'subscriptions', [ 'customer' => $customer_id, 'status' => 'all', 'limit' => 10 ] );
	}
	public static function get_subscription( $id ) {
		return self::request( 'GET', 'subscriptions/' . rawurlencode( $id ) );
	}

	/* ── Subscription changes (plan change / pause / resume / cancel) ───── */
	public static function update_subscription( $id, $args ) {
		return self::request( 'POST', 'subscriptions/' . rawurlencode( $id ), $args );
	}
	/** Cancel immediately. (For end-of-period cancel, update cancel_at_period_end.) */
	public static function cancel_subscription( $id ) {
		return self::request( 'DELETE', 'subscriptions/' . rawurlencode( $id ) );
	}

	/**
	 * Verify a webhook signature and return the decoded event.
	 * Implements Stripe's t=…,v1=… scheme without the SDK.
	 * @return array|WP_Error
	 */
	public static function construct_event( $payload, $sig_header, $secret, $tolerance = 300 ) {
		if ( ! $secret ) {
			return new WP_Error( 'hss_no_webhook_secret', 'Webhook secret is not configured.' );
		}
		$ts = null; $sigs = [];
		foreach ( explode( ',', (string) $sig_header ) as $part ) {
			$kv = explode( '=', trim( $part ), 2 );
			if ( count( $kv ) !== 2 ) { continue; }
			if ( $kv[0] === 't' ) { $ts = $kv[1]; }
			if ( $kv[0] === 'v1' ) { $sigs[] = $kv[1]; }
		}
		if ( ! $ts || ! $sigs ) {
			return new WP_Error( 'hss_bad_signature', 'Missing signature header.' );
		}
		$expected = hash_hmac( 'sha256', $ts . '.' . $payload, $secret );
		$match = false;
		foreach ( $sigs as $s ) {
			if ( hash_equals( $expected, $s ) ) { $match = true; break; }
		}
		if ( ! $match ) {
			return new WP_Error( 'hss_bad_signature', 'Signature verification failed.' );
		}
		if ( $tolerance > 0 && abs( time() - (int) $ts ) > $tolerance ) {
			return new WP_Error( 'hss_stale_event', 'Timestamp outside tolerance.' );
		}
		$event = json_decode( $payload, true );
		if ( ! is_array( $event ) ) {
			return new WP_Error( 'hss_bad_payload', 'Invalid JSON payload.' );
		}
		return $event;
	}
}
