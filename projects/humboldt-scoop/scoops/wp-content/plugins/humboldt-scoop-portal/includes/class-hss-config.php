<?php
/**
 * Pricing matrix + Stripe credential resolution.
 * @package hss-portal
 */
if ( ! defined( 'ABSPATH' ) ) { exit; }

class HSS_Config {

	const CURRENCY = 'usd';
	const INTERVAL = 'month';

	/**
	 * The single source of truth for recurring plan pricing.
	 * Amounts are whole dollars billed per month.
	 * All plans bill monthly; the visit frequency is the service level.
	 */
	public static function pricing() {
		return [
			'monthly'  => [ 'label' => 'Monthly',   'desc' => '1 visit per month',        'prices' => [ 1 => 19, 2 => 22, 3 => 25 ] ],
			'biweekly' => [ 'label' => 'Bi-Weekly',  'desc' => '2 visits per month',       'prices' => [ 1 => 30, 2 => 35, 3 => 40 ] ],
			'weekly'   => [ 'label' => 'Weekly',     'desc' => 'Weekly visits (~4/month)', 'prices' => [ 1 => 50, 2 => 60, 3 => 70 ] ],
		];
	}

	/** One-time cleanup price, in whole dollars per half hour. */
	public static function onetime_price() { return 40; }

	public static function plan( $key ) {
		$p = self::pricing();
		return isset( $p[ $key ] ) ? $p[ $key ] : null;
	}

	/** Amount in cents for a recurring plan + dog count (1–3). */
	public static function amount_cents( $plan_key, $dogs ) {
		$plan = self::plan( $plan_key );
		$dogs = max( 1, min( 3, (int) $dogs ) );
		if ( ! $plan ) { return 0; }
		return (int) round( $plan['prices'][ $dogs ] * 100 );
	}

	public static function onetime_cents() {
		return (int) round( self::onetime_price() * 100 );
	}

	public static function plan_label( $plan_key, $dogs = null ) {
		if ( $plan_key === 'onetime' ) { return 'One-Time Cleanup'; }
		$plan = self::plan( $plan_key );
		if ( ! $plan ) { return ucfirst( $plan_key ); }
		$label = $plan['label'];
		if ( $dogs ) { $label .= ' — ' . (int) $dogs . ' ' . ( (int) $dogs === 1 ? 'dog' : 'dogs' ); }
		return $label;
	}

	/* ── Credentials (env-first, never written to the DB) ─────────────── */

	/**
	 * Resolve a credential by name, e.g. 'STRIPE_SECRET_KEY'.
	 * Order: wp-config constant → environment variable → .env (loaded as
	 * a constant at bootstrap). Secrets are never stored as options.
	 */
	public static function get( $name ) {
		$const = 'HSS_' . $name;
		if ( defined( $const ) && constant( $const ) ) { return (string) constant( $const ); }
		$env = getenv( $const );
		if ( $env ) { return (string) $env; }
		// Also accept the bare name (e.g. STRIPE_SECRET_KEY) for convenience.
		if ( defined( $name ) && constant( $name ) ) { return (string) constant( $name ); }
		$env2 = getenv( $name );
		if ( $env2 ) { return (string) $env2; }
		return '';
	}

	public static function stripe_secret()      { return self::get( 'STRIPE_SECRET_KEY' ); }
	public static function stripe_publishable() { return self::get( 'STRIPE_PUBLISHABLE_KEY' ); }
	public static function webhook_secret()     { return self::get( 'STRIPE_WEBHOOK_SECRET' ); }

	public static function is_configured() {
		return self::stripe_secret() !== '';
	}

	/* ── SMS credentials (env-first, same precedence as Stripe) ───────── */

	/**
	 * Brevo v3 API key for transactional SMS.
	 *
	 * Precedence: an explicit HSS_BREVO_API_KEY (constant/env/.env) wins;
	 * otherwise we reuse the key already saved by the Kind Brevo Mailer
	 * plugin (option `kind_brevo_mailer_options['api_key']`, a v3 key), so
	 * there's nothing new to configure when that plugin is set to API mode.
	 */
	public static function brevo_api_key() {
		$k = self::get( 'BREVO_API_KEY' );
		if ( $k !== '' ) { return $k; }

		$opt = get_option( 'kind_brevo_mailer_options' );
		if ( is_array( $opt ) && ! empty( $opt['api_key'] ) ) {
			return (string) $opt['api_key'];
		}
		return '';
	}

	/** True when the Brevo key is coming from the Kind Brevo Mailer plugin. */
	public static function brevo_key_from_mailer() {
		if ( self::get( 'BREVO_API_KEY' ) !== '' ) { return false; }
		$opt = get_option( 'kind_brevo_mailer_options' );
		return is_array( $opt ) && ! empty( $opt['api_key'] );
	}
	/** Twilio (alternative provider). */
	public static function twilio_sid()     { return self::get( 'TWILIO_ACCOUNT_SID' ); }
	public static function twilio_token()   { return self::get( 'TWILIO_AUTH_TOKEN' ); }
	public static function twilio_from()    { return self::get( 'TWILIO_FROM_NUMBER' ); }

	/**
	 * Sender ID / number shown to the recipient. For US delivery this must
	 * be a real number you control (alphanumeric IDs aren't deliverable to
	 * US handsets). Defaults to a short alphanumeric for non-US testing.
	 */
	public static function sms_sender() {
		$s = self::get( 'SMS_SENDER' );
		return $s !== '' ? $s : 'ScoopSol';
	}

	/**
	 * Which SMS provider to use. Explicit HSS_SMS_PROVIDER wins; otherwise
	 * auto-detect from whichever credentials are present.
	 * @return string 'brevo' | 'twilio' | ''.
	 */
	public static function sms_provider() {
		$p = strtolower( self::get( 'SMS_PROVIDER' ) );
		if ( $p === 'brevo' || $p === 'twilio' ) { return $p; }
		if ( self::brevo_api_key() !== '' ) { return 'brevo'; }
		if ( self::twilio_sid() !== '' && self::twilio_token() !== '' && self::twilio_from() !== '' ) { return 'twilio'; }
		return '';
	}

	public static function is_sms_configured() {
		$p = self::sms_provider();
		if ( $p === 'brevo' )  { return self::brevo_api_key() !== ''; }
		if ( $p === 'twilio' ) { return self::twilio_sid() !== '' && self::twilio_token() !== '' && self::twilio_from() !== ''; }
		return false;
	}

	/** True when running against Stripe test keys. */
	public static function is_test_mode() {
		return strpos( self::stripe_secret(), 'sk_test_' ) === 0
			|| strpos( self::stripe_secret(), 'rk_test_' ) === 0;
	}
}
