import os

files = [
    r"c:\Users\prasa\OneDrive\Desktop\SF\May website 2026\Freelance_Photography_Retoucher_High_End_Fashion\pages\login.html",
    r"c:\Users\prasa\OneDrive\Desktop\SF\May website 2026\Freelance_Photography_Retoucher_High_End_Fashion\pages\signup.html"
]

controls_html = """    <!-- Theme & RTL Controls -->
    <div class="fixed top-6 right-6 z-50 flex items-center space-x-4">
        <button class="theme-toggle p-2 rounded-full bg-black/10 dark:bg-white/10 backdrop-blur-md border border-black/10 dark:border-white/20 text-black dark:text-white hover:bg-black/20 dark:hover:bg-white/20 transition-all transform hover:rotate-12 active:scale-90">
            <i class="ph ph-moon text-xl dark:hidden"></i>
            <i class="ph ph-sun text-xl hidden dark:block"></i>
        </button>
        <button class="rtl-toggle text-xs font-bold px-3 py-2 rounded-full bg-black/10 dark:bg-white/10 backdrop-blur-md border border-black/10 dark:border-white/20 text-black dark:text-white hover:bg-black/20 dark:hover:bg-white/20 transition-all transform hover:scale-110 active:scale-95">
            RTL
        </button>
    </div>"""

for filepath in files:
    if os.path.exists(filepath):
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()
        
        if 'rtl-toggle' not in content:
            if '<body' in content:
                # Insert after <body ...>
                parts = content.split('>', 1)
                new_content = parts[0] + '>\n' + controls_html + parts[1]
                with open(filepath, 'w', encoding='utf-8') as f:
                    f.write(new_content)
                print(f"Added controls to {os.path.basename(filepath)}")
