<?php
/**
 * CF7SA_Front_Filter Class
 *
 * Handles the Frontend Filters.
 *
 * @package WordPress
 * @subpackage Contact Form 7 - Stripe Add-on
 * @since 1.0
 */

// Exit if accessed directly
if ( !defined( 'ABSPATH' ) ) exit;

if ( !class_exists( 'CF7SA_Front_Filter' ) ) {

	/**
	 *  The CF7SA_Front_Filter Class
	 */
	class CF7SA_Front_Filter {

		function __construct() {

			/**
			 * Wrap form
			 */
			add_filter( 'wpcf7_form_class_attr', array( $this, 'filter__wpcf7_form_class_attr' ), 10 );

			add_filter('wpcf7_form_tag', array( $this,'cf7sa_so48515097_cf7_select_radio_values'), 10);

			add_filter('wpcf7_form_tag', array( $this,'cf7sa_so48515097_cf7_select_radio_button_values'), 10);

		}

		/*
		######## #### ##       ######## ######## ########   ######
		##        ##  ##          ##    ##       ##     ## ##    ##
		##        ##  ##          ##    ##       ##     ## ##
		######    ##  ##          ##    ######   ########   ######
		##        ##  ##          ##    ##       ##   ##         ##
		##        ##  ##          ##    ##       ##    ##  ##    ##
		##       #### ########    ##    ######## ##     ##  ######
		*/

		function cf7sa_so48515097_cf7_select_radio_button_values($tag)
		{
			if ($tag['basetype'] != 'radio') {
				return $tag;
			}

			$values = [];
			$labels = [];
			foreach ($tag['raw_values'] as $raw_value) {
				$raw_value_parts = explode('|', $raw_value);
				if (count($raw_value_parts) >= 2) {
					$values[] = $raw_value_parts[1];
					$labels[] = $raw_value_parts[0];
				} else {
					$values[] = $raw_value;
					$labels[] = $raw_value;
				}
			}
			$tag['values'] = $values;
			$tag['labels'] = $labels;

			// Optional but recommended:
			// Display labels in mails instead of values.
			// Use [_raw_tag] instead of [tag] for values.
			$reversed_raw_values = array_map(function ($raw_value) {
				$raw_value_parts = explode('|', $raw_value);
				return implode('|', array_reverse($raw_value_parts));
			}, $tag['raw_values']);
			$tag['pipes'] = new \WPCF7_Pipes($reversed_raw_values);

			return $tag;
		}

		function cf7sa_so48515097_cf7_select_radio_values($tag)
		{
			if ($tag['basetype'] != 'select' ) {
				return $tag;
			}

			$values = [];
			$labels = [];
			foreach ($tag['raw_values'] as $raw_value) {
				$raw_value_parts = explode('|', $raw_value);
				if (count($raw_value_parts) >= 2) {
					$values[] = $raw_value_parts[1];
					$labels[] = $raw_value_parts[0];
				} else {
					$values[] = $raw_value;
					$labels[] = $raw_value;
				}
			}
			$tag['values'] = $values;
			$tag['labels'] = $labels;

			// Optional but recommended:
			// Display labels in mails instead of values.
			// Use [_raw_tag] instead of [tag] for values.
			$reversed_raw_values = array_map(function ($raw_value) {
				$raw_value_parts = explode('|', $raw_value);
				return implode('|', array_reverse($raw_value_parts));
			}, $tag['raw_values']);
			$tag['pipes'] = new \WPCF7_Pipes($reversed_raw_values);

			return $tag;
		}


		function filter__wpcf7_form_class_attr( $classes ) {

			$form =  WPCF7_ContactForm::get_current();
			$form_id = $form->id();

			if ( !empty( $form_id )
				&& !empty( get_post_meta( $form_id, CF7SA_META_PREFIX . 'use_stripe', true ) )
			) {
				return $classes . ' cf7sa';
			}

			return $classes;
		}

		/*
		######## ##     ## ##    ##  ######  ######## ####  #######  ##    ##  ######
		##       ##     ## ###   ## ##    ##    ##     ##  ##     ## ###   ## ##    ##
		##       ##     ## ####  ## ##          ##     ##  ##     ## ####  ## ##
		######   ##     ## ## ## ## ##          ##     ##  ##     ## ## ## ##  ######
		##       ##     ## ##  #### ##          ##     ##  ##     ## ##  ####       ##
		##       ##     ## ##   ### ##    ##    ##     ##  ##     ## ##   ### ##    ##
		##        #######  ##    ##  ######     ##    ####  #######  ##    ##  ######
		*/

	}
}
