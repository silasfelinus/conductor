/**
 * Customizer JS
 *
 * @package    osixthreeo
 * @subpackage osixthreeo/assets/js
 * @since      1.0.0
 * @license    GPL-2.0+
 */

/*
* Live Update
*/
function osixthreeo_colors_live_update( id, selector, property, default_value ) {
	default_value = typeof default_value !== 'undefined' ? default_value : 'initial';

	wp.customize( 'osixthreeo_settings[' + id + ']', function( value ) {
		value.bind( function( newval ) {
			newval = ( '' !== newval ) ? newval : default_value;

			if ( jQuery( 'style#' + id ).length ) {
				jQuery( 'style#' + id ).html( selector + '{' + property + ':' + newval + ';}' );
			} else {
				jQuery( 'head' ).append( '<style id="' + id + '">' + selector + '{' + property + ':' + newval + '}</style>' );
				setTimeout(function() {
					jQuery( 'style#' + id ).not( ':last' ).remove();
				}, 1000);
			}
		} );
	} );
}

/*
* Live Update elements
*/
( function( $ ) {

	// Site title and description.
	wp.customize( 'blogname', function( value ) {
		value.bind( function( to ) {
			$( '.site-title a' ).text( to );
		} );
	} );
	wp.customize( 'blogdescription', function( value ) {
		value.bind( function( to ) {
			$( '.site-description' ).text( to );
		} );
	} );

	wp.customize( 'header_textcolor', function( value ) {
		value.bind( function( to ) {
			if ( 'blank' === to ) {
				$( '.site-title, .site-description' ).css( {
					'clip': 'rect(1px, 1px, 1px, 1px)',
					'position': 'absolute'
				} );
			} else {
				$( '.site-title, .site-description' ).css( {
					'clip': 'auto',
					'position': 'relative'
				} );
				$( '.site-title, .site-title a, .site-description' ).css( {
					'color': to
				} );
			}
		} );
	} );

	// Global Site Width.
	wp.customize( 'osixthreeo_settings[containment_setting]', function( value ) {
		value.bind( function( newval ) {
			if ( 'full' === newval ) {
				$( 'body' ).removeClass( 'contained' );
				$( '.site' ).removeAttr( 'style' );
			}
			if ( 'contained' === newval ) {
				$( 'body' ).addClass( 'contained' );
			}
		} );
	} );

	// Content Max Width.
	wp.customize(
		'osixthreeo_settings[max_width]', function( value ) {
			value.bind(
				function( newval ) {
					$( '.contained .site' ).css( 'max-width', newval + 'px' );
				}
			);
		}
	);

	// Header Layout.
	wp.customize( 'osixthreeo_settings[header_layout]', function( value ) {
		value.bind( function( newval ) {
			if ( 'headernormal' === newval ) {
				$( 'body' ).removeClass( 'headercentered' );
			}
			if ( 'headercentered' === newval ) {
				$( 'body' ).addClass( 'headercentered' );
			}
		} );
	} );

	// Header Top/Bottom Padding.
	wp.customize(
		'osixthreeo_settings[header_padding]', function( value ) {
			value.bind(
				function( newval ) {
					$( '.header-wrap' ).css( 'padding-top', newval + 'px' );
					$( '.header-wrap' ).css( 'padding-bottom', newval + 'px' );
				}
			);
		}
	);

	// Home Header FULL HEIGHT.
	wp.customize( 'osixthreeo_settings[home_header_fullheight]', function( value ) {
		value.bind( function( newval ) {
			if ( 'full' === newval ) {
				$( 'body' ).addClass( 'fullheight' );
			}
			if ( 'adjustable' === newval ) {
				$( 'body' ).removeClass( 'fullheight' );
			}
		} );
	} );

	// Home header height.
	wp.customize(
		'osixthreeo_settings[home_header_height]', function( value ) {
			value.bind(
				function( newval ) {
					$( '.home .site-header' ).css( 'min-height', newval + 'px' );
				}
			);
		}
	);

	// Subpage header height.
	wp.customize(
		'osixthreeo_settings[subpage_header_height]', function( value ) {
			value.bind(
				function( newval ) {
					$( '.site-header' ).css( 'min-height', newval + 'px' );
				}
			);
		}
	);

	// Custom header background image position.
	wp.customize(
		'osixthreeo_settings[header_bg_position]', function( value ) {
			value.bind(
				function( newval ) {

					var pos1 = '';
					var pos2 = '';

					if ( 'left-top' === newval ) {
						pos1 = 'left'; pos2 = 'top';
					}
					if ( 'left-center' === newval )  {
						pos1 = 'left'; pos2 = 'center';
					}
					if ( 'left-bottom' === newval )  {
						pos1 = 'left'; pos2 = 'bottom';
					}
					if ( 'right-top' === newval ) {
						pos1 = 'right'; pos2 = 'top';
					}
					if ( 'right-center' === newval )  {
						pos1 = 'right'; pos2 = 'center';
					}
					if ( 'right-bottom' === newval )  {
						pos1 = 'right'; pos2 = 'bottom';
					}
					if ( 'center-top' === newval ) {
						pos1 = 'center'; pos2 = 'top';
					}
					if ( 'center-bottom' === newval )  {
						pos1 = 'center'; pos2 = 'bottom';
					}
					$( '.custom-header .custom-header-image' ).css( 'background-position', pos1 + ' ' + pos2 );
				}
			);
		}
	);
	// Custom header background image repeat.
	wp.customize(
		'osixthreeo_settings[header_bg_repeat]', function( value ) {
			value.bind(
				function( newval ) {
					$( '.custom-header .custom-header-image' ).css( 'background-repeat', newval );
				}
			);
		}
	);
	// Custom header background image size.
	wp.customize(
		'osixthreeo_settings[header_bg_size]', function( value ) {
			value.bind(
				function( newval ) {
					$( '.custom-header .custom-header-image' ).css( 'background-size', newval );
				}
			);
		}
	);

	// HEADER COLORS ------------------------------------------------ .
	osixthreeo_colors_live_update(
		'header_background_color',
		'.header-wrap',
		'background-color',
		'transparent'
	);
	// HEADER COLORS HOMEPAGE --------------------------------------- .
	osixthreeo_colors_live_update(
		'header_background_color_home',
		'.home .header-wrap',
		'background-color',
		'transparent'
	);

	// CUSTOM HEADER TEXT COLORS ------------------------------------ .
	osixthreeo_colors_live_update(
		'hero_text_primary_color',
		'.hero-primary',
		'color',
		'#ffffff'
	);
	osixthreeo_colors_live_update(
		'hero_text_secondary_color',
		'.hero-secondary',
		'color',
		'#ffffff'
	);

	// CONTENT AREA COLORS ------------------------------------------
	osixthreeo_colors_live_update(
		'content_title_color',
		'body.page .entry-title,body.single .entry-title,body.blog .page-title,body.archive .page-title,body.search .page-title,body.error404 .page-title,.woocommerce-products-header,.product_title.entry-title,body.page.titlelift .entry-title,body.single.titlelift .entry-title,body.blog.titlelift .page-title,body.archive.titlelift .page-title,body.search.titlelift .page-title,body.error404.titlelift .page-title,.single.titlelift .entry-meta a,.single.titlelift .entry-meta,.titlelift .archive-description,.titlelift .woocommerce-products-header,.titlelift .product_title.entry-title',
		'color',
		''
	);
	osixthreeo_colors_live_update(
		'content_bgcolor',
		'.site-content',
		'background-color',
		'transparent'
	);
	osixthreeo_colors_live_update(
		'text_color',
		'body,button,input,select,textarea,.sidebar-widget ul a,.sidebar-widget .menu a,.comment-navigation .nav-previous a,.comment-navigation .nav-next a,.posts-navigation .nav-previous a,.posts-navigation .nav-next a,.post-navigation .nav-previous a,.post-navigation .nav-next a,.site-navigation .sub-menu a',
		'color',
		'#222222'
	);

	// FOOTER COLORS ------------------------------------------------
	osixthreeo_colors_live_update(
		'footer_background_color',
		'.site-footer',
		'background-color',
		'#000000'
	);
	osixthreeo_colors_live_update(
		'footer_title_color',
		'.site-info .widget-title',
		'color',
		'#ffffff'
	);
	osixthreeo_colors_live_update(
		'footer_text_color',
		'.site-info',
		'color',
		'#f5f5f5'
	);
	osixthreeo_colors_live_update(
		'footer_link_color',
		'.site-info a',
		'color',
		'#dcdcdc'
	);
	osixthreeo_colors_live_update(
		'footer_link_color_hover',
		'.site-info a:hover',
		'color',
		'#ffffff'
	);
	osixthreeo_colors_live_update(
		'meta_color',
		'.entry-meta, .entry-meta a, .entry-footer, .entry-footer a',
		'color',
		'#808080'
	);

    // FONT SIZE ----------------------------------------------------
	// base font size.
	wp.customize(
		'osixthreeo_settings[base_font_size]', function( value ) {
			value.bind(
				function( newval ) {
					$( '.content-inner-wrap' ).css( 'font-size', newval + 'px' );
				}
			);
		}
	);
	// site title
	wp.customize(
		'osixthreeo_settings[sitetitle_font_size]', function( value ) {
			value.bind(
				function( newval ) {
					$( '.site-title' ).css( 'font-size', newval + 'px' );
				}
			);
		}
	);
	// site description
	wp.customize(
		'osixthreeo_settings[sitedescription_font_size]', function( value ) {
			value.bind(
				function( newval ) {
					$( '.site-description' ).css( 'font-size', newval + 'px' );
				}
			);
		}
	);
	// menu
	wp.customize(
		'osixthreeo_settings[menu_font_size]', function( value ) {
			value.bind(
				function( newval ) {
					$( '#primary-navigation' ).css( 'font-size', newval + 'px' );
				}
			);
		}
	);
	// hero primary size
	wp.customize(
		'osixthreeo_settings[hero_text_primary_font_size]', function( value ) {
			value.bind(
				function( newval ) {
					$( '.hero-primary' ).css( 'font-size', newval + 'px' );
				}
			);
		}
	);
	// hero secondary size
	wp.customize(
		'osixthreeo_settings[hero_text_secondary_font_size]', function( value ) {
			value.bind(
				function( newval ) {
					$( '.hero-secondary' ).css( 'font-size', newval + 'px' );
				}
			);
		}
	);
	// hero primary alignment
	wp.customize(
		'osixthreeo_settings[hero_text_primary_alignment]', function( value ) {
			value.bind(
				function( newval ) {
					$( '.hero-primary' ).css( 'text-align', newval );
				}
			);
		}
	);
	// hero secondary alignment
	wp.customize(
		'osixthreeo_settings[hero_text_secondary_alignment]', function( value ) {
			value.bind(
				function( newval ) {
					$( '.hero-secondary' ).css( 'text-align', newval );
				}
			);
		}
	);
	// hero scrollbar alignment
	wp.customize(
		'osixthreeo_settings[hero_scroll_button_alignment]', function( value ) {
			value.bind(
				function( newval ) {
					$( '.hero-scroll-button' ).css( 'text-align', newval );
				}
			);
		}
	);

	// post meta
	wp.customize(
		'osixthreeo_settings[meta_font_size]', function( value ) {
			value.bind(
				function( newval ) {
					$( '.entry-meta, .entry-footer' ).css( 'font-size', newval + 'px' );
				}
			);
		}
	);

    // FONT WEIGHT -------------------------------------------------------------
	// header
	wp.customize(
		'osixthreeo_settings[header_font_weight]', function( value ) {
			value.bind( function( newval ) {
				if ( newval ) {
					$( 'h1:not(.site-title), h2, h3, h4, h5, h6' ).css( 'font-weight', newval );
				} else {
					$( 'h1:not(.site-title), h2, h3, h4, h5, h6' ).css( 'font-weight', 'normal' );
				}
			} );
		}
	);
	// site title
	wp.customize(
		'osixthreeo_settings[sitetitle_font_weight]', function( value ) {
			value.bind( function( newval ) {
				if ( newval ) {
					$( '.site-title' ).css( 'font-weight', newval );
				} else {
					$( '.site-title' ).css( 'font-weight', 'normal' );
				}
			} );
		}
	);
	// site description
	wp.customize(
		'osixthreeo_settings[sitedescription_font_weight]', function( value ) {
			value.bind( function( newval ) {
				if ( newval ) {
					$( '.site-description' ).css( 'font-weight', newval );
				} else {
					$( '.site-description' ).css( 'font-weight', 'normal' );
				}
			} );
		}
	);
	// menu
	wp.customize(
		'osixthreeo_settings[menu_font_weight]', function( value ) {
			value.bind( function( newval ) {
				if ( newval ) {
					$( '.site-navigation a' ).css( 'font-weight', newval );
				} else {
					$( '.site-navigation a' ).css( 'font-weight', 'normal' );
				}
			} );
		}
	);
	// post meta
	wp.customize(
		'osixthreeo_settings[meta_font_weight]', function( value ) {
			value.bind( function( newval ) {
				if ( newval ) {
					$( '.entry-meta, .entry-footer' ).css( 'font-weight', newval );
				} else {
					$( '.entry-meta, .entry-footer' ).css( 'font-weight', 'normal' );
				}
			} );
		}
	);

	// Archive Colors.
	osixthreeo_colors_live_update(
		'archives_background_color',
		'.blog article, .archive article, .search article',
		'background-color',
		'transparent'
	);
	osixthreeo_colors_live_update(
		'archives_text_color',
		'.blog article, .archive article, .search article',
		'color',
		''
	);
	osixthreeo_colors_live_update(
		'archives_title_color',
		'.blog article .entry-title,.archive article .entry-title,.search article .entry-title,.blog article .entry-title a,.archive article .entry-title a,.search article .entry-title a',
		'color',
		''
	);
	osixthreeo_colors_live_update(
		'archives_meta_color',
		'.blog article .entry-meta,.archive article .entry-meta,.search article .entry-meta, .blog article .entry-meta a,.archive article .entry-meta a,.search article .entry-meta a',
		'color',
		'#808080'
	);
	osixthreeo_colors_live_update(
		'archives_link_color',
		'.blog article .entry-content a,.archive article .entry-content a,.search article .entry-content a,.link-more',
		'color',
		''
	);
	osixthreeo_colors_live_update(
		'archives_link_color_hover',
		'.blog article .entry-content a:hover,.archive article .entry-content a:hover,.search article .entry-content a:hover',
		'color',
		''
	);

	// Hiding.
	wp.customize(
		'osixthreeo_settings[archives_hide_featuredimage]', function( value ) {
			value.bind( function( newval ) {
				if ( newval === true ) {
					$( '.blog article .fi-link,.archive article .fi-link,.search article .fi-link' ).css( 'display', 'none' );
				} else {
					$( '.blog article .fi-link,.archive article .fi-link,.search article .fi-link' ).css( 'display', 'block' );
				}
			} );
		}
	);
	wp.customize(
		'osixthreeo_settings[archives_hide_excerpt]', function( value ) {
			value.bind( function( newval ) {
				if ( newval === true ) {
					$( '.blog article .entry-content,.archive article .entry-content,.search article .entry-content' ).css( 'display', 'none' );
				} else {
					$( '.blog article .entry-content,.archive article .entry-content,.search article .entry-content' ).css( 'display', 'block' );
				}
			} );
		}
	);
	wp.customize(
		'osixthreeo_settings[archives_hide_readmore]', function( value ) {
			value.bind( function( newval ) {
				if ( newval === true ) {
					$( '.blog article footer,.archive article footer,.search article footer' ).css( 'display', 'none' );
				} else {
					$( '.blog article footer,.archive article footer,.search article footer' ).css( 'display', 'block' );
				}
			} );
		}
	);
	wp.customize(
		'osixthreeo_settings[archives_hide_meta]', function( value ) {
			value.bind( function( newval ) {
				if ( newval === true ) {
					$( '.blog article .entry-meta,.archive article .entry-meta,.search article .entry-meta' ).css( 'display', 'none' );
				} else {
					$( '.blog article .entry-meta,.archive article .entry-meta,.search article .entry-meta' ).css( 'display', 'block' );
				}
			} );
		}
	);

	// Padding.
	wp.customize(
		'osixthreeo_settings[archives_pad_left]', function( value ) {
			value.bind(
				function( newval ) {
					$( '.blog article .entry-header,.archive article .entry-header,.search article .entry-header,.blog article .entry-content,.archive article .entry-content,.search article .entry-content,.link-more' ).css( 'padding-left', newval + 'px' );
				}
			);
		}
	);
	wp.customize(
		'osixthreeo_settings[archives_pad_right]', function( value ) {
			value.bind(
				function( newval ) {
					$( '.blog article .entry-header,.archive article .entry-header,.search article .entry-header,.blog article .entry-content,.archive article .entry-content,.search article .entry-content,.link-more' ).css( 'padding-right', newval + 'px' );
				}
			);
		}
	);
	wp.customize(
		'osixthreeo_settings[archives_pad_top]', function( value ) {
			value.bind(
				function( newval ) {
					$( '.blog article .entry-header,.archive article .entry-header,.search article .entry-header,.archive article.format-aside .entry-content,.blog article.format-aside .entry-content,.search article.format-aside .entry-content,.archive article.format-status .entry-content,.blog article.format-status .entry-content,.search article.format-status .entry-content' ).css( 'padding-top', newval + 'px' );
				}
			);
		}
	);
	wp.customize(
		'osixthreeo_settings[archives_pad_bottom]', function( value ) {
			value.bind(
				function( newval ) {
					$( '.link-more' ).css( 'padding-bottom', newval + 'px' );
				}
			);
		}
	);

	// Border Radius.
	wp.customize(
		'osixthreeo_settings[archives_border_radius]', function( value ) {
			value.bind(
				function( newval ) {
					$( '.blog article, .archive article, .search article' ).css( 'border-radius', newval + 'px' );
				}
			);
		}
	);

} )( jQuery );
