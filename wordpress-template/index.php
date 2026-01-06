<?php
/**
 * The main template file
 *
 * @package Modern_SaaS_Landing
 */

get_header(); ?>

<main id="main" class="site-main">
    
    <!-- Hero Section -->
    <section class="hero-section">
        <div class="container">
            <div class="hero-content">
                <h1 class="hero-title">
                    <?php echo get_theme_mod('hero_title', 'Cross-Platform Notification System'); ?>
                </h1>
                <p class="hero-subtitle">
                    <?php echo get_theme_mod('hero_subtitle', 'Build a unified notification system that works seamlessly across Windows, Mac, iOS, Android, and web platforms.'); ?>
                </p>
                <div class="hero-cta">
                    <a href="<?php echo get_theme_mod('hero_cta_url', '#features'); ?>" class="btn btn-primary">
                        <?php echo get_theme_mod('hero_cta_text', 'Get Started'); ?>
                    </a>
                    <a href="<?php echo get_theme_mod('hero_secondary_cta_url', '#demo'); ?>" class="btn btn-secondary">
                        <?php echo get_theme_mod('hero_secondary_cta_text', 'View Demo'); ?>
                    </a>
                </div>
            </div>
        </div>
    </section>

    <!-- Features Section -->
    <section id="features" class="features-section">
        <div class="container">
            <div class="section-title">
                <h2><?php echo get_theme_mod('features_title', 'Powerful Features'); ?></h2>
                <p><?php echo get_theme_mod('features_subtitle', 'Everything you need to build and deploy notifications across all platforms'); ?></p>
            </div>
            
            <div class="features-grid">
                <?php
                // Feature 1
                $feature1_icon = get_theme_mod('feature1_icon', '🔔');
                $feature1_title = get_theme_mod('feature1_title', 'Cross-Platform Support');
                $feature1_description = get_theme_mod('feature1_description', 'Send notifications to Windows, Mac, iOS, Android, and web browsers from a single API.');
                ?>
                <div class="feature-card">
                    <div class="feature-icon"><?php echo $feature1_icon; ?></div>
                    <h3><?php echo $feature1_title; ?></h3>
                    <p><?php echo $feature1_description; ?></p>
                </div>

                <?php
                // Feature 2
                $feature2_icon = get_theme_mod('feature2_icon', '⚡');
                $feature2_title = get_theme_mod('feature2_title', 'Real-time Delivery');
                $feature2_description = get_theme_mod('feature2_description', 'Lightning-fast notification delivery with guaranteed message ordering and delivery confirmation.');
                ?>
                <div class="feature-card">
                    <div class="feature-icon"><?php echo $feature2_icon; ?></div>
                    <h3><?php echo $feature2_title; ?></h3>
                    <p><?php echo $feature2_description; ?></p>
                </div>

                <?php
                // Feature 3
                $feature3_icon = get_theme_mod('feature3_icon', '🎯');
                $feature3_title = get_theme_mod('feature3_title', 'Smart Targeting');
                $feature3_description = get_theme_mod('feature3_description', 'Advanced user segmentation and targeting based on behavior, location, and preferences.');
                ?>
                <div class="feature-card">
                    <div class="feature-icon"><?php echo $feature3_icon; ?></div>
                    <h3><?php echo $feature3_title; ?></h3>
                    <p><?php echo $feature3_description; ?></p>
                </div>

                <?php
                // Feature 4
                $feature4_icon = get_theme_mod('feature4_icon', '📊');
                $feature4_title = get_theme_mod('feature4_title', 'Analytics & Insights');
                $feature4_description = get_theme_mod('feature4_description', 'Comprehensive analytics dashboard with delivery rates, engagement metrics, and performance insights.');
                ?>
                <div class="feature-card">
                    <div class="feature-icon"><?php echo $feature4_icon; ?></div>
                    <h3><?php echo $feature4_title; ?></h3>
                    <p><?php echo $feature4_description; ?></p>
                </div>

                <?php
                // Feature 5
                $feature5_icon = get_theme_mod('feature5_icon', '🔒');
                $feature5_title = get_theme_mod('feature5_title', 'Enterprise Security');
                $feature5_description = get_theme_mod('feature5_description', 'End-to-end encryption, compliance with GDPR, CCPA, and enterprise-grade security standards.');
                ?>
                <div class="feature-card">
                    <div class="feature-icon"><?php echo $feature5_icon; ?></div>
                    <h3><?php echo $feature5_title; ?></h3>
                    <p><?php echo $feature5_description; ?></p>
                </div>

                <?php
                // Feature 6
                $feature6_icon = get_theme_mod('feature6_icon', '🚀');
                $feature6_title = get_theme_mod('feature6_title', 'Easy Integration');
                $feature6_description = get_theme_mod('feature6_description', 'Simple REST API, SDKs for popular languages, and comprehensive documentation to get started in minutes.');
                ?>
                <div class="feature-card">
                    <div class="feature-icon"><?php echo $feature6_icon; ?></div>
                    <h3><?php echo $feature6_title; ?></h3>
                    <p><?php echo $feature6_description; ?></p>
                </div>
            </div>
        </div>
    </section>

    <!-- Pricing Section -->
    <section id="pricing" class="py-5">
        <div class="container">
            <div class="section-title text-center">
                <h2><?php echo get_theme_mod('pricing_title', 'Simple, Transparent Pricing'); ?></h2>
                <p><?php echo get_theme_mod('pricing_subtitle', 'Choose the plan that fits your needs'); ?></p>
            </div>
            
            <div class="features-grid">
                <!-- Starter Plan -->
                <div class="feature-card">
                    <h3><?php echo get_theme_mod('plan1_name', 'Starter'); ?></h3>
                    <div style="font-size: 2.5rem; font-weight: bold; color: #667eea; margin: 1rem 0;">
                        <?php echo get_theme_mod('plan1_price', '$29'); ?><span style="font-size: 1rem; color: #666;">/month</span>
                    </div>
                    <p><?php echo get_theme_mod('plan1_description', 'Perfect for small projects and startups'); ?></p>
                    <ul style="text-align: left; margin: 1.5rem 0;">
                        <li>✓ Up to 10,000 notifications/month</li>
                        <li>✓ All platforms supported</li>
                        <li>✓ Basic analytics</li>
                        <li>✓ Email support</li>
                    </ul>
                    <a href="<?php echo get_theme_mod('plan1_cta_url', '#contact'); ?>" class="btn btn-secondary">Get Started</a>
                </div>

                <!-- Professional Plan -->
                <div class="feature-card" style="border: 3px solid #667eea; position: relative;">
                    <div style="position: absolute; top: -15px; left: 50%; transform: translateX(-50%); background: #667eea; color: white; padding: 5px 20px; border-radius: 20px; font-size: 0.9rem;">Popular</div>
                    <h3><?php echo get_theme_mod('plan2_name', 'Professional'); ?></h3>
                    <div style="font-size: 2.5rem; font-weight: bold; color: #667eea; margin: 1rem 0;">
                        <?php echo get_theme_mod('plan2_price', '$99'); ?><span style="font-size: 1rem; color: #666;">/month</span>
                    </div>
                    <p><?php echo get_theme_mod('plan2_description', 'Ideal for growing businesses'); ?></p>
                    <ul style="text-align: left; margin: 1.5rem 0;">
                        <li>✓ Up to 100,000 notifications/month</li>
                        <li>✓ Advanced targeting & segmentation</li>
                        <li>✓ Detailed analytics & reporting</li>
                        <li>✓ Priority support</li>
                        <li>✓ Custom integrations</li>
                    </ul>
                    <a href="<?php echo get_theme_mod('plan2_cta_url', '#contact'); ?>" class="btn btn-primary">Get Started</a>
                </div>

                <!-- Enterprise Plan -->
                <div class="feature-card">
                    <h3><?php echo get_theme_mod('plan3_name', 'Enterprise'); ?></h3>
                    <div style="font-size: 2.5rem; font-weight: bold; color: #667eea; margin: 1rem 0;">
                        <?php echo get_theme_mod('plan3_price', 'Custom'); ?>
                    </div>
                    <p><?php echo get_theme_mod('plan3_description', 'For large-scale deployments'); ?></p>
                    <ul style="text-align: left; margin: 1.5rem 0;">
                        <li>✓ Unlimited notifications</li>
                        <li>✓ White-label solution</li>
                        <li>✓ Dedicated support team</li>
                        <li>✓ SLA guarantees</li>
                        <li>✓ Custom development</li>
                    </ul>
                    <a href="<?php echo get_theme_mod('plan3_cta_url', '#contact'); ?>" class="btn btn-secondary">Contact Sales</a>
                </div>
            </div>
        </div>
    </section>

    <!-- CTA Section -->
    <section class="cta-section">
        <div class="container">
            <h2><?php echo get_theme_mod('cta_title', 'Ready to Get Started?'); ?></h2>
            <p><?php echo get_theme_mod('cta_subtitle', 'Join thousands of developers who trust our notification system'); ?></p>
            <div class="mt-4">
                <a href="<?php echo get_theme_mod('cta_button_url', '#contact'); ?>" class="btn btn-primary">
                    <?php echo get_theme_mod('cta_button_text', 'Start Free Trial'); ?>
                </a>
            </div>
        </div>
    </section>

    <!-- Contact Section -->
    <section id="contact" class="py-5" style="background: #f8fafc;">
        <div class="container">
            <div class="section-title text-center">
                <h2><?php echo get_theme_mod('contact_title', 'Get in Touch'); ?></h2>
                <p><?php echo get_theme_mod('contact_subtitle', 'Have questions? We\'d love to hear from you.'); ?></p>
            </div>
            
            <div style="max-width: 600px; margin: 0 auto; background: white; padding: 3rem; border-radius: 12px; box-shadow: 0 4px 20px rgba(0,0,0,0.08);">
                <?php
                // Display contact form or contact information
                $contact_email = get_theme_mod('contact_email', 'hello@yoursite.com');
                $contact_phone = get_theme_mod('contact_phone', '+1 (555) 123-4567');
                ?>
                
                <div style="text-align: center;">
                    <div style="margin-bottom: 2rem;">
                        <h4>📧 Email</h4>
                        <a href="mailto:<?php echo $contact_email; ?>" style="color: #667eea; text-decoration: none; font-size: 1.1rem;"><?php echo $contact_email; ?></a>
                    </div>
                    
                    <div style="margin-bottom: 2rem;">
                        <h4>📞 Phone</h4>
                        <a href="tel:<?php echo str_replace(['(', ')', ' ', '-'], '', $contact_phone); ?>" style="color: #667eea; text-decoration: none; font-size: 1.1rem;"><?php echo $contact_phone; ?></a>
                    </div>
                    
                    <div>
                        <h4>💬 Live Chat</h4>
                        <p>Available Monday - Friday, 9AM - 6PM EST</p>
                        <a href="#" class="btn btn-primary" onclick="alert('Live chat integration would go here!')">Start Chat</a>
                    </div>
                </div>
            </div>
        </div>
    </section>

</main>

<?php get_footer(); ?>

