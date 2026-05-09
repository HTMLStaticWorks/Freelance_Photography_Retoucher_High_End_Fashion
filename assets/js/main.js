document.addEventListener("DOMContentLoaded", () => {
    // 1. Initialize AOS
    if (typeof AOS !== 'undefined') {
        AOS.init({
            duration: 1000,
            easing: 'ease-out-cubic',
            once: true,
            offset: 50,
        });
    }

    // 2. Custom Cursor
    const cursor = document.createElement("div");
    cursor.classList.add("cursor-follower");
    document.body.appendChild(cursor);

    let mouseX = 0, mouseY = 0;
    let cursorX = 0, cursorY = 0;

    document.addEventListener("mousemove", (e) => {
        mouseX = e.clientX;
        mouseY = e.clientY;
    });

    function animateCursor() {
        let dx = mouseX - cursorX;
        let dy = mouseY - cursorY;
        cursorX += dx * 0.15;
        cursorY += dy * 0.15;
        cursor.style.transform = `translate(${cursorX}px, ${cursorY}px)`;
        requestAnimationFrame(animateCursor);
    }
    animateCursor();

    const addHoverEffect = () => {
        const hoverElements = document.querySelectorAll("a, button, .hover-target");
        hoverElements.forEach(el => {
            el.addEventListener("mouseenter", () => cursor.classList.add("hover"));
            el.addEventListener("mouseleave", () => cursor.classList.remove("hover"));
        });
    };
    addHoverEffect();

    // 3. Dark Mode Toggle
    const themeToggles = document.querySelectorAll(".theme-toggle");
    
    // Check initial state
    const isDark = localStorage.getItem("theme") === "dark" || 
        (!localStorage.getItem("theme") && window.matchMedia("(prefers-color-scheme: dark)").matches);
    
    if (isDark) {
        document.documentElement.classList.add("dark");
    }

    themeToggles.forEach(btn => {
        btn.addEventListener("click", () => {
            document.documentElement.classList.toggle("dark");
            const currentTheme = document.documentElement.classList.contains("dark") ? "dark" : "light";
            localStorage.setItem("theme", currentTheme);
        });
    });

    // 4. RTL Toggle (for Demo/Preview purposes)
    const rtlToggles = document.querySelectorAll(".rtl-toggle");
    rtlToggles.forEach(btn => {
        btn.addEventListener("click", () => {
            const html = document.documentElement;
            html.dir = html.dir === "rtl" ? "ltr" : "rtl";
        });
    });

    // 5. Mobile Menu Toggle
    const menuBtn = document.getElementById('mobile-menu-btn');
    const mobileMenu = document.getElementById('mobile-menu');
    if (menuBtn && mobileMenu) {
        menuBtn.addEventListener('click', () => {
            mobileMenu.classList.toggle('hidden');
        });
    }

    // 6. Before/After Slider Initialization (if Swiper is present)
    if (typeof Swiper !== 'undefined') {
        const swipers = document.querySelectorAll('.swiper-container');
        if(swipers.length > 0) {
            new Swiper('.swiper-container', {
                slidesPerView: 1,
                spaceBetween: 30,
                loop: true,
                navigation: {
                    nextEl: '.swiper-button-next',
                    prevEl: '.swiper-button-prev',
                },
                pagination: {
                    el: '.swiper-pagination',
                    clickable: true,
                },
            });
        }
    }
});
