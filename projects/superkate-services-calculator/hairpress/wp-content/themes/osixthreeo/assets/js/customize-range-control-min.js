/**
 * Customizer Range slider
 *
 * @package    osixthreeo
 * @subpackage osixthreeo/assets/js
 * @author     Chip Sheppard
 * @since      1.0.0
 * @license    GPL-2.0+
 */
!function(t){t(document).ready((function(t){t("input[data-input-type]").on("input change",(function(){var e=t(this).val();t(this).prev(".osixthreeo-range-value").html(e),t(this).val(e)})),t(".osixthreeo-reset-slider").on("click",(function(){var e,n;n=(e=t(this).closest("label").find("input")).data("reset_value"),e.val(n),e.change()}))}))}(jQuery);