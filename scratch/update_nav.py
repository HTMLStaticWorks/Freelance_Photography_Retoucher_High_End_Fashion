import os
import re

pages_dir = r"c:\Users\prasa\OneDrive\Desktop\SF\May website 2026\Freelance_Photography_Retoucher_High_End_Fashion\pages"
files_to_update = [
    "service-details.html",
    "pricing.html",
    "niche.html",
    "blog.html",
    "blog-details.html",
    "404.html"
]

login_btn_desktop = """       <a class="bg-black dark:bg-white text-white dark:text-black px-6 py-2 rounded-full text-sm font-bold hover:scale-105 transition-all shadow-md ml-2" href="login.html">
        Login
       </a>"""

login_btn_mobile = """      <div class="border-t border-gray-200 dark:border-gray-700 pt-4 pb-2 space-y-3">
       <a class="block w-full text-center bg-black dark:bg-white text-white dark:text-black px-6 py-3 rounded-xl text-sm font-bold" href="login.html">
        Login
       </a>
       <a class="block w-full text-center border border-gray-200 dark:border-gray-700 text-black dark:text-white px-6 py-3 rounded-xl text-sm font-bold" href="dashboard.html">
        Client Portal
       </a>
      </div>"""

for filename in files_to_update:
    filepath = os.path.join(pages_dir, filename)
    if not os.path.exists(filepath):
        continue
        
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
        
    # 1. Update Desktop Nav (Insert after RTL button)
    rtl_pattern = re.compile(r'(<button class="rtl-toggle.*?</button>)', re.DOTALL)
    if 'href="login.html"' not in content:
        content = rtl_pattern.sub(r'\1\n' + login_btn_desktop, content)
        
    # 2. Update Mobile Nav (Replace Client Portal block or empty block)
    mobile_pattern = re.compile(r'<div class="border-t border-gray-200 dark:border-gray-700 pt-2 pb-2">.*?</div>', re.DOTALL)
    if 'href="login.html"' not in content:
        content = mobile_pattern.sub(login_btn_mobile, content)
        
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(content)
        print(f"Updated {filename}")
