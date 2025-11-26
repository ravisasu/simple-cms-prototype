from PIL import Image, ImageDraw, ImageFont
import os

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
media_folder = os.path.join(ROOT, 'Content', 'articles', 'Visual Studio Helper', 'media')

# List of missing images with their formats
missing_images = [
    ('image5.png', 'PNG', (650, 325)),
    ('image6.png', 'PNG', (659, 412)),
    ('image7.png', 'PNG', (662, 497)),
    ('image8.png', 'PNG', (50, 50)),
    ('image9.png', 'PNG', (20, 20)),
    ('image11.png', 'PNG', (20, 20)),
    ('image13.png', 'PNG', (20, 20)),
    ('image14.png', 'PNG', (700, 337)),
    ('image15.png', 'PNG', (552, 127)),
    ('image16.png', 'PNG', (404, 385)),
    ('image17.png', 'PNG', (660, 281)),
    ('image18.png', 'PNG', (50, 50)),
    ('image19.png', 'PNG', (660, 510)),
    ('image20.png', 'PNG', (80, 80)),
]

for filename, format_type, size in missing_images:
    filepath = os.path.join(media_folder, filename)
    
    # Create a new image with light gray background
    img = Image.new('RGB', size, color=(240, 240, 240))
    draw = ImageDraw.Draw(img)
    
    # Draw border
    draw.rectangle([(0, 0), (size[0]-1, size[1]-1)], outline=(180, 180, 180), width=2)
    
    # Add text label
    try:
        font = ImageFont.truetype("arial.ttf", min(size[0]//15, size[1]//5, 24))
    except:
        font = ImageFont.load_default()
    
    text = f"Placeholder\n{filename}"
    
    # Get text bounding box for centering
    bbox = draw.textbbox((0, 0), text, font=font)
    text_width = bbox[2] - bbox[0]
    text_height = bbox[3] - bbox[1]
    
    position = ((size[0] - text_width) // 2, (size[1] - text_height) // 2)
    draw.text(position, text, fill=(100, 100, 100), font=font, align='center')
    
    # Save
    if format_type == 'JPEG':
        img.save(filepath, 'JPEG', quality=85)
    else:
        img.save(filepath, 'PNG')
    
    print(f"Created: {filename}")

print(f"\nAll placeholder images created in: {media_folder}")
