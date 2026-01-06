<?php
/**
 * WordPress Customizer Integration
 *
 * @package Modern_SaaS_Landing
 */

// Prevent direct access
if (!defined('ABSPATH')) {
    exit;
}

/**
 * Add customizer settings
 */
function modern_saas_landing_customize_register($wp_customize) {
    
    // ===== SITE IDENTITY SECTION =====
    $wp_customize->add_setting('site_title', array(
        'default' => get_bloginfo('name'),
        'sanitize_callback' => 'sanitize_text_field',
    ));
    
    $wp_customize->add_control('site_title', array(
        'label' => __('Site Title', 'modern-saas-landing'),
        'section' => 'title_tagline',
        'type' => 'text',
    ));

    // ===== COLORS SECTION =====
    $wp_customize->add_section('colors_section', array(
        'title' => __('Theme Colors', 'modern-saas-landing'),
        'priority' => 30,
    ));

    // Primary Color
    $wp_customize->add_setting('primary_color', array(
        'default' => '#667eea',
        'sanitize_callback' => 'sanitize_hex_color',
    ));

    $wp_customize->add_control(new WP_Customize_Color_Control($wp_customize, 'primary_color', array(
        'label' => __('Primary Color', 'modern-saas-landing'),
        'section' => 'colors_section',
        'settings' => 'primary_color',
    )));

    // Secondary Color
    $wp_customize->add_setting('secondary_color', array(
        'default' => '#764ba2',
        'sanitize_callback' => 'sanitize_hex_color',
    ));

    $wp_customize->add_control(new WP_Customize_Color_Control($wp_customize, 'secondary_color', array(
        'label' => __('Secondary Color', 'modern-saas-landing'),
        'section' => 'colors_section',
        'settings' => 'secondary_color',
    )));

    // ===== HERO SECTION =====
    $wp_customize->add_section('hero_section', array(
        'title' => __('Hero Section', 'modern-saas-landing'),
        'priority' => 35,
    ));

    // Hero Title
    $wp_customize->add_setting('hero_title', array(
        'default' => 'Cross-Platform Notification System',
        'sanitize_callback' => 'sanitize_text_field',
    ));

    $wp_customize->add_control('hero_title', array(
        'label' => __('Hero Title', 'modern-saas-landing'),
        'section' => 'hero_section',
        'type' => 'text',
    ));

    // Hero Subtitle
    $wp_customize->add_setting('hero_subtitle', array(
        'default' => 'Build a unified notification system that works seamlessly across Windows, Mac, iOS, Android, and web platforms.',
        'sanitize_callback' => 'sanitize_textarea_field',
    ));

    $wp_customize->add_control('hero_subtitle', array(
        'label' => __('Hero Subtitle', 'modern-saas-landing'),
        'section' => 'hero_section',
        'type' => 'textarea',
    ));

    // Hero CTA Button Text
    $wp_customize->add_setting('hero_cta_text', array(
        'default' => 'Get Started',
        'sanitize_callback' => 'sanitize_text_field',
    ));

    $wp_customize->add_control('hero_cta_text', array(
        'label' => __('Primary Button Text', 'modern-saas-landing'),
        'section' => 'hero_section',
        'type' => 'text',
    ));

    // Hero CTA Button URL
    $wp_customize->add_setting('hero_cta_url', array(
        'default' => '#features',
        'sanitize_callback' => 'esc_url_raw',
    ));

    $wp_customize->add_control('hero_cta_url', array(
        'label' => __('Primary Button URL', 'modern-saas-landing'),
        'section' => 'hero_section',
        'type' => 'url',
    ));

    // Hero Secondary CTA Button Text
    $wp_customize->add_setting('hero_secondary_cta_text', array(
        'default' => 'View Demo',
        'sanitize_callback' => 'sanitize_text_field',
    ));

    $wp_customize->add_control('hero_secondary_cta_text', array(
        'label' => __('Secondary Button Text', 'modern-saas-landing'),
        'section' => 'hero_section',
        'type' => 'text',
    ));

    // Hero Secondary CTA Button URL
    $wp_customize->add_setting('hero_secondary_cta_url', array(
        'default' => '#demo',
        'sanitize_callback' => 'esc_url_raw',
    ));

    $wp_customize->add_control('hero_secondary_cta_url', array(
        'label' => __('Secondary Button URL', 'modern-saas-landing'),
        'section' => 'hero_section',
        'type' => 'url',
    ));

    // ===== FEATURES SECTION =====
    $wp_customize->add_section('features_section', array(
        'title' => __('Features Section', 'modern-saas-landing'),
        'priority' => 40,
    ));

    // Features Title
    $wp_customize->add_setting('features_title', array(
        'default' => 'Powerful Features',
        'sanitize_callback' => 'sanitize_text_field',
    ));

    $wp_customize->add_control('features_title', array(
        'label' => __('Features Section Title', 'modern-saas-landing'),
        'section' => 'features_section',
        'type' => 'text',
    ));

    // Features Subtitle
    $wp_customize->add_setting('features_subtitle', array(
        'default' => 'Everything you need to build and deploy notifications across all platforms',
        'sanitize_callback' => 'sanitize_textarea_field',
    ));

    $wp_customize->add_control('features_subtitle', array(
        'label' => __('Features Section Subtitle', 'modern-saas-landing'),
        'section' => 'features_section',
        'type' => 'textarea',
    ));

    // Feature 1
    for ($i = 1; $i <= 6; $i++) {
        $defaults = array(
            1 => array('icon' => '🔔', 'title' => 'Cross-Platform Support', 'desc' => 'Send notifications to Windows, Mac, iOS, Android, and web browsers from a single API.'),
            2 => array('icon' => '⚡', 'title' => 'Real-time Delivery', 'desc' => 'Lightning-fast notification delivery with guaranteed message ordering and delivery confirmation.'),
            3 => array('icon' => '🎯', 'title' => 'Smart Targeting', 'desc' => 'Advanced user segmentation and targeting based on behavior, location, and preferences.'),
            4 => array('icon' => '📊', 'title' => 'Analytics & Insights', 'desc' => 'Comprehensive analytics dashboard with delivery rates, engagement metrics, and performance insights.'),
            5 => array('icon' => '🔒', 'title' => 'Enterprise Security', 'desc' => 'End-to-end encryption, compliance with GDPR, CCPA, and enterprise-grade security standards.'),
            6 => array('icon' => '🚀', 'title' => 'Easy Integration', 'desc' => 'Simple REST API, SDKs for popular languages, and comprehensive documentation to get started in minutes.'),
        );

        // Feature Icon
        $wp_customize->add_setting("feature{$i}_icon", array(
            'default' => $defaults[$i]['icon'],
            'sanitize_callback' => 'sanitize_text_field',
        ));

        $wp_customize->add_control("feature{$i}_icon", array(
            'label' => sprintf(__('Feature %d Icon', 'modern-saas-landing'), $i),
            'section' => 'features_section',
            'type' => 'text',
            'description' => __('Use emoji or text for the icon', 'modern-saas-landing'),
        ));

        // Feature Title
        $wp_customize->add_setting("feature{$i}_title", array(
            'default' => $defaults[$i]['title'],
            'sanitize_callback' => 'sanitize_text_field',
        ));

        $wp_customize->add_control("feature{$i}_title", array(
            'label' => sprintf(__('Feature %d Title', 'modern-saas-landing'), $i),
            'section' => 'features_section',
            'type' => 'text',
        ));

        // Feature Description
        $wp_customize->add_setting("feature{$i}_description", array(
            'default' => $defaults[$i]['desc'],
            'sanitize_callback' => 'sanitize_textarea_field',
        ));

        $wp_customize->add_control("feature{$i}_description", array(
            'label' => sprintf(__('Feature %d Description', 'modern-saas-landing'), $i),
            'section' => 'features_section',
            'type' => 'textarea',
        ));
    }

    // ===== PRICING SECTION =====
    $wp_customize->add_section('pricing_section', array(
        'title' => __('Pricing Section', 'modern-saas-landing'),
        'priority' => 45,
    ));

    // Pricing Title
    $wp_customize->add_setting('pricing_title', array(
        'default' => 'Simple, Transparent Pricing',
        'sanitize_callback' => 'sanitize_text_field',
    ));

    $wp_customize->add_control('pricing_title', array(
        'label' => __('Pricing Section Title', 'modern-saas-landing'),
        'section' => 'pricing_section',
        'type' => 'text',
    ));

    // Pricing Subtitle
    $wp_customize->add_setting('pricing_subtitle', array(
        'default' => 'Choose the plan that fits your needs',
        'sanitize_callback' => 'sanitize_textarea_field',
    ));

    $wp_customize->add_control('pricing_subtitle', array(
        'label' => __('Pricing Section Subtitle', 'modern-saas-landing'),
        'section' => 'pricing_section',
        'type' => 'textarea',
    ));

    // Pricing Plans
    $plan_defaults = array(
        1 => array('name' => 'Starter', 'price' => '$29', 'desc' => 'Perfect for small projects and startups', 'url' => '#contact'),
        2 => array('name' => 'Professional', 'price' => '$99', 'desc' => 'Ideal for growing businesses', 'url' => '#contact'),
        3 => array('name' => 'Enterprise', 'price' => 'Custom', 'desc' => 'For large-scale deployments', 'url' => '#contact'),
    );

    for ($i = 1; $i <= 3; $i++) {
        // Plan Name
        $wp_customize->add_setting("plan{$i}_name", array(
            'default' => $plan_defaults[$i]['name'],
            'sanitize_callback' => 'sanitize_text_field',
        ));

        $wp_customize->add_control("plan{$i}_name", array(
            'label' => sprintf(__('Plan %d Name', 'modern-saas-landing'), $i),
            'section' => 'pricing_section',
            'type' => 'text',
        ));

        // Plan Price
        $wp_customize->add_setting("plan{$i}_price", array(
            'default' => $plan_defaults[$i]['price'],
            'sanitize_callback' => 'sanitize_text_field',
        ));

        $wp_customize->add_control("plan{$i}_price", array(
            'label' => sprintf(__('Plan %d Price', 'modern-saas-landing'), $i),
            'section' => 'pricing_section',
            'type' => 'text',
        ));

        // Plan Description
        $wp_customize->add_setting("plan{$i}_description", array(
            'default' => $plan_defaults[$i]['desc'],
            'sanitize_callback' => 'sanitize_textarea_field',
        ));

        $wp_customize->add_control("plan{$i}_description", array(
            'label' => sprintf(__('Plan %d Description', 'modern-saas-landing'), $i),
            'section' => 'pricing_section',
            'type' => 'textarea',
        ));

        // Plan CTA URL
        $wp_customize->add_setting("plan{$i}_cta_url", array(
            'default' => $plan_defaults[$i]['url'],
            'sanitize_callback' => 'esc_url_raw',
        ));

        $wp_customize->add_control("plan{$i}_cta_url", array(
            'label' => sprintf(__('Plan %d Button URL', 'modern-saas-landing'), $i),
            'section' => 'pricing_section',
            'type' => 'url',
        ));
    }

    // ===== CTA SECTION =====
    $wp_customize->add_section('cta_section', array(
        'title' => __('Call to Action Section', 'modern-saas-landing'),
        'priority' => 50,
    ));

    // CTA Title
    $wp_customize->add_setting('cta_title', array(
        'default' => 'Ready to Get Started?',
        'sanitize_callback' => 'sanitize_text_field',
    ));

    $wp_customize->add_control('cta_title', array(
        'label' => __('CTA Title', 'modern-saas-landing'),
        'section' => 'cta_section',
        'type' => 'text',
    ));

    // CTA Subtitle
    $wp_customize->add_setting('cta_subtitle', array(
        'default' => 'Join thousands of developers who trust our notification system',
        'sanitize_callback' => 'sanitize_textarea_field',
    ));

    $wp_customize->add_control('cta_subtitle', array(
        'label' => __('CTA Subtitle', 'modern-saas-landing'),
        'section' => 'cta_section',
        'type' => 'textarea',
    ));

    // CTA Button Text
    $wp_customize->add_setting('cta_button_text', array(
        'default' => 'Start Free Trial',
        'sanitize_callback' => 'sanitize_text_field',
    ));

    $wp_customize->add_control('cta_button_text', array(
        'label' => __('CTA Button Text', 'modern-saas-landing'),
        'section' => 'cta_section',
        'type' => 'text',
    ));

    // CTA Button URL
    $wp_customize->add_setting('cta_button_url', array(
        'default' => '#contact',
        'sanitize_callback' => 'esc_url_raw',
    ));

    $wp_customize->add_control('cta_button_url', array(
        'label' => __('CTA Button URL', 'modern-saas-landing'),
        'section' => 'cta_section',
        'type' => 'url',
    ));

    // ===== CONTACT SECTION =====
    $wp_customize->add_section('contact_section', array(
        'title' => __('Contact Section', 'modern-saas-landing'),
        'priority' => 55,
    ));

    // Contact Title
    $wp_customize->add_setting('contact_title', array(
        'default' => 'Get in Touch',
        'sanitize_callback' => 'sanitize_text_field',
    ));

    $wp_customize->add_control('contact_title', array(
        'label' => __('Contact Title', 'modern-saas-landing'),
        'section' => 'contact_section',
        'type' => 'text',
    ));

    // Contact Subtitle
    $wp_customize->add_setting('contact_subtitle', array(
        'default' => 'Have questions? We\'d love to hear from you.',
        'sanitize_callback' => 'sanitize_textarea_field',
    ));

    $wp_customize->add_control('contact_subtitle', array(
        'label' => __('Contact Subtitle', 'modern-saas-landing'),
        'section' => 'contact_section',
        'type' => 'textarea',
    ));

    // Contact Email
    $wp_customize->add_setting('contact_email', array(
        'default' => 'hello@yoursite.com',
        'sanitize_callback' => 'sanitize_email',
    ));

    $wp_customize->add_control('contact_email', array(
        'label' => __('Contact Email', 'modern-saas-landing'),
        'section' => 'contact_section',
        'type' => 'email',
    ));

    // Contact Phone
    $wp_customize->add_setting('contact_phone', array(
        'default' => '+1 (555) 123-4567',
        'sanitize_callback' => 'sanitize_text_field',
    ));

    $wp_customize->add_control('contact_phone', array(
        'label' => __('Contact Phone', 'modern-saas-landing'),
        'section' => 'contact_section',
        'type' => 'text',
    ));

    // ===== FOOTER SECTION =====
    $wp_customize->add_section('footer_section', array(
        'title' => __('Footer Settings', 'modern-saas-landing'),
        'priority' => 60,
    ));

    // Footer Section Titles
    for ($i = 1; $i <= 4; $i++) {
        $defaults = array(
            1 => 'Product',
            2 => 'Company', 
            3 => 'Support',
            4 => 'Connect'
        );

        $wp_customize->add_setting("footer_section{$i}_title", array(
            'default' => $defaults[$i],
            'sanitize_callback' => 'sanitize_text_field',
        ));

        $wp_customize->add_control("footer_section{$i}_title", array(
            'label' => sprintf(__('Footer Section %d Title', 'modern-saas-landing'), $i),
            'section' => 'footer_section',
            'type' => 'text',
        ));
    }

    // Social Media Links
    $social_platforms = array(
        'twitter' => 'Twitter URL',
        'linkedin' => 'LinkedIn URL',
        'github' => 'GitHub URL',
    );

    foreach ($social_platforms as $platform => $label) {
        $wp_customize->add_setting("social_{$platform}", array(
            'default' => '',
            'sanitize_callback' => 'esc_url_raw',
        ));

        $wp_customize->add_control("social_{$platform}", array(
            'label' => __($label, 'modern-saas-landing'),
            'section' => 'footer_section',
            'type' => 'url',
        ));
    }

    // Copyright Text
    $wp_customize->add_setting('copyright_text', array(
        'default' => '© ' . date('Y') . ' ' . get_bloginfo('name') . '. All rights reserved.',
        'sanitize_callback' => 'sanitize_text_field',
    ));

    $wp_customize->add_control('copyright_text', array(
        'label' => __('Copyright Text', 'modern-saas-landing'),
        'section' => 'footer_section',
        'type' => 'text',
    ));

    // Footer Tagline
    $wp_customize->add_setting('footer_tagline', array(
        'default' => 'Built with ❤️ using Modern SaaS Landing Theme',
        'sanitize_callback' => 'sanitize_text_field',
    ));

    $wp_customize->add_control('footer_tagline', array(
        'label' => __('Footer Tagline', 'modern-saas-landing'),
        'section' => 'footer_section',
        'type' => 'text',
    ));

    // ===== TYPOGRAPHY SECTION =====
    $wp_customize->add_section('typography_section', array(
        'title' => __('Typography', 'modern-saas-landing'),
        'priority' => 65,
    ));

    // Custom Font
    $wp_customize->add_setting('custom_font', array(
        'default' => '',
        'sanitize_callback' => 'sanitize_text_field',
    ));

    $wp_customize->add_control('custom_font', array(
        'label' => __('Custom Font Family', 'modern-saas-landing'),
        'section' => 'typography_section',
        'type' => 'text',
        'description' => __('Enter a Google Font name (e.g., "Roboto", "Open Sans"). Leave empty to use default.', 'modern-saas-landing'),
    ));
}
add_action('customize_register', 'modern_saas_landing_customize_register');

/**
 * Enqueue Google Fonts based on customizer selection
 */
function modern_saas_landing_custom_fonts() {
    $custom_font = get_theme_mod('custom_font', '');
    if (!empty($custom_font)) {
        $font_url = 'https://fonts.googleapis.com/css2?family=' . urlencode($custom_font) . ':wght@300;400;500;600;700&display=swap';
        wp_enqueue_style('custom-google-font', $font_url, array(), null);
    }
}
add_action('wp_enqueue_scripts', 'modern_saas_landing_custom_fonts');
?>

