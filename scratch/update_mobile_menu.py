import os
import re

pages_dir = r"c:\Users\prasa\OneDrive\Desktop\SF\May website 2026\Freelance_Photography_Retoucher_High_End_Fashion\pages"

# Breakpoint Update Patterns
patterns = [
    (r'class="hidden md:flex', 'class="hidden lg:flex'),
    (r'class="md:hidden flex', 'class="lg:hidden flex'),
    (r'class="hidden md:hidden', 'class="hidden lg:hidden'),
]

# Mobile Nav Link Pattern
# <a class="block ... mobile-nav-link" href="...">Name</a> 
# -> <a class="flex items-center ... mobile-nav-link" href="..."><i class="ph ph-list mr-2"></i>Name</a>
nav_link_pattern = re.compile(r'<a class="block (.*?)mobile-nav-link(.*?)href="(.*?)">\s*(.*?)\s*</a>', re.DOTALL)

for filename in os.listdir(pages_dir):
    if filename.endswith(".html"):
        filepath = os.path.join(pages_dir, filename)
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # 1. Update Breakpoints
        for old, new in patterns:
            content = content.replace(old, new)
            
        # 2. Add Icons to Mobile Nav Links
        def add_icon(match):
            classes_before = match.group(1)
            classes_after = match.group(2)
            href = match.group(3)
            text = match.group(4).strip()
            
            # Avoid double icons
            if '<i class="ph ph-list' in text:
                return match.group(0)
                
            return f'<a class="flex items-center {classes_before}mobile-nav-link{classes_after}href="{href}">\n      <i class="ph ph-list mr-2"></i>\n      {text}\n     </a>'

        content = nav_link_pattern.sub(add_icon, content)
        
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(content)
        print(f"Updated {filename}")
