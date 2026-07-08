<?php

/**
 * @package coolrestx
 */
if (!function_exists('coolrestx_setup')) :

    function coolrestx_setup() {
        add_theme_support('automatic-feed-links');
        add_theme_support('woocommerce');
        add_theme_support('post-thumbnails');
        add_theme_support('custom-header');
        add_theme_support('title-tag');
        register_nav_menus(array(
            'primary' => esc_html__('Primary Menu', 'coolrestx'),
            'footer'  => esc_html__('Footer Menu', 'coolrestx'),
        ));
        add_theme_support('custom-background', array(
            'default-color' => 'ffffff'
        ));

        $defaults = array(
            'default-image'      => get_template_directory_uri() . '/frontend/images/slider1.jpg',
            'default-text-color' => '05305a',
            'width'              => 1400,
            'height'             => 500,
            'uploads'            => true,
            'wp-head-callback'   => 'coolrestx_header_style',
        );
        add_theme_support('custom-header', $defaults);

        /**
         * Add post-formats support.
         */
        add_theme_support(
                'post-formats',
                array(
                    'link',
                    'aside',
                    'gallery',
                    'image',
                    'quote',
                    'status',
                    'video',
                    'audio',
                    'chat',
                )
        );

        /*
         * Switch default core markup for search form, comment form, and comments
         * to output valid HTML5.
         */
        add_theme_support(
                'html5',
                array(
                    'comment-form',
                    'comment-list',
                    'gallery',
                    'caption',
                    'style',
                    'script',
                    'navigation-widgets',
                )
        );

        // Add theme support for selective refresh for widgets.
        add_theme_support('customize-selective-refresh-widgets');

        // Add support for Block Styles.
        add_theme_support('wp-block-styles');

        // Add support for full and wide align images.
        add_theme_support('align-wide');

        // Add support for responsive embedded content.
        add_theme_support('responsive-embeds');

        // Add support for custom line height controls.
        add_theme_support('custom-line-height');

        // Add support for experimental link color control.
        add_theme_support('experimental-link-color');

        // Add support for experimental cover block spacing.
        add_theme_support('custom-spacing');

        // Add support for custom units.
        // This was removed in WordPress 5.6 but is still required to properly support WP 5.5.
        add_theme_support('custom-units');

        add_theme_support('jetpack-content-options', array(
            'blog-display'       => 'content', // the default setting of the theme: 'content', 'excerpt' or array( 'content', 'excerpt' ) for themes mixing both display.
            'author-bio'         => true, // display or not the author bio: true or false.
            'author-bio-default' => false, // the default setting of the author bio, if it's being displayed or not: true or false (only required if false).
            'masonry'            => '.site-main', // a CSS selector matching the elements that triggers a masonry refresh if the theme is using a masonry layout.
            'post-details'       => array(
                'stylesheet' => 'themeslug-style', // name of the theme's stylesheet.
                'date'       => '.posted-on', // a CSS selector matching the elements that display the post date.
                'categories' => '.cat-links', // a CSS selector matching the elements that display the post categories.
                'tags'       => '.tags-links', // a CSS selector matching the elements that display the post tags.
                'author'     => '.byline', // a CSS selector matching the elements that display the post author.
                'comment'    => '.comments-link', // a CSS selector matching the elements that display the comment link.
            ),
            'featured-images'    => array(
                'archive'         => true, // enable or not the featured image check for archive pages: true or false.
                'archive-default' => false, // the default setting of the featured image on archive pages, if it's being displayed or not: true or false (only required if false).
                'post'            => true, // enable or not the featured image check for single posts: true or false.
                'post-default'    => false, // the default setting of the featured image on single posts, if it's being displayed or not: true or false (only required if false).
                'page'            => true, // enable or not the featured image check for single pages: true or false.
                'page-default'    => false, // the default setting of the featured image on single pages, if it's being displayed or not: true or false (only required if false).
            ),
        ));


        if (!isset($content_width))
            $content_width = 900;
    }

endif; // coolrestx_setup
add_action('after_setup_theme', 'coolrestx_setup');
?>
<?php

function coolrestx_header_style() {
    $coolrestx_header_text_color = get_header_textcolor();
    if (get_theme_support('custom-header', 'default-text-color') === $coolrestx_header_text_color) {
        return;
    }
    echo '<style id="coolrestx-custom-header-styles" type="text/css">';
    if ('blank' !== $coolrestx_header_text_color) {
        echo '.logotxt, .logotxt a
			 {
				color: #' . esc_attr($coolrestx_header_text_color) . '
			}';
    }
    echo '</style>';
}
