<?php
/**
 * Builds our admin page.
 *
 */

if ( ! defined( 'ABSPATH' ) ) {
	exit; // Exit if accessed directly.
}

if ( ! function_exists( 'lingam_create_menu' ) ) {
	add_action( 'admin_menu', 'lingam_create_menu' );
	/**
	 * Adds our "Lingam" dashboard menu item
	 *
	 */
	function lingam_create_menu() {
		$lingam_page = add_theme_page( 'Lingam', 'Lingam', apply_filters( 'lingam_dashboard_page_capability', 'edit_theme_options' ), 'lingam-options', 'lingam_settings_page' );
		add_action( "admin_print_styles-$lingam_page", 'lingam_options_styles' );
	}
}

if ( ! function_exists( 'lingam_options_styles' ) ) {
	/**
	 * Adds any necessary scripts to the Lingam dashboard page
	 *
	 */
	function lingam_options_styles() {
		wp_enqueue_style( 'lingam-options', get_template_directory_uri() . '/css/admin/admin-style.css', array(), LINGAM_VERSION );
	}
}

if ( ! function_exists( 'lingam_settings_page' ) ) {
	/**
	 * Builds the content of our Lingam dashboard page
	 *
	 */
	function lingam_settings_page() {
		?>
		<div class="wrap">
			<div class="metabox-holder">
				<div class="lingam-masthead clearfix">
					<div class="lingam-container">
						<div class="lingam-title">
							<a href="<?php echo esc_url(LINGAM_THEME_URL); ?>" target="_blank"><?php esc_html_e( 'Lingam', 'lingam' ); ?></a> <span class="lingam-version"><?php echo LINGAM_VERSION; ?></span>
						</div>
						<div class="lingam-masthead-links">
							<?php if ( ! defined( 'LINGAM_PREMIUM_VERSION' ) ) : ?>
								<a class="lingam-masthead-links-bold" href="<?php echo esc_url(LINGAM_THEME_URL); ?>" target="_blank"><?php esc_html_e( 'Premium', 'lingam' );?></a>
							<?php endif; ?>
							<a href="<?php echo esc_url(LINGAM_WPKOI_AUTHOR_URL); ?>" target="_blank"><?php esc_html_e( 'WPKoi', 'lingam' ); ?></a>
                            <a href="<?php echo esc_url(LINGAM_DOCUMENTATION); ?>" target="_blank"><?php esc_html_e( 'Documentation', 'lingam' ); ?></a>
						</div>
					</div>
				</div>

				<?php
				/**
				 * lingam_dashboard_after_header hook.
				 *
				 */
				 do_action( 'lingam_dashboard_after_header' );
				 ?>

				<div class="lingam-container">
					<div class="postbox-container clearfix" style="float: none;">
						<div class="grid-container grid-parent">

							<?php
							/**
							 * lingam_dashboard_inside_container hook.
							 *
							 */
							 do_action( 'lingam_dashboard_inside_container' );
							 ?>

							<div class="form-metabox grid-70" style="padding-left: 0;">
								<h2 style="height:0;margin:0;"><!-- admin notices below this element --></h2>
								<form method="post" action="options.php">
									<?php settings_fields( 'lingam-settings-group' ); ?>
									<?php do_settings_sections( 'lingam-settings-group' ); ?>
									<div class="customize-button hide-on-desktop">
										<?php
										printf( '<a id="lingam_customize_button" class="button button-primary" href="%1$s">%2$s</a>',
											esc_url( admin_url( 'customize.php' ) ),
											esc_html__( 'Customize', 'lingam' )
										);
										?>
									</div>

									<?php
									/**
									 * lingam_inside_options_form hook.
									 *
									 */
									 do_action( 'lingam_inside_options_form' );
									 ?>
								</form>

								<?php
								$modules = array(
									'Backgrounds' => array(
											'url' => LINGAM_THEME_URL,
									),
									'Blog' => array(
											'url' => LINGAM_THEME_URL,
									),
									'Colors' => array(
											'url' => LINGAM_THEME_URL,
									),
									'Copyright' => array(
											'url' => LINGAM_THEME_URL,
									),
									'Disable Elements' => array(
											'url' => LINGAM_THEME_URL,
									),
									'Demo Import' => array(
											'url' => LINGAM_THEME_URL,
									),
									'Hooks' => array(
											'url' => LINGAM_THEME_URL,
									),
									'Import / Export' => array(
											'url' => LINGAM_THEME_URL,
									),
									'Menu Plus' => array(
											'url' => LINGAM_THEME_URL,
									),
									'Page Header' => array(
											'url' => LINGAM_THEME_URL,
									),
									'Secondary Nav' => array(
											'url' => LINGAM_THEME_URL,
									),
									'Spacing' => array(
											'url' => LINGAM_THEME_URL,
									),
									'Typography' => array(
											'url' => LINGAM_THEME_URL,
									),
									'Elementor Addon' => array(
											'url' => LINGAM_THEME_URL,
									)
								);

								if ( ! defined( 'LINGAM_PREMIUM_VERSION' ) ) : ?>
									<div class="postbox lingam-metabox">
										<h3 class="hndle"><?php esc_html_e( 'Premium Modules', 'lingam' ); ?></h3>
										<div class="inside" style="margin:0;padding:0;">
											<div class="premium-addons">
												<?php foreach( $modules as $module => $info ) { ?>
												<div class="add-on activated lingam-clear addon-container grid-parent">
													<div class="addon-name column-addon-name" style="">
														<a href="<?php echo esc_url( $info[ 'url' ] ); ?>" target="_blank"><?php echo esc_html( $module ); ?></a>
													</div>
													<div class="addon-action addon-addon-action" style="text-align:right;">
														<a href="<?php echo esc_url( $info[ 'url' ] ); ?>" target="_blank"><?php esc_html_e( 'More info', 'lingam' ); ?></a>
													</div>
												</div>
												<div class="lingam-clear"></div>
												<?php } ?>
											</div>
										</div>
									</div>
								<?php
								endif;

								/**
								 * lingam_options_items hook.
								 *
								 */
								do_action( 'lingam_options_items' );
								?>
							</div>

							<div class="lingam-right-sidebar grid-30" style="padding-right: 0;">
								<div class="customize-button hide-on-mobile">
									<?php
									printf( '<a id="lingam_customize_button" class="button button-primary" href="%1$s">%2$s</a>',
										esc_url( admin_url( 'customize.php' ) ),
										esc_html__( 'Customize', 'lingam' )
									);
									?>
								</div>

								<?php
								/**
								 * lingam_admin_right_panel hook.
								 *
								 */
								 do_action( 'lingam_admin_right_panel' );

								  ?>
                                
                                <div class="wpkoi-doc">
                                	<h3><?php esc_html_e( 'Lingam documentation', 'lingam' ); ?></h3>
                                	<p><?php esc_html_e( 'If You`ve stuck, the documentation may help on WPKoi.com', 'lingam' ); ?></p>
                                    <a href="<?php echo esc_url(LINGAM_DOCUMENTATION); ?>" class="wpkoi-admin-button" target="_blank"><?php esc_html_e( 'Lingam documentation', 'lingam' ); ?></a>
                                </div>
                                
                                <div class="wpkoi-social">
                                	<h3><?php esc_html_e( 'WPKoi on Facebook', 'lingam' ); ?></h3>
                                	<p><?php esc_html_e( 'If You want to get useful info about WordPress and the theme, follow WPKoi on Facebook.', 'lingam' ); ?></p>
                                    <a href="<?php echo esc_url(LINGAM_WPKOI_SOCIAL_URL); ?>" class="wpkoi-admin-button" target="_blank"><?php esc_html_e( 'Go to Facebook', 'lingam' ); ?></a>
                                </div>
                                
                                <div class="wpkoi-review">
                                	<h3><?php esc_html_e( 'Help with You review', 'lingam' ); ?></h3>
                                	<p><?php esc_html_e( 'If You like Lingam theme, show it to the world with Your review. Your feedback helps a lot.', 'lingam' ); ?></p>
                                    <a href="<?php echo esc_url(LINGAM_WORDPRESS_REVIEW); ?>" class="wpkoi-admin-button" target="_blank"><?php esc_html_e( 'Add my review', 'lingam' ); ?></a>
                                </div>
							</div>
						</div>
					</div>
				</div>
			</div>
		</div>
		<?php
	}
}

if ( ! function_exists( 'lingam_admin_errors' ) ) {
	add_action( 'admin_notices', 'lingam_admin_errors' );
	/**
	 * Add our admin notices
	 *
	 */
	function lingam_admin_errors() {
		$screen = get_current_screen();

		if ( 'appearance_page_lingam-options' !== $screen->base ) {
			return;
		}

		if ( isset( $_GET['settings-updated'] ) && 'true' == $_GET['settings-updated'] ) {
			 add_settings_error( 'lingam-notices', 'true', esc_html__( 'Settings saved.', 'lingam' ), 'updated' );
		}

		if ( isset( $_GET['status'] ) && 'imported' == $_GET['status'] ) {
			 add_settings_error( 'lingam-notices', 'imported', esc_html__( 'Import successful.', 'lingam' ), 'updated' );
		}

		if ( isset( $_GET['status'] ) && 'reset' == $_GET['status'] ) {
			 add_settings_error( 'lingam-notices', 'reset', esc_html__( 'Settings removed.', 'lingam' ), 'updated' );
		}

		settings_errors( 'lingam-notices' );
	}
}
