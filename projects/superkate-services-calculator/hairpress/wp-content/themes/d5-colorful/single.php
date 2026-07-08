<?php

/* 	COLORFUL Theme'sSingle Page to display Single Page or Post
	Copyright: 2012-2017, D5 Creation, www.d5creation.com
	Since COLORFUL 1.0
*/


get_header(); ?>

<div id="content">
          
		  <?php if ( have_posts() ) while ( have_posts() ) : the_post(); ?>
          
            <h1 class="page-title"><?php the_title(); ?></h1>
            <p class="postmetadataw"><?php esc_html_e('Posted by:', 'd5-colorful'); ?> <?php the_author_posts_link() ?> | on <?php the_time('F j, Y'); ?></p>
                        
            <div class="content-ver-sep"> </div>
            <div class="entrytext"><?php the_post_thumbnail('thumbnail'); ?>
			<?php the_content(); ?>
            </div>
            <div class="clear"> </div>
            <div class="up-bottom-border">
           <p class="postmetadata"><?php esc_html_e('Posted in', 'd5-colorful'); ?> <?php the_category(', ') ?> | <?php edit_post_link(esc_html__('Edit', 'd5-colorful'), '', ' | '); ?>  <?php comments_popup_link(esc_html__('No Comments &#187;', 'd5-colorful'), esc_html__('1 Comment &#187;', 'd5-colorful'), esc_html__('% Comments &#187;'.'d5-colorful')); ?> <?php the_tags(esc_html__('Tags: ','d5-colorful'), ', ', '<br />'); ?></p><br />
            <?php  wp_link_pages( array( 'before' => '<div class="page-link"><span>' . esc_html__('Pages:','d5-colorful') . '</span>', 'after' => '</div><br/>' ) ); ?>
            <div class="floatleft"><?php previous_post_link('&laquo; %link'); ?></div>
			<div class="floatright"><?php next_post_link('%link &raquo;'); ?></div><br /><br />
            <?php if ( is_attachment() ): ?>
            <div class="floatleft"><?php previous_image_link( false, esc_html__('&laquo; Previous Image','d5-colorful') ); ?></div>
			<div class="floatright"><?php next_image_link( false, esc_html__('Next Image &raquo;','d5-colorful') ); ?></div> 
            <?php endif; ?>
          	</div>
			
			<?php endwhile;?>
          	            
          <!-- End the Loop. -->          
        	
			<?php comments_template( '', true ); ?>
            
</div>			
<?php get_sidebar(); ?>
<?php get_footer(); ?>