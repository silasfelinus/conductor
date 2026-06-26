<?php
/**
 * Humboldt Scoop Solutions – functions.php
 */

// ── Enqueue styles & scripts ─────────────────────────────────────────────────

function hss_enqueue_assets() {
    wp_enqueue_style(
        'hss-styles',
        get_template_directory_uri() . '/assets/hss.css',
        [],
        '1.0'
    );
}
add_action( 'wp_enqueue_scripts', 'hss_enqueue_assets' );


// ── Theme setup ───────────────────────────────────────────────────────────────

function hss_theme_setup() {
    // Let WordPress manage the document title
    add_theme_support( 'title-tag' );

    // Featured images
    add_theme_support( 'post-thumbnails' );

    // Register nav menu
    register_nav_menus([
        'primary' => __( 'Primary Navigation', 'hss' ),
    ]);

    // Wide/full-width block alignment support
    add_theme_support( 'align-wide' );

    // Editor stylesheet so block styles preview correctly
    add_editor_style( 'assets/hss.css' );
}
add_action( 'after_setup_theme', 'hss_theme_setup' );


// ── Remove Gutenberg block styles we don't need ───────────────────────────────

function hss_dequeue_block_styles() {
    wp_dequeue_style( 'wp-block-library' );
    wp_dequeue_style( 'wp-block-library-theme' );
    wp_dequeue_style( 'global-styles' );
}
add_action( 'wp_enqueue_scripts', 'hss_dequeue_block_styles', 100 );
