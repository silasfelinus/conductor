<?php
/**
 * Admin dashboard: overview, customers, subscriptions, invoices,
 * quote requests, and a settings/status page.
 * @package hss-portal
 */
if ( ! defined( 'ABSPATH' ) ) { exit; }

class HSS_Admin {

	const CAP  = 'manage_options';
	const SLUG = 'hss-portal';

	public static function init() {
		add_action( 'admin_menu', [ __CLASS__, 'menu' ] );
		add_action( 'admin_enqueue_scripts', [ __CLASS__, 'styles' ] );
	}

	public static function menu() {
		add_menu_page( 'Scoop Solutions', 'Scoop Solutions', self::CAP, self::SLUG, [ __CLASS__, 'page_overview' ], 'dashicons-pets', 26 );
		add_submenu_page( self::SLUG, 'Overview', 'Overview', self::CAP, self::SLUG, [ __CLASS__, 'page_overview' ] );
		add_submenu_page( self::SLUG, 'Customers', 'Customers', self::CAP, self::SLUG . '-customers', [ __CLASS__, 'page_customers' ] );
		add_submenu_page( self::SLUG, 'Subscriptions', 'Subscriptions', self::CAP, self::SLUG . '-subscriptions', [ __CLASS__, 'page_subscriptions' ] );
		add_submenu_page( self::SLUG, 'Visits', 'Visits', self::CAP, self::SLUG . '-visits', [ __CLASS__, 'page_visits' ] );
		add_submenu_page( self::SLUG, 'Invoices', 'Invoices', self::CAP, self::SLUG . '-invoices', [ __CLASS__, 'page_invoices' ] );
		add_submenu_page( self::SLUG, 'Change Requests', 'Change Requests', self::CAP, self::SLUG . '-requests', [ __CLASS__, 'page_requests' ] );
		add_submenu_page( self::SLUG, 'Quote Requests', 'Quote Requests', self::CAP, self::SLUG . '-quotes', [ __CLASS__, 'page_quotes' ] );
		add_submenu_page( self::SLUG, 'Settings', 'Settings', self::CAP, self::SLUG . '-settings', [ __CLASS__, 'page_settings' ] );
	}

	public static function styles( $hook ) {
		if ( strpos( $hook, self::SLUG ) === false ) { return; }
		$css = '.hss-adm-cards{display:flex;gap:16px;flex-wrap:wrap;margin:18px 0}'
			. '.hss-adm-card{background:#fff;border:1px solid #dcd7cf;border-left:4px solid #8a3b2c;border-radius:10px;padding:16px 20px;min-width:170px}'
			. '.hss-adm-card .n{font-size:2rem;font-weight:800;color:#6b2c20;line-height:1}'
			. '.hss-adm-card .l{color:#5d534d;font-size:.85rem;text-transform:uppercase;letter-spacing:.04em;margin-top:4px}'
			. '.hss-adm table{margin-top:10px}'
			. '.hss-pill{display:inline-block;padding:2px 9px;border-radius:999px;font-size:.75rem;font-weight:700;text-transform:capitalize}'
			. '.hss-pill.ok{background:#e7f3ee;color:#1d6b52}.hss-pill.warn{background:#fdf3e7;color:#8a5a1c}.hss-pill.bad{background:#fbeae7;color:#8a3b2c}.hss-pill.neutral{background:#f1efec;color:#6d635c}'
			. '.hss-status-ok{color:#1d6b52;font-weight:700}.hss-status-no{color:#b3261e;font-weight:700}'
			. '.hss-code{background:#f6f7f7;border:1px solid #dcd7cf;border-radius:6px;padding:2px 6px;font-family:monospace}';
		wp_add_inline_style( 'common', $css );
	}

	protected static function open( $title ) {
		echo '<div class="wrap hss-adm"><h1>' . esc_html( $title ) . '</h1>';
	}
	protected static function close() { echo '</div>'; }

	protected static function count( $table, $where = '' ) {
		global $wpdb;
		$t = HSS_DB::t( $table );
		return (int) $wpdb->get_var( "SELECT COUNT(*) FROM $t" . ( $where ? " WHERE $where" : '' ) );
	}

	protected static function pill_class( $status ) {
		$status = strtolower( $status );
		if ( in_array( $status, [ 'active', 'paid', 'trialing', 'completed', 'approved' ], true ) ) { return 'ok'; }
		if ( in_array( $status, [ 'past_due', 'open', 'unpaid', 'new', 'scheduled', 'enroute' ], true ) ) { return 'warn'; }
		if ( in_array( $status, [ 'canceled', 'void', 'uncollectible', 'failed', 'skipped', 'declined' ], true ) ) { return 'bad'; }
		return 'neutral';
	}

	/* ── Overview ─────────────────────────────────────────────────────── */
	public static function page_overview() {
		global $wpdb;
		self::open( 'Scoop Solutions — Overview' );

		$active_subs = self::count( 'subscriptions', "status IN ('active','trialing','past_due')" );
		$st = HSS_DB::t( 'subscriptions' );
		$mrr = (int) $wpdb->get_var( "SELECT COALESCE(SUM(amount_cents),0) FROM $st WHERE status IN ('active','trialing')" );

		echo '<div class="hss-adm-cards">';
		self::card( self::count( 'customers' ), 'Customers' );
		self::card( $active_subs, 'Active plans' );
		self::card( '$' . number_format( $mrr / 100, 0 ), 'Monthly recurring' );
		self::card( HSS_Visits::count_open(), 'Open visits' );
		self::card( HSS_Change_Requests::count_open(), 'Open requests' );
		self::card( self::count( 'quote_requests', "status='new'" ), 'New quotes' );
		echo '</div>';

		if ( ! HSS_Config::is_configured() ) {
			echo '<div class="notice notice-warning"><p><strong>Stripe is not configured yet.</strong> Add your keys (see <a href="' . esc_url( admin_url( 'admin.php?page=' . self::SLUG . '-settings' ) ) . '">Settings</a>) to enable online payments. The brochure site and quote form work without it.</p></div>';
		} elseif ( HSS_Config::is_test_mode() ) {
			echo '<div class="notice notice-info"><p>Stripe is connected in <strong>test mode</strong>. Switch to live keys when you\'re ready to take real payments.</p></div>';
		} else {
			echo '<div class="notice notice-success"><p>Stripe is connected in <strong>live mode</strong>.</p></div>';
		}

		echo '<h2>Recent quote requests</h2>';
		$qt = HSS_DB::t( 'quote_requests' );
		$rows = $wpdb->get_results( "SELECT * FROM $qt ORDER BY created_at DESC LIMIT 5" );
		self::quotes_table( $rows );

		self::close();
	}

	protected static function card( $n, $l ) {
		echo '<div class="hss-adm-card"><div class="n">' . esc_html( $n ) . '</div><div class="l">' . esc_html( $l ) . '</div></div>';
	}

	/* ── Customers ────────────────────────────────────────────────────── */
	public static function page_customers() {
		global $wpdb;
		self::open( 'Customers' );
		$t = HSS_DB::t( 'customers' );
		$rows = $wpdb->get_results( "SELECT * FROM $t ORDER BY created_at DESC LIMIT 200" );
		if ( ! $rows ) { echo '<p>No customers yet.</p>'; self::close(); return; }

		echo '<table class="widefat striped"><thead><tr><th>Name</th><th>Email</th><th>Phone</th><th>City</th><th>Dogs</th><th>Address</th><th>Stripe</th><th>Joined</th></tr></thead><tbody>';
		foreach ( $rows as $r ) {
			echo '<tr>';
			echo '<td><strong>' . esc_html( $r->name ) . '</strong></td>';
			echo '<td>' . esc_html( $r->email ) . '</td>';
			echo '<td>' . esc_html( $r->phone ) . '</td>';
			echo '<td>' . esc_html( $r->city ) . '</td>';
			echo '<td>' . esc_html( $r->dog_count ) . '</td>';
			echo '<td>' . esc_html( $r->address ) . '</td>';
			echo '<td>' . ( $r->stripe_customer_id ? '<span class="hss-pill ok">linked</span>' : '<span class="hss-pill neutral">—</span>' ) . '</td>';
			echo '<td>' . esc_html( date_i18n( 'M j, Y', strtotime( $r->created_at ) ) ) . '</td>';
			echo '</tr>';
			if ( $r->gate_notes || $r->yard_notes || $r->pet_notes ) {
				echo '<tr><td colspan="8" style="color:#5d534d;font-size:.9em;background:#fbf9f5">';
				$notes = array_filter( [
					$r->gate_notes ? 'Gate: ' . $r->gate_notes : '',
					$r->yard_notes ? 'Yard: ' . $r->yard_notes : '',
					$r->pet_notes ? 'Pets: ' . $r->pet_notes : '',
				] );
				echo esc_html( implode( '  ·  ', $notes ) );
				echo '</td></tr>';
			}
		}
		echo '</tbody></table>';
		self::close();
	}

	/* ── Subscriptions ────────────────────────────────────────────────── */
	public static function page_subscriptions() {
		global $wpdb;
		self::open( 'Subscriptions' );
		$t = HSS_DB::t( 'subscriptions' );
		$c = HSS_DB::t( 'customers' );
		$rows = $wpdb->get_results( "SELECT s.*, c.name, c.email FROM $t s LEFT JOIN $c c ON c.id = s.customer_id ORDER BY s.updated_at DESC LIMIT 200" );
		if ( ! $rows ) { echo '<p>No subscriptions yet.</p>'; self::close(); return; }

		echo '<table class="widefat striped"><thead><tr><th>Customer</th><th>Plan</th><th>Dogs</th><th>Amount</th><th>Status</th><th>Next billing</th><th>Stripe ID</th></tr></thead><tbody>';
		foreach ( $rows as $r ) {
			echo '<tr>';
			echo '<td><strong>' . esc_html( $r->name ?: ( '#' . $r->user_id ) ) . '</strong><br><span style="color:#5d534d">' . esc_html( $r->email ) . '</span></td>';
			echo '<td>' . esc_html( HSS_Config::plan_label( $r->plan_key ) ) . '</td>';
			echo '<td>' . esc_html( $r->dog_count ) . '</td>';
			echo '<td>$' . esc_html( number_format( $r->amount_cents / 100, 2 ) ) . '/mo</td>';
			echo '<td><span class="hss-pill ' . esc_attr( self::pill_class( $r->status ) ) . '">' . esc_html( str_replace( '_', ' ', $r->status ) ) . '</span></td>';
			echo '<td>' . ( $r->current_period_end ? esc_html( date_i18n( 'M j, Y', strtotime( $r->current_period_end ) ) ) : '—' ) . '</td>';
			echo '<td><span class="hss-code">' . esc_html( $r->stripe_subscription_id ) . '</span></td>';
			echo '</tr>';
		}
		echo '</tbody></table>';
		self::close();
	}

	/* ── Visits: schedule + log ───────────────────────────────────────── */
	public static function page_visits() {
		global $wpdb;

		// Handle: create a new visit.
		if ( ( $_POST['hss_action'] ?? '' ) === 'visit_new' && check_admin_referer( 'hss_visit_new' ) ) {
			$cid  = (int) ( $_POST['customer_id'] ?? 0 );
			$ct   = HSS_DB::t( 'customers' );
			$cust = $wpdb->get_row( $wpdb->prepare( "SELECT * FROM $ct WHERE id = %d", $cid ) );
			if ( $cust ) {
				$date = sanitize_text_field( $_POST['scheduled_date'] ?? '' );
				$notify = empty( $_POST['notify'] ) ? 0 : 1;
				$vid = HSS_Visits::create( [
					'user_id'       => (int) $cust->user_id,
					'customer_id'   => (int) $cust->id,
					'scheduled_date'=> $date !== '' ? $date : null,
					'time_window'   => sanitize_text_field( $_POST['time_window'] ?? '' ),
					'crew'          => sanitize_text_field( $_POST['crew'] ?? '' ),
					'customer_note' => sanitize_textarea_field( $_POST['customer_note'] ?? '' ),
					'admin_notes'   => sanitize_textarea_field( $_POST['admin_notes'] ?? '' ),
					'notify'        => $notify,
					'status'        => 'scheduled',
				] );
				if ( $vid && $notify ) {
					HSS_Visits::notify( HSS_Visits::get( $vid ) );
				}
				echo '<div class="notice notice-success is-dismissible"><p>Visit scheduled'
					. ( $notify ? ' and the customer was emailed.' : '.' ) . '</p></div>';
			} else {
				echo '<div class="notice notice-error is-dismissible"><p>Pick a customer to schedule a visit.</p></div>';
			}
		}

		// Handle: advance a visit's status.
		if ( ( $_POST['hss_action'] ?? '' ) === 'visit_status' && check_admin_referer( 'hss_visit_action' ) ) {
			$vid  = (int) ( $_POST['visit'] ?? 0 );
			$to   = sanitize_text_field( $_POST['to'] ?? '' );
			$note = sanitize_textarea_field( $_POST['note'] ?? '' );
			if ( HSS_Visits::is_valid_status( $to ) && HSS_Visits::set_status( $vid, $to, [ 'customer_note' => $note ] ) ) {
				$v = HSS_Visits::get( $vid );
				$emailed = ( $v && (int) $v->notify === 1 && in_array( $to, [ 'scheduled', 'enroute', 'completed', 'skipped' ], true ) );
				echo '<div class="notice notice-success is-dismissible"><p>Visit marked &ldquo;'
					. esc_html( HSS_Visits::status_label( $to ) ) . '&rdquo;'
					. ( $emailed ? ' — customer emailed.' : '.' ) . '</p></div>';
			}
		}

		self::open( 'Visits — Schedule &amp; Log' );

		// Customer lookup map for display.
		$ct        = HSS_DB::t( 'customers' );
		$customers = $wpdb->get_results( "SELECT id, user_id, name, email, city, address FROM $ct ORDER BY name ASC" );
		$cmap      = [];
		foreach ( $customers as $c ) { $cmap[ (int) $c->id ] = $c; }

		/* Schedule form */
		echo '<h2>Schedule a visit</h2>';
		if ( ! $customers ) {
			echo '<p>No customers yet. Once someone registers in the portal, you can schedule visits for them here.</p>';
		} else {
			echo '<form method="post" style="background:#fff;border:1px solid #dcd7cf;border-radius:10px;padding:16px 20px;max-width:680px;">';
			wp_nonce_field( 'hss_visit_new' );
			echo '<input type="hidden" name="hss_action" value="visit_new">';

			echo '<p><label><strong>Customer</strong><br><select name="customer_id" required style="min-width:320px;">';
			echo '<option value="">— select —</option>';
			foreach ( $customers as $c ) {
				$tag = $c->name ?: ( $c->email ?: ( '#' . $c->user_id ) );
				if ( $c->city ) { $tag .= ' (' . $c->city . ')'; }
				echo '<option value="' . esc_attr( $c->id ) . '">' . esc_html( $tag ) . '</option>';
			}
			echo '</select></label></p>';

			echo '<p style="display:flex;gap:18px;flex-wrap:wrap;">';
			echo '<label><strong>Date</strong><br><input type="date" name="scheduled_date" value="' . esc_attr( current_time( 'Y-m-d' ) ) . '"></label>';
			echo '<label><strong>Time window</strong><br><input type="text" name="time_window" list="hss-windows" placeholder="e.g. Morning" style="width:160px;"></label>';
			echo '<datalist id="hss-windows"><option value="Morning"><option value="Midday"><option value="Afternoon"><option value="Evening"></datalist>';
			echo '<label><strong>Crew / scooper</strong><br><input type="text" name="crew" placeholder="optional" style="width:160px;"></label>';
			echo '</p>';

			echo '<p><label><strong>Note to customer</strong> <span style="color:#5d534d;font-weight:400;">(shown to them, included in email)</span><br>'
				. '<textarea name="customer_note" rows="2" style="width:100%;max-width:640px;" placeholder="optional"></textarea></label></p>';
			echo '<p><label><strong>Internal notes</strong> <span style="color:#5d534d;font-weight:400;">(admin only)</span><br>'
				. '<textarea name="admin_notes" rows="2" style="width:100%;max-width:640px;" placeholder="optional"></textarea></label></p>';

			echo '<p><label><input type="checkbox" name="notify" value="1" checked> Email the customer that they&rsquo;re scheduled</label></p>';
			echo '<p><button type="submit" class="button button-primary">Schedule visit</button></p>';
			echo '</form>';
		}

		/* Upcoming queue */
		echo '<h2 style="margin-top:28px;">Upcoming &amp; in progress</h2>';
		$upcoming = HSS_Visits::upcoming();
		if ( ! $upcoming ) {
			echo '<p>No open visits. Schedule one above.</p>';
		} else {
			echo '<table class="widefat striped"><thead><tr><th>Date</th><th>Window</th><th>Customer</th><th>Crew</th><th>Status</th><th>Note</th><th>Update</th></tr></thead><tbody>';
			foreach ( $upcoming as $v ) {
				$c = $cmap[ (int) $v->customer_id ] ?? null;
				echo '<tr>';
				echo '<td>' . ( $v->scheduled_date ? esc_html( date_i18n( 'D, M j', strtotime( $v->scheduled_date ) ) ) : '—' ) . '</td>';
				echo '<td>' . esc_html( $v->time_window ?: '—' ) . '</td>';
				echo '<td><strong>' . esc_html( $c ? ( $c->name ?: $c->email ) : ( '#' . $v->user_id ) ) . '</strong>'
					. ( $c && $c->address ? '<br><span style="color:#5d534d;font-size:.9em;">' . esc_html( $c->address ) . '</span>' : '' ) . '</td>';
				echo '<td>' . esc_html( $v->crew ?: '—' ) . '</td>';
				echo '<td><span class="hss-pill ' . esc_attr( self::pill_class( $v->status ) ) . '">' . esc_html( HSS_Visits::status_label( $v->status ) ) . '</span>'
					. ( (int) $v->notify === 1 ? '' : '<br><span style="color:#8a5a1c;font-size:.8em;">no email</span>' ) . '</td>';
				echo '<td style="max-width:220px;color:#5d534d;">' . esc_html( $v->customer_note ?: ( $v->admin_notes ? '(internal) ' . $v->admin_notes : '' ) ) . '</td>';
				echo '<td>';
				echo '<form method="post" style="display:flex;flex-direction:column;gap:6px;min-width:200px;">';
				wp_nonce_field( 'hss_visit_action' );
				echo '<input type="hidden" name="hss_action" value="visit_status">';
				echo '<input type="hidden" name="visit" value="' . esc_attr( $v->id ) . '">';
				echo '<input type="text" name="note" placeholder="note to customer (optional)" style="width:100%;">';
				echo '<span style="display:flex;gap:6px;flex-wrap:wrap;">';
				if ( $v->status === 'scheduled' ) {
					echo '<button class="button button-small" name="to" value="enroute">On the way</button>';
				}
				echo '<button class="button button-small button-primary" name="to" value="completed">Completed</button>';
				echo '<button class="button button-small" name="to" value="skipped">Skip</button>';
				echo '<button class="button button-small" name="to" value="canceled" onclick="return confirm(\'Cancel this visit? No email is sent.\')">Cancel</button>';
				echo '</span>';
				echo '</form>';
				echo '</td>';
				echo '</tr>';
			}
			echo '</tbody></table>';
		}

		/* Completed log */
		echo '<h2 style="margin-top:28px;">Recent log</h2>';
		$recent = HSS_Visits::recent( 60 );
		if ( ! $recent ) {
			echo '<p>No completed visits yet.</p>';
		} else {
			echo '<table class="widefat striped"><thead><tr><th>Date</th><th>Customer</th><th>Crew</th><th>Result</th><th>Note</th></tr></thead><tbody>';
			foreach ( $recent as $v ) {
				$c = $cmap[ (int) $v->customer_id ] ?? null;
				$on = $v->completed_at ?: $v->updated_at;
				echo '<tr>';
				echo '<td>' . esc_html( date_i18n( 'M j, Y', strtotime( $v->scheduled_date ?: $on ) ) ) . '</td>';
				echo '<td>' . esc_html( $c ? ( $c->name ?: $c->email ) : ( '#' . $v->user_id ) ) . '</td>';
				echo '<td>' . esc_html( $v->crew ?: '—' ) . '</td>';
				echo '<td><span class="hss-pill ' . esc_attr( self::pill_class( $v->status ) ) . '">' . esc_html( HSS_Visits::status_label( $v->status ) ) . '</span></td>';
				echo '<td style="max-width:280px;color:#5d534d;">' . esc_html( $v->customer_note ) . '</td>';
				echo '</tr>';
			}
			echo '</tbody></table>';
		}

		self::close();
	}

	/* ── Invoices ─────────────────────────────────────────────────────── */
	public static function page_invoices() {
		global $wpdb;
		self::open( 'Invoices' );
		$t = HSS_DB::t( 'invoices' );
		$c = HSS_DB::t( 'customers' );
		$rows = $wpdb->get_results( "SELECT i.*, c.name, c.email FROM $t i LEFT JOIN $c c ON c.id = i.customer_id ORDER BY i.created_at DESC LIMIT 200" );
		if ( ! $rows ) { echo '<p>No invoices yet.</p>'; self::close(); return; }

		echo '<table class="widefat striped"><thead><tr><th>Date</th><th>Customer</th><th>Number</th><th>Description</th><th>Amount</th><th>Status</th><th></th></tr></thead><tbody>';
		foreach ( $rows as $r ) {
			echo '<tr>';
			echo '<td>' . esc_html( date_i18n( 'M j, Y', strtotime( $r->created_at ) ) ) . '</td>';
			echo '<td>' . esc_html( $r->name ?: ( '#' . $r->user_id ) ) . '</td>';
			echo '<td>' . esc_html( $r->number ) . '</td>';
			echo '<td>' . esc_html( $r->description ) . '</td>';
			echo '<td>$' . esc_html( number_format( $r->amount_cents / 100, 2 ) ) . '</td>';
			echo '<td><span class="hss-pill ' . esc_attr( self::pill_class( $r->status ) ) . '">' . esc_html( $r->status ) . '</span></td>';
			echo '<td>' . ( $r->hosted_url ? '<a href="' . esc_url( $r->hosted_url ) . '" target="_blank" rel="noopener">View</a>' : '' ) . '</td>';
			echo '</tr>';
		}
		echo '</tbody></table>';
		self::close();
	}

	/* ── Change requests (plan change / pause / cancel) ───────────────── */
	public static function page_requests() {
		global $wpdb;

		// Handle: approve / decline.
		if ( ( $_POST['hss_action'] ?? '' ) === 'request_resolve' && check_admin_referer( 'hss_request_resolve' ) ) {
			$rid  = (int) ( $_POST['request'] ?? 0 );
			$to   = sanitize_text_field( $_POST['to'] ?? '' );
			$note = sanitize_textarea_field( $_POST['admin_note'] ?? '' );
			$req  = HSS_Change_Requests::get( $rid );

			if ( $req && HSS_Change_Requests::is_resolution( $to ) ) {
				$stripe_msg = '';
				$blocked    = false;

				// On approval, try to apply the change to Stripe first.
				if ( $to === 'approved' ) {
					$applied = HSS_Change_Requests::apply_to_stripe( $req );
					if ( is_wp_error( $applied ) ) {
						$blocked = true;
						echo '<div class="notice notice-error is-dismissible"><p><strong>Couldn\'t apply to Stripe:</strong> '
							. esc_html( $applied->get_error_message() )
							. ' The request was left open — fix it (or make the change in Stripe) and approve again.</p></div>';
					} else {
						$stripe_msg = (string) $applied;
					}
				}

				if ( ! $blocked && HSS_Change_Requests::set_status( $rid, $to, $note ) ) {
					echo '<div class="notice notice-success is-dismissible"><p>Request marked &ldquo;'
						. esc_html( HSS_Change_Requests::status_label( $to ) ) . '&rdquo; — customer emailed.'
						. ( $stripe_msg ? ' <em>Stripe: ' . esc_html( $stripe_msg ) . '</em>' : '' )
						. '</p></div>';
				}
			}
		}

		self::open( 'Change Requests' );

		// Customer lookup map.
		$ct        = HSS_DB::t( 'customers' );
		$customers = $wpdb->get_results( "SELECT id, user_id, name, email FROM $ct" );
		$cmap      = [];
		foreach ( $customers as $c ) { $cmap[ (int) $c->id ] = $c; }

		echo '<p>Customers request plan changes, pauses, resumes, or cancellations from their portal dashboard. '
			. '<strong>Approving applies the change to Stripe automatically</strong> and emails the customer. '
			. 'If Stripe can\'t be reached, the request stays open so you can retry. Plan changes are prorated; '
			. 'cancellations take effect at the end of the current billing period.</p>';

		/* Pending queue */
		echo '<h2>Pending</h2>';
		$pending = HSS_Change_Requests::pending();
		if ( ! $pending ) {
			echo '<p>No open requests. 🎉</p>';
		} else {
			echo '<table class="widefat striped"><thead><tr><th>Date</th><th>Customer</th><th>Request</th><th>Current plan</th><th>Their note</th><th>Decision</th></tr></thead><tbody>';
			foreach ( $pending as $r ) {
				$c = $cmap[ (int) $r->customer_id ] ?? null;
				$cur = $r->current_plan_key ? HSS_Config::plan_label( $r->current_plan_key ) : '—';
				echo '<tr>';
				echo '<td>' . esc_html( date_i18n( 'M j', strtotime( $r->created_at ) ) ) . '</td>';
				echo '<td><strong>' . esc_html( $c ? ( $c->name ?: $c->email ) : ( '#' . $r->user_id ) ) . '</strong>'
					. ( $c && $c->email ? '<br><a href="mailto:' . esc_attr( $c->email ) . '">' . esc_html( $c->email ) . '</a>' : '' ) . '</td>';
				echo '<td><strong>' . esc_html( HSS_Change_Requests::summary( $r ) ) . '</strong></td>';
				echo '<td>' . esc_html( $cur ) . '</td>';
				echo '<td style="max-width:240px;color:#5d534d;">' . esc_html( $r->message ) . '</td>';
				echo '<td>';
				echo '<form method="post" style="display:flex;flex-direction:column;gap:6px;min-width:210px;">';
				wp_nonce_field( 'hss_request_resolve' );
				echo '<input type="hidden" name="hss_action" value="request_resolve">';
				echo '<input type="hidden" name="request" value="' . esc_attr( $r->id ) . '">';
				echo '<input type="text" name="admin_note" placeholder="note to customer (optional)" style="width:100%;">';
				echo '<span style="display:flex;gap:6px;">';
				echo '<button class="button button-small button-primary" name="to" value="approved">Approve</button>';
				echo '<button class="button button-small" name="to" value="declined">Decline</button>';
				echo '</span>';
				echo '</form>';
				echo '</td>';
				echo '</tr>';
			}
			echo '</tbody></table>';
		}

		/* Resolved log */
		echo '<h2 style="margin-top:28px;">Resolved</h2>';
		$recent = HSS_Change_Requests::recent( 60 );
		if ( ! $recent ) {
			echo '<p>Nothing resolved yet.</p>';
		} else {
			echo '<table class="widefat striped"><thead><tr><th>Date</th><th>Customer</th><th>Request</th><th>Outcome</th><th>Note</th></tr></thead><tbody>';
			foreach ( $recent as $r ) {
				$c = $cmap[ (int) $r->customer_id ] ?? null;
				echo '<tr>';
				echo '<td>' . esc_html( date_i18n( 'M j, Y', strtotime( $r->resolved_at ?: $r->updated_at ) ) ) . '</td>';
				echo '<td>' . esc_html( $c ? ( $c->name ?: $c->email ) : ( '#' . $r->user_id ) ) . '</td>';
				echo '<td>' . esc_html( HSS_Change_Requests::summary( $r ) ) . '</td>';
				echo '<td><span class="hss-pill ' . esc_attr( self::pill_class( $r->status ) ) . '">' . esc_html( HSS_Change_Requests::status_label( $r->status ) ) . '</span></td>';
				echo '<td style="max-width:260px;color:#5d534d;">' . esc_html( $r->admin_note ) . '</td>';
				echo '</tr>';
			}
			echo '</tbody></table>';
		}

		self::close();
	}

	/* ── Quote requests ───────────────────────────────────────────────── */
	public static function page_quotes() {
		global $wpdb;
		$t = HSS_DB::t( 'quote_requests' );

		// Mark-as-handled action.
		if ( isset( $_GET['done'] ) && check_admin_referer( 'hss_quote_done' ) ) {
			$wpdb->update( $t, [ 'status' => 'handled' ], [ 'id' => (int) $_GET['done'] ] );
			echo '<div class="notice notice-success is-dismissible"><p>Marked as handled.</p></div>';
		}

		self::open( 'Quote Requests' );
		$rows = $wpdb->get_results( "SELECT * FROM $t ORDER BY created_at DESC LIMIT 200" );
		self::quotes_table( $rows, true );
		self::close();
	}

	protected static function quotes_table( $rows, $with_actions = false ) {
		if ( ! $rows ) { echo '<p>No quote requests yet.</p>'; return; }
		echo '<table class="widefat striped"><thead><tr><th>Date</th><th>Name</th><th>Contact</th><th>City</th><th>Dogs</th><th>Interest</th><th>Message</th><th>Status</th>' . ( $with_actions ? '<th></th>' : '' ) . '</tr></thead><tbody>';
		foreach ( $rows as $r ) {
			echo '<tr>';
			echo '<td>' . esc_html( date_i18n( 'M j', strtotime( $r->created_at ) ) ) . '</td>';
			echo '<td><strong>' . esc_html( $r->name ) . '</strong></td>';
			echo '<td><a href="mailto:' . esc_attr( $r->email ) . '">' . esc_html( $r->email ) . '</a><br>' . esc_html( $r->phone ) . '</td>';
			echo '<td>' . esc_html( $r->city ) . '</td>';
			echo '<td>' . esc_html( $r->dogs ) . '</td>';
			echo '<td>' . esc_html( $r->interest ) . '</td>';
			echo '<td style="max-width:280px">' . esc_html( $r->message ) . '</td>';
			echo '<td><span class="hss-pill ' . esc_attr( self::pill_class( $r->status ) ) . '">' . esc_html( $r->status ) . '</span></td>';
			if ( $with_actions ) {
				if ( $r->status === 'new' ) {
					$url = wp_nonce_url( admin_url( 'admin.php?page=' . self::SLUG . '-quotes&done=' . (int) $r->id ), 'hss_quote_done' );
					echo '<td><a class="button button-small" href="' . esc_url( $url ) . '">Mark handled</a></td>';
				} else {
					echo '<td>—</td>';
				}
			}
			echo '</tr>';
		}
		echo '</tbody></table>';
	}

	/* ── Settings / status ────────────────────────────────────────────── */
	public static function page_settings() {
		self::open( 'Settings &amp; Stripe Status' );

		$secret  = HSS_Config::stripe_secret();
		$pub     = HSS_Config::stripe_publishable();
		$hook    = HSS_Config::webhook_secret();
		$webhook = rest_url( HSS_Rest::NS . '/webhook' );

		echo '<h2>Stripe credentials</h2>';
		echo '<p>Keys are read from the environment — never stored in the database. Define them in <span class="hss-code">wp-config.php</span>, as server environment variables, or in <span class="hss-code">' . esc_html( HSS_PORTAL_DIR ) . '.env</span>.</p>';
		echo '<table class="widefat" style="max-width:680px"><tbody>';
		self::status_row( 'Secret key (HSS_STRIPE_SECRET_KEY)', $secret, true );
		self::status_row( 'Publishable key (HSS_STRIPE_PUBLISHABLE_KEY)', $pub, false );
		self::status_row( 'Webhook signing secret (HSS_STRIPE_WEBHOOK_SECRET)', $hook, true );
		echo '<tr><td>Mode</td><td>' . ( $secret ? ( HSS_Config::is_test_mode() ? '<span class="hss-pill warn">Test</span>' : '<span class="hss-pill ok">Live</span>' ) : '<span class="hss-pill bad">Not set</span>' ) . '</td></tr>';
		echo '</tbody></table>';

		echo '<h2>SMS notifications</h2>';
		$sms_provider = HSS_Config::sms_provider();
		if ( HSS_Config::is_sms_configured() ) {
			$src = ( $sms_provider === 'brevo' && HSS_Config::brevo_key_from_mailer() )
				? ' (key reused from Kind Brevo Mailer)'
				: '';
			echo '<p><span class="hss-status-ok">✓ ' . esc_html( ucfirst( $sms_provider ) ) . ' connected</span>' . esc_html( $src ) . ' — '
				. 'sender <span class="hss-code">' . esc_html( HSS_Config::sms_sender() ) . '</span>. '
				. 'Customers who opt in (a checkbox on their dashboard) get short visit texts.</p>';
		} else {
			echo '<p><span class="hss-status-no">— not set</span>. Optional. Add <span class="hss-code">HSS_BREVO_API_KEY</span> '
				. '(reuses your Brevo account) or Twilio keys to enable opt-in visit texts. See <span class="hss-code">.env.example</span>.</p>';
		}
		echo '<p style="color:#5d534d;"><strong>US delivery note:</strong> texting US phones requires a real number you control and '
			. 'A2P&nbsp;10DLC / toll-free registration with your provider. Alphanumeric sender IDs are not delivered to US handsets.</p>';

		echo '<h2>Webhook endpoint</h2>';
		echo '<p>In the Stripe Dashboard → Developers → Webhooks, add an endpoint pointing to:</p>';
		echo '<p><span class="hss-code">' . esc_html( $webhook ) . '</span></p>';
		echo '<p>Subscribe to: <span class="hss-code">checkout.session.completed</span>, <span class="hss-code">customer.subscription.*</span>, <span class="hss-code">invoice.paid</span>, <span class="hss-code">invoice.payment_failed</span>. Then copy the signing secret into <span class="hss-code">HSS_STRIPE_WEBHOOK_SECRET</span>.</p>';
		echo '<p>Also enable the <strong>Customer Billing Portal</strong> (Stripe → Settings → Billing → Customer portal) so customers can manage and cancel plans.</p>';

		echo '<h2>Current pricing</h2>';
		echo '<p>Pricing is defined in code (<span class="hss-code">includes/class-hss-config.php</span>) so it stays version-controlled and free of plugin sprawl. All plans bill monthly via Stripe.</p>';
		echo '<table class="widefat striped" style="max-width:560px"><thead><tr><th>Plan</th><th>1 dog</th><th>2 dogs</th><th>3 dogs</th></tr></thead><tbody>';
		foreach ( HSS_Config::pricing() as $plan ) {
			echo '<tr><td><strong>' . esc_html( $plan['label'] ) . '</strong><br><span style="color:#5d534d">' . esc_html( $plan['desc'] ) . '</span></td>';
			echo '<td>$' . esc_html( $plan['prices'][1] ) . '/mo</td><td>$' . esc_html( $plan['prices'][2] ) . '/mo</td><td>$' . esc_html( $plan['prices'][3] ) . '/mo</td></tr>';
		}
		echo '<tr><td><strong>One-Time Cleanup</strong></td><td colspan="3">$' . esc_html( HSS_Config::onetime_price() ) . ' per half hour</td></tr>';
		echo '</tbody></table>';
		echo '<p style="color:#5d534d">4+ dogs / commercial: handled by quote, no online plan.</p>';

		self::close();
	}

	protected static function status_row( $label, $value, $secret = false ) {
		echo '<tr><td>' . esc_html( $label ) . '</td><td>';
		if ( $value ) {
			$hint = $secret ? '••••' . substr( $value, -4 ) : esc_html( substr( $value, 0, 12 ) . '…' );
			echo '<span class="hss-status-ok">✓ detected</span> <span class="hss-code">' . esc_html( $hint ) . '</span>';
		} else {
			echo '<span class="hss-status-no">— not set</span>';
		}
		echo '</td></tr>';
	}
}
