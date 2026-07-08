<?php
/* COLORFUL Theme'sGeneral Page to display all Pages
	Copyright: 2012-2017, D5 Creation, www.d5creation.com
	
	Since COLORFUL 1.0
*/

 get_header(); ?>

	<div id="content">

		<?php if (have_posts()) : while (have_posts()) : the_post(); ?>
		<div <?php post_class(); ?> id="post-<?php the_ID(); ?>">
		<h1 class="page-title"><?php the_title(); ?></h1>
			<div class="content-ver-sep"> </div>
            <div class="entrytext">
 <?php the_post_thumbnail('thumbnail'); ?>
 <?php the_content('<p class="read-more">'. esc_html__('Read the rest of this page &raquo;', 'd5-colorful').'</p>'); ?>

				<?php wp_link_pages(array('before' => esc_html__('<p><strong>Pages:</strong> ','d5-colorful'), 'after' => '</p>', 'next_or_number' => 'number')); ?>

			</div>
		</div>
		<?php endwhile; ?><div class="clear"> </div>
	<?php edit_post_link(esc_html__('Edit This Entry','d5-colorful'), '<p>', '</p>'); ?>
	<?php comments_template('', true); ?>
	<?php else: ?>
		<p><?php esc_html_e('Sorry, no pages matched your criteria','d5-colorful'); ?></p>
	<?php endif; ?>
	</div>

<?php get_sidebar(); ?>

<?php get_footer(); ?>