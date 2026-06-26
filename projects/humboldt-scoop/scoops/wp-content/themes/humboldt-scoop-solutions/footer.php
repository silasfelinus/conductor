<?php
/**
 * Footer.
 * @package hss
 */
if ( ! defined( 'ABSPATH' ) ) { exit; }
?>
</main><!-- /.site-main -->

<footer class="hss-footer">
	<div class="hss-footer-inner">
		<div class="hss-footer-brand">
			<strong>Humboldt Scoop Solutions</strong>
			<span>Your dog's business is our business.</span>
		</div>
		<nav class="hss-footer-links" aria-label="Footer">
			<a href="<?php echo esc_url( home_url( '/#hss-services' ) ); ?>">Services</a>
			<a href="<?php echo esc_url( home_url( '/#hss-pricing' ) ); ?>">Pricing</a>
			<a href="<?php echo esc_url( home_url( '/#hss-about' ) ); ?>">About</a>
			<a href="<?php echo esc_url( home_url( '/#hss-faq' ) ); ?>">FAQ</a>
			<a href="<?php echo esc_url( hss_portal_url() ); ?>">Customer Login</a>
			<a href="<?php echo esc_url( home_url( '/#hss-contact' ) ); ?>">Contact</a>
		</nav>
		<div class="hss-footer-follow">
			<span>Follow Along</span>
			<small>Social channels coming soon.</small>
		</div>
	</div>
	<p class="hss-footer-legal">
		© <?php echo esc_html( date( 'Y' ) ); ?> Humboldt Scoop Solutions &middot; Arcata, CA
		&middot; <a href="mailto:info@humboldtscoopsolutions.com">info@humboldtscoopsolutions.com</a>
	</p>
</footer>

<?php wp_footer(); ?>
</body>
</html>
