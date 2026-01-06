    <footer id="colophon" class="site-footer">
        <div class="container">
            <div class="footer-content">
                <div class="footer-section">
                    <h4><?php echo get_theme_mod('footer_section1_title', 'Product'); ?></h4>
                    <?php
                    if (is_active_sidebar('footer-1')) {
                        dynamic_sidebar('footer-1');
                    } else {
                        // Default footer content
                        echo '<ul style="list-style: none; padding: 0;">';
                        echo '<li><a href="#features">Features</a></li>';
                        echo '<li><a href="#pricing">Pricing</a></li>';
                        echo '<li><a href="#demo">Demo</a></li>';
                        echo '<li><a href="#api">API Docs</a></li>';
                        echo '</ul>';
                    }
                    ?>
                </div>

                <div class="footer-section">
                    <h4><?php echo get_theme_mod('footer_section2_title', 'Company'); ?></h4>
                    <?php
                    if (is_active_sidebar('footer-2')) {
                        dynamic_sidebar('footer-2');
                    } else {
                        // Default footer content
                        echo '<ul style="list-style: none; padding: 0;">';
                        echo '<li><a href="#about">About Us</a></li>';
                        echo '<li><a href="#careers">Careers</a></li>';
                        echo '<li><a href="#blog">Blog</a></li>';
                        echo '<li><a href="#contact">Contact</a></li>';
                        echo '</ul>';
                    }
                    ?>
                </div>

                <div class="footer-section">
                    <h4><?php echo get_theme_mod('footer_section3_title', 'Support'); ?></h4>
                    <?php
                    if (is_active_sidebar('footer-3')) {
                        dynamic_sidebar('footer-3');
                    } else {
                        // Default footer content
                        echo '<ul style="list-style: none; padding: 0;">';
                        echo '<li><a href="#help">Help Center</a></li>';
                        echo '<li><a href="#status">Status Page</a></li>';
                        echo '<li><a href="#community">Community</a></li>';
                        echo '<li><a href="#security">Security</a></li>';
                        echo '</ul>';
                    }
                    ?>
                </div>

                <div class="footer-section">
                    <h4><?php echo get_theme_mod('footer_section4_title', 'Connect'); ?></h4>
                    <div class="social-links">
                        <?php
                        $twitter_url = get_theme_mod('social_twitter', '');
                        $linkedin_url = get_theme_mod('social_linkedin', '');
                        $github_url = get_theme_mod('social_github', '');
                        $email = get_theme_mod('contact_email', '');
                        
                        if ($twitter_url) {
                            echo '<a href="' . esc_url($twitter_url) . '" target="_blank" rel="noopener">🐦 Twitter</a><br>';
                        }
                        if ($linkedin_url) {
                            echo '<a href="' . esc_url($linkedin_url) . '" target="_blank" rel="noopener">💼 LinkedIn</a><br>';
                        }
                        if ($github_url) {
                            echo '<a href="' . esc_url($github_url) . '" target="_blank" rel="noopener">🐙 GitHub</a><br>';
                        }
                        if ($email) {
                            echo '<a href="mailto:' . esc_attr($email) . '">📧 Email</a><br>';
                        }
                        
                        // Default social links if none are set
                        if (!$twitter_url && !$linkedin_url && !$github_url && !$email) {
                            echo '<a href="#" onclick="alert(\'Add your social links in WordPress Customizer!\')">🐦 Twitter</a><br>';
                            echo '<a href="#" onclick="alert(\'Add your social links in WordPress Customizer!\')">💼 LinkedIn</a><br>';
                            echo '<a href="#" onclick="alert(\'Add your social links in WordPress Customizer!\')">🐙 GitHub</a><br>';
                        }
                        ?>
                    </div>
                </div>
            </div>

            <div class="footer-bottom">
                <p>
                    <?php
                    $copyright_text = get_theme_mod('copyright_text', '© ' . date('Y') . ' ' . get_bloginfo('name') . '. All rights reserved.');
                    echo esc_html($copyright_text);
                    ?>
                </p>
                <p style="margin-top: 0.5rem; font-size: 0.9rem;">
                    <?php
                    $footer_tagline = get_theme_mod('footer_tagline', 'Built with ❤️ using Modern SaaS Landing Theme');
                    echo esc_html($footer_tagline);
                    ?>
                </p>
            </div>
        </div>
    </footer>
</div><!-- #page -->

<?php wp_footer(); ?>

<!-- Custom JavaScript for smooth scrolling and header effects -->
<script>
document.addEventListener('DOMContentLoaded', function() {
    // Smooth scrolling for anchor links
    const links = document.querySelectorAll('a[href^="#"]');
    links.forEach(link => {
        link.addEventListener('click', function(e) {
            e.preventDefault();
            const target = document.querySelector(this.getAttribute('href'));
            if (target) {
                const headerHeight = document.querySelector('.site-header').offsetHeight;
                const targetPosition = target.offsetTop - headerHeight - 20;
                window.scrollTo({
                    top: targetPosition,
                    behavior: 'smooth'
                });
            }
        });
    });

    // Header scroll effect
    const header = document.querySelector('.site-header');
    let lastScrollTop = 0;
    
    window.addEventListener('scroll', function() {
        const scrollTop = window.pageYOffset || document.documentElement.scrollTop;
        
        if (scrollTop > 100) {
            header.classList.add('scrolled');
        } else {
            header.classList.remove('scrolled');
        }
        
        lastScrollTop = scrollTop;
    });

    // Add loading animation to buttons
    const buttons = document.querySelectorAll('.btn');
    buttons.forEach(button => {
        button.addEventListener('click', function(e) {
            // Add a subtle loading effect
            const originalText = this.textContent;
            if (!this.href || this.href.includes('#')) {
                this.style.opacity = '0.7';
                setTimeout(() => {
                    this.style.opacity = '1';
                }, 200);
            }
        });
    });

    // Intersection Observer for fade-in animations
    const observerOptions = {
        threshold: 0.1,
        rootMargin: '0px 0px -50px 0px'
    };

    const observer = new IntersectionObserver(function(entries) {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                entry.target.style.opacity = '1';
                entry.target.style.transform = 'translateY(0)';
            }
        });
    }, observerOptions);

    // Observe feature cards and other elements
    const animatedElements = document.querySelectorAll('.feature-card, .section-title');
    animatedElements.forEach(el => {
        el.style.opacity = '0';
        el.style.transform = 'translateY(30px)';
        el.style.transition = 'opacity 0.6s ease, transform 0.6s ease';
        observer.observe(el);
    });
});
</script>

</body>
</html>

