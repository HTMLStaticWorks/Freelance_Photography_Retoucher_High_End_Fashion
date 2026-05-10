import os
from bs4 import BeautifulSoup

dir_path = r'c:\Users\prasa\OneDrive\Desktop\SF\May website 2026\Freelance_Photography_Retoucher_High_End_Fashion\pages'

pages = [
    ('about.html', 'About'),
    ('services.html', 'Services'),
    ('niche.html', 'Fashion'),
    ('portfolio.html', 'Portfolio'),
    ('contact.html', 'Contact')
]

def process_file(filepath):
    with open(filepath, 'r', encoding='utf-8') as f:
        html = f.read()

    soup = BeautifulSoup(html, 'html.parser')
    filename = os.path.basename(filepath)

    nav = soup.find('nav', class_=lambda c: c and 'hidden md:flex' in c)
    if nav:
        home_dropdown = None
        # Use find_all with a function to check text content robustly
        for child in nav.find_all(recursive=False):
            if 'Home' in child.get_text():
                home_dropdown = child
                break
        
        # If we couldn't find it as a direct child, maybe it was deleted in previous run?
        # But wait, we are reading the file fresh.
        # Let's see if we can find ANY link with 'Home' and get its top-most parent within nav
        if not home_dropdown:
            home_link = nav.find('a', string=lambda t: t and 'Home' in t) or \
                        nav.find(lambda tag: tag.name == 'a' and 'Home' in tag.get_text())
            if home_link:
                curr = home_link
                while curr.parent != nav:
                    curr = curr.parent
                home_dropdown = curr

        # Fallback Home dropdown if it's completely missing
        if not home_dropdown:
            # Create a basic Home dropdown structure similar to others
            home_dropdown = BeautifulSoup("""
            <div class="relative group h-full inline-flex items-center">
                <a href="index.html" class="hover:text-gold-400 transition-colors">Home <i class="ph ph-caret-down ml-1 text-xs"></i></a>
                <div class="absolute top-full left-0 mt-0 w-40 bg-white dark:bg-luxury-900 border border-gray-100 dark:border-gray-800 shadow-xl rounded-b-xl overflow-hidden opacity-0 invisible group-hover:opacity-100 group-hover:visible transition-all duration-300 z-50">
                    <a href="index.html" class="block px-6 py-3 text-sm font-medium hover:bg-gray-50 dark:hover:bg-black transition-colors border-b border-gray-50 dark:border-gray-800 text-black dark:text-gray-300">Home 1</a>
                    <a href="home2.html" class="block px-6 py-3 text-sm font-medium hover:bg-gray-50 dark:hover:bg-black transition-colors text-black dark:text-gray-300">Home 2</a>
                </div>
            </div>
            """, 'html.parser').div

        # Extract classes
        inactive_cls = ""
        active_cls = ""
        for a in nav.find_all('a'):
            if 'Home' in a.get_text() or 'Login' in a.get_text() or 'Portal' in a.get_text():
                continue
            href = a.get('href')
            cls = " ".join(a.get('class', []))
            if href == filename:
                active_cls = cls
            else:
                inactive_cls = cls
        
        if not inactive_cls:
            if 'portfolio' in filepath or 'niche' in filepath:
                inactive_cls = "text-xs uppercase tracking-[0.2em] hover:text-gold-400 transition-colors"
                active_cls = "text-xs uppercase tracking-[0.2em] text-gold-400 font-bold"
            else:
                inactive_cls = "text-sm font-medium hover:text-gray-500 transition-colors"
                active_cls = "text-sm font-medium font-bold"
        
        if not active_cls:
            active_cls = inactive_cls + " font-bold"

        nav.clear()
        nav.append(home_dropdown)
        
        # Ensure Home link has the right class
        home_link = home_dropdown.find('a')
        if home_link:
            h_cls = inactive_cls.replace('font-bold', '').strip()
            # If it's a dropdown, usually we don't want 'font-bold' on the trigger unless it's index.html
            if filename == 'index.html' or filename == 'home2.html':
                h_cls = active_cls
            home_link['class'] = h_cls.split()

        for href, text in pages:
            new_a = soup.new_tag('a', href=href)
            new_a['class'] = (active_cls if href == filename else inactive_cls).split()
            new_a.string = text
            nav.append(new_a)

    # --- MOBILE MENU ---
    mobile_menu = soup.find('div', id='mobile-menu')
    if mobile_menu:
        inner = mobile_menu.find('div', recursive=False)
        if inner:
            home_m_block = None
            for child in inner.find_all(recursive=False):
                if 'Home' in child.get_text():
                    home_m_block = child
                    break
            
            if not home_m_block:
                home_m_block = BeautifulSoup("""
                <div class="space-y-1">
                    <span class="block px-3 py-2 rounded-md text-sm uppercase tracking-[0.2em] font-bold text-white">Home</span>
                    <div class="pl-6 space-y-1">
                        <a href="index.html" class="block px-3 py-2 rounded-md text-xs uppercase tracking-[0.2em] text-gray-400 hover:text-gold-400">Home 1</a>
                        <a href="home2.html" class="block px-3 py-2 rounded-md text-xs uppercase tracking-[0.2em] text-gray-400 hover:text-gold-400">Home 2</a>
                    </div>
                </div>
                """, 'html.parser').div

            login_block = inner.find('div', class_=lambda c: c and 'border-t' in c)

            m_inactive = "block px-3 py-2 rounded-md text-sm uppercase tracking-[0.2em] text-white"
            m_active = "block px-3 py-2 rounded-md text-sm uppercase tracking-[0.2em] font-bold text-gold-400"
            if 'index.html' in filepath or 'about.html' in filepath:
                 m_inactive = "block px-3 py-2 rounded-md text-base font-medium"
                 m_active = "block px-3 py-2 rounded-md text-base font-bold"

            inner.clear()
            inner.append(home_m_block)
            for href, text in pages:
                new_a = soup.new_tag('a', href=href)
                new_a['class'] = (m_active if href == filename else m_inactive).split()
                new_a.string = text
                inner.append(new_a)
            if login_block:
                inner.append(login_block)

    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(soup.prettify())
    print("Processed", filename)

for filename in os.listdir(dir_path):
    if filename.endswith('.html'):
        process_file(os.path.join(dir_path, filename))
