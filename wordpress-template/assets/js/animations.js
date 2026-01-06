/**
 * Advanced Animations for Modern SaaS Landing Theme
 */

(function($) {
    'use strict';

    // Initialize animations when document is ready
    $(document).ready(function() {
        initializeAnimations();
    });

    /**
     * Initialize all animations
     */
    function initializeAnimations() {
        setupParallaxEffects();
        setupHoverAnimations();
        setupLoadingAnimations();
        setupScrollAnimations();
        setupTypingEffect();
        setupParticleBackground();
        setupFloatingElements();
    }

    /**
     * Setup parallax scrolling effects
     */
    function setupParallaxEffects() {
        if ($(window).width() > 768) { // Only on desktop
            $(window).on('scroll', throttle(function() {
                const scrolled = $(window).scrollTop();
                const parallaxElements = $('.parallax-element');
                
                parallaxElements.each(function() {
                    const element = $(this);
                    const speed = element.data('speed') || 0.5;
                    const yPos = -(scrolled * speed);
                    element.css('transform', `translateY(${yPos}px)`);
                });
            }, 16));
        }
    }

    /**
     * Setup advanced hover animations
     */
    function setupHoverAnimations() {
        // Feature card hover effects
        $('.feature-card').hover(
            function() {
                $(this).find('.feature-icon').addClass('bounce');
                setTimeout(() => {
                    $(this).find('.feature-icon').removeClass('bounce');
                }, 600);
            }
        );

        // Button hover effects with ripple
        $('.btn').on('mouseenter', function(e) {
            const button = $(this);
            const ripple = $('<span class="ripple"></span>');
            
            button.append(ripple);
            
            const x = e.pageX - button.offset().left;
            const y = e.pageY - button.offset().top;
            
            ripple.css({
                left: x,
                top: y
            }).addClass('animate');
            
            setTimeout(() => {
                ripple.remove();
            }, 600);
        });

        // Logo hover animation
        $('.site-logo').hover(
            function() {
                $(this).addClass('logo-hover');
            },
            function() {
                $(this).removeClass('logo-hover');
            }
        );
    }

    /**
     * Setup loading animations
     */
    function setupLoadingAnimations() {
        // Stagger animation for feature cards
        $('.features-grid .feature-card').each(function(index) {
            $(this).css('animation-delay', (index * 0.1) + 's');
        });

        // Loading skeleton effect
        $('.loading-skeleton').each(function() {
            const skeleton = $(this);
            const shimmer = $('<div class="shimmer"></div>');
            skeleton.append(shimmer);
        });
    }

    /**
     * Setup scroll-triggered animations
     */
    function setupScrollAnimations() {
        // Create scroll timeline
        const scrollTimeline = [];
        
        $('.animate-on-scroll').each(function() {
            const element = $(this);
            const animationType = element.data('animation') || 'fadeInUp';
            const delay = element.data('delay') || 0;
            
            scrollTimeline.push({
                element: element,
                animation: animationType,
                delay: delay,
                triggered: false
            });
        });

        // Check scroll position
        $(window).on('scroll', throttle(function() {
            const windowTop = $(window).scrollTop();
            const windowBottom = windowTop + $(window).height();
            
            scrollTimeline.forEach(function(item) {
                if (!item.triggered) {
                    const elementTop = item.element.offset().top;
                    
                    if (elementTop < windowBottom - 100) {
                        setTimeout(function() {
                            item.element.addClass('animate-' + item.animation);
                        }, item.delay);
                        item.triggered = true;
                    }
                }
            });
        }, 16));
    }

    /**
     * Setup typing effect for hero title
     */
    function setupTypingEffect() {
        const typingElement = $('.typing-effect');
        if (typingElement.length) {
            const text = typingElement.text();
            const speed = typingElement.data('speed') || 100;
            
            typingElement.text('');
            
            let i = 0;
            const typeWriter = function() {
                if (i < text.length) {
                    typingElement.text(typingElement.text() + text.charAt(i));
                    i++;
                    setTimeout(typeWriter, speed);
                } else {
                    typingElement.addClass('typing-complete');
                }
            };
            
            // Start typing after a delay
            setTimeout(typeWriter, 1000);
        }
    }

    /**
     * Setup particle background effect
     */
    function setupParticleBackground() {
        const particleContainer = $('.particle-background');
        if (particleContainer.length && $(window).width() > 768) {
            
            // Create particles
            for (let i = 0; i < 50; i++) {
                const particle = $('<div class="particle"></div>');
                const size = Math.random() * 4 + 1;
                const x = Math.random() * 100;
                const y = Math.random() * 100;
                const duration = Math.random() * 20 + 10;
                
                particle.css({
                    left: x + '%',
                    top: y + '%',
                    width: size + 'px',
                    height: size + 'px',
                    animationDuration: duration + 's',
                    animationDelay: Math.random() * 20 + 's'
                });
                
                particleContainer.append(particle);
            }
        }
    }

    /**
     * Setup floating elements animation
     */
    function setupFloatingElements() {
        $('.floating-element').each(function(index) {
            const element = $(this);
            const duration = 3 + (index * 0.5);
            const delay = index * 0.2;
            
            element.css({
                animationDuration: duration + 's',
                animationDelay: delay + 's'
            });
        });
    }

    /**
     * Advanced scroll progress indicator
     */
    function setupScrollProgress() {
        const progressBar = $('<div class="scroll-progress"><div class="scroll-progress-bar"></div></div>');
        $('body').append(progressBar);
        
        $(window).on('scroll', function() {
            const scrollTop = $(window).scrollTop();
            const docHeight = $(document).height() - $(window).height();
            const scrollPercent = (scrollTop / docHeight) * 100;
            
            $('.scroll-progress-bar').css('width', scrollPercent + '%');
        });
    }

    /**
     * Mouse trail effect
     */
    function setupMouseTrail() {
        if ($(window).width() > 1024) { // Only on large screens
            const trail = [];
            const trailLength = 10;
            
            for (let i = 0; i < trailLength; i++) {
                const dot = $('<div class="trail-dot"></div>');
                $('body').append(dot);
                trail.push(dot);
            }
            
            $(document).on('mousemove', function(e) {
                trail.forEach(function(dot, index) {
                    setTimeout(function() {
                        dot.css({
                            left: e.pageX + 'px',
                            top: e.pageY + 'px',
                            opacity: (trailLength - index) / trailLength
                        });
                    }, index * 20);
                });
            });
        }
    }

    /**
     * 3D tilt effect for cards
     */
    function setup3DTilt() {
        $('.tilt-card').on('mousemove', function(e) {
            const card = $(this);
            const rect = this.getBoundingClientRect();
            const x = e.clientX - rect.left;
            const y = e.clientY - rect.top;
            
            const centerX = rect.width / 2;
            const centerY = rect.height / 2;
            
            const rotateX = (y - centerY) / 10;
            const rotateY = (centerX - x) / 10;
            
            card.css('transform', `perspective(1000px) rotateX(${rotateX}deg) rotateY(${rotateY}deg)`);
        });
        
        $('.tilt-card').on('mouseleave', function() {
            $(this).css('transform', 'perspective(1000px) rotateX(0deg) rotateY(0deg)');
        });
    }

    /**
     * Magnetic button effect
     */
    function setupMagneticButtons() {
        $('.btn-magnetic').on('mousemove', function(e) {
            const button = $(this);
            const rect = this.getBoundingClientRect();
            const x = e.clientX - rect.left - rect.width / 2;
            const y = e.clientY - rect.top - rect.height / 2;
            
            button.css('transform', `translate(${x * 0.1}px, ${y * 0.1}px)`);
        });
        
        $('.btn-magnetic').on('mouseleave', function() {
            $(this).css('transform', 'translate(0px, 0px)');
        });
    }

    /**
     * Smooth reveal animation for sections
     */
    function setupSectionReveal() {
        const sections = $('.reveal-section');
        
        const revealObserver = new IntersectionObserver(function(entries) {
            entries.forEach(function(entry) {
                if (entry.isIntersecting) {
                    const section = $(entry.target);
                    const children = section.find('.reveal-child');
                    
                    children.each(function(index) {
                        setTimeout(() => {
                            $(this).addClass('revealed');
                        }, index * 100);
                    });
                    
                    revealObserver.unobserve(entry.target);
                }
            });
        }, { threshold: 0.1 });
        
        sections.each(function() {
            revealObserver.observe(this);
        });
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

    // Initialize additional animations
    setupScrollProgress();
    setup3DTilt();
    setupMagneticButtons();
    setupSectionReveal();
    
    // Optional: Mouse trail (can be resource intensive)
    // setupMouseTrail();

})(jQuery);

// CSS animations that work with the JavaScript above
const animationCSS = `
<style>
/* Bounce animation for icons */
.bounce {
    animation: bounce 0.6s ease-in-out;
}

@keyframes bounce {
    0%, 20%, 60%, 100% { transform: translateY(0); }
    40% { transform: translateY(-10px); }
    80% { transform: translateY(-5px); }
}

/* Ripple effect for buttons */
.btn {
    position: relative;
    overflow: hidden;
}

.ripple {
    position: absolute;
    border-radius: 50%;
    background: rgba(255, 255, 255, 0.3);
    transform: scale(0);
    pointer-events: none;
}

.ripple.animate {
    animation: ripple-animation 0.6s linear;
}

@keyframes ripple-animation {
    to {
        transform: scale(4);
        opacity: 0;
    }
}

/* Logo hover animation */
.logo-hover {
    animation: logo-pulse 0.6s ease-in-out;
}

@keyframes logo-pulse {
    0% { transform: scale(1); }
    50% { transform: scale(1.05); }
    100% { transform: scale(1); }
}

/* Shimmer loading effect */
.loading-skeleton {
    position: relative;
    overflow: hidden;
    background: #f0f0f0;
}

.shimmer {
    position: absolute;
    top: 0;
    left: -100%;
    width: 100%;
    height: 100%;
    background: linear-gradient(90deg, transparent, rgba(255,255,255,0.8), transparent);
    animation: shimmer 1.5s infinite;
}

@keyframes shimmer {
    0% { left: -100%; }
    100% { left: 100%; }
}

/* Scroll animations */
.animate-fadeInUp {
    animation: fadeInUp 0.8s ease forwards;
}

.animate-fadeInLeft {
    animation: fadeInLeft 0.8s ease forwards;
}

.animate-fadeInRight {
    animation: fadeInRight 0.8s ease forwards;
}

@keyframes fadeInLeft {
    from {
        opacity: 0;
        transform: translateX(-30px);
    }
    to {
        opacity: 1;
        transform: translateX(0);
    }
}

@keyframes fadeInRight {
    from {
        opacity: 0;
        transform: translateX(30px);
    }
    to {
        opacity: 1;
        transform: translateX(0);
    }
}

/* Typing effect */
.typing-effect::after {
    content: '|';
    animation: blink 1s infinite;
}

.typing-complete::after {
    display: none;
}

@keyframes blink {
    0%, 50% { opacity: 1; }
    51%, 100% { opacity: 0; }
}

/* Particle background */
.particle-background {
    position: absolute;
    top: 0;
    left: 0;
    width: 100%;
    height: 100%;
    overflow: hidden;
    pointer-events: none;
}

.particle {
    position: absolute;
    background: rgba(255, 255, 255, 0.1);
    border-radius: 50%;
    animation: float infinite linear;
}

@keyframes float {
    0% {
        transform: translateY(100vh) rotate(0deg);
        opacity: 0;
    }
    10% {
        opacity: 1;
    }
    90% {
        opacity: 1;
    }
    100% {
        transform: translateY(-100px) rotate(360deg);
        opacity: 0;
    }
}

/* Floating elements */
.floating-element {
    animation: floating infinite ease-in-out;
}

@keyframes floating {
    0%, 100% { transform: translateY(0px); }
    50% { transform: translateY(-10px); }
}

/* Scroll progress bar */
.scroll-progress {
    position: fixed;
    top: 0;
    left: 0;
    width: 100%;
    height: 3px;
    background: rgba(0, 0, 0, 0.1);
    z-index: 9999;
}

.scroll-progress-bar {
    height: 100%;
    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
    transition: width 0.1s ease;
}

/* Mouse trail */
.trail-dot {
    position: absolute;
    width: 4px;
    height: 4px;
    background: #667eea;
    border-radius: 50%;
    pointer-events: none;
    z-index: 9999;
    transition: opacity 0.2s ease;
}

/* 3D Tilt cards */
.tilt-card {
    transition: transform 0.1s ease;
    transform-style: preserve-3d;
}

/* Magnetic buttons */
.btn-magnetic {
    transition: transform 0.2s ease;
}

/* Section reveal */
.reveal-section .reveal-child {
    opacity: 0;
    transform: translateY(30px);
    transition: opacity 0.6s ease, transform 0.6s ease;
}

.reveal-section .reveal-child.revealed {
    opacity: 1;
    transform: translateY(0);
}
</style>
`;

// Inject the CSS
$('head').append(animationCSS);

