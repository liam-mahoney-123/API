<?php
/**
 * Modern SaaS Landing Theme Functions
 *
 * @package Modern_SaaS_Landing
 */

// Prevent direct access
if (!defined('ABSPATH')) {
    exit;
}

/**
 * Theme setup
 */
function modern_saas_landing_setup() {
    // Add theme support for various features
    add_theme_support('title-tag');
    add_theme_support('post-thumbnails');
    add_theme_support('html5', array(
        'search-form',
        'comment-form',
        'comment-list',
        'gallery',
        'caption',
    ));
    add_theme_support('customize-selective-refresh-widgets');
    
    // Register navigation menus
    register_nav_menus(array(
        'primary' => esc_html__('Primary Menu', 'modern-saas-landing'),
        'footer' => esc_html__('Footer Menu', 'modern-saas-landing'),
    ));
}
add_action('after_setup_theme', 'modern_saas_landing_setup');

/**
 * Enqueue scripts and styles
 */
function modern_saas_landing_scripts() {
    // Enqueue Google Fonts
    wp_enqueue_style('google-fonts', 'https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap', array(), null);
    
    // Enqueue theme stylesheet
    wp_enqueue_style('modern-saas-landing-style', get_stylesheet_uri(), array(), '1.0.0');
    
    // Enqueue custom CSS
    wp_enqueue_style('modern-saas-landing-main', get_template_directory_uri() . '/assets/css/main.css', array(), '1.0.0');
    
    // Enqueue JavaScript
    wp_enqueue_script('modern-saas-landing-main', get_template_directory_uri() . '/assets/js/main.js', array('jquery'), '1.0.0', true);
    
    // Enqueue animations
    wp_enqueue_script('modern-saas-landing-animations', get_template_directory_uri() . '/assets/js/animations.js', array('jquery'), '1.0.0', true);
}
add_action('wp_enqueue_scripts', 'modern_saas_landing_scripts');

/**
 * Include customizer file
 */
require get_template_directory() . '/inc/customizer.php';

/**
 * Widget areas
 */
function modern_saas_landing_widgets_init() {
    register_sidebar(array(
        'name'          => esc_html__('Footer Widget Area 1', 'modern-saas-landing'),
        'id'            => 'footer-1',
        'description'   => esc_html__('Add widgets here to appear in the first footer column.', 'modern-saas-landing'),
        'before_widget' => '<div id="%1$s" class="widget %2$s">',
        'after_widget'  => '</div>',
        'before_title'  => '<h4 class="widget-title">',
        'after_title'   => '</h4>',
    ));
    
    register_sidebar(array(
        'name'          => esc_html__('Footer Widget Area 2', 'modern-saas-landing'),
        'id'            => 'footer-2',
        'description'   => esc_html__('Add widgets here to appear in the second footer column.', 'modern-saas-landing'),
        'before_widget' => '<div id="%1$s" class="widget %2$s">',
        'after_widget'  => '</div>',
        'before_title'  => '<h4 class="widget-title">',
        'after_title'   => '</h4>',
    ));
    
    register_sidebar(array(
        'name'          => esc_html__('Footer Widget Area 3', 'modern-saas-landing'),
        'id'            => 'footer-3',
        'description'   => esc_html__('Add widgets here to appear in the third footer column.', 'modern-saas-landing'),
        'before_widget' => '<div id="%1$s" class="widget %2$s">',
        'after_widget'  => '</div>',
        'before_title'  => '<h4 class="widget-title">',
        'after_title'   => '</h4>',
    ));
}
add_action('widgets_init', 'modern_saas_landing_widgets_init');

/**
 * Custom excerpt length
 */
function modern_saas_landing_excerpt_length($length) {
    return 20;
}
add_filter('excerpt_length', 'modern_saas_landing_excerpt_length');

/**
 * Custom excerpt more
 */
function modern_saas_landing_excerpt_more($more) {
    return '...';
}
add_filter('excerpt_more', 'modern_saas_landing_excerpt_more');

/**
 * Add custom CSS for theme customizations
 */
function modern_saas_landing_custom_css() {
    $custom_css = '';
    
    // Primary color customization
    $primary_color = get_theme_mod('primary_color', '#667eea');
    if ($primary_color !== '#667eea') {
        $custom_css .= "
        .btn-primary, .feature-icon {
            background: {$primary_color} !important;
        }
        .btn-secondary {
            color: {$primary_color} !important;
            border-color: {$primary_color} !important;
        }
        .btn-secondary:hover {
            background: {$primary_color} !important;
        }
        .main-nav a:hover {
            color: {$primary_color} !important;
        }
        ";
    }
    
    // Secondary color customization
    $secondary_color = get_theme_mod('secondary_color', '#764ba2');
    if ($secondary_color !== '#764ba2') {
        $custom_css .= "
        .hero-section, .cta-section {
            background: linear-gradient(135deg, {$primary_color} 0%, {$secondary_color} 100%) !important;
        }
        ";
    }
    
    // Custom font
    $custom_font = get_theme_mod('custom_font', '');
    if (!empty($custom_font)) {
        $custom_css .= "
        body {
            font-family: '{$custom_font}', -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif !important;
        }
        ";
    }
    
    if (!empty($custom_css)) {
        wp_add_inline_style('modern-saas-landing-style', $custom_css);
    }
}
add_action('wp_enqueue_scripts', 'modern_saas_landing_custom_css');

/**
 * Add admin styles for better customizer experience
 */
function modern_saas_landing_admin_styles() {
    wp_enqueue_style('modern-saas-landing-admin', get_template_directory_uri() . '/assets/css/admin.css', array(), '1.0.0');
}
add_action('admin_enqueue_scripts', 'modern_saas_landing_admin_styles');

/**
 * Add support for Gutenberg editor styles
 */
function modern_saas_landing_editor_styles() {
    add_theme_support('editor-styles');
    add_editor_style('assets/css/editor-style.css');
}
add_action('after_setup_theme', 'modern_saas_landing_editor_styles');

/**
 * Custom logo setup
 */
function modern_saas_landing_custom_logo_setup() {
    $defaults = array(
        'height'      => 50,
        'width'       => 200,
        'flex-height' => true,
        'flex-width'  => true,
        'header-text' => array('site-title', 'site-description'),
    );
    add_theme_support('custom-logo', $defaults);
}
add_action('after_setup_theme', 'modern_saas_landing_custom_logo_setup');

/**
 * Security enhancements
 */
function modern_saas_landing_security() {
    // Remove WordPress version from head
    remove_action('wp_head', 'wp_generator');
    
    // Remove RSD link
    remove_action('wp_head', 'rsd_link');
    
    // Remove wlwmanifest.xml
    remove_action('wp_head', 'wlwmanifest_link');
    
    // Remove shortlink
    remove_action('wp_head', 'wp_shortlink_wp_head');
}
add_action('init', 'modern_saas_landing_security');

/**
 * Optimize performance
 */
function modern_saas_landing_performance() {
    // Remove emoji scripts
    remove_action('wp_head', 'print_emoji_detection_script', 7);
    remove_action('wp_print_styles', 'print_emoji_styles');
    remove_action('admin_print_scripts', 'print_emoji_detection_script');
    remove_action('admin_print_styles', 'print_emoji_styles');
    
    // Remove jQuery migrate
    function remove_jquery_migrate($scripts) {
        if (!is_admin() && isset($scripts->registered['jquery'])) {
            $script = $scripts->registered['jquery'];
            if ($script->deps) {
                $script->deps = array_diff($script->deps, array('jquery-migrate'));
            }
        }
    }
    add_action('wp_default_scripts', 'remove_jquery_migrate');
}
add_action('init', 'modern_saas_landing_performance');

/**
 * Add schema markup for better SEO
 */
function modern_saas_landing_schema_markup() {
    if (is_front_page()) {
        $schema = array(
            '@context' => 'https://schema.org',
            '@type' => 'Organization',
            'name' => get_bloginfo('name'),
            'description' => get_bloginfo('description'),
            'url' => home_url(),
        );
        
        if (has_custom_logo()) {
            $custom_logo_id = get_theme_mod('custom_logo');
            $logo = wp_get_attachment_image_src($custom_logo_id, 'full');
            if ($logo) {
                $schema['logo'] = $logo[0];
            }
        }
        
        echo '<script type="application/ld+json">' . json_encode($schema) . '</script>';
    }
}
add_action('wp_head', 'modern_saas_landing_schema_markup');

/**
 * Add custom post types for testimonials (optional)
 */
function modern_saas_landing_custom_post_types() {
    // Testimonials post type
    register_post_type('testimonials', array(
        'labels' => array(
            'name' => 'Testimonials',
            'singular_name' => 'Testimonial',
            'add_new' => 'Add New Testimonial',
            'add_new_item' => 'Add New Testimonial',
            'edit_item' => 'Edit Testimonial',
            'new_item' => 'New Testimonial',
            'view_item' => 'View Testimonial',
            'search_items' => 'Search Testimonials',
            'not_found' => 'No testimonials found',
            'not_found_in_trash' => 'No testimonials found in trash'
        ),
        'public' => false,
        'show_ui' => true,
        'show_in_menu' => true,
        'show_in_admin_bar' => true,
        'menu_icon' => 'dashicons-format-quote',
        'supports' => array('title', 'editor', 'thumbnail'),
        'has_archive' => false,
    ));
}
add_action('init', 'modern_saas_landing_custom_post_types');
?>

