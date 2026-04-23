import codecs
import os

os.chdir('Kotti')

def read(*parts):
    with codecs.open(os.path.join(*parts), 'rb', 'utf-8') as f:
        return f.read()

long_description = '\n\n'.join([read('README.rst'), read('AUTHORS.txt'), read('CHANGES.txt')])

# 检查换行符
print('Checking line endings...')
lines = long_description.split('\n')
print(f'Total lines: {len(lines)}')

# 检查第536行
if len(lines) > 536:
    line_536 = lines[535]
    print(f'Line 536: {repr(line_536)}')
    print(f'Line 536 bytes: {line_536.encode("utf-8")}')

    # 检查前后几行
    print('\nLines 534-538:')
    for i in range(533, min(538, len(lines))):
        print(f'Line {i+1}: {repr(lines[i][:50])}')
