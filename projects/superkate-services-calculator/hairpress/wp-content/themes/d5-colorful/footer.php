<?php
/* COLORFUL Theme's Footer
	Copyright: 2012-2017, D5 Creation, www.d5creation.com
	
	Since COLORFUL 1.0
*/
?>





<div id="footer">

<div id="footer-content">

<div id="footer-sidebar">
<?php
   	get_sidebar( 'footer' );
?>
</div>
<div id="creditline">&copy;&nbsp;<?php echo date("Y") ?>&nbsp;<?php bloginfo( 'name' ); echo '&nbsp| COLORFUL '.esc_html__('Theme by', 'd5-colorful') .': <a href="'.esc_url('https://d5creation.com').'" target="_blank">D5 Creation</a> |  '.esc_html__('Powered by', 'd5-colorful') .': <a href="http://wordpress.org" target="_blank">WordPress</a>' ?></div>

<?php wp_footer(); ?>
</div> <!-- footer-content -->
</div> <!-- footer -->
</div><!-- container -->
</body>
</html>