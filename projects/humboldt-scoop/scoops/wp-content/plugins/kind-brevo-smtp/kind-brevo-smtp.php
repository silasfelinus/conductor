<?php
/**
 * Plugin Name: Kind Brevo Mailer
 * Description: Routes WordPress wp_mail through Brevo (Sendinblue) via API v3 (or SMTP fallback).
 * Version: 1.0.0
 * Author: Kind Robots
 * License: GPLv2 or later
 */

if (!defined('ABSPATH')) exit;

final class Kind_Brevo_Mailer {
  const OPTION_KEY = 'kind_brevo_mailer_options';
  const CAPABILITY = 'manage_options';
  const NONCE_ACTION_TEST = 'kind_brevo_mailer_send_test';
  const NONCE_ACTION_CLEARLOG = 'kind_brevo_mailer_clear_log';

  public static function init(): void {
    add_action('admin_menu', [__CLASS__, 'admin_menu']);
    add_action('admin_init', [__CLASS__, 'register_settings']);

    add_filter('pre_wp_mail', [__CLASS__, 'pre_wp_mail'], 10, 2);

    add_action('phpmailer_init', [__CLASS__, 'configure_phpmailer'], 10, 1);
    add_filter('wp_mail_from', [__CLASS__, 'filter_mail_from']);
    add_filter('wp_mail_from_name', [__CLASS__, 'filter_mail_from_name']);

    add_action('admin_post_kind_brevo_mailer_send_test', [__CLASS__, 'handle_send_test']);
    add_action('admin_post_kind_brevo_mailer_clear_log', [__CLASS__, 'handle_clear_log']);

    register_activation_hook(__FILE__, [__CLASS__, 'activate']);
  }

  public static function activate(): void {
    $opts = get_option(self::OPTION_KEY);
    if (!is_array($opts)) add_option(self::OPTION_KEY, self::default_options());
  }

  private static function default_options(): array {
    return [
      'enabled' => 1,
      'method' => 'api',

      'api_key' => '',
      'api_base_url' => 'https://api.brevo.com/v3',
      'api_sandbox' => 0,

      'smtp_host' => 'smtp-relay.brevo.com',
      'smtp_port' => 587,
      'smtp_encryption' => 'tls',
      'smtp_auth' => 1,
      'smtp_username' => '',
      'smtp_password' => '',

      'from_email' => '',
      'from_name' => '',
      'force_from' => 1,

      'timeout' => 15,

      'attachment_max_bytes' => 5242880,

      'debug' => 1,
      'last_log' => [
        'time' => '',
        'ok' => null,
        'message' => '',
        'http_code' => null,
        'brevo_code' => null,
        'brevo_message' => '',
        'request_id' => '',
        'details' => '',
      ],
    ];
  }

  private static function get_options(): array {
    $opts = get_option(self::OPTION_KEY, self::default_options());
    if (!is_array($opts)) $opts = self::default_options();
    $merged = array_merge(self::default_options(), $opts);

    if (!isset($merged['last_log']) || !is_array($merged['last_log'])) {
      $merged['last_log'] = self::default_options()['last_log'];
    }
    return $merged;
  }

  private static function update_options(array $opts): void {
    update_option(self::OPTION_KEY, $opts, false);
  }

  public static function admin_menu(): void {
    add_options_page(
      'Kind Brevo Mailer',
      'Kind Brevo Mailer',
      self::CAPABILITY,
      'kind-brevo-mailer',
      [__CLASS__, 'render_settings_page']
    );
  }

  public static function register_settings(): void {
    register_setting(
      'kind_brevo_mailer_group',
      self::OPTION_KEY,
      [
        'type' => 'array',
        'sanitize_callback' => [__CLASS__, 'sanitize_options'],
        'default' => self::default_options(),
      ]
    );

    add_settings_section(
      'kind_brevo_mailer_section_main',
      'Brevo Mail Settings',
      function () {
        echo '<p>Choose Brevo API (recommended) or SMTP. API sends via Brevo v3 Transactional Email endpoint.</p>';
      },
      'kind-brevo-mailer'
    );

    $fields = [
      'enabled' => ['Enabled', 'checkbox'],
      'method' => ['Send Method', 'select_method'],

      'api_key' => ['Brevo API Key (v3)', 'password'],
      'api_sandbox' => ['API Sandbox Mode', 'checkbox'],
      'api_base_url' => ['API Base URL', 'text'],

      'smtp_host' => ['SMTP Host', 'text'],
      'smtp_port' => ['SMTP Port', 'number'],
      'smtp_encryption' => ['SMTP Encryption', 'select_encryption'],
      'smtp_auth' => ['SMTP Use Auth', 'checkbox'],
      'smtp_username' => ['SMTP Username', 'text'],
      'smtp_password' => ['SMTP Password (SMTP key)', 'password'],

      'from_email' => ['From Email', 'email'],
      'from_name' => ['From Name', 'text'],
      'force_from' => ['Force From Name/Email', 'checkbox'],

      'timeout' => ['Timeout (seconds)', 'number'],
      'attachment_max_bytes' => ['Attachment Max Bytes (API mode)', 'number'],
      'debug' => ['Debug Log Last Result', 'checkbox'],
    ];

    foreach ($fields as $key => [$label, $type]) {
      add_settings_field(
        'kind_brevo_mailer_' . $key,
        esc_html($label),
        function () use ($key, $type) {
          self::render_field($key, $type);
        },
        'kind-brevo-mailer',
        'kind_brevo_mailer_section_main'
      );
    }
  }

  public static function sanitize_options($input): array {
    $d = self::default_options();
    $in = is_array($input) ? $input : [];
    $out = [];

    $out['enabled'] = !empty($in['enabled']) ? 1 : 0;

    $method = isset($in['method']) ? strtolower(sanitize_text_field($in['method'])) : $d['method'];
    $out['method'] = in_array($method, ['api', 'smtp'], true) ? $method : $d['method'];

    $out['api_key'] = isset($in['api_key']) ? self::sanitize_secret($in['api_key']) : '';
    $out['api_sandbox'] = !empty($in['api_sandbox']) ? 1 : 0;

    $base = isset($in['api_base_url']) ? esc_url_raw($in['api_base_url']) : $d['api_base_url'];
    if (empty($base)) $base = $d['api_base_url'];
    $out['api_base_url'] = rtrim($base, '/');

    $out['smtp_host'] = isset($in['smtp_host']) ? sanitize_text_field($in['smtp_host']) : $d['smtp_host'];

    $port = isset($in['smtp_port']) ? intval($in['smtp_port']) : $d['smtp_port'];
    if ($port < 1 || $port > 65535) $port = $d['smtp_port'];
    $out['smtp_port'] = $port;

    $enc = isset($in['smtp_encryption']) ? strtolower(sanitize_text_field($in['smtp_encryption'])) : $d['smtp_encryption'];
    $out['smtp_encryption'] = in_array($enc, ['none', 'tls', 'ssl'], true) ? $enc : $d['smtp_encryption'];

    $out['smtp_auth'] = !empty($in['smtp_auth']) ? 1 : 0;
    $out['smtp_username'] = isset($in['smtp_username']) ? sanitize_text_field($in['smtp_username']) : '';
    $out['smtp_password'] = isset($in['smtp_password']) ? self::sanitize_secret($in['smtp_password']) : '';

    $out['from_email'] = isset($in['from_email']) ? sanitize_email($in['from_email']) : '';
    $out['from_name'] = isset($in['from_name']) ? sanitize_text_field($in['from_name']) : '';
    $out['force_from'] = !empty($in['force_from']) ? 1 : 0;

    $timeout = isset($in['timeout']) ? intval($in['timeout']) : $d['timeout'];
    if ($timeout < 1 || $timeout > 120) $timeout = $d['timeout'];
    $out['timeout'] = $timeout;

    $maxb = isset($in['attachment_max_bytes']) ? intval($in['attachment_max_bytes']) : $d['attachment_max_bytes'];
    if ($maxb < 0) $maxb = $d['attachment_max_bytes'];
    $out['attachment_max_bytes'] = $maxb;

    $out['debug'] = !empty($in['debug']) ? 1 : 0;

    $existing = self::get_options();
    $out['last_log'] = $existing['last_log'] ?? $d['last_log'];

    return $out;
  }

  private static function sanitize_secret($value): string {
    if (!is_string($value)) return '';
    $value = wp_unslash($value);
    $value = preg_replace('/[\x00-\x1F\x7F]/u', '', $value);
    return trim($value);
  }

  private static function render_field(string $key, string $type): void {
    $o = self::get_options();
    $name = self::OPTION_KEY . '[' . $key . ']';
    $value = $o[$key] ?? '';

    if ($type === 'checkbox') {
      $checked = !empty($value) ? 'checked' : '';
      echo '<label><input type="checkbox" name="' . esc_attr($name) . '" value="1" ' . $checked . ' /></label>';
      return;
    }

    if ($type === 'select_method') {
      $val = (string) $value;
      echo '<select name="' . esc_attr($name) . '">';
      echo '<option value="api" ' . selected($val, 'api', false) . '>Brevo API (recommended)</option>';
      echo '<option value="smtp" ' . selected($val, 'smtp', false) . '>SMTP (fallback)</option>';
      echo '</select>';
      echo '<p class="description">API uses Brevo v3 transactional endpoint with api-key header.</p>';
      return;
    }

    if ($type === 'select_encryption') {
      $val = (string) $value;
      echo '<select name="' . esc_attr($name) . '">';
      echo '<option value="tls" ' . selected($val, 'tls', false) . '>TLS</option>';
      echo '<option value="ssl" ' . selected($val, 'ssl', false) . '>SSL</option>';
      echo '<option value="none" ' . selected($val, 'none', false) . '>None</option>';
      echo '</select>';
      return;
    }

    $input_type = $type;
    $class = 'regular-text';

    if ($type === 'number') {
      echo '<input name="' . esc_attr($name) . '" type="number" class="' . esc_attr($class) . '" value="' . esc_attr((string) $value) . '" />';
      return;
    }

    $autocomplete = ($type === 'password') ? 'new-password' : 'off';
    echo '<input name="' . esc_attr($name) . '" type="' . esc_attr($input_type) . '" class="' . esc_attr($class) . '" value="' . esc_attr((string) $value) . '" autocomplete="' . esc_attr($autocomplete) . '" />';
  }

  public static function render_settings_page(): void {
    if (!current_user_can(self::CAPABILITY)) return;

    $o = self::get_options();

    $test_result = isset($_GET['kbm_test']) ? sanitize_text_field(wp_unslash($_GET['kbm_test'])) : '';
    $test_msg = isset($_GET['kbm_msg']) ? sanitize_text_field(wp_unslash($_GET['kbm_msg'])) : '';

    echo '<div class="wrap">';
    echo '<h1>Kind Brevo Mailer</h1>';

    if ($test_result === 'success') {
      echo '<div class="notice notice-success"><p>' . esc_html($test_msg ?: 'Test email sent.') . '</p></div>';
    } elseif ($test_result === 'error') {
      echo '<div class="notice notice-error"><p>' . esc_html($test_msg ?: 'Test email failed.') . '</p></div>';
    }

    echo '<form method="post" action="options.php">';
    settings_fields('kind_brevo_mailer_group');
    do_settings_sections('kind-brevo-mailer');
    submit_button('Save Settings');
    echo '</form>';

    echo '<hr/>';

    echo '<h2>Send Test Email</h2>';
    echo '<p>Sends using wp_mail(). If API method is selected, it is sent through Brevo API v3.</p>';
    echo '<form method="post" action="' . esc_url(admin_url('admin-post.php')) . '">';
    echo '<input type="hidden" name="action" value="kind_brevo_mailer_send_test" />';
    wp_nonce_field(self::NONCE_ACTION_TEST, 'kbm_nonce');

    $default_to = wp_get_current_user() && wp_get_current_user()->user_email ? wp_get_current_user()->user_email : get_option('admin_email');

    echo '<table class="form-table" role="presentation">';
    echo '<tr><th scope="row"><label for="kbm_test_to">To</label></th><td>';
    echo '<input name="to" id="kbm_test_to" type="email" class="regular-text" value="' . esc_attr($default_to) . '" required />';
    echo '</td></tr>';

    echo '<tr><th scope="row"><label for="kbm_test_subject">Subject</label></th><td>';
    echo '<input name="subject" id="kbm_test_subject" type="text" class="regular-text" value="Brevo Mailer Test" required />';
    echo '</td></tr>';

    echo '<tr><th scope="row"><label for="kbm_test_message">Message</label></th><td>';
    echo '<textarea name="message" id="kbm_test_message" class="large-text" rows="4" required>Hello from Kind Brevo Mailer.</textarea>';
    echo '<p class="description">Tip: add <code>&lt;b&gt;bold&lt;/b&gt;</code> to confirm HTML sending.</p>';
    echo '</td></tr>';

    echo '<tr><th scope="row"><label for="kbm_test_is_html">HTML</label></th><td>';
    echo '<label><input name="is_html" id="kbm_test_is_html" type="checkbox" value="1" checked /> Send as HTML</label>';
    echo '</td></tr>';
    echo '</table>';

    submit_button('Send Test Email');
    echo '</form>';

    echo '<hr/>';

    echo '<h2>Last Result</h2>';
    $log = $o['last_log'] ?? [];
    $time = $log['time'] ?? '';
    $ok = array_key_exists('ok', $log) ? $log['ok'] : null;

    echo '<p><strong>Status:</strong> ' . esc_html($ok === true ? 'OK' : ($ok === false ? 'FAILED' : 'None yet')) . '</p>';
    echo '<p><strong>Time:</strong> ' . esc_html($time ?: '-') . '</p>';
    echo '<p><strong>Message:</strong> ' . esc_html($log['message'] ?? '-') . '</p>';

    if (!empty($o['debug'])) {
      echo '<details style="max-width: 900px;"><summary>Details</summary>';
      echo '<pre style="white-space: pre-wrap; background: #fff; padding: 12px; border: 1px solid #ddd;">' . esc_html(print_r($log, true)) . '</pre>';
      echo '</details>';

      echo '<form method="post" action="' . esc_url(admin_url('admin-post.php')) . '">';
      echo '<input type="hidden" name="action" value="kind_brevo_mailer_clear_log" />';
      wp_nonce_field(self::NONCE_ACTION_CLEARLOG, 'kbm_clear_nonce');
      submit_button('Clear Last Result', 'secondary');
      echo '</form>';
    }

    echo '<hr/>';
    echo '<h2>Brevo Notes</h2>';
    echo '<ul>';
    echo '<li>API sending uses <code>POST /v3/smtp/email</code> with header <code>api-key</code>.</li>';
    echo '<li>SMTP sending uses an SMTP key, not the API key.</li>';
    echo '</ul>';

    echo '</div>';
  }

  public static function handle_clear_log(): void {
    if (!current_user_can(self::CAPABILITY)) wp_die('Unauthorized', 403);
    $nonce = isset($_POST['kbm_clear_nonce']) ? sanitize_text_field(wp_unslash($_POST['kbm_clear_nonce'])) : '';
    if (!wp_verify_nonce($nonce, self::NONCE_ACTION_CLEARLOG)) wp_die('Invalid nonce', 403);

    $o = self::get_options();
    $o['last_log'] = self::default_options()['last_log'];
    self::update_options($o);

    wp_safe_redirect(add_query_arg(['page' => 'kind-brevo-mailer'], admin_url('options-general.php')));
    exit;
  }

  public static function handle_send_test(): void {
    if (!current_user_can(self::CAPABILITY)) wp_die('Unauthorized', 403);

    $nonce = isset($_POST['kbm_nonce']) ? sanitize_text_field(wp_unslash($_POST['kbm_nonce'])) : '';
    if (!wp_verify_nonce($nonce, self::NONCE_ACTION_TEST)) wp_die('Invalid nonce', 403);

    $to = isset($_POST['to']) ? sanitize_email(wp_unslash($_POST['to'])) : '';
    $subject = isset($_POST['subject']) ? sanitize_text_field(wp_unslash($_POST['subject'])) : '';
    $message = isset($_POST['message']) ? wp_kses_post(wp_unslash($_POST['message'])) : '';
    $is_html = !empty($_POST['is_html']);

    if (empty($to) || !is_email($to)) self::redirect_with_msg('error', 'Invalid To email address.');
    if (empty($subject) || empty($message)) self::redirect_with_msg('error', 'Subject and message are required.');

    $headers = [];
    if ($is_html) $headers[] = 'Content-Type: text/html; charset=UTF-8';

    $sent = wp_mail($to, $subject, $message, $headers);

    if ($sent) self::redirect_with_msg('success', 'Test email sent successfully.');
    self::redirect_with_msg('error', 'wp_mail() returned false. Check Brevo credentials and logs below.');
  }

  private static function redirect_with_msg(string $result, string $msg): void {
    $url = add_query_arg(
      [
        'page' => 'kind-brevo-mailer',
        'kbm_test' => $result,
        'kbm_msg' => rawurlencode($msg),
      ],
      admin_url('options-general.php')
    );
    wp_safe_redirect($url);
    exit;
  }

  private static function set_last_log(array $patch): void {
    $o = self::get_options();
    if (empty($o['debug'])) return;

    $log = $o['last_log'] ?? self::default_options()['last_log'];
    $merged = array_merge($log, $patch);
    $o['last_log'] = $merged;
    self::update_options($o);
  }

  public static function pre_wp_mail($null, $atts) {
    $o = self::get_options();
    if (empty($o['enabled'])) return $null;

    if (($o['method'] ?? 'api') !== 'api') return $null;

    $api_key = $o['api_key'] ?? '';
    if (empty($api_key)) {
      self::set_last_log([
        'time' => gmdate('c'),
        'ok' => false,
        'message' => 'Brevo API key is missing.',
      ]);
      return false;
    }

    $parsed = self::normalize_wp_mail_atts($atts);
    $result = self::send_via_brevo_api($parsed, $o);

    if ($result['ok']) return true;

    return false;
  }

  private static function normalize_wp_mail_atts($atts): array {
    $to = $atts['to'] ?? [];
    $subject = $atts['subject'] ?? '';
    $message = $atts['message'] ?? '';
    $headers = $atts['headers'] ?? [];
    $attachments = $atts['attachments'] ?? [];

    if (!is_array($to)) $to = [$to];
    if (!is_array($headers)) $headers = [$headers];
    if (!is_array($attachments)) $attachments = [$attachments];

    $header_map = self::parse_headers($headers);

    $content_type = $header_map['content-type'] ?? '';
    $is_html = stripos($content_type, 'text/html') !== false;

    return [
      'to' => self::parse_address_list($to),
      'subject' => (string) $subject,
      'message' => (string) $message,
      'is_html' => $is_html,
      'reply_to' => self::parse_address_list($header_map['reply-to'] ?? []),
      'cc' => self::parse_address_list($header_map['cc'] ?? []),
      'bcc' => self::parse_address_list($header_map['bcc'] ?? []),
      'attachments' => array_values(array_filter($attachments, 'is_string')),
    ];
  }

  private static function parse_headers(array $headers): array {
    $map = [
      'content-type' => '',
      'reply-to' => [],
      'cc' => [],
      'bcc' => [],
    ];

    foreach ($headers as $h) {
      if (!is_string($h)) continue;
      $h = trim($h);
      if ($h === '') continue;

      $parts = explode(':', $h, 2);
      if (count($parts) !== 2) continue;

      $key = strtolower(trim($parts[0]));
      $val = trim($parts[1]);

      if ($key === 'content-type') {
        $map['content-type'] = $val;
        continue;
      }

      if (in_array($key, ['reply-to', 'cc', 'bcc'], true)) {
        $items = array_map('trim', explode(',', $val));
        foreach ($items as $item) {
          if ($item !== '') $map[$key][] = $item;
        }
      }
    }

    return $map;
  }

  private static function parse_address_list(array $items): array {
    $out = [];
    foreach ($items as $item) {
      if (!is_string($item)) continue;
      $item = trim($item);
      if ($item === '') continue;

      $name = '';
      $email = $item;

      if (preg_match('/^(.*)<(.+)>$/', $item, $m)) {
        $name = trim(trim($m[1]), "\"' ");
        $email = trim($m[2]);
      }

      $email = sanitize_email($email);
      if (!is_email($email)) continue;

      $out[] = [
        'email' => $email,
        'name' => $name,
      ];
    }
    return $out;
  }

  private static function build_sender(array $o): array {
    $email = $o['from_email'] ?? '';
    $name = $o['from_name'] ?? '';

    if (empty($email) || !is_email($email)) {
      $email = get_option('admin_email');
    }
    if (empty($name)) {
      $name = get_bloginfo('name');
    }

    return [
      'email' => $email,
      'name' => $name,
    ];
  }

  private static function send_via_brevo_api(array $mail, array $o): array {
    $base = rtrim((string) ($o['api_base_url'] ?? 'https://api.brevo.com/v3'), '/');
    $url = $base . '/smtp/email';

    $payload = [
      'sender' => self::build_sender($o),
      'to' => $mail['to'],
      'subject' => $mail['subject'],
    ];

    if (!empty($mail['reply_to'])) {
      $payload['replyTo'] = [
        'email' => $mail['reply_to'][0]['email'],
        'name' => $mail['reply_to'][0]['name'] ?? '',
      ];
    }

    if (!empty($mail['cc'])) $payload['cc'] = $mail['cc'];
    if (!empty($mail['bcc'])) $payload['bcc'] = $mail['bcc'];

    if (!empty($mail['is_html'])) {
      $payload['htmlContent'] = $mail['message'];
    } else {
      $payload['textContent'] = wp_strip_all_tags($mail['message']);
    }

    $attachments = self::prepare_attachments($mail['attachments'], (int) ($o['attachment_max_bytes'] ?? 0));
    if ($attachments['error']) {
      self::set_last_log([
        'time' => gmdate('c'),
        'ok' => false,
        'message' => 'Attachment error: ' . $attachments['error'],
        'details' => $attachments['details'],
      ]);
      return ['ok' => false];
    }
    if (!empty($attachments['files'])) {
      $payload['attachment'] = $attachments['files'];
    }

    $headers = [
      'accept' => 'application/json',
      'content-type' => 'application/json',
      'api-key' => (string) ($o['api_key'] ?? ''),
    ];

    if (!empty($o['api_sandbox'])) {
      $headers['X-sib-sandbox'] = 'drop';
    }

    $resp = wp_remote_post($url, [
      'headers' => $headers,
      'timeout' => (int) ($o['timeout'] ?? 15),
      'body' => wp_json_encode($payload),
    ]);

    if (is_wp_error($resp)) {
      self::set_last_log([
        'time' => gmdate('c'),
        'ok' => false,
        'message' => 'WP HTTP error: ' . $resp->get_error_message(),
      ]);
      return ['ok' => false];
    }

    $code = wp_remote_retrieve_response_code($resp);
    $body = wp_remote_retrieve_body($resp);
    $json = json_decode($body, true);
    $request_id = wp_remote_retrieve_header($resp, 'x-request-id');

    $ok = ($code >= 200 && $code < 300);

    $brevo_code = is_array($json) && isset($json['code']) ? (string) $json['code'] : null;
    $brevo_msg = is_array($json) && isset($json['message']) ? (string) $json['message'] : '';

    self::set_last_log([
      'time' => gmdate('c'),
      'ok' => $ok,
      'message' => $ok ? 'Sent via Brevo API.' : 'Brevo API failed.',
      'http_code' => $code,
      'brevo_code' => $brevo_code,
      'brevo_message' => $brevo_msg,
      'request_id' => is_string($request_id) ? $request_id : '',
      'details' => $ok ? '' : $body,
    ]);

    return ['ok' => $ok];
  }

  private static function prepare_attachments(array $paths, int $max_bytes): array {
    if ($max_bytes <= 0) return ['error' => '', 'files' => [], 'details' => ''];

    $total = 0;
    $files = [];

    foreach ($paths as $path) {
      $path = (string) $path;
      if ($path === '') continue;
      if (!file_exists($path) || !is_readable($path)) {
        return ['error' => 'Attachment not readable: ' . basename($path), 'files' => [], 'details' => $path];
      }

      $size = filesize($path);
      if ($size === false) $size = 0;

      $total += (int) $size;
      if ($total > $max_bytes) {
        return ['error' => 'Attachments exceed max bytes (' . $max_bytes . ').', 'files' => [], 'details' => 'Total: ' . $total];
      }

      $content = file_get_contents($path);
      if ($content === false) {
        return ['error' => 'Failed to read attachment: ' . basename($path), 'files' => [], 'details' => $path];
      }

      $files[] = [
        'name' => basename($path),
        'content' => base64_encode($content),
      ];
    }

    return ['error' => '', 'files' => $files, 'details' => ''];
  }

  public static function configure_phpmailer($phpmailer): void {
    $o = self::get_options();
    if (empty($o['enabled'])) return;
    if (($o['method'] ?? 'api') !== 'smtp') return;

    if (empty($o['smtp_host']) || empty($o['smtp_port'])) return;

    $phpmailer->isSMTP();
    $phpmailer->Host = (string) $o['smtp_host'];
    $phpmailer->Port = (int) $o['smtp_port'];
    $phpmailer->Timeout = (int) ($o['timeout'] ?? 15);

    if (!empty($o['smtp_auth'])) {
      $phpmailer->SMTPAuth = true;
      $phpmailer->Username = (string) ($o['smtp_username'] ?? '');
      $phpmailer->Password = (string) ($o['smtp_password'] ?? '');
    } else {
      $phpmailer->SMTPAuth = false;
    }

    $enc = (string) ($o['smtp_encryption'] ?? 'tls');
    if ($enc === 'tls') {
      $phpmailer->SMTPSecure = 'tls';
    } elseif ($enc === 'ssl') {
      $phpmailer->SMTPSecure = 'ssl';
    } else {
      $phpmailer->SMTPSecure = '';
      $phpmailer->SMTPAutoTLS = false;
    }

    if (!empty($o['force_from'])) {
      $sender = self::build_sender($o);
      try {
        $phpmailer->setFrom($sender['email'], $sender['name'], false);
      } catch (Exception $e) {
      }
    }
  }

  public static function filter_mail_from($from): string {
    $o = self::get_options();
    if (empty($o['enabled']) || empty($o['force_from'])) return $from;
    if (!empty($o['from_email']) && is_email($o['from_email'])) return $o['from_email'];
    return $from;
  }

  public static function filter_mail_from_name($name): string {
    $o = self::get_options();
    if (empty($o['enabled']) || empty($o['force_from'])) return $name;
    if (!empty($o['from_name'])) return $o['from_name'];
    return $name;
  }
}

Kind_Brevo_Mailer::init();