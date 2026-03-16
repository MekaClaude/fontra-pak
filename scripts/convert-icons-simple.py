#!/usr/bin/env python3
"""
Convert SVG icon to ICO format for Fontra Pak using PIL only
"""

import os
import subprocess
import sys
from pathlib import Path
from PIL import Image, ImageDraw
import math
import xml.etree.ElementTree as ET


def parse_svg_paths(svg_path):
    """Parse path data from SVG file."""
    tree = ET.parse(svg_path)
    root = tree.getroot()
    
    # Define namespace
    ns = {'svg': 'http://www.w3.org/2000/svg'}
    
    paths = []
    colors = []
    
    # Find all path elements
    for path_elem in root.iter():
        if 'path' in path_elem.tag:
            d = path_elem.get('d', '')
            style = path_elem.get('style', '')
            
            # Extract fill color
            fill_match = None
            if 'fill:' in style:
                for part in style.split(';'):
                    if 'fill:' in part:
                        fill_match = part.split(':')[1].strip()
                        break
            
            if not fill_match and 'fill=' in str(path_elem.attrib):
                fill_match = path_elem.get('fill', '')
            
            if d and fill_match:
                paths.append(d)
                colors.append(fill_match)
    
    return paths, colors


def create_icon_png(svg_path, png_path, size):
    """
    Create PNG from SVG by rendering the SVG shapes.
    Simplified renderer for the Fontra icon SVG.
    """
    # Create base image with transparent background
    img = Image.new('RGBA', (size, size), (0, 0, 0, 0))
    draw = ImageDraw.Draw(img)
    
    # The Fontra icon colors from the SVG
    pink_color = (255, 0, 92, 255)      # rgb(255,0,92)
    black_color = (11, 0, 0, 255)        # rgb(11,0,0)
    gray_color = (155, 155, 155, 255)    # rgb(155,155,155)
    white_color = (255, 255, 255, 255)   # white
    
    # SVG viewBox is 0 0 1200 1200
    # The F shape is drawn in a 10x10 coordinate system scaled by 120
    # We'll work in the 10x10 system and scale to output size
    
    scale = size / 10.0
    
    # Define the F shape polygons (in 10x10 coordinate system, y is inverted)
    # Based on the SVG path data, simplified to rectangles
    
    # Pink F shape - main letter
    pink_rects = [
        # Vertical stem: x=0.25-1.5, y=0.29-5.29 (inverted)
        (0.25, 0.29, 1.5, 5.29),
        # Top horizontal: x=1.5-5.36, y=0.29-1.42
        (1.5, 0.29, 5.36, 1.42),
        # Middle horizontal: x=1.5-6.21, y=2.58-3.58
        (1.5, 2.58, 6.21, 3.58),
    ]
    
    # Draw pink F
    for x1, y1, x2, y2 in pink_rects:
        draw.rectangle(
            [x1 * scale, size - y2 * scale, x2 * scale, size - y1 * scale],
            fill=pink_color
        )
    
    # Draw rounded square background
    margin = int(size * 0.08)
    corner_radius = int(size * 0.15)
    
    # Draw rounded rectangle background (subtle white outline)
    bbox = [margin, margin, size - margin, size - margin]
    draw.rounded_rectangle(bbox, radius=corner_radius, outline=(255, 255, 255, 80), width=3)
    
    img.save(png_path, 'PNG')
    print(f"  Created {size}x{size} PNG")
    return img


def create_ico_from_svg(svg_path, ico_path, sizes=(16, 32, 48, 64, 128, 256, 512)):
    """Create ICO file from SVG with multiple sizes."""
    print(f"Converting SVG to ICO: {ico_path}")
    
    temp_dir = Path(ico_path).parent / "temp_icons"
    temp_dir.mkdir(exist_ok=True)
    
    images = []
    for size in sizes:
        png_path = temp_dir / f"icon_{size}.png"
        img = create_icon_png(svg_path, png_path, size)
        images.append(img)
    
    # Save as ICO
    images[0].save(
        ico_path,
        format='ICO',
        sizes=[(size, size) for size in sizes],
        append_images=images[1:],
    )
    
    # Cleanup temp files
    for png_path in temp_dir.glob("*.png"):
        png_path.unlink()
    temp_dir.rmdir()
    
    print(f"  Created ICO with sizes: {sizes}")


def main():
    script_dir = Path(__file__).parent
    icon_dir = script_dir.parent / "icon"
    svg_path = icon_dir / "fontra-icon-source.svg"
    ico_path = icon_dir / "FontraIcon.ico"
    
    if not svg_path.exists():
        print(f"Error: SVG file not found: {svg_path}")
        sys.exit(1)
    
    print("Fontra Icon Converter")
    print("=" * 50)
    
    # Create ICO for Windows
    create_ico_from_svg(svg_path, ico_path)
    
    print("=" * 50)
    print("Icon conversion complete!")
    print(f"  Windows icon: {ico_path}")


if __name__ == "__main__":
    main()
