import os

pages_dir = r"c:\Users\prasa\OneDrive\Desktop\SF\May website 2026\Freelance_Photography_Retoucher_High_End_Fashion\pages"

for filename in os.listdir(pages_dir):
    if filename.endswith(".html"):
        filepath = os.path.join(pages_dir, filename)
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Fix the "Home" header in mobile menu
        old_header = '<span class="block px-3 py-2 rounded-md text-sm uppercase tracking-[0.2em] font-bold text-white">\n       Home\n      </span>'
        new_header = '<span class="block px-3 py-2 rounded-md text-sm uppercase tracking-[0.2em] font-bold text-black dark:text-white">\n       Home\n      </span>'
        
        if old_header in content:
            content = content.replace(old_header, new_header)
            with open(filepath, 'w', encoding='utf-8') as f:
                f.write(content)
            print(f"Fixed Home header in {filename}")
        else:
            # Try without exact whitespace
            old_header_alt = 'font-bold text-white">\n       Home'
            new_header_alt = 'font-bold text-black dark:text-white">\n       Home'
            if old_header_alt in content:
                content = content.replace(old_header_alt, new_header_alt)
                with open(filepath, 'w', encoding='utf-8') as f:
                    f.write(content)
                print(f"Fixed Home header (alt) in {filename}")
