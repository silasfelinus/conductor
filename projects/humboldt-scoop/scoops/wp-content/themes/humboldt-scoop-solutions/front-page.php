<?php
/**
 * front-page.php — Humboldt Scoop Solutions homepage.
 * Self-contained brochure layout (no reliance on Gutenberg block content).
 * @package hss
 */
if ( ! defined( 'ABSPATH' ) ) { exit; }
get_header();

$pricing     = hss_pricing();
$portal      = hss_portal_url();
$logged_in   = is_user_logged_in();
?>

<!-- ░░ HERO ░░ -->
<header class="hss-hero">
	<div class="hss-container hss-hero-inner">
		<p class="hss-eyebrow">Humboldt County, California</p>
		<h1 class="hss-hero-title">A cleaner yard,<br>without the dirty work.</h1>
		<p class="hss-hero-sub">
			Humboldt Scoop Solutions handles your dog's business so you don't have to.
			Reliable, local, and friendly pooper-scooper service for homes, rentals, and shared spaces.
		</p>
		<div class="hss-hero-cta">
			<a href="#hss-pricing" class="hss-btn hss-btn-primary">See Plans &amp; Pricing</a>
			<a href="#hss-contact" class="hss-btn hss-btn-ghost">Get a Free Quote</a>
		</div>
		<ul class="hss-hero-badges">
			<li>✓ Locally owned</li>
			<li>✓ Flat, honest pricing</li>
			<li>✓ Cancel anytime</li>
		</ul>
	</div>
</header>

<!-- ░░ WHY US ░░ -->
<section id="hss-why" class="hss-section hss-why">
	<div class="hss-container">
		<h2 class="hss-section-title">Why Choose Us</h2>
		<div class="hss-grid hss-grid-3">
			<article class="hss-card">
				<div class="hss-card-icon">🌲</div>
				<h3>Local &amp; dependable</h3>
				<p>We live here too. You get a familiar face on a schedule you can count on — not a faceless franchise.</p>
			</article>
			<article class="hss-card">
				<div class="hss-card-icon">🧼</div>
				<h3>Thorough &amp; tidy</h3>
				<p>We sweep the whole yard, double-check the corners, and haul everything away. You just enjoy the grass.</p>
			</article>
			<article class="hss-card">
				<div class="hss-card-icon">💙</div>
				<h3>Friendly &amp; flexible</h3>
				<p>Gate codes, shy dogs, special instructions — tell us once and we've got it. Change or pause anytime.</p>
			</article>
		</div>
	</div>
</section>

<!-- ░░ SERVICES ░░ -->
<section id="hss-services" class="hss-section hss-alt">
	<div class="hss-container">
		<h2 class="hss-section-title">What We Offer</h2>
		<p class="hss-section-lead">Pick a regular plan to stay on top of it, or book a one-time cleanup to reset the yard.</p>
		<div class="hss-grid hss-grid-4">
			<article class="hss-service">
				<h3>One-Time Cleanup</h3>
				<p>Perfect for a spring reset, a move-out, or before a backyard party. We clear the backlog in one visit.</p>
			</article>
			<article class="hss-service">
				<h3>Weekly</h3>
				<p>Our most popular plan. The yard never gets a chance to build up. Ideal for active dogs and busy households.</p>
			</article>
			<article class="hss-service">
				<h3>Bi-Weekly</h3>
				<p>Twice-a-month visits that keep things in check without the weekly cadence.</p>
			</article>
			<article class="hss-service">
				<h3>Monthly</h3>
				<p>A light-touch plan for smaller dogs or larger properties that just need a regular tidy.</p>
			</article>
		</div>
		<p class="hss-note">Commercial, HOA, and shared-space service available — <a href="#hss-contact">ask for a custom quote</a>.</p>
	</div>
</section>

<!-- ░░ PRICING ░░ -->
<section id="hss-pricing" class="hss-section">
	<div class="hss-container">
		<h2 class="hss-section-title">Plans &amp; Pricing</h2>
		<p class="hss-section-lead">Simple monthly pricing based on how often we visit and how many dogs you have. No contracts, cancel anytime.</p>

		<div class="hss-pricing-grid">
			<?php
			$featured = 'weekly';
			foreach ( $pricing as $key => $plan ) :
				$is_feat = ( $key === $featured );
			?>
			<div class="hss-plan <?php echo $is_feat ? 'hss-plan-featured' : ''; ?>">
				<?php if ( $is_feat ) : ?><span class="hss-plan-flag">Most popular</span><?php endif; ?>
				<h3 class="hss-plan-name"><?php echo esc_html( $plan['label'] ); ?></h3>
				<p class="hss-plan-desc"><?php echo esc_html( $plan['desc'] ); ?></p>
				<p class="hss-plan-price">
					<span class="hss-plan-from">from</span>
					<span class="hss-plan-amount">$<?php echo esc_html( $plan['prices'][1] ); ?></span>
					<span class="hss-plan-per">/mo</span>
				</p>
				<table class="hss-plan-tiers">
					<tr><td>1 dog</td><td>$<?php echo esc_html( $plan['prices'][1] ); ?>/mo</td></tr>
					<tr><td>2 dogs</td><td>$<?php echo esc_html( $plan['prices'][2] ); ?>/mo</td></tr>
					<tr><td>3 dogs</td><td>$<?php echo esc_html( $plan['prices'][3] ); ?>/mo</td></tr>
				</table>
				<div class="hss-plan-actions">
					<label class="hss-plan-dogs">
						Dogs
						<select data-plan-dogs>
							<option value="1">1</option>
							<option value="2">2</option>
							<option value="3">3</option>
						</select>
					</label>
					<a class="hss-btn hss-btn-primary hss-plan-cta"
					   data-plan="<?php echo esc_attr( $key ); ?>"
					   href="<?php echo esc_url( add_query_arg( [ 'plan' => $key, 'dogs' => 1 ], $portal ) ); ?>">
						Choose <?php echo esc_html( $plan['label'] ); ?>
					</a>
				</div>
			</div>
			<?php endforeach; ?>

			<!-- One-time -->
			<div class="hss-plan hss-plan-onetime">
				<h3 class="hss-plan-name">One-Time Cleanup</h3>
				<p class="hss-plan-desc">Great for a one-off reset</p>
				<p class="hss-plan-price">
					<span class="hss-plan-amount">$40</span>
					<span class="hss-plan-per">/ half hour</span>
				</p>
				<p class="hss-plan-onetime-note">Most standard yards are handled in a single half-hour visit. Larger backlogs are billed per additional half hour.</p>
				<a class="hss-btn hss-btn-secondary"
				   data-plan="onetime"
				   href="<?php echo esc_url( add_query_arg( [ 'plan' => 'onetime' ], $portal ) ); ?>">
					Book a Cleanup
				</a>
			</div>
		</div>

		<p class="hss-note hss-pricing-foot">
			Have <strong>4 or more dogs</strong>, a large property, or a commercial space?
			<a href="#hss-contact">Request a custom quote</a> — we'll size it to your yard.
		</p>
	</div>
</section>

<!-- ░░ WHO WE SERVE ░░ -->
<section id="hss-who" class="hss-section hss-alt">
	<div class="hss-container">
		<h2 class="hss-section-title">Who We Serve</h2>
		<ul class="hss-chips">
			<li>Homeowners</li>
			<li>Apartments &amp; HOAs</li>
			<li>Landlords</li>
			<li>Elderly clients</li>
			<li>Clients with disabilities</li>
			<li>Busy professionals</li>
			<li>Dog breeders</li>
			<li>Landscapers</li>
			<li>Contractors</li>
			<li>Parks &amp; shared spaces</li>
		</ul>
	</div>
</section>

<!-- ░░ ABOUT / TEAM ░░ -->
<!--
	Bios below are easy-to-edit placeholders drawn from the project notes.
	Swap in real photos by replacing the .hss-team-avatar initials block with
	<img class="hss-team-photo" src="…" alt="Name">.
-->
<section id="hss-about" class="hss-section">
	<div class="hss-container hss-narrow hss-center">
		<p class="hss-eyebrow">Local &amp; independent</p>
		<h2 class="hss-section-title">Meet the Team</h2>
		<p class="hss-section-lead">
			Humboldt Scoop Solutions is a small, local crew — real people from right here,
			not a franchise call center. When you book with us, you're supporting neighbors.
		</p>
	</div>
	<div class="hss-container">
		<div class="hss-team hss-grid hss-grid-3">
			<article class="hss-team-card">
				<div class="hss-team-avatar" aria-hidden="true">VG</div>
				<h3 class="hss-team-name">Viktors Graube</h3>
				<p class="hss-team-role">Founder</p>
				<p class="hss-team-bio">Started Humboldt Scoop Solutions to bring dependable, no-hassle yard cleanup to the county. Keeps the operation moving behind the scenes.</p>
			</article>
			<article class="hss-team-card">
				<div class="hss-team-avatar" aria-hidden="true">SK</div>
				<h3 class="hss-team-name">Silas Knight</h3>
				<p class="hss-team-role">Operations &amp; Web</p>
				<p class="hss-team-bio">Builds and runs the booking system and customer portal, and keeps every route on schedule so your yard stays on track.</p>
			</article>
			<article class="hss-team-card">
				<div class="hss-team-avatar" aria-hidden="true">KK</div>
				<h3 class="hss-team-name">Kathryn “superkate!” Knight</h3>
				<p class="hss-team-role">Marketing &amp; Community</p>
				<p class="hss-team-bio">Spreads the word, runs the Poopstakes, and keeps our community ties strong across Humboldt.</p>
			</article>
		</div>
	</div>
</section>

<!-- ░░ FAQ ░░ -->
<section id="hss-faq" class="hss-section">
	<div class="hss-container hss-narrow">
		<h2 class="hss-section-title">Frequently Asked Questions</h2>
		<div class="hss-faq">
			<details class="hss-faq-item">
				<summary>Do I need to be home during service?</summary>
				<p>Nope. As long as we can safely access the yard — a gate code or unlocked side gate is perfect — you don't need to be there. We'll let you know when we're on the way and when we're done.</p>
			</details>
			<details class="hss-faq-item">
				<summary>What do you do with the waste?</summary>
				<p>We bag everything and haul it away with us, or place it in your bin if you prefer. Your yard is left clean and ready to enjoy.</p>
			</details>
			<details class="hss-faq-item">
				<summary>What about my dogs while you're working?</summary>
				<p>We're comfortable around dogs of all kinds. If your dog is shy, protective, or needs to stay inside during service, just tell us in your service notes and we'll work around it.</p>
			</details>
			<details class="hss-faq-item">
				<summary>Can I change or cancel my plan?</summary>
				<p>Anytime. There are no contracts. You can upgrade, downgrade, pause, or cancel right from your customer account.</p>
			</details>
			<details class="hss-faq-item">
				<summary>How do I pay?</summary>
				<p>Securely online. Recurring plans are billed monthly to your card, and one-time cleanups are paid at booking. You can view invoices and manage billing anytime in your account.</p>
			</details>
			<details class="hss-faq-item">
				<summary>What areas do you cover?</summary>
				<p>We serve Humboldt County, centered around Arcata, Eureka, and the surrounding communities. Not sure if you're in range? <a href="#hss-contact">Ask us</a>.</p>
			</details>
		</div>
	</div>
</section>

<!-- ░░ POOPSTAKES ░░ -->
<section id="hss-poopstakes" class="hss-section hss-poopstakes">
	<div class="hss-container hss-narrow hss-center">
		<p class="hss-eyebrow hss-eyebrow-light">Our giveaway</p>
		<h2 class="hss-section-title hss-title-light">The Poopstakes 💩🎟️</h2>
		<p class="hss-poopstakes-copy">
			Every new customer is automatically entered into the Poopstakes — our recurring giveaway for free service,
			local goodies, and good-dog bragging rights. Sign up for any plan and you're in.
		</p>
		<a href="#hss-pricing" class="hss-btn hss-btn-light">Enter by Signing Up</a>
	</div>
</section>

<!-- ░░ CONTACT / QUOTE ░░ -->
<section id="hss-contact" class="hss-section hss-alt">
	<div class="hss-container hss-narrow">
		<h2 class="hss-section-title">Get a Free Quote</h2>
		<p class="hss-section-lead">Tell us about your yard and we'll get back to you with pricing — usually within a day.</p>

		<form class="hss-quote-form" id="hss-quote-form">
			<div class="hss-form-row">
				<label>Name
					<input type="text" name="name" required autocomplete="name">
				</label>
				<label>Phone
					<input type="tel" name="phone" autocomplete="tel">
				</label>
			</div>
			<div class="hss-form-row">
				<label>Email
					<input type="email" name="email" required autocomplete="email">
				</label>
				<label>Service area / city
					<input type="text" name="city" placeholder="Arcata, Eureka…">
				</label>
			</div>
			<div class="hss-form-row">
				<label>Number of dogs
					<select name="dogs">
						<option>1</option><option>2</option><option>3</option><option>4+</option>
					</select>
				</label>
				<label>Interested in
					<select name="interest">
						<option>Weekly</option>
						<option>Bi-Weekly</option>
						<option>Monthly</option>
						<option>One-time cleanup</option>
						<option>Commercial / HOA</option>
						<option>Not sure yet</option>
					</select>
				</label>
			</div>
			<label>Anything we should know?
				<textarea name="message" rows="4" placeholder="Yard size, gate access, special instructions…"></textarea>
			</label>
			<input type="text" name="hss_hp" class="hss-hp" tabindex="-1" autocomplete="off" aria-hidden="true">
			<button type="submit" class="hss-btn hss-btn-primary">Request My Quote</button>
			<p class="hss-form-status" data-quote-status role="status"></p>
		</form>
	</div>
</section>

<?php
get_footer();
