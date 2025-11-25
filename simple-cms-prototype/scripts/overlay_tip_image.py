from PIL import Image, ImageDraw, ImageFont
import os
import textwrap

# Paths
ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
source_image = os.path.join(ROOT, 'media', 'image-2.jpeg')
output_image = os.path.join(ROOT, 'Content', 'articles', 'Visual Studio Helper', 'media', 'image4.png')

# Tip text
tip_text = """Tip
Another way to download content locally so you can view it when you don't have an internet connection is to download a PDF version of it. Many documentation sets on Microsoft Learn include a link at the bottom of the table of contents to download a PDF file that contains all the articles for that TOC."""

# Load the source image
img = Image.open(source_image)
width, height = img.size

# Create a drawing context
draw = ImageDraw.Draw(img)

# Calculate tip box dimensions
padding = 20
box_width = width - (2 * padding)
tip_y_start = padding

# Try to load a font (fallback to default if not available)
try:
    font = ImageFont.truetype("arial.ttf", 14)
    title_font = ImageFont.truetype("arialbd.ttf", 16)
except:
    font = ImageFont.load_default()
    title_font = ImageFont.load_default()

# Wrap text
wrapped_lines = textwrap.wrap(tip_text, width=80)

# Calculate box height
line_height = 20
box_height = (len(wrapped_lines) + 1) * line_height + (2 * padding)

# Draw semi-transparent background box for tip
box_coords = [padding, tip_y_start, padding + box_width, tip_y_start + box_height]
overlay = Image.new('RGBA', img.size, (255, 255, 255, 0))
overlay_draw = ImageDraw.Draw(overlay)
overlay_draw.rectangle(box_coords, fill=(255, 248, 220, 230), outline=(255, 165, 0, 255), width=2)

# Composite overlay onto image
img = img.convert('RGBA')
img = Image.alpha_composite(img, overlay)
draw = ImageDraw.Draw(img)

# Draw text
text_y = tip_y_start + padding
for line in wrapped_lines:
    draw.text((padding + 10, text_y), line, fill=(0, 0, 0), font=font)
    text_y += line_height

# Convert back to RGB and save
img = img.convert('RGB')
img.save(output_image)
print(f"Created: {output_image}")
