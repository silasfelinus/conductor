<?php

/**
 * @package coolrestx
 */
function coolrestx_style_js() {
    wp_enqueue_style('bootstrap', get_template_directory_uri() . '/frontend/bootstrap/css/bootstrap.css');
    wp_enqueue_style('font-awesome', get_template_directory_uri() . '/css/font-awesome.css');
    wp_enqueue_style('coolrestx-basic-style', get_stylesheet_uri());
    wp_enqueue_script('bootstrap', get_template_directory_uri() . '/frontend/bootstrap/js/bootstrap.js', array('jquery'));
    wp_enqueue_script('coolrestx-toggle-jquery', get_template_directory_uri() . '/frontend/js/coolrestx-toggle.js', array('jquery'));
}

add_action('wp_enqueue_scripts', 'coolrestx_style_js');
