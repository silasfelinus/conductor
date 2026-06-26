<?php
/**
 * Customer records: bridge WordPress users to hss_customers rows and
 * to Stripe customer objects.
 * @package hss-portal
 */
if ( ! defined( 'ABSPATH' ) ) { exit; }

class HSS_Customers {

	/** Get the customer row for a WP user, creating it if missing. */
	public static function get_or_create( $user_id ) {
		$row = self::get_by_user( $user_id );
		if ( $row ) { return $row; }

		$user = get_userdata( $user_id );
		if ( ! $user ) { return null; }

		global $wpdb;
		$wpdb->insert( HSS_DB::t( 'customers' ), [
			'user_id' => $user_id,
			'name'    => $user->display_name ?: $user->user_login,
			'email'   => $user->user_email,
			'status'  => 'active',
		] );
		return self::get_by_user( $user_id );
	}

	public static function get_by_user( $user_id ) {
		global $wpdb;
		$t = HSS_DB::t( 'customers' );
		return $wpdb->get_row( $wpdb->prepare( "SELECT * FROM $t WHERE user_id = %d", $user_id ) );
	}

	public static function get_by_stripe_id( $stripe_customer_id ) {
		global $wpdb;
		$t = HSS_DB::t( 'customers' );
		return $wpdb->get_row( $wpdb->prepare( "SELECT * FROM $t WHERE stripe_customer_id = %s", $stripe_customer_id ) );
	}

	public static function update( $id, $data ) {
		global $wpdb;
		return $wpdb->update( HSS_DB::t( 'customers' ), $data, [ 'id' => $id ] );
	}

	/**
	 * Ensure the customer has a Stripe customer object; create it if not.
	 * @return string|WP_Error the Stripe customer id.
	 */
	public static function ensure_stripe_customer( $row ) {
		if ( ! empty( $row->stripe_customer_id ) ) {
			return $row->stripe_customer_id;
		}
		$res = HSS_Stripe::create_customer( [
			'email'           => $row->email,
			'name'            => $row->name,
			'phone'           => $row->phone,
			'metadata[hss_user_id]'     => $row->user_id,
			'metadata[hss_customer_id]' => $row->id,
		] );
		if ( is_wp_error( $res ) ) { return $res; }

		self::update( $row->id, [ 'stripe_customer_id' => $res['id'] ] );
		update_user_meta( $row->user_id, 'hss_stripe_customer_id', $res['id'] );
		return $res['id'];
	}

	/**
	 * Register a brand-new customer (WP user + customer row) and sign in.
	 * @return int|WP_Error new user id.
	 */
	public static function register( $name, $email, $password, $extra = [] ) {
		if ( ! is_email( $email ) ) {
			return new WP_Error( 'hss_bad_email', 'Please enter a valid email address.' );
		}
		if ( email_exists( $email ) ) {
			return new WP_Error( 'hss_email_exists', 'An account with that email already exists. Try logging in.' );
		}
		if ( strlen( $password ) < 8 ) {
			return new WP_Error( 'hss_weak_password', 'Please use a password of at least 8 characters.' );
		}

		$username = self::unique_username( $email );
		$user_id  = wp_insert_user( [
			'user_login'   => $username,
			'user_email'   => $email,
			'user_pass'    => $password,
			'display_name' => $name ?: $username,
			'first_name'   => $name,
			'role'         => 'subscriber',
		] );
		if ( is_wp_error( $user_id ) ) { return $user_id; }

		global $wpdb;
		$wpdb->insert( HSS_DB::t( 'customers' ), [
			'user_id' => $user_id,
			'name'    => $name,
			'email'   => $email,
			'phone'   => isset( $extra['phone'] ) ? sanitize_text_field( $extra['phone'] ) : '',
			'city'    => isset( $extra['city'] ) ? sanitize_text_field( $extra['city'] ) : '',
			'status'  => 'active',
		] );

		return $user_id;
	}

	protected static function unique_username( $email ) {
		$base = sanitize_user( current( explode( '@', $email ) ), true );
		$base = $base ?: 'customer';
		$name = $base; $i = 1;
		while ( username_exists( $name ) ) { $name = $base . $i; $i++; }
		return $name;
	}
}
