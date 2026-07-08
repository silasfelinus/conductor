<?php
/*
Plugin Name: Superkate's Special Plugin
Plugin URI: https://hairbysuperkate.com
Description: Admin tool for Hair by Superkate
Version: 0.0.1
Author: Silas Knight
License: GPL2
*/


function addAdminPageContent() {
    add_menu_page('superk8\'s Special Plugin', 'superk8\'s Special Plugin', 'manage_options', __FILE__, 'adminPageContent', 'dashicons-wordpress');
  }

function adminPageContent() {
    echo '<h2>superk8\'s Special Plugin</h2>Under Construction';
  }
  add_action('admin_menu', 'addAdminPageContent');
