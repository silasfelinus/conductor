/**
 * Customizer Radio Image Control
 *
 * @package    osixthreeo
 * @subpackage osixthreeo/assets/js
 * @author     Chip Sheppard
 * @since      1.0.0
 * @license    GPL-2.0+
 */
jQuery(document).ready((function(){jQuery("#osixthreeo-img-container.controls label img").click((function(){jQuery(this).parents("#osixthreeo-img-container.controls").find("img").removeClass("osixthreeo-radio-img-selected"),jQuery(this).addClass("osixthreeo-radio-img-selected")}))}));