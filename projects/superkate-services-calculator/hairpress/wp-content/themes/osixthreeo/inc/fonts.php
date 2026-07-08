<?php
/**
 * FONTS
 *
 * @package    osixthreeo
 * @subpackage osixthreeo/inc
 * @author     Chip Sheppard
 * @since      1.0.0
 * @license    GPL-2.0+
 */

if ( ! defined( 'ABSPATH' ) ) {
	exit; // Exit if accessed directly.
}

/**
 * Theme Fonts URL
 */
function osixthreeo_theme_fonts_url() {

	$osixthreeo_settings = wp_parse_args(
		get_option( 'osixthreeo_settings', array() ),
		osixthreeo_get_defaults()
	);

	$gweights = ':100,100i,200,200i,300,300i,400,400i,500,500i,600,600i,700,700i,800,800i,900,900i';

	$gf1  = 'Alegreya+Sans' . $gweights;
	$gf2  = 'Alegreya+Sans+SC' . $gweights;
	$gf3  = 'Archivo' . $gweights;
	$gf4  = 'Archivo+Narrow' . $gweights;
	$gf5  = 'B612' . $gweights;
	$gf6  = 'Cabin' . $gweights;
	$gf7  = 'Cairo' . $gweights;
	$gf8  = 'Chivo' . $gweights;
	$gf9  = 'Exo 2' . $gweights;
	$gf10 = 'Fjalla+One' . $gweights;
	$gf11 = 'Fira+Sans' . $gweights;
	$gf12 = 'IBM+Plex+Sans' . $gweights;
	$gf13 = 'Karla' . $gweights;
	$gf14 = 'Lato' . $gweights;
	$gf15 = 'Libre+Franklin' . $gweights;
	$gf16 = 'Montserrat' . $gweights;
	$gf17 = 'Montserrat+Alternates' . $gweights;
	$gf18 = 'Muli' . $gweights;
	$gf19 = 'Noto+Sans' . $gweights;
	$gf20 = 'Nunito' . $gweights;
	$gf21 = 'Open+Sans' . $gweights;
	$gf22 = 'Oswald' . $gweights;
	$gf23 = 'Oxygen' . $gweights;
	$gf24 = 'Poppins' . $gweights;
	$gf25 = 'Proza+Libre' . $gweights;
	$gf26 = 'PT+Sans' . $gweights;
	$gf27 = 'Raleway' . $gweights;
	$gf28 = 'Roboto' . $gweights;
	$gf29 = 'Rubik' . $gweights;
	$gf30 = 'Source+Sans+Pro' . $gweights;
	$gf31 = 'Titillium+Web' . $gweights;
	$gf32 = 'Ubuntu' . $gweights;
	$gf33 = 'Varela' . $gweights;
	$gf34 = 'Varela+Round' . $gweights;
	$gf35 = 'Work+Sans' . $gweights;
	$gf36 = 'Alegreya' . $gweights;
	$gf37 = 'Alegreya+SC' . $gweights;
	$gf38 = 'Arvo' . $gweights;
	$gf39 = 'BioRhyme' . $gweights;
	$gf40 = 'Cardo' . $gweights;
	$gf41 = 'Cormorant' . $gweights;
	$gf42 = 'Crimson+Text' . $gweights;
	$gf43 = 'Domine' . $gweights;
	$gf44 = 'Eczar' . $gweights;
	$gf45 = 'Frank+Ruhl+Libre' . $gweights;
	$gf46 = 'IBM+Plex+Serif' . $gweights;
	$gf47 = 'Inknut+Antiqua' . $gweights;
	$gf48 = 'Libre+Baskerville' . $gweights;
	$gf49 = 'Lora' . $gweights;
	$gf50 = 'Merriweather' . $gweights;
	$gf51 = 'Neuton' . $gweights;
	$gf52 = 'Old+Standard TT' . $gweights;
	$gf53 = 'Playfair+Display' . $gweights;
	$gf54 = 'PT+Serif' . $gweights;
	$gf55 = 'Roboto+Slab' . $gweights;
	$gf56 = 'Rokkitt' . $gweights;
	$gf57 = 'Source+Serif+Pro' . $gweights;
	$gf58 = 'Spectral' . $gweights;
	$gf59 = 'Vollkorn' . $gweights;
	$gf60 = 'Vollkorn+SC' . $gweights;
	$gf61 = 'Abril+Fatface' . $gweights;
	$gf62 = 'Alfa+Slab+One' . $gweights;
	$gf63 = 'Baloo' . $gweights;
	$gf64 = 'Barrio' . $gweights;
	$gf65 = 'Black+Ops+One' . $gweights;
	$gf66 = 'Cabin+Sketch' . $gweights;
	$gf67 = 'Chela+One' . $gweights;
	$gf68 = 'Concert+One' . $gweights;
	$gf69 = 'Erica+One' . $gweights;
	$gf70 = 'Fascinate' . $gweights;
	$gf71 = 'Flamenco' . $gweights;
	$gf72 = 'Fredericka+the+Great' . $gweights;
	$gf73 = 'Lily+Script+One' . $gweights;
	$gf74 = 'Lobster' . $gweights;
	$gf75 = 'Lobster+Two' . $gweights;
	$gf76 = 'Monoton' . $gweights;
	$gf77 = 'Nixie+One' . $gweights;
	$gf78 = 'Oleo+Script' . $gweights;
	$gf79 = 'Oleo+Script+Swash+Caps' . $gweights;
	$gf80 = 'Ranchers' . $gweights;
	$gf81 = 'Rakkas' . $gweights;
	$gf82 = 'Special+Elite' . $gweights;
	$gf83 = 'Yatra+One' . $gweights;
	$gf84 = 'Inconsolata' . $gweights;
	$gf85 = 'Space+Mono' . $gweights;

	$gfonts = '';

	if ( 'alegreyasans' === $osixthreeo_settings['base_font'] ) {
		$f1 = $gf1;
	} elseif ( 'alegreyasanssc' === $osixthreeo_settings['base_font'] ) {
		$f1 = $gf2;
	} elseif ( 'archivo' === $osixthreeo_settings['base_font'] ) {
		$f1 = $gf3;
	} elseif ( 'archivonarrow' === $osixthreeo_settings['base_font'] ) {
		$f1 = $gf4;
	} elseif ( 'b612' === $osixthreeo_settings['base_font'] ) {
		$f1 = $gf5;
	} elseif ( 'cabin' === $osixthreeo_settings['base_font'] ) {
		$f1 = $gf6;
	} elseif ( 'cairo' === $osixthreeo_settings['base_font'] ) {
		$f1 = $gf7;
	} elseif ( 'chivo' === $osixthreeo_settings['base_font'] ) {
		$f1 = $gf8;
	} elseif ( 'exo2' === $osixthreeo_settings['base_font'] ) {
		$f1 = $gf9;
	} elseif ( 'fjallaone' === $osixthreeo_settings['base_font'] ) {
		$f1 = $gf10;
	} elseif ( 'firasans' === $osixthreeo_settings['base_font'] ) {
		$f1 = $gf11;
	} elseif ( 'ibmplexsans' === $osixthreeo_settings['base_font'] ) {
		$f1 = $gf12;
	} elseif ( 'karla' === $osixthreeo_settings['base_font'] ) {
		$f1 = $gf13;
	} elseif ( 'lato' === $osixthreeo_settings['base_font'] ) {
		$f1 = $gf14;
	} elseif ( 'librefranklin' === $osixthreeo_settings['base_font'] ) {
		$f1 = $gf15;
	} elseif ( 'montserrat' === $osixthreeo_settings['base_font'] ) {
		$f1 = $gf16;
	} elseif ( 'montserratalternates' === $osixthreeo_settings['base_font'] ) {
		$f1 = $gf17;
	} elseif ( 'muli' === $osixthreeo_settings['base_font'] ) {
		$f1 = $gf18;
	} elseif ( 'notosans' === $osixthreeo_settings['base_font'] ) {
		$f1 = $gf19;
	} elseif ( 'nunito' === $osixthreeo_settings['base_font'] ) {
		$f1 = $gf20;
	} elseif ( 'opensans' === $osixthreeo_settings['base_font'] ) {
		$f1 = $gf21;
	} elseif ( 'oswald' === $osixthreeo_settings['base_font'] ) {
		$f1 = $gf22;
	} elseif ( 'oxygen' === $osixthreeo_settings['base_font'] ) {
		$f1 = $gf23;
	} elseif ( 'poppins' === $osixthreeo_settings['base_font'] ) {
		$f1 = $gf24;
	} elseif ( 'prozalibre' === $osixthreeo_settings['base_font'] ) {
		$f1 = $gf25;
	} elseif ( 'ptsans' === $osixthreeo_settings['base_font'] ) {
		$f1 = $gf26;
	} elseif ( 'raleway' === $osixthreeo_settings['base_font'] ) {
		$f1 = $gf27;
	} elseif ( 'roboto' === $osixthreeo_settings['base_font'] ) {
		$f1 = $gf28;
	} elseif ( 'rubik' === $osixthreeo_settings['base_font'] ) {
		$f1 = $gf29;
	} elseif ( 'sourcesanspro' === $osixthreeo_settings['base_font'] ) {
		$f1 = $gf30;
	} elseif ( 'titilliumweb' === $osixthreeo_settings['base_font'] ) {
		$f1 = $gf31;
	} elseif ( 'ubuntu' === $osixthreeo_settings['base_font'] ) {
		$f1 = $gf31;
	} elseif ( 'varela' === $osixthreeo_settings['base_font'] ) {
		$f1 = $gf33;
	} elseif ( 'varelaround' === $osixthreeo_settings['base_font'] ) {
		$f1 = $gf34;
	} elseif ( 'worksans' === $osixthreeo_settings['base_font'] ) {
		$f1 = $gf35;
	} elseif ( 'alegreya' === $osixthreeo_settings['base_font'] ) {
		$f1 = $gf36;
	} elseif ( 'alegreyasc' === $osixthreeo_settings['base_font'] ) {
		$f1 = $gf37;
	} elseif ( 'arvo' === $osixthreeo_settings['base_font'] ) {
		$f1 = $gf38;
	} elseif ( 'biothyme' === $osixthreeo_settings['base_font'] ) {
		$f1 = $gf39;
	} elseif ( 'cardo' === $osixthreeo_settings['base_font'] ) {
		$f1 = $gf40;
	} elseif ( 'cormorant' === $osixthreeo_settings['base_font'] ) {
		$f1 = $gf41;
	} elseif ( 'crimsontext' === $osixthreeo_settings['base_font'] ) {
		$f1 = $gf42;
	} elseif ( 'domine' === $osixthreeo_settings['base_font'] ) {
		$f1 = $gf43;
	} elseif ( 'eczar' === $osixthreeo_settings['base_font'] ) {
		$f1 = $gf44;
	} elseif ( 'frankruhllibre' === $osixthreeo_settings['base_font'] ) {
		$f1 = $gf45;
	} elseif ( 'ibmplexserif' === $osixthreeo_settings['base_font'] ) {
		$f1 = $gf46;
	} elseif ( 'inknutantiqua' === $osixthreeo_settings['base_font'] ) {
		$f1 = $gf47;
	} elseif ( 'librebaskerville' === $osixthreeo_settings['base_font'] ) {
		$f1 = $gf48;
	} elseif ( 'lora' === $osixthreeo_settings['base_font'] ) {
		$f1 = $gf49;
	} elseif ( 'merriweather' === $osixthreeo_settings['base_font'] ) {
		$f1 = $gf50;
	} elseif ( 'neuton' === $osixthreeo_settings['base_font'] ) {
		$f1 = $gf51;
	} elseif ( 'oldstandardtt' === $osixthreeo_settings['base_font'] ) {
		$f1 = $gf52;
	} elseif ( 'playfairdisplay' === $osixthreeo_settings['base_font'] ) {
		$f1 = $gf53;
	} elseif ( 'ptserif' === $osixthreeo_settings['base_font'] ) {
		$f1 = $gf54;
	} elseif ( 'robotoslab' === $osixthreeo_settings['base_font'] ) {
		$f1 = $gf55;
	} elseif ( 'rokkitt' === $osixthreeo_settings['base_font'] ) {
		$f1 = $gf56;
	} elseif ( 'sourceserifpro' === $osixthreeo_settings['base_font'] ) {
		$f1 = $gf57;
	} elseif ( 'spectral' === $osixthreeo_settings['base_font'] ) {
		$f1 = $gf58;
	} elseif ( 'vollkorn' === $osixthreeo_settings['base_font'] ) {
		$f1 = $gf59;
	} elseif ( 'vollkornsc' === $osixthreeo_settings['base_font'] ) {
		$f1 = $gf60;
	} elseif ( 'abrilfatface' === $osixthreeo_settings['base_font'] ) {
		$f1 = $gf61;
	} elseif ( 'alfaslabone' === $osixthreeo_settings['base_font'] ) {
		$f1 = $gf62;
	} elseif ( 'baloo' === $osixthreeo_settings['base_font'] ) {
		$f1 = $gf63;
	} elseif ( 'barrio' === $osixthreeo_settings['base_font'] ) {
		$f1 = $gf64;
	} elseif ( 'blackopsone' === $osixthreeo_settings['base_font'] ) {
		$f1 = $gf65;
	} elseif ( 'cabinsketch' === $osixthreeo_settings['base_font'] ) {
		$f1 = $gf66;
	} elseif ( 'chelaone' === $osixthreeo_settings['base_font'] ) {
		$f1 = $gf67;
	} elseif ( 'concertone' === $osixthreeo_settings['base_font'] ) {
		$f1 = $gf68;
	} elseif ( 'ericaone' === $osixthreeo_settings['base_font'] ) {
		$f1 = $gf69;
	} elseif ( 'fascinate' === $osixthreeo_settings['base_font'] ) {
		$f1 = $gf70;
	} elseif ( 'flamenco' === $osixthreeo_settings['base_font'] ) {
		$f1 = $gf71;
	} elseif ( 'frederickathegreat' === $osixthreeo_settings['base_font'] ) {
		$f1 = $gf72;
	} elseif ( 'lilyscriptone' === $osixthreeo_settings['base_font'] ) {
		$f1 = $gf73;
	} elseif ( 'lobster' === $osixthreeo_settings['base_font'] ) {
		$f1 = $gf74;
	} elseif ( 'lobstertwo' === $osixthreeo_settings['base_font'] ) {
		$f1 = $gf75;
	} elseif ( 'monoton' === $osixthreeo_settings['base_font'] ) {
		$f1 = $gf76;
	} elseif ( 'nixieone' === $osixthreeo_settings['base_font'] ) {
		$f1 = $gf77;
	} elseif ( 'oleoscript' === $osixthreeo_settings['base_font'] ) {
		$f1 = $gf78;
	} elseif ( 'oleoscriptswashcaps' === $osixthreeo_settings['base_font'] ) {
		$f1 = $gf79;
	} elseif ( 'ranchers' === $osixthreeo_settings['base_font'] ) {
		$f1 = $gf80;
	} elseif ( 'rakkas' === $osixthreeo_settings['base_font'] ) {
		$f1 = $gf81;
	} elseif ( 'specialelite' === $osixthreeo_settings['base_font'] ) {
		$f1 = $gf82;
	} elseif ( 'yatraone' === $osixthreeo_settings['base_font'] ) {
		$f1 = $gf83;
	} elseif ( 'inconsolata' === $osixthreeo_settings['base_font'] ) {
		$f1 = $gf84;
	} elseif ( 'spacemono' === $osixthreeo_settings['base_font'] ) {
		$f1 = $gf85;
	} else {
		$f1 = '';
	}

	if ( 'alegreyasans' === $osixthreeo_settings['header_font'] ) {
		$f2 = $gf1;
	} elseif ( 'alegreyasanssc' === $osixthreeo_settings['header_font'] ) {
		$f2 = $gf2;
	} elseif ( 'archivo' === $osixthreeo_settings['header_font'] ) {
		$f2 = $gf3;
	} elseif ( 'archivonarrow' === $osixthreeo_settings['header_font'] ) {
		$f2 = $gf4;
	} elseif ( 'b612' === $osixthreeo_settings['header_font'] ) {
		$f2 = $gf5;
	} elseif ( 'cabin' === $osixthreeo_settings['header_font'] ) {
		$f2 = $gf6;
	} elseif ( 'cairo' === $osixthreeo_settings['header_font'] ) {
		$f2 = $gf7;
	} elseif ( 'chivo' === $osixthreeo_settings['header_font'] ) {
		$f2 = $gf8;
	} elseif ( 'exo2' === $osixthreeo_settings['header_font'] ) {
		$f2 = $gf9;
	} elseif ( 'fjallaone' === $osixthreeo_settings['header_font'] ) {
		$f2 = $gf10;
	} elseif ( 'firasans' === $osixthreeo_settings['header_font'] ) {
		$f2 = $gf11;
	} elseif ( 'ibmplexsans' === $osixthreeo_settings['header_font'] ) {
		$f2 = $gf12;
	} elseif ( 'karla' === $osixthreeo_settings['header_font'] ) {
		$f2 = $gf13;
	} elseif ( 'lato' === $osixthreeo_settings['header_font'] ) {
		$f2 = $gf14;
	} elseif ( 'librefranklin' === $osixthreeo_settings['header_font'] ) {
		$f2 = $gf15;
	} elseif ( 'montserrat' === $osixthreeo_settings['header_font'] ) {
		$f2 = $gf16;
	} elseif ( 'montserratalternates' === $osixthreeo_settings['header_font'] ) {
		$f2 = $gf17;
	} elseif ( 'muli' === $osixthreeo_settings['header_font'] ) {
		$f2 = $gf18;
	} elseif ( 'notosans' === $osixthreeo_settings['header_font'] ) {
		$f2 = $gf19;
	} elseif ( 'nunito' === $osixthreeo_settings['header_font'] ) {
		$f2 = $gf20;
	} elseif ( 'opensans' === $osixthreeo_settings['header_font'] ) {
		$f2 = $gf21;
	} elseif ( 'oswald' === $osixthreeo_settings['header_font'] ) {
		$f2 = $gf22;
	} elseif ( 'oxygen' === $osixthreeo_settings['header_font'] ) {
		$f2 = $gf23;
	} elseif ( 'poppins' === $osixthreeo_settings['header_font'] ) {
		$f2 = $gf24;
	} elseif ( 'prozalibre' === $osixthreeo_settings['header_font'] ) {
		$f2 = $gf25;
	} elseif ( 'ptsans' === $osixthreeo_settings['header_font'] ) {
		$f2 = $gf26;
	} elseif ( 'raleway' === $osixthreeo_settings['header_font'] ) {
		$f2 = $gf27;
	} elseif ( 'roboto' === $osixthreeo_settings['header_font'] ) {
		$f2 = $gf28;
	} elseif ( 'rubik' === $osixthreeo_settings['header_font'] ) {
		$f2 = $gf29;
	} elseif ( 'sourcesanspro' === $osixthreeo_settings['header_font'] ) {
		$f2 = $gf30;
	} elseif ( 'titilliumweb' === $osixthreeo_settings['header_font'] ) {
		$f2 = $gf31;
	} elseif ( 'ubuntu' === $osixthreeo_settings['header_font'] ) {
		$f2 = $gf31;
	} elseif ( 'varela' === $osixthreeo_settings['header_font'] ) {
		$f2 = $gf33;
	} elseif ( 'varelaround' === $osixthreeo_settings['header_font'] ) {
		$f2 = $gf34;
	} elseif ( 'worksans' === $osixthreeo_settings['header_font'] ) {
		$f2 = $gf35;
	} elseif ( 'alegreya' === $osixthreeo_settings['header_font'] ) {
		$f2 = $gf36;
	} elseif ( 'alegreyasc' === $osixthreeo_settings['header_font'] ) {
		$f2 = $gf37;
	} elseif ( 'arvo' === $osixthreeo_settings['header_font'] ) {
		$f2 = $gf38;
	} elseif ( 'biothyme' === $osixthreeo_settings['header_font'] ) {
		$f2 = $gf39;
	} elseif ( 'cardo' === $osixthreeo_settings['header_font'] ) {
		$f2 = $gf40;
	} elseif ( 'cormorant' === $osixthreeo_settings['header_font'] ) {
		$f2 = $gf41;
	} elseif ( 'crimsontext' === $osixthreeo_settings['header_font'] ) {
		$f2 = $gf42;
	} elseif ( 'domine' === $osixthreeo_settings['header_font'] ) {
		$f2 = $gf43;
	} elseif ( 'eczar' === $osixthreeo_settings['header_font'] ) {
		$f2 = $gf44;
	} elseif ( 'frankruhllibre' === $osixthreeo_settings['header_font'] ) {
		$f2 = $gf45;
	} elseif ( 'ibmplexserif' === $osixthreeo_settings['header_font'] ) {
		$f2 = $gf46;
	} elseif ( 'inknutantiqua' === $osixthreeo_settings['header_font'] ) {
		$f2 = $gf47;
	} elseif ( 'librebaskerville' === $osixthreeo_settings['header_font'] ) {
		$f2 = $gf48;
	} elseif ( 'lora' === $osixthreeo_settings['header_font'] ) {
		$f2 = $gf49;
	} elseif ( 'merriweather' === $osixthreeo_settings['header_font'] ) {
		$f2 = $gf50;
	} elseif ( 'neuton' === $osixthreeo_settings['header_font'] ) {
		$f2 = $gf51;
	} elseif ( 'oldstandardtt' === $osixthreeo_settings['header_font'] ) {
		$f2 = $gf52;
	} elseif ( 'playfairdisplay' === $osixthreeo_settings['header_font'] ) {
		$f2 = $gf53;
	} elseif ( 'ptserif' === $osixthreeo_settings['header_font'] ) {
		$f2 = $gf54;
	} elseif ( 'robotoslab' === $osixthreeo_settings['header_font'] ) {
		$f2 = $gf55;
	} elseif ( 'rokkitt' === $osixthreeo_settings['header_font'] ) {
		$f2 = $gf56;
	} elseif ( 'sourceserifpro' === $osixthreeo_settings['header_font'] ) {
		$f2 = $gf57;
	} elseif ( 'spectral' === $osixthreeo_settings['header_font'] ) {
		$f2 = $gf58;
	} elseif ( 'vollkorn' === $osixthreeo_settings['header_font'] ) {
		$f2 = $gf59;
	} elseif ( 'vollkornsc' === $osixthreeo_settings['header_font'] ) {
		$f2 = $gf60;
	} elseif ( 'abrilfatface' === $osixthreeo_settings['header_font'] ) {
		$f2 = $gf61;
	} elseif ( 'alfaslabone' === $osixthreeo_settings['header_font'] ) {
		$f2 = $gf62;
	} elseif ( 'baloo' === $osixthreeo_settings['header_font'] ) {
		$f2 = $gf63;
	} elseif ( 'barrio' === $osixthreeo_settings['header_font'] ) {
		$f2 = $gf64;
	} elseif ( 'blackopsone' === $osixthreeo_settings['header_font'] ) {
		$f2 = $gf65;
	} elseif ( 'cabinsketch' === $osixthreeo_settings['header_font'] ) {
		$f2 = $gf66;
	} elseif ( 'chelaone' === $osixthreeo_settings['header_font'] ) {
		$f2 = $gf67;
	} elseif ( 'concertone' === $osixthreeo_settings['header_font'] ) {
		$f2 = $gf68;
	} elseif ( 'ericaone' === $osixthreeo_settings['header_font'] ) {
		$f2 = $gf69;
	} elseif ( 'fascinate' === $osixthreeo_settings['header_font'] ) {
		$f2 = $gf70;
	} elseif ( 'flamenco' === $osixthreeo_settings['header_font'] ) {
		$f2 = $gf71;
	} elseif ( 'frederickathegreat' === $osixthreeo_settings['header_font'] ) {
		$f2 = $gf72;
	} elseif ( 'lilyscriptone' === $osixthreeo_settings['header_font'] ) {
		$f2 = $gf73;
	} elseif ( 'lobster' === $osixthreeo_settings['header_font'] ) {
		$f2 = $gf74;
	} elseif ( 'lobstertwo' === $osixthreeo_settings['header_font'] ) {
		$f2 = $gf75;
	} elseif ( 'monoton' === $osixthreeo_settings['header_font'] ) {
		$f2 = $gf76;
	} elseif ( 'nixieone' === $osixthreeo_settings['header_font'] ) {
		$f2 = $gf77;
	} elseif ( 'oleoscript' === $osixthreeo_settings['header_font'] ) {
		$f2 = $gf78;
	} elseif ( 'oleoscriptswashcaps' === $osixthreeo_settings['header_font'] ) {
		$f2 = $gf79;
	} elseif ( 'ranchers' === $osixthreeo_settings['header_font'] ) {
		$f2 = $gf80;
	} elseif ( 'rakkas' === $osixthreeo_settings['header_font'] ) {
		$f2 = $gf81;
	} elseif ( 'specialelite' === $osixthreeo_settings['header_font'] ) {
		$f2 = $gf82;
	} elseif ( 'yatraone' === $osixthreeo_settings['header_font'] ) {
		$f2 = $gf83;
	} elseif ( 'inconsolata' === $osixthreeo_settings['header_font'] ) {
		$f2 = $gf84;
	} elseif ( 'spacemono' === $osixthreeo_settings['header_font'] ) {
		$f2 = $gf85;
	} else {
		$f2 = '';
	}

	if ( 'alegreyasans' === $osixthreeo_settings['highlite_font'] ) {
		$f3 = $gf1;
	} elseif ( 'alegreyasanssc' === $osixthreeo_settings['highlite_font'] ) {
		$f3 = $gf2;
	} elseif ( 'archivo' === $osixthreeo_settings['highlite_font'] ) {
		$f3 = $gf3;
	} elseif ( 'archivonarrow' === $osixthreeo_settings['highlite_font'] ) {
		$f3 = $gf4;
	} elseif ( 'b612' === $osixthreeo_settings['highlite_font'] ) {
		$f3 = $gf5;
	} elseif ( 'cabin' === $osixthreeo_settings['highlite_font'] ) {
		$f3 = $gf6;
	} elseif ( 'cairo' === $osixthreeo_settings['highlite_font'] ) {
		$f3 = $gf7;
	} elseif ( 'chivo' === $osixthreeo_settings['highlite_font'] ) {
		$f3 = $gf8;
	} elseif ( 'exo2' === $osixthreeo_settings['highlite_font'] ) {
		$f3 = $gf9;
	} elseif ( 'fjallaone' === $osixthreeo_settings['highlite_font'] ) {
		$f3 = $gf10;
	} elseif ( 'firasans' === $osixthreeo_settings['highlite_font'] ) {
		$f3 = $gf11;
	} elseif ( 'ibmplexsans' === $osixthreeo_settings['highlite_font'] ) {
		$f3 = $gf12;
	} elseif ( 'karla' === $osixthreeo_settings['highlite_font'] ) {
		$f3 = $gf13;
	} elseif ( 'lato' === $osixthreeo_settings['highlite_font'] ) {
		$f3 = $gf14;
	} elseif ( 'librefranklin' === $osixthreeo_settings['highlite_font'] ) {
		$f3 = $gf15;
	} elseif ( 'montserrat' === $osixthreeo_settings['highlite_font'] ) {
		$f3 = $gf16;
	} elseif ( 'montserratalternates' === $osixthreeo_settings['highlite_font'] ) {
		$f3 = $gf17;
	} elseif ( 'muli' === $osixthreeo_settings['highlite_font'] ) {
		$f3 = $gf18;
	} elseif ( 'notosans' === $osixthreeo_settings['highlite_font'] ) {
		$f3 = $gf19;
	} elseif ( 'nunito' === $osixthreeo_settings['highlite_font'] ) {
		$f3 = $gf20;
	} elseif ( 'opensans' === $osixthreeo_settings['highlite_font'] ) {
		$f3 = $gf21;
	} elseif ( 'oswald' === $osixthreeo_settings['highlite_font'] ) {
		$f3 = $gf22;
	} elseif ( 'oxygen' === $osixthreeo_settings['highlite_font'] ) {
		$f3 = $gf23;
	} elseif ( 'poppins' === $osixthreeo_settings['highlite_font'] ) {
		$f3 = $gf24;
	} elseif ( 'prozalibre' === $osixthreeo_settings['highlite_font'] ) {
		$f3 = $gf25;
	} elseif ( 'ptsans' === $osixthreeo_settings['highlite_font'] ) {
		$f3 = $gf26;
	} elseif ( 'raleway' === $osixthreeo_settings['highlite_font'] ) {
		$f3 = $gf27;
	} elseif ( 'roboto' === $osixthreeo_settings['highlite_font'] ) {
		$f3 = $gf28;
	} elseif ( 'rubik' === $osixthreeo_settings['highlite_font'] ) {
		$f3 = $gf29;
	} elseif ( 'sourcesanspro' === $osixthreeo_settings['highlite_font'] ) {
		$f3 = $gf30;
	} elseif ( 'titilliumweb' === $osixthreeo_settings['highlite_font'] ) {
		$f3 = $gf31;
	} elseif ( 'ubuntu' === $osixthreeo_settings['highlite_font'] ) {
		$f3 = $gf31;
	} elseif ( 'varela' === $osixthreeo_settings['highlite_font'] ) {
		$f3 = $gf33;
	} elseif ( 'varelaround' === $osixthreeo_settings['highlite_font'] ) {
		$f3 = $gf34;
	} elseif ( 'worksans' === $osixthreeo_settings['highlite_font'] ) {
		$f3 = $gf35;
	} elseif ( 'alegreya' === $osixthreeo_settings['highlite_font'] ) {
		$f3 = $gf36;
	} elseif ( 'alegreyasc' === $osixthreeo_settings['highlite_font'] ) {
		$f3 = $gf37;
	} elseif ( 'arvo' === $osixthreeo_settings['highlite_font'] ) {
		$f3 = $gf38;
	} elseif ( 'biothyme' === $osixthreeo_settings['highlite_font'] ) {
		$f3 = $gf39;
	} elseif ( 'cardo' === $osixthreeo_settings['highlite_font'] ) {
		$f3 = $gf40;
	} elseif ( 'cormorant' === $osixthreeo_settings['highlite_font'] ) {
		$f3 = $gf41;
	} elseif ( 'crimsontext' === $osixthreeo_settings['highlite_font'] ) {
		$f3 = $gf42;
	} elseif ( 'domine' === $osixthreeo_settings['highlite_font'] ) {
		$f3 = $gf43;
	} elseif ( 'eczar' === $osixthreeo_settings['highlite_font'] ) {
		$f3 = $gf44;
	} elseif ( 'frankruhllibre' === $osixthreeo_settings['highlite_font'] ) {
		$f3 = $gf45;
	} elseif ( 'ibmplexserif' === $osixthreeo_settings['highlite_font'] ) {
		$f3 = $gf46;
	} elseif ( 'inknutantiqua' === $osixthreeo_settings['highlite_font'] ) {
		$f3 = $gf47;
	} elseif ( 'librebaskerville' === $osixthreeo_settings['highlite_font'] ) {
		$f3 = $gf48;
	} elseif ( 'lora' === $osixthreeo_settings['highlite_font'] ) {
		$f3 = $gf49;
	} elseif ( 'merriweather' === $osixthreeo_settings['highlite_font'] ) {
		$f3 = $gf50;
	} elseif ( 'neuton' === $osixthreeo_settings['highlite_font'] ) {
		$f3 = $gf51;
	} elseif ( 'oldstandardtt' === $osixthreeo_settings['highlite_font'] ) {
		$f3 = $gf52;
	} elseif ( 'playfairdisplay' === $osixthreeo_settings['highlite_font'] ) {
		$f3 = $gf53;
	} elseif ( 'ptserif' === $osixthreeo_settings['highlite_font'] ) {
		$f3 = $gf54;
	} elseif ( 'robotoslab' === $osixthreeo_settings['highlite_font'] ) {
		$f3 = $gf55;
	} elseif ( 'rokkitt' === $osixthreeo_settings['highlite_font'] ) {
		$f3 = $gf56;
	} elseif ( 'sourceserifpro' === $osixthreeo_settings['highlite_font'] ) {
		$f3 = $gf57;
	} elseif ( 'spectral' === $osixthreeo_settings['highlite_font'] ) {
		$f3 = $gf58;
	} elseif ( 'vollkorn' === $osixthreeo_settings['highlite_font'] ) {
		$f3 = $gf59;
	} elseif ( 'vollkornsc' === $osixthreeo_settings['highlite_font'] ) {
		$f3 = $gf60;
	} elseif ( 'abrilfatface' === $osixthreeo_settings['highlite_font'] ) {
		$f3 = $gf61;
	} elseif ( 'alfaslabone' === $osixthreeo_settings['highlite_font'] ) {
		$f3 = $gf62;
	} elseif ( 'baloo' === $osixthreeo_settings['highlite_font'] ) {
		$f3 = $gf63;
	} elseif ( 'barrio' === $osixthreeo_settings['highlite_font'] ) {
		$f3 = $gf64;
	} elseif ( 'blackopsone' === $osixthreeo_settings['highlite_font'] ) {
		$f3 = $gf65;
	} elseif ( 'cabinsketch' === $osixthreeo_settings['highlite_font'] ) {
		$f3 = $gf66;
	} elseif ( 'chelaone' === $osixthreeo_settings['highlite_font'] ) {
		$f3 = $gf67;
	} elseif ( 'concertone' === $osixthreeo_settings['highlite_font'] ) {
		$f3 = $gf68;
	} elseif ( 'ericaone' === $osixthreeo_settings['highlite_font'] ) {
		$f3 = $gf69;
	} elseif ( 'fascinate' === $osixthreeo_settings['highlite_font'] ) {
		$f3 = $gf70;
	} elseif ( 'flamenco' === $osixthreeo_settings['highlite_font'] ) {
		$f3 = $gf71;
	} elseif ( 'frederickathegreat' === $osixthreeo_settings['highlite_font'] ) {
		$f3 = $gf72;
	} elseif ( 'lilyscriptone' === $osixthreeo_settings['highlite_font'] ) {
		$f3 = $gf73;
	} elseif ( 'lobster' === $osixthreeo_settings['highlite_font'] ) {
		$f3 = $gf74;
	} elseif ( 'lobstertwo' === $osixthreeo_settings['highlite_font'] ) {
		$f3 = $gf75;
	} elseif ( 'monoton' === $osixthreeo_settings['highlite_font'] ) {
		$f3 = $gf76;
	} elseif ( 'nixieone' === $osixthreeo_settings['highlite_font'] ) {
		$f3 = $gf77;
	} elseif ( 'oleoscript' === $osixthreeo_settings['highlite_font'] ) {
		$f3 = $gf78;
	} elseif ( 'oleoscriptswashcaps' === $osixthreeo_settings['highlite_font'] ) {
		$f3 = $gf79;
	} elseif ( 'ranchers' === $osixthreeo_settings['highlite_font'] ) {
		$f3 = $gf80;
	} elseif ( 'rakkas' === $osixthreeo_settings['highlite_font'] ) {
		$f3 = $gf81;
	} elseif ( 'specialelite' === $osixthreeo_settings['highlite_font'] ) {
		$f3 = $gf82;
	} elseif ( 'yatraone' === $osixthreeo_settings['highlite_font'] ) {
		$f3 = $gf83;
	} elseif ( 'inconsolata' === $osixthreeo_settings['highlite_font'] ) {
		$f3 = $gf84;
	} elseif ( 'spacemono' === $osixthreeo_settings['highlite_font'] ) {
		$f3 = $gf85;
	} else {
		$f3 = '';
	}

	if ( '' === $f1 && '' === $f2 && '' === $f3 ) {
		return;
	}

	if ( '' !== $f1 && '' !== $f2 && '' !== $f3 ) {
		if ( $f1 === $f2 && $f1 === $f3 ) {
			$gfonts = $f1;
		} elseif ( $f1 === $f2 && $f1 !== $f3 ) {
			$gfonts = $f1 . '|' . $f3;
		} elseif ( $f1 !== $f2 && $f1 === $f3 ) {
			$gfonts = $f1 . '|' . $f2;
		} elseif ( $f1 !== $f2 && $f1 !== $f3 && $f2 === $f3 ) {
			$gfonts = $f1 . '|' . $f2;
		} else {
			$gfonts = $f1 . '|' . $f2 . '|' . $f3;
		}
	}
	if ( '' !== $f1 && '' !== $f2 && '' === $f3 ) {
		if ( $f1 === $f2 ) {
			$gfonts = $f1;
		} else {
			$gfonts = $f1 . '|' . $f2;
		}
	}
	if ( '' !== $f1 && '' === $f2 && '' !== $f3 ) {
		if ( $f1 === $f3 ) {
			$gfonts = $f1;
		} else {
			$gfonts = $f1 . '|' . $f3;
		}
	}
	if ( '' === $f1 && '' !== $f2 && '' !== $f3 ) {
		if ( $f2 === $f3 ) {
			$gfonts = $f2;
		} else {
			$gfonts = $f2 . '|' . $f3;
		}
	}
	if ( '' !== $f1 && '' === $f2 && '' === $f3 ) {
		$gfonts = $f1;
	}
	if ( '' === $f1 && '' !== $f2 && '' === $f3 ) {
		$gfonts = $f2;
	}
	if ( '' === $f1 && '' === $f2 && '' !== $f3 ) {
		$gfonts = $f3;
	}

	$font_families = apply_filters( 'osixthreeo_theme_fonts', array( $gfonts ) );
	$query_args    = array(
		'family'  => implode( '|', $font_families ),
		'display' => 'swap',
		'subset'  => 'latin,latin-ext',
	);
	$fonts_url     = add_query_arg( $query_args, 'https://fonts.googleapis.com/css' );
	return $fonts_url;
}
