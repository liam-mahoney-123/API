/**
 * Main JavaScript for Modern SaaS Landing Theme
 */

(function($) {
    'use strict';

    // Document ready
    $(document).ready(function() {
        initializeTheme();
    });

    // Window load
    $(window).on('load', function() {
        handlePageLoad();
    });

    /**
     * Initialize all theme functionality
     */
    function initializeTheme() {
        setupSmoothScrolling();
        setupHeaderEffects();
        setupMobileMenu();
        setupScrollToTop();
        setupFormHandling();
        setupAnimations();
        setupFAQ();
        setupCounters();
        setupLazyLoading();
    }

    /**
     * Handle page load events
     */
    function handlePageLoad() {
        // Hide loading states
        $('.loading').removeClass('loading');
        
        // Trigger animations for visible elements
        triggerVisibleAnimations();
    }

    /**
     * Setup smooth scrolling for anchor links
     */
    function setupSmoothScrolling() {
        $('a[href^="#"]').on('click', function(e) {
            e.preventDefault();
            
            const target = $(this.getAttribute('href'));
            if (target.length) {
                const headerHeight = $('.site-header').outerHeight();
                const targetPosition = target.offset().top - headerHeight - 20;
                
                $('html, body').animate({
                    scrollTop: targetPosition
                }, 800, 'easeInOutCubic');
            }
        });
    }

    /**
     * Setup header scroll effects
     */
    function setupHeaderEffects() {
        const header = $('.site-header');
        let lastScrollTop = 0;
        let ticking = false;

        function updateHeader() {
            const scrollTop = $(window).scrollTop();
            
            // Add/remove scrolled class
            if (scrollTop > 100) {
                header.addClass('scrolled');
            } else {
                header.removeClass('scrolled');
            }
            
            // Hide/show header on scroll (optional)
            if (scrollTop > lastScrollTop && scrollTop > 200) {
                header.addClass('header-hidden');
            } else {
                header.removeClass('header-hidden');
            }
            
            lastScrollTop = scrollTop;
            ticking = false;
        }

        $(window).on('scroll', function() {
            if (!ticking) {
                requestAnimationFrame(updateHeader);
                ticking = true;
            }
        });
    }

    /**
     * Setup mobile menu functionality
     */
    function setupMobileMenu() {
        const mobileToggle = $('.mobile-menu-toggle');
        const mobileMenu = $('.mobile-menu');
        const body = $('body');

        // Create mobile menu if it doesn't exist
        if (mobileMenu.length === 0) {
            const navMenu = $('.main-nav ul').clone();
            const mobileMenuHTML = `
                <div class="mobile-menu">
                    <button class="mobile-menu-close">&times;</button>
                    ${navMenu.prop('outerHTML')}
                </div>
            `;
            body.append(mobileMenuHTML);
        }

        // Toggle mobile menu
        mobileToggle.on('click', function() {
            $('.mobile-menu').addClass('active');
            body.addClass('menu-open');
        });

        // Close mobile menu
        $(document).on('click', '.mobile-menu-close, .mobile-menu a', function() {
            $('.mobile-menu').removeClass('active');
            body.removeClass('menu-open');
        });

        // Close on escape key
        $(document).on('keydown', function(e) {
            if (e.keyCode === 27 && $('.mobile-menu').hasClass('active')) {
                $('.mobile-menu').removeClass('active');
                body.removeClass('menu-open');
            }
        });
    }

    /**
     * Setup scroll to top button
     */
    function setupScrollToTop() {
        // Create scroll to top button if it doesn't exist
        if ($('.scroll-to-top').length === 0) {
            $('body').append('<button class="scroll-to-top" aria-label="Scroll to top">↑</button>');
        }

        const scrollBtn = $('.scroll-to-top');

        $(window).on('scroll', function() {
            if ($(window).scrollTop() > 300) {
                scrollBtn.addClass('visible');
            } else {
                scrollBtn.removeClass('visible');
            }
        });

        scrollBtn.on('click', function() {
            $('html, body').animate({
                scrollTop: 0
            }, 800, 'easeInOutCubic');
        });
    }

    /**
     * Setup form handling
     */
    function setupFormHandling() {
        // Handle contact forms
        $('form').on('submit', function(e) {
            const form = $(this);
            const submitBtn = form.find('button[type="submit"], input[type="submit"]');
            
            // Add loading state
            submitBtn.addClass('loading').prop('disabled', true);
            
            // Remove loading state after 2 seconds (replace with actual form handling)
            setTimeout(function() {
                submitBtn.removeClass('loading').prop('disabled', false);
                
                // Show success message (customize as needed)
                showNotification('Thank you! Your message has been sent.', 'success');
            }, 2000);
        });

        // Email validation
        $('input[type="email"]').on('blur', function() {
            const email = $(this).val();
            const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
            
            if (email && !emailRegex.test(email)) {
                $(this).addClass('error');
                showNotification('Please enter a valid email address.', 'error');
            } else {
                $(this).removeClass('error');
            }
        });
    }

    /**
     * Setup scroll animations
     */
    function setupAnimations() {
        // Intersection Observer for fade-in animations
        if ('IntersectionObserver' in window) {
            const observerOptions = {
                threshold: 0.1,
                rootMargin: '0px 0px -50px 0px'
            };

            const observer = new IntersectionObserver(function(entries) {
                entries.forEach(function(entry) {
                    if (entry.isIntersecting) {
                        $(entry.target).addClass('visible');
                        observer.unobserve(entry.target);
                    }
                });
            }, observerOptions);

            // Observe elements
            $('.feature-card, .section-title, .testimonial-card, .blog-card').each(function() {
                $(this).addClass('fade-in-up');
                observer.observe(this);
            });
        } else {
            // Fallback for older browsers
            $('.fade-in-up').addClass('visible');
        }
    }

    /**
     * Trigger animations for visible elements
     */
    function triggerVisibleAnimations() {
        $('.fade-in-up').each(function() {
            const element = $(this);
            const elementTop = element.offset().top;
            const windowBottom = $(window).scrollTop() + $(window).height();
            
            if (elementTop < windowBottom - 100) {
                element.addClass('visible');
            }
        });
    }

    /**
     * Setup FAQ functionality
     */
    function setupFAQ() {
        $('.faq-question').on('click', function() {
            const question = $(this);
            const answer = question.next('.faq-answer');
            const isActive = question.hasClass('active');
            
            // Close all other FAQs
            $('.faq-question').removeClass('active');
            $('.faq-answer').removeClass('active');
            
            // Toggle current FAQ
            if (!isActive) {
                question.addClass('active');
                answer.addClass('active');
            }
        });
    }

    /**
     * Setup animated counters
     */
    function setupCounters() {
        $('.stat-item h3').each(function() {
            const counter = $(this);
            const target = parseInt(counter.text().replace(/[^0-9]/g, ''));
            
            if (target > 0) {
                counter.text('0');
                
                const observer = new IntersectionObserver(function(entries) {
                    entries.forEach(function(entry) {
                        if (entry.isIntersecting) {
                            animateCounter(counter, target);
                            observer.unobserve(entry.target);
                        }
                    });
                });
                
                observer.observe(counter[0]);
            }
        });
    }

    /**
     * Animate counter numbers
     */
    function animateCounter(element, target) {
        let current = 0;
        const increment = target / 100;
        const timer = setInterval(function() {
            current += increment;
            if (current >= target) {
                current = target;
                clearInterval(timer);
            }
            
            const suffix = element.text().replace(/[0-9]/g, '');
            element.text(Math.floor(current) + suffix);
        }, 20);
    }

    /**
     * Setup lazy loading for images
     */
    function setupLazyLoading() {
        if ('IntersectionObserver' in window) {
            const imageObserver = new IntersectionObserver(function(entries) {
                entries.forEach(function(entry) {
                    if (entry.isIntersecting) {
                        const img = entry.target;
                        img.src = img.dataset.src;
                        img.classList.remove('lazy');
                        imageObserver.unobserve(img);
                    }
                });
            });

            document.querySelectorAll('img[data-src]').forEach(function(img) {
                imageObserver.observe(img);
            });
        }
    }

    /**
     * Show notification messages
     */
    function showNotification(message, type) {
        const notification = $(`
            <div class="notification notification-${type}">
                ${message}
                <button class="notification-close">&times;</button>
            </div>
        `);
        
        $('body').append(notification);
        
        setTimeout(function() {
            notification.addClass('show');
        }, 100);
        
        // Auto hide after 5 seconds
        setTimeout(function() {
            hideNotification(notification);
        }, 5000);
        
        // Manual close
        notification.find('.notification-close').on('click', function() {
            hideNotification(notification);
        });
    }

    /**
     * Hide notification
     */
    function hideNotification(notification) {
        notification.removeClass('show');
        setTimeout(function() {
            notification.remove();
        }, 300);
    }

    /**
     * Utility: Debounce function
     */
    function debounce(func, wait, immediate) {
        let timeout;
        return function() {
            const context = this;
            const args = arguments;
            const later = function() {
                timeout = null;
                if (!immediate) func.apply(context, args);
            };
            const callNow = immediate && !timeout;
            clearTimeout(timeout);
            timeout = setTimeout(later, wait);
            if (callNow) func.apply(context, args);
        };
    }

    /**
     * Utility: Throttle function
     */
    function throttle(func, limit) {
        let inThrottle;
        return function() {
            const args = arguments;
            const context = this;
            if (!inThrottle) {
                func.apply(context, args);
                inThrottle = true;
                setTimeout(() => inThrottle = false, limit);
            }
        };
    }

    // Add easing function for smooth animations
    $.easing.easeInOutCubic = function(x, t, b, c, d) {
        if ((t /= d / 2) < 1) return c / 2 * t * t * t + b;
        return c / 2 * ((t -= 2) * t * t + 2) + b;
    };

    // Expose some functions globally if needed
    window.ModernSaaSTheme = {
        showNotification: showNotification,
        hideNotification: hideNotification,
        debounce: debounce,
        throttle: throttle
    };

})(jQuery);

