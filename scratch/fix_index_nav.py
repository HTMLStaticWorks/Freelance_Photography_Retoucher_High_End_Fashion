import os

file_path = r'c:\Users\prasa\OneDrive\Desktop\SF\May website 2026\Freelance_Photography_Retoucher_High_End_Fashion\index.html'

with open(file_path, 'r', encoding='utf-8') as f:
    lines = f.readlines()

new_lines = []
for line in lines:
    new_lines.append(line)
    if 'href="login.html"' in line and 'nav-link' not in line and 'block w-full' not in line:
        # This matches the desktop login link (the one in the Actions div)
        # We check for 'block w-full' to avoid matching the mobile one which we already fixed
        # or we check line by line and detect the div.
        pass

# Let's be more precise
output = []
in_actions = False
found = False
for i, line in enumerate(lines):
    if '<!-- Actions -->' in line:
        in_actions = True
    if in_actions and 'href="login.html"' in line and not found:
        output.append(line)
        # Add the next line (Login) and the next (</a>)
        # Actually just add the button after the </a> of login
        continue
    
    if in_actions and '</a>' in line and i > 0 and 'href="login.html"' in lines[i-2]:
         output.append(line)
         indent = line[:line.find('</a>')]
         output.append(f'{indent}<a class="bg-black dark:bg-white text-white dark:text-black px-5 py-2 rounded-full text-sm font-medium hover:bg-gray-800 dark:hover:bg-gray-200 transition-all transform hover:scale-105 ml-2" href="dashboard.html">\n')
         output.append(f'{indent} Client Portal\n')
         output.append(f'{indent}</a>\n')
         found = True
         in_actions = False # Stop looking
         continue
    
    output.append(line)

with open(file_path, 'w', encoding='utf-8') as f:
    f.writelines(output)
print("Successfully updated index.html")
