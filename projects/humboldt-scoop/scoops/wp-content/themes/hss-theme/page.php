<?php
/**
 * page.php — Full-width canvas page template.
 * No sidebar, no post title, no WP chrome. Just your blocks.
 */
get_header();
?>

<?php while ( have_posts() ) : the_post(); ?>
  <div class="hss-page">
    <?php the_content(); ?>
  </div>
<?php endwhile; ?>

<?php
get_footer();
