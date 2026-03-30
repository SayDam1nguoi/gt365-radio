import re

file_path = r'c:\Users\admin\Desktop\ProjectSekai\gt365 radio\giao_dien\styles.py'
with open(file_path, 'r', encoding='utf-8') as f:
    text = f.read()

# Make corners square
text = re.sub(r'--r:\s*16px;', '--r:            0px;', text)
text = re.sub(r'--r-sm:\s*10px;', '--r-sm:         0px;', text)
text = re.sub(r'--r-xs:\s*7px;', '--r-xs:         0px;', text)
text = re.sub(r'border-radius:\s*999px( !important)?(;\n)', r'border-radius: 0px\1\2', text)
text = re.sub(r'border-radius:\s*var\(--r\) var\(--r\) 0 0;', 'border-radius: 0px;', text)
text = re.sub(r'border-radius:\s*0 0 var\(--r\) var\(--r\);', 'border-radius: 0px;', text)
text = re.sub(r'border-radius:\s*3px;', 'border-radius: 0px;', text)

# Remove background circle gradients which look modern-bubbly
text = re.sub(r'background:\s*radial-gradient\(circle,.*?\);', 'background: transparent;', text)

# Sharp shadows and borders to feel 'more website-like'
text = re.sub(r'--shadow-sm:.*?;', '--shadow-sm:    0 1px 2px rgba(0,0,0,0.1), 0 0 0 1px rgba(0,0,0,0.05);', text)
text = re.sub(r'--shadow:.*?;', '--shadow:       0 8px 30px rgba(0,0,0,0.08), 0 0 0 1px rgba(0,0,0,0.05);', text)
text = re.sub(r'--shadow-lg:.*?;', '--shadow-lg:    0 15px 45px rgba(0,0,0,0.1);', text)

with open(file_path, 'w', encoding='utf-8') as f:
    f.write(text)

print('Updated styles successfully.')
