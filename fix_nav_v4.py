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

    # --- DESKTOP NAV ---
    nav = soup.find('nav', class_=lambda c: c and 'hidden md:flex' in c)
    if nav:
        # Find Home dropdown
        home_dropdown = None
        # Look for a top-level div in nav that contains "Home"
        for div in nav.find_all('div', recursive=False):
            if div.find('a', string=lambda t: t and 'Home' in t):
                home_dropdown = div
                break
        
        # If not found in a div, look for an <a> tag directly
        if not home_dropdown:
            home_dropdown = nav.find('a', string=lambda t: t and 'Home' in t)

        # Extract classes from existing links to use as template
        inactive_cls = ""
        active_cls = ""
        for a in nav.find_all('a'):
            link_text = a.get_text(strip=True)
            if 'Home' in link_text or 'Login' in link_text or 'Portal' in link_text:
                continue
            href = a.get('href')
            cls = " ".join(a.get('class', []))
            if href == filename:
                active_cls = cls
            else:
                inactive_cls = cls
        
        if not inactive_cls and active_cls:
            inactive_cls = active_cls.replace('text-gold-400 font-bold', 'hover:text-gold-400 transition-colors').replace('font-bold', '')
        if not active_cls and inactive_cls:
            active_cls = inactive_cls.replace('hover:text-gold-400 transition-colors', 'text-gold-400 font-bold').replace('hover:text-gray-500', 'font-bold')

        # Default classes if none found
        if not inactive_cls:
            if 'portfolio.html' in filepath or 'niche.html' in filepath:
                 inactive_cls = "text-xs uppercase tracking-[0.2em] hover:text-gold-400 transition-colors"
                 active_cls = "text-xs uppercase tracking-[0.2em] text-gold-400 font-bold"
            else:
                 inactive_cls = "text-sm font-medium hover:text-gray-500 transition-colors"
                 active_cls = "text-sm font-medium font-bold"

        # Clear nav and rebuild
        nav.clear()
        if home_dropdown:
            nav.append(home_dropdown)
        
        for href, text in pages:
            new_a = soup.new_tag('a', href=href)
            new_a['class'] = (active_cls if href == filename else inactive_cls).split()
            new_a.string = text
            nav.append(new_a)

    # --- MOBILE MENU ---
    mobile_menu = soup.find('div', id='mobile-menu')
    if mobile_menu:
        # Usually has an inner container div
        inner = mobile_menu.find('div', recursive=False)
        if inner:
            # Find Home block
            home_block = None
            # Home block can be a div.space-y-1 or div.relative
            for div in inner.find_all('div', recursive=False):
                if div.find('a', string=lambda t: t and 'Home' in t) or div.find('span', string=lambda t: t and 'Home' in t):
                    home_block = div
                    break
            
            # Find Login/Portal block
            login_block = inner.find('div', class_=lambda c: c and 'border-t' in c)

            # Rebuild inner
            m_inactive = "block px-3 py-2 rounded-md text-sm uppercase tracking-[0.2em] text-white"
            m_active = "block px-3 py-2 rounded-md text-sm uppercase tracking-[0.2em] font-bold text-gold-400"
            if 'index.html' in filepath or 'about.html' in filepath:
                 m_inactive = "block px-3 py-2 rounded-md text-base font-medium"
                 m_active = "block px-3 py-2 rounded-md text-base font-bold"

            inner.clear()
            if home_block:
                inner.append(home_block)
            
            for href, text in pages:
                new_a = soup.new_tag('a', href=href)
                new_a['class'] = (m_active if href == filename else m_inactive).split()
                new_a.string = text
                inner.append(new_a)
            
            if login_block:
                inner.append(login_block)

    # Write back
    # Using soup.encode() to preserve as much as possible, but formatting will change slightly
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(soup.prettify())
    print("Processed", filename)

for filename in os.listdir(dir_path):
    if filename.endswith('.html'):
        process_file(os.path.join(dir_path, filename))
