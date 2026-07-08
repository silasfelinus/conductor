<?php
/* 	COLORFUL Theme's Functions
	Copyright: 2012-2017, D5 Creation, www.d5creation.com
	
	Since COLORFUL 1.0
*/
   
 // Tell WordPress for wp_title in order to modify document title content
	function colorful_filter_wp_title( $title ) {
    $site_name = get_bloginfo( 'name' );
    $filtered_title = $site_name . $title;
    return $filtered_title;
	}
	add_filter( 'wp_title', 'colorful_filter_wp_title' );
	

	function colorful_setup() {
//	Theme TextDomain for the Language File
	load_theme_textdomain( 'd5-colorful', get_template_directory() . '/languages' );

// 	Theme Menus
	register_nav_menus( array( 'main-menu' => 'Main Menu' ) );
	add_theme_support( 'automatic-feed-links' );
	add_theme_support( "title-tag" );
	add_theme_support('html5', array('search-form', 'comment-form', 'comment-list', 'gallery', 'caption', 'script', 'style', ));

//	Set the content width based on the theme's design and stylesheet.
	global $content_width;
	if ( ! isset( $content_width ) ) $content_width = 584;

		
// 	WordPress Custom Background Support	
	$colorful_custom_background = array(
	'default-color'          => 'CB4560',
	'default-image'          => get_template_directory_uri() . '/images/back.jpg',
	'default-repeat'         => 'repeat-y',
	'default-position-x'     => 'center',
    'default-position-y'     => 'top',
    'default-size'           => '100% auto',
	);
	add_theme_support( 'custom-background', $colorful_custom_background );		
		

// 	This theme uses Featured Images (also known as post thumbnails) for per-post/per-page Custom Header images
	if ( function_exists( 'add_theme_support' ) ) { 
	add_theme_support( 'post-thumbnails' );
	set_post_thumbnail_size( 150, 150, true ); // default Post Thumbnail dimensions (cropped)

	// additional image sizes
	// delete the next line if you do not need additional image sizes
	add_image_size( 'category-thumb', 300, 9999 ); //300 pixels wide (and unlimited height)
	}
	
	add_editor_style(); }
	
	add_action( 'after_setup_theme', 'colorful_setup' );
		
// 	Functions for adding script
	function colorful_enqueue_scripts() {
	wp_enqueue_style('colorful-style', get_stylesheet_uri(), false );
	if ( is_singular() && comments_open() && get_option( 'thread_comments' ) ) { 
		wp_enqueue_script( 'comment-reply' ); 
	}
	
	wp_enqueue_script( 'colorful-menu-style', get_template_directory_uri(). '/js/menu.js', array( 'jquery' ) );
	wp_enqueue_style('colorful-gfonts', '//fonts.googleapis.com/css?family=Creepster', false );
		
	wp_enqueue_script( 'd5-colorful-html5', get_template_directory_uri().'/js/html5.js');
    wp_script_add_data( 'd5-colorful-html5', 'conditional', 'lt IE 9' );	
	
	}
	add_action( 'wp_enqueue_scripts', 'colorful_enqueue_scripts' );

//Multi-level pages menu  
	function d5_colorful_page_menu() {
		echo '<div id="mainmenuparent" class="mainmenu-parent"><ul id="main-menu-items-con" class="main-menu-items">'; wp_list_pages(array('sort_column'  => 'menu_order, post_title', 'title_li'  => '' )); echo '</ul></div>';
	}

//	Get our wp_nav_menu() fallback, wp_page_menu(), to show a home link
	function colorful_page_menu_args( $args ) {
	$args['show_home'] = true;
	return $args;
	}
	add_filter( 'wp_page_menu_args', 'colorful_page_menu_args' );


//	Registers the Widgets and Sidebars for the site
	function colorful_widgets_init() {

	register_sidebar( array(
		'name' =>  esc_html__('Primary Sidebar','d5-colorful'), 
		'id' => 'sidebar-1',
		'before_widget' => '<aside id="%1$s" class="widget %2$s">',
		'after_widget' => "</aside>",
		'before_title' => '<h3 class="widget-title">',
		'after_title' => '</h3>',
	) );

	register_sidebar( array(
		'name' =>  esc_html__('Secondary Sidebar', 'd5-colorful'),
		'id' => 'sidebar-2',
		'before_widget' => '<aside id="%1$s" class="widget %2$s">',
		'after_widget' => "</aside>",
		'before_title' => '<h3 class="widget-title">',
		'after_title' => '</h3>',
	) );

	register_sidebar( array(
		'name' =>  esc_html__('Footer Area', 'd5-colorful'),
		'id' => 'sidebar-3',
		'before_widget' => '<aside id="%1$s" class="widget %2$s">',
		'after_widget' => "</aside>",
		'before_title' => '<h3 class="widget-title">',
		'after_title' => '</h3>',
	) );

}
	add_action( 'widgets_init', 'colorful_widgets_init' );


// 	When the post has no post title, but is required to link to the single-page post view.

	add_filter('the_title', 'colorful_title');
	function colorful_title($title) {
        if ( '' == $title ) {
            return esc_html__('(Untitled)', 'd5-colorful');
        } else {
            return $title;
        }
    }