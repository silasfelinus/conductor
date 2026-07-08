<?php

add_action('customize_register', 'coolrestx_customize_register_custom_controls', 9);

function coolrestx_customize_register_custom_controls($wp_customize) {
    get_template_part('backend/proupgrade/coolrestx', 'sectionpro');
}

function coolrestx_customize_controls_js() {
    $theme = wp_get_theme();
    wp_enqueue_script('coolrestx-customizer-section-pro-jquery', get_template_directory_uri() . '/backend/proupgrade/coolrestx_customize-controls.js', array('customize-controls'), $theme->get('Version'), true);
    wp_enqueue_style('coolrestx-customizer-section-pro', get_template_directory_uri() . '/backend/proupgrade/coolrestx_customize-controls.css', $theme->get('Version'));
}

add_action('customize_controls_enqueue_scripts', 'coolrestx_customize_controls_js');

function coolrestx_enqueue_comments_reply() {
    if (get_option('thread_comments')) {
        wp_enqueue_script('comment-reply');
    }
}

add_action('comment_form_before', 'coolrestx_enqueue_comments_reply');

if (!function_exists('coolrestx_sanitize_page')) :

    function coolrestx_sanitize_page($page_id, $setting) {
        // Ensure $input is an absolute integer.
        $page_id = absint($page_id);
        // If $page_id is an ID of a published page, return it; otherwise, return the default.
        return ( 'publish' === get_post_status($page_id) ? $page_id : $setting->default );
    }

endif;

function coolrestx_customize_register($wp_customize) {

    // Register custom section types.
    $wp_customize->register_section_type('coolrestx_Customize_Section_Pro');

    // Register sections.
    $wp_customize->add_section(new coolrestx_Customize_Section_Pro(
                    $wp_customize,
                    'theme_go_pro',
                    array(
                'priority' => 1,
                'title'    => esc_html__('coolrestx', 'coolrestx'),
                'pro_text' => esc_html__('Upgrade To Pro', 'coolrestx'),
                'pro_url'  => 'https://themestulip.com/themes/spa-wordpress-theme/',
                    )
    ));
    $wp_customize->add_section('coolrestx_header', array(
        'title'       => esc_html__('coolrestx Header Phone and Address', 'coolrestx'),
        'description' => '',
        'priority'    => 30,
    ));
    $wp_customize->add_section('coolrestx_social', array(
        'title'       => esc_html__('coolrestx Social Link', 'coolrestx'),
        'description' => '',
        'priority'    => 35,
    ));


    //  =============================
    //  = Text Input phone number                =
    //  =============================
    $wp_customize->add_setting('coolrestx_phone', array(
        'default'           => '',
        'sanitize_callback' => 'coolrestx_sanitize_phone_number'
    ));

    $wp_customize->add_control('coolrestx_phone', array(
        'label'   => esc_html__('Phone Number', 'coolrestx'),
        'section' => 'coolrestx_header',
        'setting' => 'coolrestx_phone',
        'type'    => 'text'
    ));

    //  =============================
    //  = Text Input Email                =
    //  =============================
    $wp_customize->add_setting('coolrestx_address', array(
        'default'           => '',
        'sanitize_callback' => 'sanitize_textarea_field'
    ));

    $wp_customize->add_control('coolrestx_address', array(
        'label'   => esc_html__('Full Address', 'coolrestx'),
        'section' => 'coolrestx_header',
        'setting' => 'coolrestx_address',
        'type'    => 'textarea'
    ));

    //  =============================
    //  = Text Input facebook                =
    //  =============================
    $wp_customize->add_setting('coolrestx_fb', array(
        'default'           => '',
        'sanitize_callback' => 'esc_url_raw'
    ));

    $wp_customize->add_control('coolrestx_fb', array(
        'label'   => esc_html__('Facebook', 'coolrestx'),
        'section' => 'coolrestx_social',
        'setting' => 'coolrestx_fb',
    ));
    //  =============================
    //  = Text Input Twitter                =
    //  =============================
    $wp_customize->add_setting('coolrestx_twitter', array(
        'default'           => '',
        'sanitize_callback' => 'esc_url_raw'
    ));

    $wp_customize->add_control('coolrestx_twitter', array(
        'label'   => esc_html__('Twitter', 'coolrestx'),
        'section' => 'coolrestx_social',
        'setting' => 'coolrestx_twitter',
    ));
    //  =============================
    //  = Text Input googleplus                =
    //  =============================
    $wp_customize->add_setting('coolrestx_glplus', array(
        'default'           => '',
        'sanitize_callback' => 'esc_url_raw'
    ));

    $wp_customize->add_control('coolrestx_glplus', array(
        'label'   => esc_html__('Google Plus', 'coolrestx'),
        'section' => 'coolrestx_social',
        'setting' => 'coolrestx_glplus',
    ));
    //  =============================
    //  = Text Input linkedin                =
    //  =============================
    $wp_customize->add_setting('coolrestx_in', array(
        'default'           => '',
        'sanitize_callback' => 'esc_url_raw'
    ));

    $wp_customize->add_control('coolrestx_in', array(
        'label'   => esc_html__('Linkedin', 'coolrestx'),
        'section' => 'coolrestx_social',
        'setting' => 'coolrestx_in',
    ));

    //  =============================
    //  = slider section              =
    //  =============================
    $wp_customize->add_section('business_multi_lite_banner', array(
        'title'       => esc_html__('coolrestx Home Banner Text', 'coolrestx'),
        'description' => esc_html__('add home banner text here.', 'coolrestx'),
        'priority'    => 36,
    ));

// Banner heading Text
    $wp_customize->add_setting('banner_heading', array(
        'default'           => null,
        'sanitize_callback' => 'sanitize_text_field'
    ));

    $wp_customize->add_control('banner_heading', array(
        'type'    => 'text',
        'label'   => esc_html__('Add Banner heading here', 'coolrestx'),
        'section' => 'business_multi_lite_banner',
        'setting' => 'banner_heading'
    )); // Banner heading Text
    // Banner heading Text
    $wp_customize->add_setting('banner_sub_heading', array(
        'default'           => null,
        'sanitize_callback' => 'sanitize_text_field'
    ));

    $wp_customize->add_control('banner_sub_heading', array(
        'type'    => 'text',
        'label'   => esc_html__('Add Banner sub heading here', 'coolrestx'),
        'section' => 'business_multi_lite_banner',
        'setting' => 'banner_sub_heading'
    )); // Banner heading Text
    //  =============================
    //  = Footer              =
    //  =============================

    $wp_customize->add_section('coolrestx_footer', array(
        'title'       => esc_html__('coolrestx Footer', 'coolrestx'),
        'description' => '',
        'priority'    => 37,
    ));

    // Footer design and developed
    $wp_customize->add_setting('coolrestx_design', array(
        'default'           => '',
        'sanitize_callback' => 'sanitize_textarea_field'
    ));

    $wp_customize->add_control('coolrestx_design', array(
        'label'   => esc_html__('Design and developed', 'coolrestx'),
        'section' => 'coolrestx_footer',
        'setting' => 'coolrestx_design',
        'type'    => 'textarea'
    ));
    // Footer copyright
    $wp_customize->add_setting('coolrestx_copyright', array(
        'default'           => '',
        'sanitize_callback' => 'sanitize_textarea_field'
    ));

    $wp_customize->add_control('coolrestx_copyright', array(
        'label'   => esc_html__('Copyright', 'coolrestx'),
        'section' => 'coolrestx_footer',
        'setting' => 'coolrestx_copyright',
        'type'    => 'textarea'
    ));
}

add_action('customize_register', 'coolrestx_customize_register');
