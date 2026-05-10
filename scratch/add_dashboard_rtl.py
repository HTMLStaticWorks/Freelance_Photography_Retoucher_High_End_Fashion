import os

filepath = r"c:\Users\prasa\OneDrive\Desktop\SF\May website 2026\Freelance_Photography_Retoucher_High_End_Fashion\pages\dashboard.html"

rtl_button = """       <button class="rtl-toggle text-xs font-bold px-3 py-1 rounded-full hover:bg-gray-100 dark:hover:bg-gray-800 transition-all transform hover:scale-110 active:scale-95">
        RTL
       </button>"""

with open(filepath, 'r', encoding='utf-8') as f:
    content = f.read()

if 'rtl-toggle' not in content:
    # Find the theme toggle button end and insert RTL button after it
    if '</button>' in content:
        # We need to find the specific one in the header
        header_part = content.split('<header')[1].split('</header')[0]
        if 'theme-toggle' in header_part:
            new_header_part = header_part.replace('</button>', '</button>\n' + rtl_button, 1)
            content = content.replace(header_part, new_header_part)
            with open(filepath, 'w', encoding='utf-8') as f:
                f.write(content)
            print("Added RTL toggle to dashboard.html")
