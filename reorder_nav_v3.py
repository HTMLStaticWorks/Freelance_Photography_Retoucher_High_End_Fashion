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

    # Find desktop nav
    nav_match = re.search(r'(<nav[^>]*>)(.*?)(</nav>)', content, re.DOTALL)
    if nav_match:
        nav_open = nav_match.group(1)
        nav_inner = nav_match.group(2)
        nav_close = nav_match.group(3)

        # The inner usually has the Home div and then some <a> tags.
        # Let's find the Home div. It starts with <div class="relative group... and ends with </div>
        # But there might be other divs.
        # Let's just find all top-level <a> tags in nav_inner that are not 'Home'.
        # Actually, let's just extract the classes used for links.
        a_tags = re.findall(r'<a href="([^"]+)"\s*(?:class="([^"]*)")?[^>]*>(.*?)</a>', nav_inner, re.IGNORECASE)
        
        active_class = ""
        inactive_class = ""
        
        for href, cls, text in a_tags:
            if href in ['index.html', 'home2.html'] or 'Home' in text:
                continue
            if href == filename:
                active_class = cls if cls else ""
            else:
                inactive_class = cls if cls else ""

        # If we couldn't find an inactive class, fallback
        if not inactive_class and active_class:
            inactive_class = active_class.replace('text-gold-400 font-bold', 'hover:text-gold-400 transition-colors').replace('font-bold', '')
        
        # If we couldn't find an active class, fallback
        if not active_class and inactive_class:
            active_class = inactive_class.replace('hover:text-gray-500', '').replace('hover:text-gold-400', 'text-gold-400 font-bold') + ' font-bold'

        # Build new links string
        new_links_html = "\n"
        for href, text in pages:
            cls = active_class if href == filename else inactive_class
            # cleanup double spaces in class
            cls = " ".join(cls.split())
            class_attr = f' class="{cls}"' if cls else ''
            new_links_html += f'                    <a href="{href}"{class_attr}>{text}</a>\n'

        # Now replace everything after the Home div in nav_inner
        # The Home div is usually <div class="relative group h-full inline-flex items-center">...</div>
        # We can match it with regex:
        home_div_match = re.search(r'(<div class="relative group[^>]*>.*?</div>\s*</div>)', nav_inner, re.DOTALL)
        if not home_div_match:
            # Maybe it's just <div class="relative group...">...</div> (without the extra inner div?)
            home_div_match = re.search(r'(<div class="relative group[^>]*>.*?</div>)', nav_inner, re.DOTALL)

        if home_div_match:
            new_nav_inner = home_div_match.group(1) + new_links_html + "                "
            content = content.replace(nav_open + nav_inner + nav_close, nav_open + "\n                " + new_nav_inner + nav_close)

    # Find mobile menu
    mobile_match = re.search(r'(<div id="mobile-menu"[^>]*>)(.*?)(</div>\s*</header>)', content, re.DOTALL)
    if mobile_match:
        mobile_open = mobile_match.group(1)
        mobile_inner = mobile_match.group(2)
        mobile_close = mobile_match.group(3)

        # Mobile inner has a Home block
        # <div class="space-y-1">...</div> or <div class="relative group...
        home_block_match = re.search(r'(<div class="space-y-1">.*?</div>\s*</div>|<div class="relative group[^>]*>.*?</div>\s*</div>)', mobile_inner, re.DOTALL)
        
        if home_block_match:
            # Extract classes
            m_a_tags = re.findall(r'<a href="([^"]+)"\s*(?:class="([^"]*)")?[^>]*>(.*?)</a>', mobile_inner, re.IGNORECASE)
            m_active_class = ""
            m_inactive_class = ""
            for href, cls, text in m_a_tags:
                if href in ['index.html', 'home2.html'] or 'Home' in text or 'Login' in text or 'Portal' in text:
                    continue
                if href == filename:
                    m_active_class = cls if cls else ""
                else:
                    m_inactive_class = cls if cls else ""

            if not m_inactive_class: m_inactive_class = "block px-3 py-2 rounded-md text-sm uppercase tracking-[0.2em] text-white"
            if not m_active_class: m_active_class = "block px-3 py-2 rounded-md text-sm uppercase tracking-[0.2em] font-bold text-gold-400"

            new_m_links = "\n"
            for href, text in pages:
                cls = m_active_class if href == filename else m_inactive_class
                cls = " ".join(cls.split())
                class_attr = f' class="{cls}"' if cls else ''
                new_m_links += f'                <a href="{href}"{class_attr}>{text}</a>\n'

            # Keep the login/portal block if it exists
            login_block_match = re.search(r'(<div class="border-t[^>]*>.*?</div>)', mobile_inner, re.DOTALL)
            login_block = "\n                " + login_block_match.group(1) + "\n            " if login_block_match else ""

            # Replace inside the first <div class="px... ">
            inner_container_match = re.search(r'(<div class="px-[^>]*>)(.*?)(</div>)', mobile_inner, re.DOTALL)
            if inner_container_match:
                new_container_inner = "\n                " + home_block_match.group(1) + new_m_links + login_block
                new_mobile_inner = mobile_inner.replace(inner_container_match.group(2), new_container_inner)
                content = content.replace(mobile_open + mobile_inner + mobile_close, mobile_open + new_mobile_inner + mobile_close)

    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(content)
    print("Processed", filename)

