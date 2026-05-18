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
            const newDir = html.dir === "rtl" ? "ltr" : "rtl";
            html.dir = newDir;
            
            // Update all RTL toggle buttons text
            rtlToggles.forEach(toggle => {
                toggle.innerText = newDir === "rtl" ? "LTR" : "RTL";
            });
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
    // 7. Scroll to Top
    const backToTop = document.getElementById('back-to-top');
    if (backToTop) {
        window.addEventListener('scroll', () => {
            if (window.scrollY > 500) {
                backToTop.classList.add('show');
            } else {
                backToTop.classList.remove('show');
            }
        });

        backToTop.addEventListener('click', () => {
            window.scrollTo({
                top: 0,
                behavior: 'smooth'
            });
        });
    }

    // 8. Touch Dropdown Support for Tablets (like iPad Pro) & Mobile viewports
    if (window.matchMedia("(pointer: coarse)").matches) {
        const navDropdowns = document.querySelectorAll("nav .relative.group");
        
        navDropdowns.forEach(dropdown => {
            const trigger = dropdown.querySelector("a.nav-link");
            const menu = dropdown.querySelector(".absolute");
            
            if (trigger && menu) {
                // Prevent navigation on touch and toggle the menu
                trigger.addEventListener("click", (e) => {
                    e.preventDefault();
                    e.stopPropagation();
                    
                    const isOpen = menu.style.opacity === "1";
                    
                    // Close all other dropdowns
                    document.querySelectorAll("nav .relative.group .absolute").forEach(otherMenu => {
                        if (otherMenu !== menu) {
                            otherMenu.style.opacity = "";
                            otherMenu.style.visibility = "";
                        }
                    });
                    
                    if (isOpen) {
                        menu.style.opacity = "";
                        menu.style.visibility = "";
                    } else {
                        menu.style.opacity = "1";
                        menu.style.visibility = "visible";
                    }
                });
            }
        });
        
        // Close dropdowns when clicking outside
        document.addEventListener("click", (e) => {
            if (!e.target.closest("nav .relative.group")) {
                document.querySelectorAll("nav .relative.group .absolute").forEach(menu => {
                    menu.style.opacity = "";
                    menu.style.visibility = "";
                });
            }
        });
    }
});
