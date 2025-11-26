from PIL import Image
import os

MEDIA = os.path.join(os.path.dirname(__file__), '..', 'Content', 'articles', 'Visual Studio Helper', 'media')
MEDIA = os.path.abspath(MEDIA)

count = 0
for name in os.listdir(MEDIA):
    if name.lower().endswith('.jpeg') or name.lower().endswith('.jpg'):
        src = os.path.join(MEDIA, name)
        target = os.path.splitext(src)[0] + '.png'
        try:
            with Image.open(src) as im:
                im.convert('RGBA').save(target, 'PNG')
            print(f'Converted: {name} -> {os.path.basename(target)}')
            count += 1
        except Exception as e:
            print('Failed to convert', name, e)

print(f'Done. Converted {count} file(s).')
