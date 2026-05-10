import os
import re

dir_path = r'c:\Users\prasa\OneDrive\Desktop\SF\May website 2026\Freelance_Photography_Retoucher_High_End_Fashion\pages'

pages = [
    ('about.html', 'About'),
    ('services.html', 'Services'),
    ('niche.html', 'Fashion'),
    ('portfolio.html', 'Portfolio'),
    ('contact.html', 'Contact')
]

for filename in os.listdir(dir_path):
    if not filename.endswith('.html'):
        continue
    
    filepath = os.path.join(dir_path, filename)
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()

    # --- DESKTOP NAV ---
    # Find the nav block accurately
    nav_match = re.search(r'(<nav class="hidden md:flex[^>]*>)(.*?)(</nav>)', content, re.DOTALL)
    if nav_match:
        nav_open = nav_match.group(1)
        nav_inner = nav_match.group(2)
        nav_close = nav_match.group(3)

        # Extract Home div. It is the first div with 'relative group'. We must match correctly.
        home_div_match = re.search(r'(^\s*<div class="relative group[^>]*>.*?</div>\s*</div>\s*|^\s*<div class="relative group[^>]*>.*?</div>\s*)', nav_inner, re.DOTALL)
        
        home_block = home_div_match.group(1) if home_div_match else ""

        # Remove the home block from inner to find the rest
        rest_of_inner = nav_inner[len(home_block):] if home_block else nav_inner

        # Find classes of existing links
        a_tags = re.findall(r'<a href="([^"]+)"\s*(?:class="([^"]*)")?[^>]*>(.*?)</a>', rest_of_inner, re.IGNORECASE)
        
        active_cls = ""
        inactive_cls = ""
        for href, cls, text in a_tags:
            if href == filename:
                active_cls = cls
            else:
                inactive_cls = cls

        if not inactive_cls and active_cls:
            inactive_cls = active_cls.replace('text-gold-400 font-bold', 'hover:text-gold-400 transition-colors').replace('font-bold', '')
        if not active_cls and inactive_cls:
            if 'hover:text-gold-400' in inactive_cls:
                active_cls = inactive_cls.replace('hover:text-gold-400 transition-colors', 'text-gold-400 font-bold')
            else:
                active_cls = inactive_cls.replace('hover:text-gray-500 transition-colors', 'text-gray-500 font-bold')
        
        if not inactive_cls:
            inactive_cls = "text-xs uppercase tracking-[0.2em] hover:text-gold-400 transition-colors"
            active_cls = "text-xs uppercase tracking-[0.2em] text-gold-400 font-bold"

        new_nav_inner = home_block
        if not new_nav_inner.endswith('\n'): new_nav_inner += '\n'
        for href, text in pages:
            cls = active_cls if href == filename else inactive_cls
            cls = " ".join((cls or "").split())
            class_attr = f' class="{cls}"' if cls else ''
            new_nav_inner += f'                    <a href="{href}"{class_attr}>{text}</a>\n'
        
        content = content.replace(nav_open + nav_inner + nav_close, nav_open + new_nav_inner + "                " + nav_close)

        # Remove duplicate Contact from outside nav if we just added it to nav
        # It's usually <div class="hidden md:flex items-center space-x-6"> <a href="contact.html"...
        # We can just leave it as an "Inquire" button, the prompt says "rearrange the headings like home, about, services, fashion, portfolio, and contact".
        # So having contact in the nav is correct.

    # --- MOBILE MENU ---
    mobile_match = re.search(r'(<div id="mobile-menu"[^>]*>)(.*?)(</header>)', content, re.DOTALL)
    if mobile_match:
        mobile_open = mobile_match.group(1)
        mobile_content = mobile_match.group(2)
        header_close = mobile_match.group(3)

        # The mobile content typically has an inner wrapper div like <div class="px-4 pt-2 pb-6 space-y-2">
        # Let's extract that inner wrapper.
        inner_wrapper_match = re.search(r'(^\s*<div class="px-[^>]*>)(.*?)(\s*</div>\s*</div>\s*$)', mobile_content, re.DOTALL)
        
        if inner_wrapper_match:
            wrapper_open = inner_wrapper_match.group(1)
            wrapper_inner = inner_wrapper_match.group(2)
            wrapper_close = inner_wrapper_match.group(3)

            # Find Home block in mobile
            home_m_match = re.search(r'(^\s*<div class="space-y-1">.*?</div>\s*</div>\s*|^\s*<div class="relative group[^>]*>.*?</div>\s*</div>\s*)', wrapper_inner, re.DOTALL)
            home_m_block = home_m_match.group(1) if home_m_match else ""

            # Find Login block in mobile
            login_m_match = re.search(r'(\s*<div class="border-t[^>]*>.*?</div>\s*$)', wrapper_inner, re.DOTALL)
            login_m_block = login_m_match.group(1) if login_m_match else ""

            # Find links
            # Remove home and login to get the links area
            links_area = wrapper_inner
            if home_m_block: links_area = links_area[len(home_m_block):]
            if login_m_block: links_area = links_area[:-len(login_m_block)]

            a_tags_m = re.findall(r'<a href="([^"]+)"\s*(?:class="([^"]*)")?[^>]*>(.*?)</a>', links_area, re.IGNORECASE)
            m_active = ""
            m_inactive = ""
            for href, cls, text in a_tags_m:
                if href == filename:
                    m_active = cls
                else:
                    m_inactive = cls

            if not m_inactive: m_inactive = "block px-3 py-2 rounded-md text-sm uppercase tracking-[0.2em] text-white"
            if not m_active: m_active = "block px-3 py-2 rounded-md text-sm uppercase tracking-[0.2em] font-bold text-gold-400"

            new_m_inner = home_m_block
            if not new_m_inner.endswith('\n'): new_m_inner += '\n'
            for href, text in pages:
                cls = m_active if href == filename else m_inactive
                cls = " ".join((cls or "").split())
                class_attr = f' class="{cls}"' if cls else ''
                new_m_inner += f'                <a href="{href}"{class_attr}>{text}</a>\n'
            
            if login_m_block: new_m_inner += login_m_block

            new_mobile_content = wrapper_open + new_m_inner + wrapper_close
            content = content.replace(mobile_open + mobile_content + header_close, mobile_open + new_mobile_content + header_close)

    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(content)
    print("Cleaned up", filename)

