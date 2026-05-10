import os
import re

dir_path = r'c:\Users\prasa\OneDrive\Desktop\SF\May website 2026\Freelance_Photography_Retoucher_High_End_Fashion\pages'

def process_file(filepath):
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()

    changed = False

    # Desktop Nav reorder
    nav_match = re.search(r'(<nav class="hidden md:flex[^>]*>.*?</nav>)', content, re.DOTALL)
    if nav_match:
        nav_block = nav_match.group(1)
        
        portfolio_line = re.search(r'([ \t]*<a href="portfolio\.html".*?</a>\n?)', nav_block)
        fashion_line = re.search(r'([ \t]*<a href="niche\.html".*?</a>\n?)', nav_block)
        services_line = re.search(r'([ \t]*<a href="services\.html".*?</a>\n?)', nav_block)
        about_line = re.search(r'([ \t]*<a href="about\.html".*?>)(?:Atelier|About)(</a>\n?)', nav_block)
        
        if portfolio_line and about_line:
            about_text = about_line.group(1) + "About" + about_line.group(2)
            
            new_lines = about_text
            if services_line: new_lines += services_line.group(1)
            if fashion_line: new_lines += fashion_line.group(1)
            new_lines += portfolio_line.group(1)
            
            new_nav_block = nav_block
            new_nav_block = new_nav_block.replace(portfolio_line.group(1), "")
            if fashion_line: new_nav_block = new_nav_block.replace(fashion_line.group(1), "")
            if services_line: new_nav_block = new_nav_block.replace(services_line.group(1), "")
            new_nav_block = new_nav_block.replace(about_line.group(0), "")
            
            nav_end_idx = new_nav_block.rfind('</nav>')
            if nav_end_idx != -1:
                new_nav_block = new_nav_block[:nav_end_idx] + new_lines + "                " + new_nav_block[nav_end_idx:]
            
            content = content.replace(nav_block, new_nav_block)
            changed = True

    # Mobile Nav reorder
    mobile_match = re.search(r'(<div id="mobile-menu".*?</div>\s*</div>)', content, re.DOTALL)
    if mobile_match:
        mobile_block = mobile_match.group(1)
        
        portfolio_m = re.search(r'([ \t]*<a href="portfolio\.html".*?</a>\n?)', mobile_block)
        fashion_m = re.search(r'([ \t]*<a href="niche\.html".*?</a>\n?)', mobile_block)
        services_m = re.search(r'([ \t]*<a href="services\.html".*?</a>\n?)', mobile_block)
        about_m = re.search(r'([ \t]*<a href="about\.html".*?>)(?:Atelier|About)(</a>\n?)', mobile_block)
        contact_m = re.search(r'([ \t]*<a href="contact\.html".*?</a>\n?)', mobile_block)
        
        if portfolio_m and about_m:
            about_text_m = about_m.group(1) + "About" + about_m.group(2)
            
            new_lines_m = about_text_m
            if services_m: new_lines_m += services_m.group(1)
            if fashion_m: new_lines_m += fashion_m.group(1)
            new_lines_m += portfolio_m.group(1)
            if contact_m: new_lines_m += contact_m.group(1)
            
            new_mobile_block = mobile_block
            new_mobile_block = new_mobile_block.replace(portfolio_m.group(1), "")
            if fashion_m: new_mobile_block = new_mobile_block.replace(fashion_m.group(1), "")
            if services_m: new_mobile_block = new_mobile_block.replace(services_m.group(1), "")
            new_mobile_block = new_mobile_block.replace(about_m.group(0), "")
            if contact_m: new_mobile_block = new_mobile_block.replace(contact_m.group(1), "")
            
            last_div_idx = new_mobile_block.rfind('</div>')
            prev_div_idx = new_mobile_block.rfind('</div>', 0, last_div_idx)
            if prev_div_idx != -1:
                new_mobile_block = new_mobile_block[:prev_div_idx] + new_lines_m + "            " + new_mobile_block[prev_div_idx:]
            
            content = content.replace(mobile_block, new_mobile_block)
            changed = True

    if changed:
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(content)
        print(f"Processed {filepath}")

for filename in os.listdir(dir_path):
    if filename.endswith('.html'):
        process_file(os.path.join(dir_path, filename))

