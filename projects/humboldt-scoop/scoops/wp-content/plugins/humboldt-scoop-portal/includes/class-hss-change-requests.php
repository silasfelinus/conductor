<?php
/**
 * Customer-initiated change requests (Phase 2B).
 *
 * Customers ask to change plan, pause, resume, or cancel from the portal
 * dashboard. Requests land in WP Admin for approval. The business then
 * actions the change (e.g. in Stripe) and marks the request approved or
 * declined; the customer is emailed the outcome.
 *
 * @package hss-portal
 */
if ( ! defined( 'ABSPATH' ) ) { exit; }

class HSS_Change_Requests {

	public static function table() {
		return HSS_DB::t( 'change_requests' );
	}

	/** Request types: key => label. */
	public static function types() {
		return [
			'plan_change' => 'Change plan',
			'pause'       => 'Pause service',
			'resume'      => 'Resume service',
			'cancel'      => 'Cancel service',
			'other'       => 'Other request',
		];
	}

	public static function type_label( $type ) {
		$map = self::types();
		return $map[ $type ] ?? 'Request';
	}

	public static function is_valid_type( $type ) {
		return array_key_exists( $type, self::types() );
	}

	/** Statuses: new (awaiting), approved, declined. */
	public static function statuses() {
		return [
			'new'      => 'Pending',
			'approved' => 'Approved',
			'declined' => 'Declined',
		];
	}

	public static function status_label( $status ) {
		$map = self::statuses();
		return $map[ $status ] ?? ucfirst( (string) $status );
	}

	public static function is_resolution( $status ) {
		return in_array( $status, [ 'approved', 'declined' ], true );
	}

	/* ── Writes ───────────────────────────────────────────────────────── */

	public static function create( $data ) {
		global $wpdb;
		$defaults = [
			'user_id'            => 0,
			'customer_id'        => 0,
			'type'               => 'other',
			'current_plan_key'   => '',
			'requested_plan_key' => '',
			'requested_dogs'     => 0,
			'message'            => '',
			'status'             => 'new',
			'admin_note'         => '',
			'created_at'         => current_time( 'mysql' ),
			'updated_at'         => current_time( 'mysql' ),
		];
		$row = array_merge( $defaults, $data );
		$ok  = $wpdb->insert( self::table(), $row );
		return $ok ? (int) $wpdb->insert_id : 0;
	}

	/**
	 * Resolve a request (approve/decline), stamp it, and email the customer.
	 *
	 * @param int    $id
	 * @param string $status 'approved' | 'declined'
	 * @param string $admin_note optional note shown to the customer.
	 * @return bool
	 */
	public static function set_status( $id, $status, $admin_note = '' ) {
		if ( ! self::is_resolution( $status ) ) { return false; }
		$req = self::get( $id );
		if ( ! $req ) { return false; }

		global $wpdb;
		$wpdb->update( self::table(), [
			'status'      => $status,
			'admin_note'  => $admin_note,
			'updated_at'  => current_time( 'mysql' ),
			'resolved_at' => current_time( 'mysql' ),
		], [ 'id' => (int) $id ] );

		$req = self::get( $id );
		if ( $req && class_exists( 'HSS_Mail' ) ) {
			HSS_Mail::change_request_resolved( $req );
		}
		return true;
	}

	/* ── Reads ────────────────────────────────────────────────────────── */

	public static function get( $id ) {
		global $wpdb;
		$t = self::table();
		return $wpdb->get_row( $wpdb->prepare( "SELECT * FROM $t WHERE id = %d", (int) $id ) );
	}

	/** The customer's current open (unresolved) request, if any. */
	public static function pending_for_user( $user_id ) {
		global $wpdb;
		$t = self::table();
		return $wpdb->get_row( $wpdb->prepare(
			"SELECT * FROM $t WHERE user_id = %d AND status = 'new' ORDER BY id DESC LIMIT 1",
			$user_id
		) );
	}

	public static function history_for_user( $user_id, $limit = 6 ) {
		global $wpdb;
		$t = self::table();
		return $wpdb->get_results( $wpdb->prepare(
			"SELECT * FROM $t WHERE user_id = %d AND status <> 'new' ORDER BY id DESC LIMIT %d",
			$user_id, $limit
		) );
	}

	public static function pending( $limit = 200 ) {
		global $wpdb;
		$t = self::table();
		return $wpdb->get_results( $wpdb->prepare(
			"SELECT * FROM $t WHERE status = 'new' ORDER BY created_at ASC LIMIT %d",
			$limit
		) );
	}

	public static function recent( $limit = 100 ) {
		global $wpdb;
		$t = self::table();
		return $wpdb->get_results( $wpdb->prepare(
			"SELECT * FROM $t WHERE status <> 'new' ORDER BY resolved_at DESC LIMIT %d",
			$limit
		) );
	}

	public static function count_open() {
		global $wpdb;
		$t = self::table();
		return (int) $wpdb->get_var( "SELECT COUNT(*) FROM $t WHERE status = 'new'" );
	}

	/* ── Apply an approved request to Stripe ──────────────────────────── */

	/**
	 * Action an approved request against Stripe.
	 *
	 * @return string|WP_Error  Human summary on success (including the
	 *                          "nothing to auto-apply, handle manually"
	 *                          cases, which are NOT errors), or WP_Error
	 *                          when a Stripe call fails so the caller can
	 *                          leave the request open and retry.
	 */
	public static function apply_to_stripe( $req ) {
		if ( ! HSS_Config::is_configured() ) {
			return 'Stripe isn\'t configured — apply this change manually.';
		}
		if ( $req->type === 'other' ) {
			return 'No billing change needed.';
		}

		$sub_row = HSS_Portal::active_subscription( (int) $req->user_id );
		$sub_id  = $sub_row ? $sub_row->stripe_subscription_id : '';
		if ( ! $sub_id ) {
			return 'No active Stripe subscription on file — handle this one manually.';
		}

		switch ( $req->type ) {

			case 'cancel':
				$res = HSS_Stripe::update_subscription( $sub_id, [
					'cancel_at_period_end' => 'true',
					'metadata[hss_change]' => 'cancel_requested',
				] );
				if ( is_wp_error( $res ) ) { return $res; }
				return 'Set to cancel at the end of the current billing period.';

			case 'pause':
				$res = HSS_Stripe::update_subscription( $sub_id, [
					'pause_collection[behavior]' => 'void',
				] );
				if ( is_wp_error( $res ) ) { return $res; }
				return 'Subscription paused — no invoices until resumed.';

			case 'resume':
				$res = HSS_Stripe::update_subscription( $sub_id, [
					'pause_collection' => '', // empty string clears the pause
				] );
				if ( is_wp_error( $res ) ) { return $res; }
				return 'Subscription resumed.';

			case 'plan_change':
				$plan_key = $req->requested_plan_key;
				$dogs     = (int) $req->requested_dogs ?: (int) $sub_row->dog_count;
				$dogs     = max( 1, min( 3, $dogs ) );
				$amount   = HSS_Config::amount_cents( $plan_key, $dogs );
				if ( ! $amount ) {
					return new WP_Error( 'hss_bad_plan', 'The requested plan looks invalid — set it manually in Stripe.' );
				}

				// We need the current item id and its product to build a new inline price.
				$sub = HSS_Stripe::get_subscription( $sub_id );
				if ( is_wp_error( $sub ) ) { return $sub; }
				$item    = $sub['items']['data'][0] ?? [];
				$item_id = $item['id'] ?? '';
				$product = '';
				if ( isset( $item['price']['product'] ) ) {
					$product = is_array( $item['price']['product'] )
						? ( $item['price']['product']['id'] ?? '' )
						: $item['price']['product'];
				}
				if ( ! $item_id || ! $product ) {
					return new WP_Error( 'hss_no_item', 'Could not read the current subscription price — change it manually in Stripe.' );
				}

				$res = HSS_Stripe::update_subscription( $sub_id, [
					'items[0][id]'                               => $item_id,
					'items[0][price_data][currency]'             => HSS_Config::CURRENCY,
					'items[0][price_data][product]'              => $product,
					'items[0][price_data][unit_amount]'          => $amount,
					'items[0][price_data][recurring][interval]'  => HSS_Config::INTERVAL,
					'proration_behavior'                         => 'create_prorations',
					'metadata[plan_key]'                         => $plan_key,
					'metadata[dog_count]'                        => $dogs,
					'metadata[hss_user_id]'                      => (int) $req->user_id,
				] );
				if ( is_wp_error( $res ) ) { return $res; }
				return 'Updated to ' . HSS_Config::plan_label( $plan_key, $dogs ) . ' (prorated on the next invoice).';
		}

		return 'No change applied.';
	}

	/* ── Display helper ───────────────────────────────────────────────── */

	/** Human summary of what was requested, e.g. "Change plan → Weekly (2 dogs)". */
	public static function summary( $req ) {
		$label = self::type_label( $req->type );
		if ( $req->type === 'plan_change' && $req->requested_plan_key ) {
			$plan = HSS_Config::plan( $req->requested_plan_key );
			$name = $plan ? $plan['label'] : $req->requested_plan_key;
			$label .= ' → ' . $name;
			if ( $req->requested_dogs ) {
				$label .= ' (' . (int) $req->requested_dogs . ( (int) $req->requested_dogs === 1 ? ' dog' : ' dogs' ) . ')';
			}
		}
		return $label;
	}
}
