// Performance optimizations for mobile
(function() {
    'use strict';
    
    // Add loaded class to body when page is fully loaded
    window.addEventListener('load', function() {
        document.body.classList.add('loaded');
    });
    
    // Lazy load images that aren't critical
    if ('IntersectionObserver' in window) {
        const images = document.querySelectorAll('img[loading="lazy"]');
        const imageObserver = new IntersectionObserver((entries, observer) => {
            entries.forEach(entry => {
                if (entry.isIntersecting) {
                    const img = entry.target;
                    img.src = img.dataset.src || img.src;
                    img.classList.remove('lazy');
                    observer.unobserve(img);
                }
            });
        });
        
        images.forEach(img => imageObserver.observe(img));
    }
    
    // Preload next page resources on hover/touch
    const links = document.querySelectorAll('a[href]');
    const prefetchedUrls = new Set();
    
    function prefetchUrl(url) {
        if (!prefetchedUrls.has(url) && url.startsWith('/')) {
            prefetchedUrls.add(url);
            const link = document.createElement('link');
            link.rel = 'prefetch';
            link.href = url;
            document.head.appendChild(link);
        }
    }
    
    links.forEach(link => {
        link.addEventListener('mouseenter', () => prefetchUrl(link.href));
        link.addEventListener('touchstart', () => prefetchUrl(link.href));
    });
    
    // Optimize animations for mobile
    if (window.matchMedia('(max-width: 768px)').matches) {
        document.documentElement.style.setProperty('--animation-duration', '0.2s');
    }
    
    // Reduce motion for users who prefer it
    if (window.matchMedia('(prefers-reduced-motion: reduce)').matches) {
        document.documentElement.style.setProperty('--animation-duration', '0s');
    }
    
})();
