<?php
$coolrestx_copyright = get_theme_mod('coolrestx_copyright');
$coolrestx_design    = get_theme_mod('coolrestx_design');
?>
<?php if ($coolrestx_copyright || $coolrestx_design) { ?>
    <div class="footer-bottom">

        <div class="container">

            <div class="row">
                <div class=" col-md-6 col-sm-12 col-xs-12">

                    <div class="copyright text-left">


                        <?php if (get_theme_mod('coolrestx_copyright')) { ?>
                            <?php echo esc_html($coolrestx_copyright); ?>
                        <?php } ?>         
                    </div><!--copyright-->

                </div>
                <div class=" col-md-6 col-sm-12 col-xs-12">

                    <div class="design text-right">

                        <?php if (get_theme_mod('coolrestx_design')) { ?>
                            <?php echo esc_html($coolrestx_design); ?>
                        <?php } ?>

                    </div><!--design-->

                </div><!--col-sm-6-->

                



            </div><!--row-->

        </div><!--container-->

    </div><!--footer-bottom-->
    <?php
}?>