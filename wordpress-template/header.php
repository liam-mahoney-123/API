<!DOCTYPE html>
<html <?php language_attributes(); ?>>
<head>
    <meta charset="<?php bloginfo('charset'); ?>">
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <link rel="profile" href="https://gmpg.org/xfn/11">
    
    <?php wp_head(); ?>
</head>

<body <?php body_class(); ?>>
<?php wp_body_open(); ?>

<div id="page" class="site">
    <header id="masthead" class="site-header">
        <div class="container">
            <div class="header-content">
                <div class="site-branding">
                    <?php
                    if (has_custom_logo()) {
                        the_custom_logo();
                    } else {
                        ?>
                        <a href="<?php echo esc_url(home_url('/')); ?>" class="site-logo" rel="home">
                            <?php 
                            $site_title = get_theme_mod('site_title', get_bloginfo('name'));
                            echo esc_html($site_title);
                            ?>
                        </a>
                        <?php
                    }
                    ?>
                </div>

                <nav id="site-navigation" class="main-nav">
                    <?php
                    wp_nav_menu(array(
                        'theme_location' => 'primary',
                        'menu_id'        => 'primary-menu',
                        'container'      => false,
                        'fallback_cb'    => 'modern_saas_landing_fallback_menu',
                    ));
                    ?>
                </nav>

                <!-- Mobile menu toggle (you can add mobile menu functionality) -->
                <button class="mobile-menu-toggle" style="display: none; background: none; border: none; font-size: 1.5rem; cursor: pointer;">
                    ☰
                </button>
            </div>
        </div>
    </header>

<?php
/**
 * Fallback menu for when no menu is assigned
 */
function modern_saas_landing_fallback_menu() {
    echo '<ul id="primary-menu">';
    echo '<li><a href="#features">Features</a></li>';
    echo '<li><a href="#pricing">Pricing</a></li>';
    echo '<li><a href="#contact">Contact</a></li>';
    echo '</ul>';
}
?>

