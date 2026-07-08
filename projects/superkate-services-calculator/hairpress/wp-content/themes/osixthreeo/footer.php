<?php
/**
 * Site footer
 *
 * @package  osixthreeo
 * @author   Chip Sheppard
 * @since    1.0.0
 * @license  GPL-2.0+
 */

echo '</div>';  // /content-inner-wrap.
echo '</div>'; // /site-content.

osixthreeo_footer_before();
osixthreeo_footer_after();

echo '</div>'; // /site.
osixthreeo_body_bottom();
wp_footer();

echo '</body></html>';
