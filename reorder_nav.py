import os
import re

dir_path = r'c:\Users\prasa\OneDrive\Desktop\SF\May website 2026\Freelance_Photography_Retoucher_High_End_Fashion\pages'

def process_file(filepath):
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()

    # Desktop Nav reorder
    # Find the nav block
    nav_match = re.search(r'(<nav class="hidden md:flex space-x-10 items-center">.*?</nav>)', content, re.DOTALL)
    if nav_match:
        nav_block = nav_match.group(1)
        
        # Extract the lines containing the 4 links
        portfolio_line = re.search(r'([ \t]*<a href="portfolio\.html".*?</a>\n?)', nav_block)
        fashion_line = re.search(r'([ \t]*<a href="niche\.html".*?</a>\n?)', nav_block)
        services_line = re.search(r'([ \t]*<a href="services\.html".*?</a>\n?)', nav_block)
        about_line = re.search(r'([ \t]*<a href="about\.html".*?>)Atelier(</a>\n?)', nav_block)
        
        if portfolio_line and fashion_line and services_line and about_line:
            # Change Atelier to About
            about_text = about_line.group(1) + "About" + about_line.group(2)
            
            # The order should be About, Services, Fashion, Portfolio
            new_lines = about_text + services_line.group(1) + fashion_line.group(1) + portfolio_line.group(1)
            
            # Remove the old lines from the block
            new_nav_block = nav_block.replace(portfolio_line.group(1), "")
            new_nav_block = new_nav_block.replace(fashion_line.group(1), "")
            new_nav_block = new_nav_block.replace(services_line.group(1), "")
            new_nav_block = new_nav_block.replace(about_line.group(0), "")
            
            # Insert the new lines after the Home div
            # The home div ends with '</div>' and is followed by whitespace
            home_div_end = re.search(r'(</div>\s*)\z', new_nav_block.replace('</nav>', ''))
            if home_div_end:
                new_nav_block = new_nav_block.replace('</nav>', new_lines + '                </nav>')
            else:
                # Fallback, just insert before </nav>
                new_nav_block = new_nav_block.replace('</nav>', new_lines + '                </nav>')
                
            content = content.replace(nav_block, new_nav_block)

    # Mobile Nav reorder
    mobile_match = re.search(r'(<div id="mobile-menu".*?</div>\s*</div>)', content, re.DOTALL)
    if mobile_match:
        mobile_block = mobile_match.group(1)
        
        portfolio_m = re.search(r'([ \t]*<a href="portfolio\.html".*?</a>\n?)', mobile_block)
        fashion_m = re.search(r'([ \t]*<a href="niche\.html".*?</a>\n?)', mobile_block)
        services_m = re.search(r'([ \t]*<a href="services\.html".*?</a>\n?)', mobile_block)
        about_m = re.search(r'([ \t]*<a href="about\.html".*?>)Atelier(</a>\n?)', mobile_block)
        contact_m = re.search(r'([ \t]*<a href="contact\.html".*?</a>\n?)', mobile_block)
        
        if portfolio_m and fashion_m and services_m and about_m and contact_m:
            about_text_m = about_m.group(1) + "About" + about_m.group(2)
            
            new_lines_m = about_text_m + services_m.group(1) + fashion_m.group(1) + portfolio_m.group(1) + contact_m.group(1)
            
            new_mobile_block = mobile_block.replace(portfolio_m.group(1), "")
            new_mobile_block = new_mobile_block.replace(fashion_m.group(1), "")
            new_mobile_block = new_mobile_block.replace(services_m.group(1), "")
            new_mobile_block = new_mobile_block.replace(about_m.group(0), "")
            new_mobile_block = new_mobile_block.replace(contact_m.group(1), "")
            
            # insert before the closing div of the inner container
            new_mobile_block = new_mobile_block.replace('            </div>\n        </div>', new_lines_m + '            </div>\n        </div>')
            
            content = content.replace(mobile_block, new_mobile_block)

    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(content)
        
    print(f"Processed {filepath}")

for filename in os.listdir(dir_path):
    if filename.endswith('.html'):
        process_file(os.path.join(dir_path, filename))

