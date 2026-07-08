<?php
/* COLORFUL Theme'sComments Area for Single Pages
	Copyright: 2012-2017, D5 Creation, www.d5creation.com
	
	Since COLORFUL 1.0
*/

	if ( post_password_required() ) {
		return;
	}
?>

<div id="commentsbox">
<?php if ( have_comments() ) : ?>
	<h2 class="comments"><?php comments_number(esc_html__('No Comments','d5-colorful'), esc_html__('One Comment','d5-colorful'), esc_html__('% Comments','d5-colorful') );?>to  <a href="<?php the_permalink(); ?>"><?php the_title();?></a></h2>
	<ol class="commentlist">
		<?php wp_list_comments(); ?>
	</ol>
    
	<div class="comment-nav">
		<div class="floatleft">
			<?php previous_comments_link() ?>
		</div>
		<div class="floatright">
			<?php next_comments_link() ?>
		</div>
	</div>
<?php else : ?>
	<?php if ( ! comments_open() && ! is_page() ) : ?>
		<p class="watermark"><?php echo esc_html__('Comments are Closed', 'd5-colorful'); ?></p>
	<?php endif; ?>
<?php endif; ?>
<?php if ( comments_open() ) : ?>
	<div id="comment-form">
		<?php comment_form(); ?>
	</div>
<?php endif; ?>
</div>