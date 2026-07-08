<?php
/**
 * Theme Functions
 *
 * @package    osixthreeo
 * @subpackage osixthreeo/inc
 * @author     Chip Sheppard
 * @since      1.0.0
 * @license    GPL-2.0+
 */

if ( ! defined( 'ABSPATH' ) ) {
	exit;
}


/*
 * HEADER
 * -----------------------------------------------------------------
 */
if ( ! function_exists( 'osixthreeo_display_header' ) ) {
	/**
	 * Get the branding markup
	 */
	function osixthreeo_display_header() {
		echo '<header id="masthead" class="site-header">';
		osixthreeo_header_before_wrap();
		echo '<div class="header-wrap">';
		echo '<div class="inner-wrap">';
			osixthreeo_header_top();
			osixthreeo_header_bottom();
		echo '</div>';
		echo '</div>';
		osixthreeo_header_after_wrap();
		echo '</header>';
	}
}
add_action( 'osixthreeo_header_before', 'osixthreeo_display_header' );


/*
 * HEADER Branding
 * -----------------------------------------------------------------
 */
if ( ! function_exists( 'osixthreeo_display_branding' ) ) {
	/**
	 * Get the branding markup
	 */
	function osixthreeo_display_branding() {
		echo '<div class="site-branding">';

		$custom_logo_id = get_theme_mod( 'custom_logo' );
		$logo           = wp_get_attachment_image_src( $custom_logo_id, 'full' );
		$sitename       = get_bloginfo( 'name', 'display' );
		$logoheight     = absint( $logo[2] );
		$logowidth      = absint( $logo[1] );
		$description    = get_bloginfo( 'description', 'display' );

		if ( has_custom_logo() ) {
			echo '<div class="custom-logo">';
			echo '<a href="' . esc_url( home_url( '/' ) ) . '" rel="home"><img src="' . esc_url( $logo[0] ) . '" height="' . esc_attr( $logoheight ) . '" width="' . esc_attr( $logowidth ) . '" alt="' . esc_attr( $sitename ) . '"></a>';
			echo '</div>';
		} else {
			if ( is_front_page() && is_home() ) :
				echo '<h1 class="site-title">' . esc_html( $sitename ) . '</h1>';
			else :
				echo '<div class="site-title"><a href="' . esc_url( home_url( '/' ) ) . '" rel="home">' . esc_html( $sitename ) . '</a></div>';
			endif;
		}

		if ( $description || is_customize_preview() ) :
			echo '<div class="site-description">' . wp_kses_post( $description ) . '</div>';
		endif;
		echo '</div>';
	}
}
add_action( 'osixthreeo_header_top', 'osixthreeo_display_branding' );


/*
 * HEADER Navigation
 * -----------------------------------------------------------------
 */
if ( ! function_exists( 'osixthreeo_display_nav' ) ) {
	/**
	 * Get the menu
	 * write the markup if conditions are met.
	 */
	function osixthreeo_display_nav() {

		if ( ! has_nav_menu( 'primary' ) ) {
			return;
		}

		echo '<nav id="primary-navigation" class="site-navigation" role="navigation">';
			echo '<button class="responsive-menu-icon" aria-label="mobile-menu-icon" aria-controls="primary-menu" aria-expanded="false"><span class="menu-icon-wrap"><span class="menu-icon"></span></span></button>';

			echo '<div class="menu-wrap"><div class="menu-span">';

				do_action( 'osixthreeo_inside_navigation' );

				wp_nav_menu(
					array(
						'theme_location' => 'primary',
						'menu_id'        => 'primary-menu',
						'container'      => '',
					)
				);

			echo '</div></div>';
		echo '</nav>';
	}
}
add_action( 'osixthreeo_header_bottom', 'osixthreeo_display_nav' );


/*
 * The Content
 * -----------------------------------------------------------------
 */
if ( ! function_exists( 'osixthreeo_display_content' ) ) {
	/**
	 * The Content & pagination on pages /  The Excerpt on archives.
	 */
	function osixthreeo_display_content() {

		if ( is_singular() ) :
			// Single posts, attachments, pages, custom post types.
			the_content();

			wp_link_pages(
				array(
					'before' => '<div class="page-links">' . esc_html__( 'Pages:', 'osixthreeo' ),
					'after'  => '</div>',
				)
			);

		else :

			$osixthreeo_settings = wp_parse_args(
				get_option( 'osixthreeo_settings', array() ),
				osixthreeo_get_defaults()
			);
			$hide_ex             = $osixthreeo_settings['archives_hide_excerpt'];

			// Archives & search.
			if ( true === $hide_ex ) {
				return;
			}

			the_excerpt();

		endif;
	}
}
add_action( 'osixthreeo_entry_content_before', 'osixthreeo_display_content' );


/*
 * Comments
 * -----------------------------------------------------------------
 */
if ( ! function_exists( 'osixthreeo_comments' ) ) {
	/**
	 * WP Comments
	 */
	function osixthreeo_comments() {

		if ( is_singular() && ( comments_open() || get_comments_number() ) ) {
			comments_template();
		}
	}
}
add_action( 'osixthreeo_content_while_after', 'osixthreeo_comments' );


/*
 * POST Footer Meta
 * -----------------------------------------------------------------
 */
if ( ! function_exists( 'osixthreeo_display_entry_footer' ) ) {
	/**
	 * Get the categories and tags.
	 */
	function osixthreeo_display_entry_footer() {

		$osixthreeo_settings = wp_parse_args(
			get_option( 'osixthreeo_settings', array() ),
			osixthreeo_get_defaults()
		);
		$meta_footer         = $osixthreeo_settings['meta_footer'];

		if ( true === $meta_footer && is_single() && 'post' === get_post_type() ) :
			echo '<footer class="entry-footer">';

			// Hide this on pages.
			if ( 'post' === get_post_type() ) {
				/* translators: used between list items, there is a space after the comma */
				$categories_list = get_the_category_list( esc_html__( ', ', 'osixthreeo' ) );
				if ( $categories_list ) {
					printf( '<span class="cat-links"><div class="cssicon-folder"></div>%1$s</span>', wp_kses_post( $categories_list ) );
				}

				/* translators: used between list items, there is a space after the comma */
				$tags_list = get_the_tag_list( '', esc_html__( ', ', 'osixthreeo' ) );
				if ( $tags_list ) {
					printf( '<span class="tags-links"><div class="cssicon-tag"></div>%1$s</span>', wp_kses_post( $tags_list ) );
				}
			}

			edit_post_link(
				sprintf(
					wp_kses(
						/* translators: %s: Name of current post. Only visible to screen readers */
						__( 'Edit <span class="screen-reader-text">%s</span>', 'osixthreeo' ),
						array(
							'span' => array(
								'class' => array(),
							),
						)
					),
					get_the_title()
				),
				'<span class="edit-link">',
				'</span>'
			);
			echo '</footer>';
		endif;
	}
}
add_action( 'osixthreeo_entry_bottom', 'osixthreeo_display_entry_footer' );


/*
 * POST Navigation (prev - next)
 * -----------------------------------------------------------------
 */
if ( ! function_exists( 'osixthreeo_postnav' ) ) {
	/**
	 * Post Navigation
	 */
	function osixthreeo_postnav() {

		$osixthreeo_settings = wp_parse_args(
			get_option( 'osixthreeo_settings', array() ),
			osixthreeo_get_defaults()
		);
		$post_nav            = $osixthreeo_settings['post_nav'];

		if ( true === $post_nav && is_single() ) :
			the_post_navigation(
				array(
					'prev_text' => __( '<span>previous</span> %title', 'osixthreeo' ),
					'next_text' => __( '<span>next</span> %title', 'osixthreeo' ),
				)
			);
		endif;
	}
}
add_action( 'osixthreeo_entry_after', 'osixthreeo_postnav' );


/*
 * ARCHIVE Page Titles
 * -----------------------------------------------------------------
 */
if ( ! function_exists( 'osixthreeo_archive_page_title' ) ) {
	/**
	 * Archive Page Titles
	 */
	function osixthreeo_archive_page_titles() {
		if ( is_home() && ! is_front_page() || is_archive() || is_search() ) :
			echo '<header class="page-header">';
			echo '<div class="title-wrap">';

			if ( is_search() ) :
				echo '<h1 class="page-title">';
				/* translators: %$2s: is the search term */
				printf( '<span>' . esc_html__( 'Search Results for:%1$s %2$s', 'osixthreeo' ), '</span>', get_search_query() );
				echo '</h1>';
			else :
				the_archive_title( '<h1 class="page-title">', '</h1>' );
				the_archive_description( '<div class="archive-description">', '</div>' );
			endif;

			echo '</div>';
			echo '</header>';
		endif;
	}
}
add_action( 'osixthreeo_content_while_before', 'osixthreeo_archive_page_titles' );


/*
 * ARCHIVE Pagination (<< 1 of 10 >>)
 * -----------------------------------------------------------------
 */
if ( ! function_exists( 'osixthreeo_postpagination' ) ) {
	/**
	 * Do Post Pagination on Post archive pages only.
	 */
	function osixthreeo_postpagination() {

		if ( is_archive() || is_home() ) :
			the_posts_pagination(
				array(
					'mid_size'  => 2,
					'prev_text' => __( '&laquo; Previous', 'osixthreeo' ),
					'next_text' => __( 'Next &raquo;', 'osixthreeo' ),
				)
			);
		endif;
	}
}
add_action( 'osixthreeo_content_while_after', 'osixthreeo_postpagination' );


/*
 * ARCHIVE Read More link
 * -----------------------------------------------------------------
 */
if ( ! function_exists( 'osixthreeo_display_read_more' ) ) {
	/**
	 * The Read More link markup
	 */
	function osixthreeo_display_read_more() {
		$osixthreeo_settings = wp_parse_args(
			get_option( 'osixthreeo_settings', array() ),
			osixthreeo_get_defaults()
		);
		$hide_rm             = $osixthreeo_settings['archives_hide_readmore'];

		if ( true === $hide_rm ) {
			return;
		}

		if ( is_archive() || is_home() || is_search() ) :
			$link = sprintf(
				'<footer class="link-more"><a href="%1$s" class="more-link">%2$s</a></footer>',
				get_permalink( get_the_ID() ),
				sprintf(
					/* translators: %s: Name of current post */
					__( 'Continue<span class="screen-reader-text"> "%s"</span>', 'osixthreeo' ),
					get_the_title( get_the_ID() )
				)
			);
			echo wp_kses_post( $link );
			echo '<div class="cf"></div>';
		endif;
	}
}
add_action( 'osixthreeo_entry_bottom', 'osixthreeo_display_read_more' );


/*
 * FOOTER
 * -----------------------------------------------------------------
 */
if ( ! function_exists( 'osixthreeo_display_site_footer' ) ) {
	/**
	 * The Site Footer Markup
	 */
	function osixthreeo_display_site_footer() {
		echo '<footer id="colophon" class="site-footer" role="contentinfo">';
		echo '<div class="inner-wrap">';

		osixthreeo_footer_top();

		if ( is_active_sidebar( 'footer' ) ) {
			echo '<div class="site-info">';
			dynamic_sidebar( 'footer' );
			do_action( 'osixthreeo_inside_footer' );
			echo '</div>';
		} else {
			echo '<div class="site-info">';
			?>
			<p><a href="<?php echo esc_url( __( 'https://osixthreeo.com/', 'osixthreeo' ) ); ?>">
				<?php
				/* translators: %s: theme name. */
				printf( esc_html__( 'Powered by %s', 'osixthreeo' ), 'OsixthreeO' );
				?>
			</a></p>
			<?php
			do_action( 'osixthreeo_inside_footer' );
			echo '</div>';
		}

		osixthreeo_footer_bottom();

		echo '</div>';
		echo '</footer>';

	}
}
add_action( 'osixthreeo_footer_before', 'osixthreeo_display_site_footer' );
