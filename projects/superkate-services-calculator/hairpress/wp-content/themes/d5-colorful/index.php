<?php 
/* 	COLORFUL Theme's Index Page to hsow Blog Posts
	Copyright: 2012-2017, D5 Creation, www.d5creation.com
	
	Since COLORFUL 1.0
*/

get_header(); ?>
<div id="content">
 <?php if (have_posts()) : while (have_posts()) : the_post();?>
<div <?php post_class(); ?> id="post-<?php the_ID(); ?>">
 <p class="postmetadataw"><?php esc_html_e('Posted by:', 'd5-colorful'); ?> <?php the_author_posts_link() ?> | on <?php the_time('F j, Y'); ?></p>
 <h2 class="post-title"><a href="<?php the_permalink(); ?>"><?php the_title();?></a></h2>
 <div class="content-ver-sep"> </div>
 <div class="entrytext">
 <?php the_post_thumbnail('thumbnail'); ?>
 <?php the_content('<p class="read-more">'. esc_html__('Read the rest of this page &raquo;', 'd5-colorful').'</p>'); ?>
 <div class="clear"> </div>
 <div class="up-bottom-border">
 <?php  wp_link_pages( array( 'before' => '<div class="page-link"><span>' . esc_html__('Pages:','d5-colorful') . '</span>', 'after' => '</div><br/>' ) ); ?>
 <p class="postmetadata"><?php esc_html_e('Posted in', 'd5-colorful'); ?> <?php the_category(', ') ?> | <?php edit_post_link(esc_html__('Edit', 'd5-colorful'), '', ' | '); ?>  <?php comments_popup_link(esc_html__('No Comments &#187;', 'd5-colorful'), esc_html__('1 Comment &#187;', 'd5-colorful'), esc_html__('% Comments &#187;'.'d5-colorful')); ?> <?php the_tags(esc_html__('Tags: ','d5-colorful'), ', ', '<br />'); ?></p>
 </div>
 </div></div>
 
 <?php endwhile; ?>

<div id="page-nav">
<div class="alignleft"><?php previous_posts_link(esc_html__('&laquo; Previous Entries','d5-colorful')) ?></div>
<div class="alignright"><?php next_posts_link(esc_html__('Next Entries &raquo;','d5-colorful'),'') ?></div>
</div>
  
 
 <?php else: ?>
 
 <h1 class="arc-post-title">Sorry, we couldn't find anything that matched your search.</h1>
		
<h1 class="page-title"><?php esc_html_e('Not Found', 'd5-colorful'); ?></h1>
<h3 class="arc-src"><span><?php esc_html_e('Apologies, but the page you requested could not be found. Perhaps searching will help', 'd5-colorful'); ?></span></h3>

<?php get_search_form(); ?>
<p><a href="<?php echo esc_url(home_url()); ?>" title="Browse the Home Page">&laquo; <?php esc_html_e('Or Return to the Home Page', 'd5-colorful'); ?></a></p><br /><br />
		 
 
<?php endif; ?>
 

</div>

<?php get_sidebar(); ?>
<?php get_footer(); ?>