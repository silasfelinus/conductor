<?php
/**
 * Custom database tables for operational data.
 * @package hss-portal
 */
if ( ! defined( 'ABSPATH' ) ) { exit; }

class HSS_DB {

	const SCHEMA_VERSION = '1.3.0';
	const OPTION_VERSION = 'hss_portal_schema_version';

	public static function t( $name ) {
		global $wpdb;
		return $wpdb->prefix . 'hss_' . $name;
	}

	public static function install() {
		global $wpdb;
		require_once ABSPATH . 'wp-admin/includes/upgrade.php';
		$charset = $wpdb->get_charset_collate();

		$customers = self::t( 'customers' );
		$subs      = self::t( 'subscriptions' );
		$invoices  = self::t( 'invoices' );
		$quotes    = self::t( 'quote_requests' );
		$visits    = self::t( 'service_visits' );
		$requests  = self::t( 'change_requests' );

		dbDelta( "CREATE TABLE $customers (
			id BIGINT UNSIGNED NOT NULL AUTO_INCREMENT,
			user_id BIGINT UNSIGNED NOT NULL DEFAULT 0,
			stripe_customer_id VARCHAR(64) NOT NULL DEFAULT '',
			name VARCHAR(190) NOT NULL DEFAULT '',
			email VARCHAR(190) NOT NULL DEFAULT '',
			phone VARCHAR(40) NOT NULL DEFAULT '',
			address VARCHAR(255) NOT NULL DEFAULT '',
			city VARCHAR(120) NOT NULL DEFAULT '',
			dog_count TINYINT UNSIGNED NOT NULL DEFAULT 1,
			yard_notes TEXT NULL,
			gate_notes TEXT NULL,
			pet_notes TEXT NULL,
			sms_opt_in TINYINT(1) NOT NULL DEFAULT 0,
			status VARCHAR(20) NOT NULL DEFAULT 'active',
			created_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
			PRIMARY KEY (id),
			KEY user_id (user_id),
			KEY stripe_customer_id (stripe_customer_id)
		) $charset;" );

		dbDelta( "CREATE TABLE $subs (
			id BIGINT UNSIGNED NOT NULL AUTO_INCREMENT,
			user_id BIGINT UNSIGNED NOT NULL DEFAULT 0,
			customer_id BIGINT UNSIGNED NOT NULL DEFAULT 0,
			stripe_subscription_id VARCHAR(64) NOT NULL DEFAULT '',
			plan_key VARCHAR(40) NOT NULL DEFAULT '',
			dog_count TINYINT UNSIGNED NOT NULL DEFAULT 1,
			amount_cents INT UNSIGNED NOT NULL DEFAULT 0,
			status VARCHAR(40) NOT NULL DEFAULT '',
			current_period_end DATETIME NULL,
			created_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
			updated_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
			PRIMARY KEY (id),
			UNIQUE KEY stripe_subscription_id (stripe_subscription_id),
			KEY user_id (user_id)
		) $charset;" );

		dbDelta( "CREATE TABLE $invoices (
			id BIGINT UNSIGNED NOT NULL AUTO_INCREMENT,
			user_id BIGINT UNSIGNED NOT NULL DEFAULT 0,
			customer_id BIGINT UNSIGNED NOT NULL DEFAULT 0,
			stripe_invoice_id VARCHAR(64) NOT NULL DEFAULT '',
			number VARCHAR(64) NOT NULL DEFAULT '',
			amount_cents INT UNSIGNED NOT NULL DEFAULT 0,
			status VARCHAR(40) NOT NULL DEFAULT '',
			description VARCHAR(255) NOT NULL DEFAULT '',
			hosted_url TEXT NULL,
			pdf_url TEXT NULL,
			created_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
			PRIMARY KEY (id),
			UNIQUE KEY stripe_invoice_id (stripe_invoice_id),
			KEY user_id (user_id)
		) $charset;" );

		dbDelta( "CREATE TABLE $quotes (
			id BIGINT UNSIGNED NOT NULL AUTO_INCREMENT,
			name VARCHAR(190) NOT NULL DEFAULT '',
			email VARCHAR(190) NOT NULL DEFAULT '',
			phone VARCHAR(40) NOT NULL DEFAULT '',
			city VARCHAR(120) NOT NULL DEFAULT '',
			dogs VARCHAR(10) NOT NULL DEFAULT '',
			interest VARCHAR(60) NOT NULL DEFAULT '',
			message TEXT NULL,
			status VARCHAR(20) NOT NULL DEFAULT 'new',
			created_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
			PRIMARY KEY (id),
			KEY status (status)
		) $charset;" );

		dbDelta( "CREATE TABLE $visits (
			id BIGINT UNSIGNED NOT NULL AUTO_INCREMENT,
			user_id BIGINT UNSIGNED NOT NULL DEFAULT 0,
			customer_id BIGINT UNSIGNED NOT NULL DEFAULT 0,
			subscription_id BIGINT UNSIGNED NOT NULL DEFAULT 0,
			plan_key VARCHAR(40) NOT NULL DEFAULT '',
			scheduled_date DATE NULL,
			time_window VARCHAR(40) NOT NULL DEFAULT '',
			crew VARCHAR(120) NOT NULL DEFAULT '',
			status VARCHAR(20) NOT NULL DEFAULT 'scheduled',
			customer_note TEXT NULL,
			admin_notes TEXT NULL,
			notify TINYINT(1) NOT NULL DEFAULT 1,
			completed_at DATETIME NULL,
			created_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
			updated_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
			PRIMARY KEY (id),
			KEY user_id (user_id),
			KEY scheduled_date (scheduled_date),
			KEY status (status)
		) $charset;" );

		dbDelta( "CREATE TABLE $requests (
			id BIGINT UNSIGNED NOT NULL AUTO_INCREMENT,
			user_id BIGINT UNSIGNED NOT NULL DEFAULT 0,
			customer_id BIGINT UNSIGNED NOT NULL DEFAULT 0,
			type VARCHAR(20) NOT NULL DEFAULT 'other',
			current_plan_key VARCHAR(40) NOT NULL DEFAULT '',
			requested_plan_key VARCHAR(40) NOT NULL DEFAULT '',
			requested_dogs TINYINT UNSIGNED NOT NULL DEFAULT 0,
			message TEXT NULL,
			status VARCHAR(20) NOT NULL DEFAULT 'new',
			admin_note TEXT NULL,
			created_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
			updated_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
			resolved_at DATETIME NULL,
			PRIMARY KEY (id),
			KEY user_id (user_id),
			KEY status (status)
		) $charset;" );

		update_option( self::OPTION_VERSION, self::SCHEMA_VERSION );
	}

	public static function maybe_upgrade() {
		if ( get_option( self::OPTION_VERSION ) !== self::SCHEMA_VERSION ) {
			self::install();
		}
	}
}
