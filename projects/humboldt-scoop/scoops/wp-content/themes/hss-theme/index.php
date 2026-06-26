<?php
/**
 * index.php — WordPress requires this file to exist.
 * All actual page rendering is handled by page.php.
 */
get_header();
?>

<div class="hss-page hss-section hss-container">
  <?php if ( have_posts() ) : while ( have_posts() ) : the_post(); ?>
    <h1 class="hss-title"><?php the_title(); ?></h1>
    <div><?php the_content(); ?></div>
  <?php endwhile; else : ?>
    <p>Nothing here yet.</p>
  <?php endif; ?>
</div>

<?php
get_footer();
