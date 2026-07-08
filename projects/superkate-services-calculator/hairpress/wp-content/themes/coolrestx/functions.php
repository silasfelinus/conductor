<?php

/**
 * @package coolrestx
 */
require_once get_template_directory() . "/backend/customizer/coolrestx_customizer.php";
require_once get_template_directory() . "/frontend/coolrestx_custom_jsstyle.php";
require_once get_template_directory() . "/frontend/coolrestx_custom_themesupport.php";
require_once get_template_directory() . "/frontend/coolrestx_custom_widgets.php";
require_once get_template_directory() . "/frontend/coolrestx_custom_content_excerpt.php";

function coolrestx_skip_link_focus_fix() {
    // The following is minified via `terser --compress --mangle -- js/skip-link-focus-fix.js`.
    ?>
    <script>
        /(trident|msie)/i.test(navigator.userAgent) && document.getElementById && window.addEventListener && window.addEventListener("hashchange", function () {
            var t, e = location.hash.substring(1);
            /^[A-z0-9_-]+$/.test(e) && (t = document.getElementById(e)) && (/^(?:a|select|input|button|textarea)$/i.test(t.tagName) || (t.tabIndex = -1), t.focus())
        }, !1);
    </script>
    <!-- menu dropdown accessibility -->
    <script type="text/javascript">

        jQuery(document).ready(function () {
            jQuery(".nav").coolrestxAccessibleDropDown();
        });

        jQuery.fn.coolrestxAccessibleDropDown = function () {
            var el = jQuery(this);

            /* Make dropdown menus keyboard accessible */

            jQuery("a", el).focus(function () {
                jQuery(this).parents("li").addClass("hover");
            }).blur(function () {
                jQuery(this).parents("li").removeClass("hover");
            });
        };
    </script>
    <?php

}

add_action('wp_print_footer_scripts', 'coolrestx_skip_link_focus_fix');

function coolrestx_sanitize_phone_number($phone) {
    return preg_replace('/[^\d+]/', '', $phone);
}
