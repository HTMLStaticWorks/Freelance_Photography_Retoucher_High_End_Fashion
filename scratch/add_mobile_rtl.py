import os
import re

pages_dir = r"c:\Users\prasa\OneDrive\Desktop\SF\May website 2026\Freelance_Photography_Retoucher_High_End_Fashion\pages"

# Mobile Nav Button Container Pattern
# <div class="lg:hidden flex items-center space-x-4">...<button id="mobile-menu-btn">...</div>
mobile_btn_container_pattern = re.compile(r'(<div class="lg:hidden flex items-center space-x-4">.*?)(<button.*?id="mobile-menu-btn")', re.DOTALL)

rtl_button = """        <button class="rtl-toggle text-xs font-bold px-3 py-1 rounded-full hover:bg-gray-100 dark:hover:bg-gray-800 transition-all transform hover:scale-110 active:scale-95">
         RTL
        </button>\n       """

for filename in os.listdir(pages_dir):
    if filename.endswith(".html"):
        filepath = os.path.join(pages_dir, filename)
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Add RTL button if not already there
        if 'rtl-toggle' in content and 'lg:hidden' in content:
            # Check if RTL toggle is already in the mobile section (to avoid duplicates)
            mobile_section = mobile_btn_container_pattern.search(content)
            if mobile_section and 'rtl-toggle' not in mobile_section.group(1):
                content = mobile_btn_container_pattern.sub(r'\1' + rtl_button + r'\2', content)
                
                with open(filepath, 'w', encoding='utf-8') as f:
                    f.write(content)
                print(f"Added RTL to {filename}")
