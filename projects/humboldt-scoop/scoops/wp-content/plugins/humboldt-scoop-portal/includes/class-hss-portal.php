<?php
/**
 * Front-end customer portal: login, registration, dashboard, plan picker.
 * @package hss-portal
 */
if ( ! defined( 'ABSPATH' ) ) { exit; }

class HSS_Portal {

	public static function init() {
		add_shortcode( 'hss_portal', [ __CLASS__, 'render' ] );
		add_shortcode( 'hss_pricing', [ __CLASS__, 'render_pricing_shortcode' ] );
		add_action( 'wp_enqueue_scripts', [ __CLASS__, 'enqueue' ] );
		add_action( 'template_redirect', [ __CLASS__, 'handle_forms' ] );
	}

	/* ── Page provisioning ────────────────────────────────────────────── */
	public static function ensure_portal_page() {
		if ( get_page_by_path( 'portal' ) ) { return; }
		wp_insert_post( [
			'post_title'   => 'Customer Portal',
			'post_name'    => 'portal',
			'post_status'  => 'publish',
			'post_type'    => 'page',
			'post_content' => '[hss_portal]',
		] );
	}

	public static function is_portal_page() {
		return is_page() && has_shortcode( get_post()->post_content ?? '', 'hss_portal' );
	}

	/* ── Assets ───────────────────────────────────────────────────────── */
	public static function enqueue() {
		// Quote config is needed wherever the quote form might render (front page).
		wp_register_script( 'hss-portal', HSS_PORTAL_URL . 'assets/portal.js', [], HSS_PORTAL_VERSION, true );

		$quote_cfg = [
			'endpoint' => esc_url_raw( rest_url( 'hss/v1/quote' ) ),
			'nonce'    => wp_create_nonce( 'wp_rest' ),
		];
		wp_add_inline_script( 'hss-portal', 'window.HSS_QUOTE=' . wp_json_encode( $quote_cfg ) . ';', 'before' );

		if ( self::is_portal_page() ) {
			wp_enqueue_style( 'hss-portal', HSS_PORTAL_URL . 'assets/portal.css', [], HSS_PORTAL_VERSION );
			wp_enqueue_script( 'hss-portal' );
			wp_add_inline_script( 'hss-portal', 'window.HSS_PORTAL=' . wp_json_encode( [
				'checkout' => esc_url_raw( rest_url( 'hss/v1/checkout' ) ),
				'billing'  => esc_url_raw( rest_url( 'hss/v1/billing-portal' ) ),
				'profile'  => esc_url_raw( rest_url( 'hss/v1/profile' ) ),
				'nonce'    => wp_create_nonce( 'wp_rest' ),
			] ) . ';', 'before' );
		} else {
			// Still load the small script on the front page for the quote form.
			wp_enqueue_script( 'hss-portal' );
		}
	}

	/* ── Non-AJAX form handling (login / register) ────────────────────── */
	public static function handle_forms() {
		if ( ! self::is_portal_page() || 'POST' !== ( $_SERVER['REQUEST_METHOD'] ?? '' ) ) { return; }

		$action = sanitize_text_field( $_POST['hss_action'] ?? '' );
		if ( ! $action ) { return; }

		$redirect = self::portal_url();
		// Preserve plan intent through auth.
		foreach ( [ 'plan', 'dogs' ] as $k ) {
			if ( ! empty( $_POST[ $k ] ) ) { $redirect = add_query_arg( $k, sanitize_text_field( $_POST[ $k ] ), $redirect ); }
		}

		if ( 'login' === $action && check_admin_referer( 'hss_login' ) ) {
			$creds = [
				'user_login'    => sanitize_text_field( $_POST['log'] ?? '' ),
				'user_password' => (string) ( $_POST['pwd'] ?? '' ),
				'remember'      => ! empty( $_POST['rememberme'] ),
			];
			$user = wp_signon( $creds, is_ssl() );
			if ( is_wp_error( $user ) ) {
				self::$notice = [ 'err', 'Login failed. Check your email and password.' ];
				return;
			}
			wp_safe_redirect( $redirect ); exit;
		}

		if ( 'register' === $action && check_admin_referer( 'hss_register' ) ) {
			$res = HSS_Customers::register(
				sanitize_text_field( $_POST['name'] ?? '' ),
				sanitize_email( $_POST['email'] ?? '' ),
				(string) ( $_POST['password'] ?? '' ),
				[ 'phone' => $_POST['phone'] ?? '', 'city' => $_POST['city'] ?? '' ]
			);
			if ( is_wp_error( $res ) ) {
				self::$notice = [ 'err', $res->get_error_message() ];
				return;
			}
			wp_set_current_user( $res );
			wp_set_auth_cookie( $res, true, is_ssl() );
			wp_safe_redirect( $redirect ); exit;
		}

		if ( 'change_request' === $action && is_user_logged_in() && check_admin_referer( 'hss_change_request' ) ) {
			$type = sanitize_text_field( $_POST['cr_type'] ?? '' );
			if ( ! HSS_Change_Requests::is_valid_type( $type ) ) { $type = 'other'; }

			$user = wp_get_current_user();
			$cust = HSS_Customers::get_or_create( $user->ID );
			$sub  = self::active_subscription( $user->ID );

			$rid = HSS_Change_Requests::create( [
				'user_id'            => $user->ID,
				'customer_id'        => $cust ? (int) $cust->id : 0,
				'type'               => $type,
				'current_plan_key'   => $sub ? $sub->plan_key : '',
				'requested_plan_key' => 'plan_change' === $type ? sanitize_text_field( $_POST['cr_plan'] ?? '' ) : '',
				'requested_dogs'     => 'plan_change' === $type ? max( 0, min( 6, (int) ( $_POST['cr_dogs'] ?? 0 ) ) ) : 0,
				'message'            => sanitize_textarea_field( $_POST['cr_message'] ?? '' ),
			] );

			if ( $rid && class_exists( 'HSS_Mail' ) ) {
				HSS_Mail::change_request_admin( HSS_Change_Requests::get( $rid ) );
			}
			wp_safe_redirect( add_query_arg( 'cr', $rid ? 'ok' : 'err', self::portal_url() ) ); exit;
		}
	}

	protected static $notice = null;

	public static function portal_url() {
		$page = get_page_by_path( 'portal' );
		return $page ? get_permalink( $page ) : home_url( '/portal/' );
	}

	/* ── Render ───────────────────────────────────────────────────────── */
	public static function render() {
		ob_start();
		echo '<div class="hss-portal">';

		if ( self::$notice ) {
			printf( '<div class="hss-portal-notice hss-%s">%s</div>', esc_attr( self::$notice[0] ), esc_html( self::$notice[1] ) );
		}
		$checkout = sanitize_text_field( $_GET['checkout'] ?? '' );
		if ( 'success' === $checkout ) {
			echo '<div class="hss-portal-notice hss-ok">You\'re all set — thanks! Your details are below. It can take a moment for billing info to appear.</div>';
		} elseif ( 'cancel' === $checkout ) {
			echo '<div class="hss-portal-notice hss-warn">Checkout canceled. No charge was made — you can pick a plan whenever you\'re ready.</div>';
		}
		$cr = sanitize_text_field( $_GET['cr'] ?? '' );
		if ( 'ok' === $cr ) {
			echo '<div class="hss-portal-notice hss-ok">Thanks — your request is in. We\'ll review it and follow up by email.</div>';
		} elseif ( 'err' === $cr ) {
			echo '<div class="hss-portal-notice hss-err">Sorry, we couldn\'t submit that request. Please try again or contact us.</div>';
		}

		if ( is_user_logged_in() ) {
			self::render_dashboard();
		} else {
			self::render_auth();
		}

		echo '</div>';
		return ob_get_clean();
	}

	/**
	 * [hss_pricing] — render the live pricing matrix anywhere (e.g. a
	 * Gutenberg Shortcode block on the marketing homepage). Pulls from
	 * HSS_Config so the public prices always match checkout, and styles
	 * itself with the active theme's brand classes (hss-price-card etc.).
	 *
	 * Optional attribute: featured="weekly" highlights that plan.
	 */
	public static function render_pricing_shortcode( $atts = [] ) {
		$atts = shortcode_atts( [ 'featured' => 'weekly' ], $atts, 'hss_pricing' );
		$pricing  = HSS_Config::pricing();
		$portal   = self::portal_url();
		$featured = $atts['featured'];

		ob_start();
		echo '<div class="hss-pricing-grid hss-sc-pricing" style="display:grid;grid-template-columns:repeat(auto-fit,minmax(220px,1fr));gap:1.75rem;margin-top:2rem;">';

		foreach ( $pricing as $key => $plan ) {
			$is_feat = ( $key === $featured );
			$base    = add_query_arg( [ 'plan' => $key ], $portal );
			echo '<div class="hss-price-card' . ( $is_feat ? ' hss-price-card--featured' : '' ) . '">';
			echo '<h3>' . esc_html( $plan['label'] ) . '</h3>';
			echo '<p>' . esc_html( $plan['desc'] ) . '</p>';
			echo '<p class="hss-price">$' . esc_html( $plan['prices'][1] ) . '<span style="font-size:.78rem;font-weight:700;"> /mo · 1 dog</span></p>';
			echo '<p style="font-size:.88rem;color:var(--hss-text-muted);margin-bottom:1rem;">2 dogs $' . esc_html( $plan['prices'][2] ) . '/mo · 3 dogs $' . esc_html( $plan['prices'][3] ) . '/mo</p>';
			echo '<label style="display:block;font-size:.8rem;font-weight:800;margin-bottom:.6rem;">Dogs '
				. '<select data-dogs style="margin-left:.4rem;padding:.3rem .5rem;border-radius:8px;border:1px solid var(--hss-border);font:inherit;">'
				. '<option value="1">1</option><option value="2">2</option><option value="3">3</option></select></label>';
			echo '<div class="wp-block-button hss-btn--primary"><a class="wp-block-button__link" data-cta data-base="' . esc_url( $base ) . '" href="' . esc_url( add_query_arg( [ 'dogs' => 1 ], $base ) ) . '">Choose ' . esc_html( $plan['label'] ) . '</a></div>';
			echo '</div>';
		}

		// One-time cleanup card.
		$ot = add_query_arg( [ 'plan' => 'onetime' ], $portal );
		echo '<div class="hss-price-card">';
		echo '<h3>One-Time Cleanup</h3>';
		echo '<p>Great for a one-off reset, a move-out, or before a backyard party.</p>';
		echo '<p class="hss-price">$' . esc_html( HSS_Config::onetime_price() ) . '<span style="font-size:.78rem;font-weight:700;"> / half hour</span></p>';
		echo '<div class="wp-block-button hss-btn--primary" style="margin-top:auto;"><a class="wp-block-button__link" href="' . esc_url( $ot ) . '">Book a Cleanup</a></div>';
		echo '</div>';

		echo '</div>'; // grid

		echo '<p class="hss-pricing-note hss-center">Have <strong>4 or more dogs</strong>, a large property, or a commercial space? <a href="#hss-contact">Request a custom quote</a> — we\'ll size it to your yard.</p>';

		// Wire each card's dog selector to its checkout link (printed once).
		static $printed = false;
		if ( ! $printed ) {
			$printed = true;
			echo '<script>(function(){document.querySelectorAll(".hss-sc-pricing .hss-price-card").forEach(function(c){var s=c.querySelector("[data-dogs]"),a=c.querySelector("[data-cta]");if(s&&a){s.addEventListener("change",function(){var b=a.getAttribute("data-base");a.href=b+(b.indexOf("?")>-1?"&":"?")+"dogs="+s.value;});}});})();</script>';
		}

		return ob_get_clean();
	}

	/* ── Logged-out: login + register ─────────────────────────────────── */
	protected static function render_auth() {
		$plan = sanitize_text_field( $_GET['plan'] ?? '' );
		$dogs = (int) ( $_GET['dogs'] ?? 1 );
		$intent_fields = '';
		if ( $plan ) {
			$intent_fields = sprintf(
				'<input type="hidden" name="plan" value="%s"><input type="hidden" name="dogs" value="%d">',
				esc_attr( $plan ), $dogs
			);
			$label = HSS_Config::plan_label( $plan, $plan === 'onetime' ? null : $dogs );
			echo '<p class="hss-portal-intent">Log in or create an account to continue with <strong>' . esc_html( $label ) . '</strong>.</p>';
		}
		?>
		<div class="hss-auth">
			<div class="hss-auth-tabs">
				<button class="hss-tab is-active" data-tab="login">Log In</button>
				<button class="hss-tab" data-tab="register">Create Account</button>
			</div>

			<form class="hss-auth-panel" data-panel="login" method="post">
				<?php wp_nonce_field( 'hss_login' ); ?>
				<input type="hidden" name="hss_action" value="login">
				<?php echo $intent_fields; // phpcs:ignore ?>
				<label>Email or username<input type="text" name="log" required autocomplete="username"></label>
				<label>Password<input type="password" name="pwd" required autocomplete="current-password"></label>
				<label class="hss-checkbox"><input type="checkbox" name="rememberme" value="1"> Keep me logged in</label>
				<button type="submit" class="hss-btn hss-btn-primary">Log In</button>
				<a class="hss-auth-forgot" href="<?php echo esc_url( wp_lostpassword_url() ); ?>">Forgot password?</a>
			</form>

			<form class="hss-auth-panel is-hidden" data-panel="register" method="post">
				<?php wp_nonce_field( 'hss_register' ); ?>
				<input type="hidden" name="hss_action" value="register">
				<?php echo $intent_fields; // phpcs:ignore ?>
				<label>Name<input type="text" name="name" required autocomplete="name"></label>
				<label>Email<input type="email" name="email" required autocomplete="email"></label>
				<div class="hss-auth-row">
					<label>Phone<input type="tel" name="phone" autocomplete="tel"></label>
					<label>City<input type="text" name="city"></label>
				</div>
				<label>Password<input type="password" name="password" required minlength="8" autocomplete="new-password"></label>
				<button type="submit" class="hss-btn hss-btn-primary">Create My Account</button>
			</form>
		</div>
		<?php
	}

	/* ── Logged-in dashboard ──────────────────────────────────────────── */
	protected static function render_dashboard() {
		$user = wp_get_current_user();
		$cust = HSS_Customers::get_or_create( $user->ID );
		$sub  = self::active_subscription( $user->ID );

		echo '<header class="hss-dash-head"><div><h2>Welcome back, ' . esc_html( $user->display_name ) . '</h2>';
		echo '<p class="hss-muted">' . esc_html( $user->user_email ) . '</p></div>';
		echo '<a class="hss-btn hss-btn-ghost hss-logout" href="' . esc_url( wp_logout_url( self::portal_url() ) ) . '">Log Out</a></header>';

		// Pending plan intent (user clicked a plan, then logged in/registered).
		$plan = sanitize_text_field( $_GET['plan'] ?? '' );
		if ( $plan ) {
			self::render_plan_confirm( $plan, (int) ( $_GET['dogs'] ?? 1 ) );
		}

		echo '<div class="hss-dash-grid">';

		/* Current plan card */
		echo '<section class="hss-card hss-dash-card"><h3>Your Plan</h3>';
		if ( $sub && in_array( $sub->status, [ 'active', 'trialing', 'past_due' ], true ) ) {
			echo '<p class="hss-plan-current">' . esc_html( HSS_Config::plan_label( $sub->plan_key, $sub->dog_count ) ) . '</p>';
			echo '<p class="hss-plan-rate">$' . esc_html( number_format( $sub->amount_cents / 100, 2 ) ) . ' / month</p>';
			echo '<p class="hss-pill hss-pill-' . esc_attr( $sub->status ) . '">' . esc_html( ucfirst( str_replace( '_', ' ', $sub->status ) ) ) . '</p>';
			if ( $sub->current_period_end ) {
				echo '<p class="hss-muted">Next billing date: ' . esc_html( date_i18n( 'F j, Y', strtotime( $sub->current_period_end ) ) ) . '</p>';
			}
			echo '<button class="hss-btn hss-btn-secondary" data-hss-billing>Manage / Cancel Plan</button>';
		} else {
			echo '<p class="hss-muted">You don\'t have an active plan yet.</p>';
			echo '<a class="hss-btn hss-btn-primary" href="' . esc_url( home_url( '/#hss-pricing' ) ) . '">Choose a Plan</a>';
		}
		echo '</section>';

		/* One-time booking card */
		echo '<section class="hss-card hss-dash-card"><h3>One-Time Cleanup</h3>';
		echo '<p class="hss-muted">Need a single reset? Book a one-time cleanup for $' . esc_html( HSS_Config::onetime_price() ) . ' per half hour.</p>';
		echo '<button class="hss-btn hss-btn-secondary" data-hss-checkout data-plan="onetime">Book a Cleanup</button>';
		echo '</section>';

		echo '</div>'; // grid

		/* Plan change / pause / cancel requests */
		self::render_change_request( $user->ID, $sub );

		/* Visits */
		self::render_visits( $user->ID );

		/* Service details */
		self::render_service_details( $cust );

		/* Invoices */
		self::render_invoices( $user->ID );
	}

	protected static function render_change_request( $user_id, $sub ) {
		if ( ! class_exists( 'HSS_Change_Requests' ) ) { return; }
		$pending = HSS_Change_Requests::pending_for_user( $user_id );

		echo '<section class="hss-card hss-dash-card hss-change"><h3>Manage Your Plan</h3>';

		if ( $pending ) {
			echo '<div class="hss-cr-pending">';
			echo '<span class="hss-pill hss-pill-new">Pending</span> ';
			echo '<strong>' . esc_html( HSS_Change_Requests::summary( $pending ) ) . '</strong>';
			echo '<p class="hss-muted">Submitted ' . esc_html( date_i18n( 'M j, Y', strtotime( $pending->created_at ) ) )
				. '. We\'ll review it and email you. Need to adjust it? Just reply to our email or contact us.</p>';
			if ( $pending->message ) {
				echo '<p class="hss-muted">Your note: ' . esc_html( $pending->message ) . '</p>';
			}
			echo '</div>';
		} else {
			$has_plan = $sub && in_array( $sub->status, [ 'active', 'trialing', 'past_due' ], true );
			echo '<p class="hss-muted">Want to change how often we visit, pause for a while, or cancel? Send a request and we\'ll take care of it.</p>';
			?>
			<form class="hss-cr-form" method="post" action="<?php echo esc_url( self::portal_url() ); ?>">
				<?php wp_nonce_field( 'hss_change_request' ); ?>
				<input type="hidden" name="hss_action" value="change_request">
				<label>What would you like to do?
					<select name="cr_type">
						<?php foreach ( HSS_Change_Requests::types() as $k => $label ) : ?>
							<option value="<?php echo esc_attr( $k ); ?>"<?php echo ( ! $has_plan && $k === 'plan_change' ) ? ' selected' : ''; ?>><?php echo esc_html( $label ); ?></option>
						<?php endforeach; ?>
					</select>
				</label>
				<div class="hss-auth-row">
					<label>New plan <span class="hss-muted">(if changing)</span>
						<select name="cr_plan">
							<option value="">—</option>
							<?php foreach ( HSS_Config::pricing() as $k => $plan ) : ?>
								<option value="<?php echo esc_attr( $k ); ?>"><?php echo esc_html( $plan['label'] ); ?></option>
							<?php endforeach; ?>
						</select>
					</label>
					<label>Dogs <span class="hss-muted">(if changing)</span>
						<select name="cr_dogs">
							<option value="0">—</option>
							<?php for ( $i = 1; $i <= 6; $i++ ) : ?>
								<option value="<?php echo $i; ?>"><?php echo $i; ?></option>
							<?php endfor; ?>
						</select>
					</label>
				</div>
				<label>Anything we should know?
					<textarea name="cr_message" rows="3" placeholder="Optional — dates, reasons, special requests…"></textarea>
				</label>
				<button type="submit" class="hss-btn hss-btn-primary">Submit Request</button>
			</form>
			<?php
		}

		$hist = HSS_Change_Requests::history_for_user( $user_id );
		if ( $hist ) {
			echo '<table class="hss-invoice-table hss-cr-history"><thead><tr><th>Date</th><th>Request</th><th>Outcome</th></tr></thead><tbody>';
			foreach ( $hist as $r ) {
				$d = $r->resolved_at ?: $r->created_at;
				echo '<tr>';
				echo '<td>' . esc_html( date_i18n( 'M j, Y', strtotime( $d ) ) ) . '</td>';
				echo '<td>' . esc_html( HSS_Change_Requests::summary( $r ) ) . '</td>';
				echo '<td><span class="hss-pill hss-pill-' . esc_attr( $r->status ) . '">' . esc_html( HSS_Change_Requests::status_label( $r->status ) ) . '</span></td>';
				echo '</tr>';
			}
			echo '</tbody></table>';
		}

		echo '</section>';
	}

	protected static function render_visits( $user_id ) {
		if ( ! class_exists( 'HSS_Visits' ) ) { return; }
		$next = HSS_Visits::next_for_user( $user_id );
		$hist = HSS_Visits::history_for_user( $user_id );

		echo '<section class="hss-card hss-dash-card hss-visits"><h3>Your Visits</h3>';

		if ( $next ) {
			$when = $next->scheduled_date
				? date_i18n( 'l, F j', strtotime( $next->scheduled_date ) )
				: 'To be scheduled';
			$window = $next->time_window ? ' · ' . $next->time_window : '';
			echo '<div class="hss-visit-next">';
			echo '<span class="hss-visit-label">Next visit</span>';
			echo '<span class="hss-visit-when">' . esc_html( $when ) . esc_html( $window ) . '</span>';
			echo ' <span class="hss-pill hss-pill-' . esc_attr( $next->status ) . '">' . esc_html( HSS_Visits::status_label( $next->status ) ) . '</span>';
			if ( $next->customer_note ) {
				echo '<p class="hss-muted">' . esc_html( $next->customer_note ) . '</p>';
			}
			echo '</div>';
		} else {
			echo '<p class="hss-muted">No upcoming visit scheduled yet. We\'ll email you as soon as your next cleanup is on the calendar.</p>';
		}

		if ( $hist ) {
			echo '<table class="hss-invoice-table hss-visit-history"><thead><tr><th>Date</th><th>Result</th><th>Note</th></tr></thead><tbody>';
			foreach ( $hist as $v ) {
				$d = $v->scheduled_date ?: $v->completed_at;
				echo '<tr>';
				echo '<td>' . esc_html( $d ? date_i18n( 'M j, Y', strtotime( $d ) ) : '—' ) . '</td>';
				echo '<td><span class="hss-pill hss-pill-' . esc_attr( $v->status ) . '">' . esc_html( HSS_Visits::status_label( $v->status ) ) . '</span></td>';
				echo '<td>' . esc_html( $v->customer_note ) . '</td>';
				echo '</tr>';
			}
			echo '</tbody></table>';
		}

		echo '</section>';
	}

	protected static function render_plan_confirm( $plan_key, $dogs ) {
		if ( $plan_key === 'onetime' ) {
			$label = 'One-Time Cleanup';
			$rate  = '$' . HSS_Config::onetime_price() . ' per half hour';
		} else {
			$cfg = HSS_Config::plan( $plan_key );
			if ( ! $cfg ) { return; }
			$dogs  = max( 1, min( 3, $dogs ) );
			$label = HSS_Config::plan_label( $plan_key, $dogs );
			$rate  = '$' . $cfg['prices'][ $dogs ] . ' / month';
		}
		echo '<section class="hss-confirm">';
		echo '<div><h3>Ready to start: ' . esc_html( $label ) . '</h3><p class="hss-muted">' . esc_html( $rate ) . ' · secure checkout via Stripe · cancel anytime</p></div>';
		echo '<button class="hss-btn hss-btn-primary" data-hss-checkout data-plan="' . esc_attr( $plan_key ) . '" data-dogs="' . esc_attr( $dogs ) . '">Continue to Checkout</button>';
		echo '</section>';
	}

	protected static function render_service_details( $cust ) {
		?>
		<section class="hss-card hss-dash-card hss-service-details">
			<h3>Service Details</h3>
			<p class="hss-muted">Help our team do a great job. These notes go straight to whoever services your yard.</p>
			<form data-hss-profile>
				<div class="hss-auth-row">
					<label>Service address<input type="text" name="address" value="<?php echo esc_attr( $cust->address ); ?>"></label>
					<label>City<input type="text" name="city" value="<?php echo esc_attr( $cust->city ); ?>"></label>
				</div>
				<div class="hss-auth-row">
					<label>Phone<input type="tel" name="phone" value="<?php echo esc_attr( $cust->phone ); ?>"></label>
					<label>Number of dogs
						<select name="dog_count">
							<?php for ( $i = 1; $i <= 6; $i++ ) : ?>
								<option value="<?php echo $i; ?>" <?php selected( (int) $cust->dog_count, $i ); ?>><?php echo $i; ?></option>
							<?php endfor; ?>
						</select>
					</label>
				</div>
				<label>Gate / access notes<textarea name="gate_notes" rows="2"><?php echo esc_textarea( $cust->gate_notes ); ?></textarea></label>
				<label>Yard notes<textarea name="yard_notes" rows="2"><?php echo esc_textarea( $cust->yard_notes ); ?></textarea></label>
				<label>Pet notes / special instructions<textarea name="pet_notes" rows="2"><?php echo esc_textarea( $cust->pet_notes ); ?></textarea></label>
				<?php if ( HSS_Config::is_sms_configured() ) : ?>
				<label class="hss-checkbox hss-sms-optin">
					<input type="checkbox" name="sms_opt_in" value="1" <?php checked( (int) ( $cust->sms_opt_in ?? 0 ), 1 ); ?>>
					Text me visit updates (on the way / all done). Message &amp; data rates may apply; reply STOP to opt out.
				</label>
				<?php endif; ?>
				<button type="submit" class="hss-btn hss-btn-primary">Save Details</button>
				<span class="hss-form-status" data-profile-status role="status"></span>
			</form>
		</section>
		<?php
	}

	protected static function render_invoices( $user_id ) {
		$rows = self::invoices( $user_id );
		echo '<section class="hss-card hss-dash-card"><h3>Billing History</h3>';
		if ( empty( $rows ) ) {
			echo '<p class="hss-muted">No invoices yet. Charges will appear here after your first payment.</p>';
		} else {
			echo '<table class="hss-invoice-table"><thead><tr><th>Date</th><th>Description</th><th>Amount</th><th>Status</th><th></th></tr></thead><tbody>';
			foreach ( $rows as $inv ) {
				echo '<tr>';
				echo '<td>' . esc_html( date_i18n( 'M j, Y', strtotime( $inv->created_at ) ) ) . '</td>';
				echo '<td>' . esc_html( $inv->description ?: ( $inv->number ?: 'Invoice' ) ) . '</td>';
				echo '<td>$' . esc_html( number_format( $inv->amount_cents / 100, 2 ) ) . '</td>';
				echo '<td><span class="hss-pill hss-pill-' . esc_attr( $inv->status ) . '">' . esc_html( ucfirst( $inv->status ) ) . '</span></td>';
				echo '<td>' . ( $inv->hosted_url ? '<a href="' . esc_url( $inv->hosted_url ) . '" target="_blank" rel="noopener">View</a>' : '' ) . '</td>';
				echo '</tr>';
			}
			echo '</tbody></table>';
		}
		echo '</section>';
	}

	/* ── Data helpers ─────────────────────────────────────────────────── */
	public static function active_subscription( $user_id ) {
		global $wpdb;
		$t = HSS_DB::t( 'subscriptions' );
		return $wpdb->get_row( $wpdb->prepare(
			"SELECT * FROM $t WHERE user_id = %d ORDER BY FIELD(status,'active','trialing','past_due') = 0, updated_at DESC LIMIT 1",
			$user_id
		) );
	}

	public static function invoices( $user_id, $limit = 12 ) {
		global $wpdb;
		$t = HSS_DB::t( 'invoices' );
		return $wpdb->get_results( $wpdb->prepare(
			"SELECT * FROM $t WHERE user_id = %d ORDER BY created_at DESC LIMIT %d",
			$user_id, $limit
		) );
	}
}
