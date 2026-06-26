<?php
/**
 * Branded transactional email.
 *
 * Sends simple, responsive HTML email through wp_mail(), so it rides
 * whatever SMTP relay the site already uses (e.g. Brevo). No external
 * dependencies. Each send temporarily sets the HTML content type and
 * removes the filter afterward so it never leaks into other mail.
 *
 * @package hss-portal
 */
if ( ! defined( 'ABSPATH' ) ) { exit; }

class HSS_Mail {

	public static function content_type() { return 'text/html; charset=UTF-8'; }

	/**
	 * Send one branded HTML email.
	 *
	 * @param string $to
	 * @param string $subject
	 * @param string $heading    big heading inside the email body
	 * @param string $body_html  inner HTML (already escaped/trusted)
	 * @param array  $cta        optional ['label'=>..., 'url'=>...]
	 */
	public static function send( $to, $subject, $heading, $body_html, $cta = [], $headers = [] ) {
		if ( ! is_email( $to ) ) { return false; }

		add_filter( 'wp_mail_content_type', [ __CLASS__, 'content_type' ] );
		$ok = wp_mail( $to, $subject, self::wrap( $heading, $body_html, $cta ), $headers );
		remove_filter( 'wp_mail_content_type', [ __CLASS__, 'content_type' ] );
		return $ok;
	}

	/** Wrap inner content in the brand shell. */
	protected static function wrap( $heading, $body_html, $cta = [] ) {
		$brand   = esc_html( get_bloginfo( 'name' ) );
		$tagline = 'Your dog&rsquo;s business is our business.';
		$home    = esc_url( home_url( '/' ) );
		$year    = esc_html( date( 'Y' ) );

		$button = '';
		if ( ! empty( $cta['url'] ) && ! empty( $cta['label'] ) ) {
			$button = '<tr><td style="padding:8px 0 4px;">'
				. '<a href="' . esc_url( $cta['url'] ) . '" '
				. 'style="display:inline-block;background:#8a3b2c;color:#ffffff;text-decoration:none;'
				. 'font-weight:700;padding:12px 22px;border-radius:999px;">'
				. esc_html( $cta['label'] ) . '</a></td></tr>';
		}

		return '
<div style="background:#eef4f2;padding:24px 12px;font-family:Segoe UI,Helvetica,Arial,sans-serif;color:#2a2320;">
  <table role="presentation" width="100%" cellpadding="0" cellspacing="0" style="max-width:560px;margin:0 auto;background:#ffffff;border:1px solid #e4ddd4;border-radius:14px;overflow:hidden;">
    <tr>
      <td style="background:linear-gradient(150deg,#14617a,#0e4a5d);padding:22px 28px;">
        <div style="color:#ffffff;font-size:1.15rem;font-weight:800;letter-spacing:-.01em;">' . $brand . '</div>
        <div style="color:#a7dccb;font-size:.85rem;font-style:italic;">' . $tagline . '</div>
      </td>
    </tr>
    <tr>
      <td style="padding:28px;">
        <h1 style="margin:0 0 12px;color:#6b2c20;font-size:1.4rem;line-height:1.25;">' . esc_html( $heading ) . '</h1>
        <table role="presentation" width="100%" cellpadding="0" cellspacing="0" style="font-size:1rem;line-height:1.6;color:#2a2320;">
          ' . $body_html . '
          ' . $button . '
        </table>
      </td>
    </tr>
    <tr>
      <td style="padding:18px 28px;border-top:1px solid #e4ddd4;color:#5d534d;font-size:.82rem;">
        &copy; ' . $year . ' ' . $brand . ' &middot; <a href="' . $home . '" style="color:#14617a;">' . $home . '</a>
      </td>
    </tr>
  </table>
</div>';
	}

	protected static function p( $text ) {
		return '<tr><td style="padding:4px 0;">' . esc_html( $text ) . '</td></tr>';
	}

	/* ── Visit lifecycle ──────────────────────────────────────────────── */

	/**
	 * Notify the customer about a visit's current status.
	 * Called by HSS_Visits when notify is on.
	 */
	public static function visit_status( $visit ) {
		$user = get_userdata( (int) $visit->user_id );
		if ( ! $user ) { return false; }

		$first  = $user->first_name ?: $user->display_name;
		$first  = $first ? ' ' . $first : '';
		$when   = $visit->scheduled_date
			? date_i18n( 'l, F j', strtotime( $visit->scheduled_date ) )
			: 'soon';
		$window = $visit->time_window ? ' (' . $visit->time_window . ')' : '';
		$portal = HSS_Portal::portal_url();
		$cta    = [ 'label' => 'View my account', 'url' => $portal ];

		switch ( $visit->status ) {
			case 'scheduled':
				$subject = 'Your next yard cleanup is scheduled';
				$heading = "You're on the schedule";
				$body  = self::p( 'Hi' . $first . ',' );
				$body .= self::p( 'Your next cleanup is set for ' . $when . $window . '. You don\'t need to be home — just make sure we can reach the yard.' );
				if ( $visit->customer_note ) { $body .= self::p( 'Note: ' . $visit->customer_note ); }
				break;

			case 'enroute':
				$subject = "We're on the way";
				$heading = "We're headed your way";
				$body  = self::p( 'Hi' . $first . ',' );
				$body .= self::p( 'Your cleanup is starting — we\'re on the way now. We\'ll let you know as soon as it\'s done.' );
				if ( $visit->customer_note ) { $body .= self::p( 'Note: ' . $visit->customer_note ); }
				break;

			case 'completed':
				$subject = 'All done — your yard is clean';
				$heading = 'All clean!';
				$body  = self::p( 'Hi' . $first . ',' );
				$body .= self::p( 'We finished your cleanup' . ( $when === 'soon' ? '' : ' from ' . $when ) . ' — the yard is scooped and ready to enjoy.' );
				if ( $visit->customer_note ) { $body .= self::p( 'From your scooper: ' . $visit->customer_note ); }
				$body .= self::p( 'Thanks for being a customer!' );
				break;

			case 'skipped':
				$subject = 'About your scheduled cleanup';
				$heading = 'We had to skip this visit';
				$body  = self::p( 'Hi' . $first . ',' );
				$body .= self::p( 'We weren\'t able to complete your cleanup' . ( $when === 'soon' ? '' : ' on ' . $when ) . ' this time.' );
				if ( $visit->customer_note ) { $body .= self::p( 'Reason: ' . $visit->customer_note ); }
				$body .= self::p( 'We\'ll catch it on the next visit. Questions? Just reply to this email.' );
				break;

			default:
				return false; // canceled etc. — no customer email
		}

		return self::send( $user->user_email, $subject, $heading, $body, $cta );
	}

	/* ── Change requests ──────────────────────────────────────────────── */

	/** Notify the business that a customer submitted a change request. */
	public static function change_request_admin( $req ) {
		$user = get_userdata( (int) $req->user_id );
		$cname = $user ? $user->display_name : ( '#' . $req->user_id );
		$cmail = $user ? $user->user_email : '';

		$to      = get_option( 'admin_email' );
		$subject = 'New change request — ' . HSS_Change_Requests::type_label( $req->type );
		$heading = 'New customer request';

		$body  = self::p( 'Customer: ' . $cname . ( $cmail ? ' (' . $cmail . ')' : '' ) );
		$body .= self::p( 'Request: ' . HSS_Change_Requests::summary( $req ) );
		if ( $req->current_plan_key ) {
			$body .= self::p( 'Current plan: ' . HSS_Config::plan_label( $req->current_plan_key ) );
		}
		if ( $req->message ) {
			$body .= self::p( 'Their note: ' . $req->message );
		}

		$cta     = [ 'label' => 'Review in admin', 'url' => admin_url( 'admin.php?page=hss-portal-requests' ) ];
		$headers = $cmail ? [ 'Reply-To: ' . $cname . ' <' . $cmail . '>' ] : [];
		return self::send( $to, $subject, $heading, $body, $cta, $headers );
	}

	/** Tell the customer their request was approved or declined. */
	public static function change_request_resolved( $req ) {
		$user = get_userdata( (int) $req->user_id );
		if ( ! $user ) { return false; }

		$first = $user->first_name ?: $user->display_name;
		$first = $first ? ' ' . $first : '';
		$what  = HSS_Change_Requests::summary( $req );

		if ( $req->status === 'approved' ) {
			$subject = 'Your request is approved';
			$heading = 'Good news — you\'re all set';
			$body  = self::p( 'Hi' . $first . ',' );
			$body .= self::p( 'We\'ve approved your request: ' . $what . '.' );
		} else {
			$subject = 'About your recent request';
			$heading = 'An update on your request';
			$body  = self::p( 'Hi' . $first . ',' );
			$body .= self::p( 'We weren\'t able to approve your request: ' . $what . '.' );
		}
		if ( $req->admin_note ) {
			$body .= self::p( 'Note from our team: ' . $req->admin_note );
		}
		$body .= self::p( 'Questions? Just reply to this email and we\'ll help.' );

		$cta = [ 'label' => 'View my account', 'url' => HSS_Portal::portal_url() ];
		return self::send( $user->user_email, $subject, $heading, $body, $cta );
	}
}
