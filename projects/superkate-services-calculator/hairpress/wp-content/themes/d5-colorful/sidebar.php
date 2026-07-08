<?php
/* COLORFUL Theme'sRight Sidebar Area
	Copyright: 2012-2017, D5 Creation, www.d5creation.com
	
	Since COLORFUL 1.0
*/
?>
<div id="left-sidebar">
<?php if ( ! dynamic_sidebar( 'sidebar-1' ) ) : ?>

				<aside id="archives" class="widget">
					<h3 class="widget-title"><?php esc_html_e('Archives', 'd5-colorful'); ?></h3>
					<ul>
						<?php wp_get_archives( array( 'type' => 'monthly' ) ); ?>
					</ul>
				</aside>

				<aside id="meta" class="widget">
					<h3 class="widget-title"><?php esc_html_e('Meta', 'd5-colorful'); ?></h3>
					<ul>
						<?php wp_register(); ?>
						<li><?php wp_loginout(); ?></li>
						<?php wp_meta(); ?>
					</ul>
				</aside>

<?php endif; // end sidebar widget area ?>
<?php dynamic_sidebar( 'sidebar-2' ); ?>
</div>