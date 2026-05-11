document.addEventListener("DOMContentLoaded", () => {
    // Basic interaction for the dashboard template
    
    // Sidebar toggle for mobile/tablet
    const sidebarToggle = document.getElementById('sidebar-toggle');
    const sidebar = document.getElementById('dashboard-sidebar');
    const overlay = document.getElementById('sidebar-overlay');
    
    function toggleSidebar() {
        if (sidebar && overlay) {
            sidebar.classList.toggle('-translate-x-full');
            overlay.classList.toggle('hidden');
        }
    }

    if (sidebarToggle) {
        sidebarToggle.addEventListener('click', toggleSidebar);
    }
    
    if (overlay) {
        overlay.addEventListener('click', toggleSidebar);
    }

    // Tab switching logic for Dashboard
    const tabBtns = document.querySelectorAll('.tab-btn');
    const tabContents = document.querySelectorAll('.tab-content');

    tabBtns.forEach(btn => {
        btn.addEventListener('click', () => {
            const target = btn.getAttribute('data-target');
            if (!target) return;

            // Close sidebar on mobile/tablet after clicking a link
            if (sidebar && !sidebar.classList.contains('-translate-x-full') && window.innerWidth < 1024) {
                toggleSidebar();
            }
            
            // Remove active classes from all buttons
            tabBtns.forEach(b => {
                b.classList.remove('bg-gray-100', 'dark:bg-gray-800', 'text-gray-900', 'dark:text-white');
                b.classList.add('text-gray-500');
            });

            // Hide all tab contents
            tabContents.forEach(c => c.classList.add('hidden'));

            // Add active class to clicked button
            btn.classList.remove('text-gray-500');
            btn.classList.add('bg-gray-100', 'dark:bg-gray-800', 'text-gray-900', 'dark:text-white');

            // Show target content
            const targetContent = document.getElementById(target);
            if (targetContent) {
                targetContent.classList.remove('hidden');
            }
        });
    });
});
