<?php
/**
 * Transactional SMS — short visit updates to customers who opt in.
 *
 * Provider-agnostic: Brevo (default, reuses your existing Brevo account) or
 * Twilio. Both are pay-as-you-go — no SDK, no plugin, just direct HTTPS via
 * the WordPress HTTP API. Sending is always gated on per-customer opt-in.
 *
 * @package hss-portal
 */
if ( ! defined( 'ABSPATH' ) ) { exit; }

class HSS_Sms {

	/**
	 * Send one SMS.
	 *
	 * @param string $phone  raw phone (any format); normalized to E.164.
	 * @param string $message
	 * @return true|WP_Error
	 */
	public static function send( $phone, $message ) {
		if ( ! HSS_Config::is_sms_configured() ) {
			return new WP_Error( 'hss_sms_unconfigured', 'SMS is not configured.' );
		}
		$e164 = self::normalize( $phone );
		if ( ! $e164 ) {
			return new WP_Error( 'hss_sms_bad_phone', 'No valid phone number.' );
		}
		$message = trim( wp_strip_all_tags( $message ) );
		if ( $message === '' ) {
			return new WP_Error( 'hss_sms_empty', 'Empty message.' );
		}

		$provider = HSS_Config::sms_provider();
		if ( $provider === 'brevo' )  { return self::send_brevo( $e164, $message ); }
		if ( $provider === 'twilio' ) { return self::send_twilio( $e164, $message ); }
		return new WP_Error( 'hss_sms_no_provider', 'No SMS provider selected.' );
	}

	/**
	 * Normalize a phone to E.164 (+countrycode...). Assumes US/Canada when
	 * no country code is present. Returns '' if it can't be made valid.
	 */
	public static function normalize( $phone ) {
		$digits = preg_replace( '/\D+/', '', (string) $phone );
		if ( $digits === '' ) { return ''; }

		// Already had a leading + → trust the country code as given.
		if ( strpos( (string) $phone, '+' ) === 0 ) {
			return '+' . $digits;
		}
		if ( strlen( $digits ) === 10 ) {            // bare US 10-digit
			return '+1' . $digits;
		}
		if ( strlen( $digits ) === 11 && $digits[0] === '1' ) { // 1 + 10
			return '+' . $digits;
		}
		if ( strlen( $digits ) >= 8 && strlen( $digits ) <= 15 ) {
			return '+' . $digits;                     // assume already has country code
		}
		return '';
	}

	/* ── Brevo transactional SMS ──────────────────────────────────────── */
	protected static function send_brevo( $e164, $message ) {
		$res = wp_remote_post( 'https://api.brevo.com/v3/transactionalSMS/sms', [
			'timeout' => 20,
			'headers' => [
				'api-key'      => HSS_Config::brevo_api_key(),
				'accept'       => 'application/json',
				'content-type' => 'application/json',
			],
			'body' => wp_json_encode( [
				'type'      => 'transactional',
				'sender'    => substr( HSS_Config::sms_sender(), 0, 15 ),
				'recipient' => ltrim( $e164, '+' ), // Brevo wants digits, no +
				'content'   => $message,
			] ),
		] );
		return self::interpret( $res );
	}

	/* ── Twilio ───────────────────────────────────────────────────────── */
	protected static function send_twilio( $e164, $message ) {
		$sid = HSS_Config::twilio_sid();
		$res = wp_remote_post( 'https://api.twilio.com/2010-04-01/Accounts/' . rawurlencode( $sid ) . '/Messages.json', [
			'timeout' => 20,
			'headers' => [
				'Authorization' => 'Basic ' . base64_encode( $sid . ':' . HSS_Config::twilio_token() ),
				'Content-Type'  => 'application/x-www-form-urlencoded',
			],
			'body' => [
				'To'   => $e164,
				'From' => HSS_Config::twilio_from(),
				'Body' => $message,
			],
		] );
		return self::interpret( $res );
	}

	protected static function interpret( $res ) {
		if ( is_wp_error( $res ) ) { return $res; }
		$code = wp_remote_retrieve_response_code( $res );
		if ( $code >= 200 && $code < 300 ) { return true; }
		$body = json_decode( wp_remote_retrieve_body( $res ), true );
		$msg  = $body['message'] ?? ( $body['error']['message'] ?? 'SMS provider error (HTTP ' . $code . ').' );
		return new WP_Error( 'hss_sms_send_failed', $msg, [ 'status' => $code ] );
	}

	/* ── Visit lifecycle texts ────────────────────────────────────────── */

	/**
	 * Text a customer about a visit, if they opted in and we have a number.
	 * Mirrors the email lifecycle but stays short. Silent no-op when the
	 * customer hasn't opted in or SMS isn't configured.
	 */
	public static function visit_status( $visit ) {
		if ( ! HSS_Config::is_sms_configured() ) { return false; }

		$cust = HSS_Customers::get_by_user( (int) $visit->user_id );
		if ( ! $cust || (int) $cust->sms_opt_in !== 1 || ! $cust->phone ) { return false; }

		$brand = get_bloginfo( 'name' );
		switch ( $visit->status ) {
			case 'scheduled':
				$when = $visit->scheduled_date ? date_i18n( 'D M j', strtotime( $visit->scheduled_date ) ) : 'soon';
				$msg  = $brand . ': your next cleanup is scheduled for ' . $when
					. ( $visit->time_window ? ' (' . $visit->time_window . ')' : '' ) . '.';
				break;
			case 'enroute':
				$msg = $brand . ': we\'re on the way to scoop your yard now. We\'ll text when it\'s done.';
				break;
			case 'completed':
				$msg = $brand . ': all done — your yard is clean and ready to enjoy. Thanks!';
				break;
			case 'skipped':
				$msg = $brand . ': we had to skip today\'s visit'
					. ( $visit->customer_note ? ' (' . $visit->customer_note . ')' : '' )
					. '. We\'ll catch it next time.';
				break;
			default:
				return false;
		}
		$msg .= ' Reply STOP to opt out.';

		return self::send( $cust->phone, $msg );
	}
}
