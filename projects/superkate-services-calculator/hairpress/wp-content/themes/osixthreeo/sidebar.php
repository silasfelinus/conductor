<?php
/**
 * The Sidebar.
 *
 * @package  osixthreeo
 * @author   Chip Sheppard
 * @since    1.0.0
 * @license  GPL-2.0+
 */

if ( ! is_active_sidebar( 'sidebar' ) && ! is_active_sidebar( 'sidebar-p' ) && ! is_active_sidebar( 'sidebar-w' ) ) {
	return;
}

osixthreeo_sidebars_before();
echo '<aside id="secondary" class="widget-area" role="complementary">';
osixthreeo_sidebar_top();
if ( OSTO_XTRAS ) {
	if ( OSIXTHREEO_WOOCOMMERCE_ACTIVE ) {
		if ( is_active_sidebar( 'sidebar-w' ) && ( is_woocommerce() || is_cart() || is_checkout() || is_account_page() ) ) {
			dynamic_sidebar( 'sidebar-w' );
		} elseif ( is_page() && is_active_sidebar( 'sidebar-p' ) ) {
			dynamic_sidebar( 'sidebar-p' );
		} else {
			dynamic_sidebar( 'sidebar' );
		};
	} elseif ( is_page() && is_active_sidebar( 'sidebar-p' ) ) {
		dynamic_sidebar( 'sidebar-p' );
	} else {
		dynamic_sidebar( 'sidebar' );
	};
} else {
	dynamic_sidebar( 'sidebar' );
};
osixthreeo_sidebar_bottom();
echo '</aside>';
osixthreeo_sidebars_after();
