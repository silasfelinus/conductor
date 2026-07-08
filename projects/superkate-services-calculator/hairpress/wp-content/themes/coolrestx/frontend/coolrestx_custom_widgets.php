<?php

/**
 * @package coolrestx
 */
function coolrestx_widgets_init() {

    register_sidebar(array(
        'name'          => esc_html__('Sidebar', 'coolrestx'),
        'description'   => esc_html__('Appears on sidebar', 'coolrestx'),
        'id'            => 'sidebar-1',
        'before_widget' => '<aside id="%1$s" class="widget %2$s">',
        'after_widget'  => "</aside>",
        'before_title'  => '<h3 class="widget-title">',
        'after_title'   => '</h3>',
    ));
    register_sidebar(array(
        'name'          => esc_html__('Footer 1', 'coolrestx'),
        'description'   => esc_html__('Appears on footer', 'coolrestx'),
        'id'            => 'footer-1',
        'before_widget' => '<aside id="%1$s" class="widget %2$s">',
        'after_widget'  => "</aside>",
        'before_title'  => '<h3 class="widget-title">',
        'after_title'   => '</h3>',
    ));
    register_sidebar(array(
        'name'          => esc_html__('Footer 2', 'coolrestx'),
        'description'   => esc_html__('Appears on footer', 'coolrestx'),
        'id'            => 'footer-2',
        'before_widget' => '<aside id="%1$s" class="widget %2$s">',
        'after_widget'  => "</aside>",
        'before_title'  => '<h3 class="widget-title">',
        'after_title'   => '</h3>',
    ));
    register_sidebar(array(
        'name'          => esc_html__('Footer 3', 'coolrestx'),
        'description'   => esc_html__('Appears on footer', 'coolrestx'),
        'id'            => 'footer-3',
        'before_widget' => '<aside id="%1$s" class="widget %2$s">',
        'after_widget'  => "</aside>",
        'before_title'  => '<h3 class="widget-title">',
        'after_title'   => '</h3>',
    ));
}

add_action('widgets_init', 'coolrestx_widgets_init');