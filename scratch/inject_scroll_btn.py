import os

pages_dir = r"c:\Users\prasa\OneDrive\Desktop\SF\May website 2026\Freelance_Photography_Retoucher_High_End_Fashion\pages"
button_html = '\n  <button id="back-to-top" class="back-to-top" aria-label="Back to top">\n    <i class="ph ph-caret-up"></i>\n  </button>\n'

for filename in os.listdir(pages_dir):
    if filename.endswith(".html"):
        filepath = os.path.join(pages_dir, filename)
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()
        
        if 'id="back-to-top"' not in content:
            if '</body>' in content:
                content = content.replace('</body>', button_html + ' </body>')
                with open(filepath, 'w', encoding='utf-8') as f:
                    f.write(content)
                print(f"Injected into {filename}")
