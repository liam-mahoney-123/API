<?php
/**
 * Template Name: Landing Page
 * 
 * Custom landing page template with additional sections
 *
 * @package Modern_SaaS_Landing
 */

get_header(); ?>

<main id="main" class="site-main">
    
    <!-- Hero Section -->
    <section class="hero-section">
        <div class="container">
            <div class="hero-content">
                <h1 class="hero-title typing-effect" data-speed="100">
                    <?php echo get_theme_mod('hero_title', 'Cross-Platform Notification System'); ?>
                </h1>
                <p class="hero-subtitle">
                    <?php echo get_theme_mod('hero_subtitle', 'Build a unified notification system that works seamlessly across Windows, Mac, iOS, Android, and web platforms.'); ?>
                </p>
                <div class="hero-cta">
                    <a href="<?php echo get_theme_mod('hero_cta_url', '#features'); ?>" class="btn btn-primary btn-magnetic">
                        <?php echo get_theme_mod('hero_cta_text', 'Get Started'); ?>
                    </a>
                    <a href="<?php echo get_theme_mod('hero_secondary_cta_url', '#demo'); ?>" class="btn btn-secondary">
                        <?php echo get_theme_mod('hero_secondary_cta_text', 'View Demo'); ?>
                    </a>
                </div>
            </div>
        </div>
        <div class="particle-background"></div>
    </section>

    <!-- Stats Section -->
    <section class="stats-section">
        <div class="container">
            <div class="stats-grid">
                <div class="stat-item">
                    <h3>99.9%</h3>
                    <p>Uptime Guarantee</p>
                </div>
                <div class="stat-item">
                    <h3>10M+</h3>
                    <p>Notifications Sent</p>
                </div>
                <div class="stat-item">
                    <h3>50ms</h3>
                    <p>Average Delivery Time</p>
                </div>
                <div class="stat-item">
                    <h3>24/7</h3>
                    <p>Support Available</p>
                </div>
            </div>
        </div>
    </section>

    <!-- Features Section -->
    <section id="features" class="features-section reveal-section">
        <div class="container">
            <div class="section-title reveal-child">
                <h2><?php echo get_theme_mod('features_title', 'Powerful Features'); ?></h2>
                <p><?php echo get_theme_mod('features_subtitle', 'Everything you need to build and deploy notifications across all platforms'); ?></p>
            </div>
            
            <div class="features-grid">
                <?php for ($i = 1; $i <= 6; $i++): ?>
                    <?php
                    $defaults = array(
                        1 => array('icon' => '🔔', 'title' => 'Cross-Platform Support', 'desc' => 'Send notifications to Windows, Mac, iOS, Android, and web browsers from a single API.'),
                        2 => array('icon' => '⚡', 'title' => 'Real-time Delivery', 'desc' => 'Lightning-fast notification delivery with guaranteed message ordering and delivery confirmation.'),
                        3 => array('icon' => '🎯', 'title' => 'Smart Targeting', 'desc' => 'Advanced user segmentation and targeting based on behavior, location, and preferences.'),
                        4 => array('icon' => '📊', 'title' => 'Analytics & Insights', 'desc' => 'Comprehensive analytics dashboard with delivery rates, engagement metrics, and performance insights.'),
                        5 => array('icon' => '🔒', 'title' => 'Enterprise Security', 'desc' => 'End-to-end encryption, compliance with GDPR, CCPA, and enterprise-grade security standards.'),
                        6 => array('icon' => '🚀', 'title' => 'Easy Integration', 'desc' => 'Simple REST API, SDKs for popular languages, and comprehensive documentation to get started in minutes.'),
                    );
                    
                    $icon = get_theme_mod("feature{$i}_icon", $defaults[$i]['icon']);
                    $title = get_theme_mod("feature{$i}_title", $defaults[$i]['title']);
                    $description = get_theme_mod("feature{$i}_description", $defaults[$i]['desc']);
                    ?>
                    <div class="feature-card tilt-card reveal-child floating-element">
                        <div class="feature-icon"><?php echo $icon; ?></div>
                        <h3><?php echo $title; ?></h3>
                        <p><?php echo $description; ?></p>
                    </div>
                <?php endfor; ?>
            </div>
        </div>
    </section>

    <!-- Demo Section -->
    <section id="demo" class="py-5" style="background: #f8fafc;">
        <div class="container">
            <div class="section-title text-center">
                <h2>See It In Action</h2>
                <p>Watch how easy it is to send notifications across all platforms</p>
            </div>
            
            <div style="max-width: 800px; margin: 3rem auto; background: white; border-radius: 12px; padding: 2rem; box-shadow: 0 10px 40px rgba(0,0,0,0.1);">
                <div style="background: #1a202c; color: #00ff00; padding: 1.5rem; border-radius: 8px; font-family: 'Courier New', monospace; font-size: 0.9rem; overflow-x: auto;">
                    <div style="margin-bottom: 1rem;">$ curl -X POST https://api.yournotificationservice.com/send \</div>
                    <div style="margin-left: 2rem; margin-bottom: 0.5rem;">-H "Authorization: Bearer YOUR_API_KEY" \</div>
                    <div style="margin-left: 2rem; margin-bottom: 0.5rem;">-H "Content-Type: application/json" \</div>
                    <div style="margin-left: 2rem; margin-bottom: 1rem;">-d '{</div>
                    <div style="margin-left: 4rem; margin-bottom: 0.5rem;">"title": "Welcome!",</div>
                    <div style="margin-left: 4rem; margin-bottom: 0.5rem;">"message": "Thanks for signing up",</div>
                    <div style="margin-left: 4rem; margin-bottom: 0.5rem;">"platforms": ["ios", "android", "web"],</div>
                    <div style="margin-left: 4rem; margin-bottom: 0.5rem;">"users": ["user123"]</div>
                    <div style="margin-left: 2rem; margin-bottom: 1rem;">}'</div>
                    <div style="color: #00ff00;">✓ Notification sent successfully to 3 platforms</div>
                </div>
                <div class="text-center mt-4">
                    <a href="#contact" class="btn btn-primary">Try It Now</a>
                    <a href="#" class="btn btn-secondary" style="margin-left: 1rem;">View Documentation</a>
                </div>
            </div>
        </div>
    </section>

    <!-- Testimonials Section -->
    <section class="testimonials-section">
        <div class="container">
            <div class="section-title text-center">
                <h2>What Our Customers Say</h2>
                <p>Join thousands of satisfied developers and businesses</p>
            </div>
            
            <div class="features-grid">
                <div class="testimonial-card">
                    <p class="testimonial-text">This notification system saved us months of development time. The cross-platform support is incredible!</p>
                    <div class="testimonial-author">Sarah Johnson</div>
                    <div class="testimonial-role">CTO, TechStart Inc.</div>
                </div>
                
                <div class="testimonial-card">
                    <p class="testimonial-text">The analytics dashboard gives us insights we never had before. Highly recommended for any serious app.</p>
                    <div class="testimonial-author">Mike Chen</div>
                    <div class="testimonial-role">Lead Developer, AppCorp</div>
                </div>
                
                <div class="testimonial-card">
                    <p class="testimonial-text">Easy integration, great documentation, and excellent support. Everything we needed in one package.</p>
                    <div class="testimonial-author">Emily Rodriguez</div>
                    <div class="testimonial-role">Product Manager, StartupXYZ</div>
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
                <?php for ($i = 1; $i <= 3; $i++): ?>
                    <?php
                    $plan_defaults = array(
                        1 => array('name' => 'Starter', 'price' => '$29', 'desc' => 'Perfect for small projects and startups', 'url' => '#contact'),
                        2 => array('name' => 'Professional', 'price' => '$99', 'desc' => 'Ideal for growing businesses', 'url' => '#contact'),
                        3 => array('name' => 'Enterprise', 'price' => 'Custom', 'desc' => 'For large-scale deployments', 'url' => '#contact'),
                    );
                    
                    $name = get_theme_mod("plan{$i}_name", $plan_defaults[$i]['name']);
                    $price = get_theme_mod("plan{$i}_price", $plan_defaults[$i]['price']);
                    $description = get_theme_mod("plan{$i}_description", $plan_defaults[$i]['desc']);
                    $url = get_theme_mod("plan{$i}_cta_url", $plan_defaults[$i]['url']);
                    
                    $popular_class = ($i == 2) ? 'pricing-popular' : '';
                    ?>
                    <div class="feature-card <?php echo $popular_class; ?>">
                        <h3><?php echo $name; ?></h3>
                        <div style="font-size: 2.5rem; font-weight: bold; color: #667eea; margin: 1rem 0;">
                            <?php echo $price; ?><?php if ($i < 3): ?><span style="font-size: 1rem; color: #666;">/month</span><?php endif; ?>
                        </div>
                        <p><?php echo $description; ?></p>
                        <ul style="text-align: left; margin: 1.5rem 0;">
                            <?php if ($i == 1): ?>
                                <li>✓ Up to 10,000 notifications/month</li>
                                <li>✓ All platforms supported</li>
                                <li>✓ Basic analytics</li>
                                <li>✓ Email support</li>
                            <?php elseif ($i == 2): ?>
                                <li>✓ Up to 100,000 notifications/month</li>
                                <li>✓ Advanced targeting & segmentation</li>
                                <li>✓ Detailed analytics & reporting</li>
                                <li>✓ Priority support</li>
                                <li>✓ Custom integrations</li>
                            <?php else: ?>
                                <li>✓ Unlimited notifications</li>
                                <li>✓ White-label solution</li>
                                <li>✓ Dedicated support team</li>
                                <li>✓ SLA guarantees</li>
                                <li>✓ Custom development</li>
                            <?php endif; ?>
                        </ul>
                        <a href="<?php echo $url; ?>" class="btn <?php echo ($i == 2) ? 'btn-primary' : 'btn-secondary'; ?>">
                            <?php echo ($i == 3) ? 'Contact Sales' : 'Get Started'; ?>
                        </a>
                    </div>
                <?php endfor; ?>
            </div>
        </div>
    </section>

    <!-- FAQ Section -->
    <section class="faq-section">
        <div class="container">
            <div class="section-title text-center">
                <h2>Frequently Asked Questions</h2>
                <p>Get answers to common questions about our notification system</p>
            </div>
            
            <div style="max-width: 800px; margin: 0 auto;">
                <div class="faq-item">
                    <h4 class="faq-question">How quickly can I integrate the notification system?</h4>
                    <div class="faq-answer">
                        <p>Most developers can integrate our system in under 30 minutes using our comprehensive SDKs and documentation. We provide code examples for all major programming languages.</p>
                    </div>
                </div>
                
                <div class="faq-item">
                    <h4 class="faq-question">Do you support all mobile platforms?</h4>
                    <div class="faq-answer">
                        <p>Yes! We support iOS, Android, Windows, macOS, and web browsers. Our unified API handles all platform-specific requirements automatically.</p>
                    </div>
                </div>
                
                <div class="faq-item">
                    <h4 class="faq-question">What about data privacy and security?</h4>
                    <div class="faq-answer">
                        <p>We take security seriously. All data is encrypted in transit and at rest, and we're compliant with GDPR, CCPA, and other privacy regulations. We never share your data with third parties.</p>
                    </div>
                </div>
                
                <div class="faq-item">
                    <h4 class="faq-question">Can I customize the notification appearance?</h4>
                    <div class="faq-answer">
                        <p>Absolutely! You can customize colors, icons, sounds, and even create rich notifications with images and action buttons. Our API gives you full control over the user experience.</p>
                    </div>
                </div>
                
                <div class="faq-item">
                    <h4 class="faq-question">What kind of analytics do you provide?</h4>
                    <div class="faq-answer">
                        <p>Our analytics dashboard shows delivery rates, open rates, click-through rates, and user engagement metrics. You can also export data and integrate with your existing analytics tools.</p>
                    </div>
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
                <a href="<?php echo get_theme_mod('cta_button_url', '#contact'); ?>" class="btn btn-primary btn-magnetic">
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

