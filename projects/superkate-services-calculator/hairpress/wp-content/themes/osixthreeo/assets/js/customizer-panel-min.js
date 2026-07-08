/**
 * Customizer Hide/Show Panel functions
 *
 * @package    osixthreeo
 * @subpackage osixthreeo/assets/js
 * @author     Chip Sheppard
 * @since      1.0.0
 * @license    GPL-2.0+
 */
!function(e){"use strict";e("osixthreeo_settings[home_header_fullheight]",(function(t){var o;o=function(e){var o=function(){"adjustable"===t.get()||1===t.get()?e.container.slideDown(180):e.container.slideUp(180)};o(),t.bind(o)},e.control("osixthreeo_settings[home_header_height]",o),e.control("osixthreeo_settings[home_mobile_header_height]",o)}))}(wp.customize);