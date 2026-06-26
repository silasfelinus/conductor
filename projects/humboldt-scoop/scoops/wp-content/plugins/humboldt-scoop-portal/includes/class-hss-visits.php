<?php
/**
 * Service visits — scheduling and logging of yard cleanups.
 *
 * Visits are created and advanced by the business from WP Admin. Customers
 * see their next visit and recent history in the portal dashboard. Each
 * status change can notify the customer by email (see HSS_Mail).
 *
 * @package hss-portal
 */
if ( ! defined( 'ABSPATH' ) ) { exit; }

class HSS_Visits {

	public static function table() {
		return HSS_DB::t( 'service_visits' );
	}

	/** Status machine: key => human label. */
	public static function statuses() {
		return [
			'scheduled' => 'Scheduled',
			'enroute'   => 'On the way',
			'completed' => 'Completed',
			'skipped'   => 'Skipped',
			'canceled'  => 'Canceled',
		];
	}

	public static function status_label( $status ) {
		$map = self::statuses();
		return $map[ $status ] ?? ucfirst( (string) $status );
	}

	public static function is_valid_status( $status ) {
		return array_key_exists( $status, self::statuses() );
	}

	/* ── Writes ───────────────────────────────────────────────────────── */

	/**
	 * Create a visit. Snapshots the customer's active plan if present.
	 * @return int new visit id (0 on failure).
	 */
	public static function create( $data ) {
		global $wpdb;

		$defaults = [
			'user_id'         => 0,
			'customer_id'     => 0,
			'subscription_id' => 0,
			'plan_key'        => '',
			'scheduled_date'  => null,
			'time_window'     => '',
			'crew'            => '',
			'status'          => 'scheduled',
			'customer_note'   => '',
			'admin_notes'     => '',
			'notify'          => 1,
			'created_at'      => current_time( 'mysql' ),
			'updated_at'      => current_time( 'mysql' ),
		];
		$row = array_merge( $defaults, $data );

		// Snapshot plan context from the customer's active subscription.
		if ( $row['user_id'] && ( ! $row['plan_key'] || ! $row['subscription_id'] ) ) {
			$sub = HSS_Portal::active_subscription( (int) $row['user_id'] );
			if ( $sub ) {
				if ( ! $row['plan_key'] )        { $row['plan_key'] = $sub->plan_key; }
				if ( ! $row['subscription_id'] ) { $row['subscription_id'] = (int) $sub->id; }
			}
		}

		$ok = $wpdb->insert( self::table(), $row );
		return $ok ? (int) $wpdb->insert_id : 0;
	}

	public static function update( $id, $data ) {
		global $wpdb;
		$data['updated_at'] = current_time( 'mysql' );
		return $wpdb->update( self::table(), $data, [ 'id' => (int) $id ] );
	}

	/**
	 * Advance a visit to a new status. Stamps completed_at for terminal
	 * states and emails the customer when the visit opts into notifications.
	 *
	 * @param int    $id
	 * @param string $status one of statuses()
	 * @param array  $opts   optional: 'customer_note' to attach a note.
	 * @return bool
	 */
	public static function set_status( $id, $status, $opts = [] ) {
		if ( ! self::is_valid_status( $status ) ) { return false; }
		$visit = self::get( $id );
		if ( ! $visit ) { return false; }

		$data = [ 'status' => $status ];
		if ( in_array( $status, [ 'completed', 'skipped' ], true ) ) {
			$data['completed_at'] = current_time( 'mysql' );
		}
		if ( isset( $opts['customer_note'] ) && $opts['customer_note'] !== '' ) {
			$data['customer_note'] = $opts['customer_note'];
		}

		self::update( $id, $data );

		self::notify( self::get( $id ) ); // reload with new values, then notify
		return true;
	}

	/**
	 * Notify the customer about a visit by every enabled channel (email +
	 * opted-in SMS). Respects the per-visit notify flag; each channel
	 * additionally checks its own configuration/consent.
	 */
	public static function notify( $visit ) {
		if ( ! $visit || (int) $visit->notify !== 1 ) { return; }
		if ( class_exists( 'HSS_Mail' ) ) { HSS_Mail::visit_status( $visit ); }
		if ( class_exists( 'HSS_Sms' ) )  { HSS_Sms::visit_status( $visit ); }
	}

	/* ── Reads ────────────────────────────────────────────────────────── */

	public static function get( $id ) {
		global $wpdb;
		$t = self::table();
		return $wpdb->get_row( $wpdb->prepare( "SELECT * FROM $t WHERE id = %d", (int) $id ) );
	}

	/** The customer's soonest open visit (today or later, or undated). */
	public static function next_for_user( $user_id ) {
		global $wpdb;
		$t = self::table();
		$today = current_time( 'Y-m-d' );
		return $wpdb->get_row( $wpdb->prepare(
			"SELECT * FROM $t
			 WHERE user_id = %d
			   AND status IN ('scheduled','enroute')
			   AND ( scheduled_date IS NULL OR scheduled_date >= %s )
			 ORDER BY ( scheduled_date IS NULL ), scheduled_date ASC, id ASC
			 LIMIT 1",
			$user_id, $today
		) );
	}

	/** The customer's recent completed/skipped visits. */
	public static function history_for_user( $user_id, $limit = 6 ) {
		global $wpdb;
		$t = self::table();
		return $wpdb->get_results( $wpdb->prepare(
			"SELECT * FROM $t
			 WHERE user_id = %d AND status IN ('completed','skipped')
			 ORDER BY scheduled_date DESC, id DESC
			 LIMIT %d",
			$user_id, $limit
		) );
	}

	/** Open visits across all customers (admin queue). */
	public static function upcoming( $limit = 200 ) {
		global $wpdb;
		$t = self::table();
		return $wpdb->get_results( $wpdb->prepare(
			"SELECT * FROM $t
			 WHERE status IN ('scheduled','enroute')
			 ORDER BY ( scheduled_date IS NULL ), scheduled_date ASC, id ASC
			 LIMIT %d",
			$limit
		) );
	}

	/** Closed visits across all customers (admin log). */
	public static function recent( $limit = 100 ) {
		global $wpdb;
		$t = self::table();
		return $wpdb->get_results( $wpdb->prepare(
			"SELECT * FROM $t
			 WHERE status IN ('completed','skipped','canceled')
			 ORDER BY COALESCE( completed_at, updated_at ) DESC
			 LIMIT %d",
			$limit
		) );
	}

	public static function count_open() {
		global $wpdb;
		$t = self::table();
		return (int) $wpdb->get_var( "SELECT COUNT(*) FROM $t WHERE status IN ('scheduled','enroute')" );
	}
}
