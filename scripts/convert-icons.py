#!/usr/bin/env python3
"""
Convert SVG icon to ICO and ICNS formats for Fontra Pak
"""

import os
import subprocess
import sys
from pathlib import Path

try:
    from PIL import Image
    import cairosvg
except ImportError:
    print("Installing required packages...")
    subprocess.check_call([sys.executable, "-m", "pip", "install", "pillow", "cairosvg"])
    from PIL import Image
    import cairosvg


def convert_svg_to_png(svg_path, png_path, size):
    """Convert SVG to PNG at specified size."""
    cairosvg.svg2png(
        url=svg_path,
        write_to=png_path,
        output_width=size,
        output_height=size,
    )
    print(f"  Created {size}x{size} PNG")


def create_ico_from_svg(svg_path, ico_path, sizes=(16, 32, 48, 64, 128, 256, 512)):
    """Create ICO file from SVG with multiple sizes."""
    print(f"Converting SVG to ICO: {ico_path}")
    
    temp_dir = Path(ico_path).parent / "temp_icons"
    temp_dir.mkdir(exist_ok=True)
    
    png_files = []
    for size in sizes:
        png_path = temp_dir / f"icon_{size}.png"
        convert_svg_to_png(svg_path, png_path, size)
        png_files.append(png_path)
    
    # Create ICO from PNGs
    images = []
    for png_path in png_files:
        with Image.open(png_path) as img:
            # Convert to RGBA if necessary
            if img.mode != 'RGBA':
                img = img.convert('RGBA')
            images.append(img)
    
    # Save as ICO
    images[0].save(
        ico_path,
        format='ICO',
        sizes=[(size, size) for size in sizes],
        append_images=images[1:],
    )
    
    # Cleanup temp files
    for png_path in png_files:
        png_path.unlink()
    temp_dir.rmdir()
    
    print(f"  Created ICO with sizes: {sizes}")


def create_icns_from_svg(svg_path, icns_path):
    """Create ICNS file from SVG for macOS."""
    print(f"Converting SVG to ICNS: {icns_path}")
    
    # macOS icon sizes
    sizes = {
        'ic07': 128,  # 128x128
        'ic08': 256,  # 256x256
        'ic09': 512,  # 512x512
        'ic10': 1024, # 1024x1024
        'ic11': 32,   # 32x32
        'ic12': 64,   # 64x64
        'ic13': 256,  # 256x256 (2x)
        'ic14': 512,  # 512x512 (2x)
    }
    
    temp_dir = Path(icns_path).parent / "temp_icons"
    temp_dir.mkdir(exist_ok=True)
    
    # Create PNG files for each size
    iconset_dir = temp_dir / "icon.iconset"
    iconset_dir.mkdir(exist_ok=True)
    
    for icon_name, size in sizes.items():
        png_path = iconset_dir / f"{icon_name}.png"
        convert_svg_to_png(svg_path, png_path, size)
    
    # Use iconutil to create ICNS (macOS only)
    if sys.platform == 'darwin':
        subprocess.check_call([
            'iconutil', '-c', 'icns', str(iconset_dir), '-o', icns_path
        ])
        print(f"  Created ICNS using iconutil")
    else:
        # On Windows/Linux, just create a placeholder
        print(f"  Note: ICNS creation requires macOS. Creating placeholder.")
        # Create a simple PNG representation
        png_path = icns_path.with_suffix('.png')
        convert_svg_to_png(svg_path, png_path, 1024)
    
    # Cleanup
    import shutil
    shutil.rmtree(iconset_dir)
    temp_dir.rmdir()


def main():
    script_dir = Path(__file__).parent
    icon_dir = script_dir / "icon"
    svg_path = icon_dir / "fontra-icon-source.svg"
    ico_path = icon_dir / "FontraIcon.ico"
    icns_path = icon_dir / "FontraIcon.icns"
    
    if not svg_path.exists():
        print(f"Error: SVG file not found: {svg_path}")
        sys.exit(1)
    
    print("Fontra Icon Converter")
    print("=" * 50)
    
    # Create ICO for Windows
    create_ico_from_svg(svg_path, ico_path)
    
    # Create ICNS for macOS
    create_icns_from_svg(svg_path, icns_path)
    
    print("=" * 50)
    print("Icon conversion complete!")
    print(f"  Windows icon: {ico_path}")
    print(f"  macOS icon: {icns_path}")


if __name__ == "__main__":
    main()
