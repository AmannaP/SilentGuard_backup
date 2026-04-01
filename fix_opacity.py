import os, re
d = 'lib/screens'
for f in os.listdir(d):
    if f.endswith('.dart'):
        filepath = os.path.join(d, f)
        with open(filepath, 'r', encoding='utf-8') as file:
            content = file.read()
        
        # Avoid overriding auth_service.dart completely if it's 0 bytes
        if len(content) == 0 and f != 'auth_service.dart':
            continue
            
        new_content = re.sub(r'\.withOpacity\(([^)]+)\)', r'.withValues(alpha: \1)', content)
        
        if new_content != content:
            with open(filepath, 'w', encoding='utf-8') as file:
                file.write(new_content)
