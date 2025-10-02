import os
from PIL import Image
import argparse

def resize_images(input_folder, output_folder, width=None, height=None, 
                  scale_percent=None, format=None, quality=95):
    """
    Resize all images in a folder and save them to output folder.
    
    Args:
        input_folder: Path to folder containing images
        output_folder: Path to save resized images
        width: Target width in pixels
        height: Target height in pixels
        scale_percent: Scale by percentage (e.g., 50 for 50%)
        format: Output format (jpg, png, webp, etc.)
        quality: Quality for JPEG/WebP (1-100)
    """
    
    # Create output folder if it doesn't exist
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)
    
    # Supported image extensions
    supported_formats = ('.jpg', '.jpeg', '.png', '.bmp', '.gif', '.tiff', '.webp')
    
    # Counter for processed images
    processed = 0
    failed = 0
    
    # Process each file in input folder
    for filename in os.listdir(input_folder):
        # Check if file is an image
        if filename.lower().endswith(supported_formats):
            input_path = os.path.join(input_folder, filename)
            
            try:
                # Open image
                with Image.open(input_path) as img:
                    # Get original dimensions
                    original_width, original_height = img.size
                    
                    # Calculate new dimensions
                    if scale_percent:
                        new_width = int(original_width * scale_percent / 100)
                        new_height = int(original_height * scale_percent / 100)
                    elif width and height:
                        new_width = width
                        new_height = height
                    elif width:
                        # Maintain aspect ratio based on width
                        new_width = width
                        new_height = int(original_height * (width / original_width))
                    elif height:
                        # Maintain aspect ratio based on height
                        new_height = height
                        new_width = int(original_width * (height / original_height))
                    else:
                        # No resize specified, use original dimensions
                        new_width = original_width
                        new_height = original_height
                    
                    # Resize image with high-quality resampling
                    resized_img = img.resize((new_width, new_height), Image.LANCZOS)
                    
                    # Determine output format and filename
                    if format:
                        output_filename = os.path.splitext(filename)[0] + f'.{format}'
                    else:
                        output_filename = filename
                    
                    output_path = os.path.join(output_folder, output_filename)
                    
                    # Save with appropriate settings
                    if format in ['jpg', 'jpeg'] or filename.lower().endswith(('.jpg', '.jpeg')):
                        # Convert RGBA to RGB for JPEG
                        if resized_img.mode in ('RGBA', 'LA', 'P'):
                            rgb_img = Image.new('RGB', resized_img.size, (255, 255, 255))
                            rgb_img.paste(resized_img, mask=resized_img.split()[-1] if resized_img.mode == 'RGBA' else None)
                            resized_img = rgb_img
                        resized_img.save(output_path, 'JPEG', quality=quality, optimize=True)
                    elif format == 'webp' or filename.lower().endswith('.webp'):
                        resized_img.save(output_path, 'WEBP', quality=quality)
                    else:
                        resized_img.save(output_path)
                    
                    processed += 1
                    print(f"Processed: {filename} ({original_width}x{original_height} -> {new_width}x{new_height})")
                    
            except Exception as e:
                failed += 1
                print(f"Failed to process {filename}: {str(e)}")
    
    # Summary
    print(f"\n{'='*50}")
    print(f"Processing complete!")
    print(f"Successfully processed: {processed} images")
    print(f"Failed: {failed} images")
    print(f"Output saved to: {output_folder}")
    print(f"{'='*50}")


def main():
    """Main function with command-line interface."""
    parser = argparse.ArgumentParser(description='Batch resize images in a folder')
    
    parser.add_argument('input_folder', help='Path to input folder containing images')
    parser.add_argument('output_folder', help='Path to output folder for resized images')
    parser.add_argument('-w', '--width', type=int, help='Target width in pixels')
    parser.add_argument('-ht', '--height', type=int, help='Target height in pixels')
    parser.add_argument('-s', '--scale', type=int, help='Scale percentage (e.g., 50 for 50%%)')
    parser.add_argument('-f', '--format', choices=['jpg', 'jpeg', 'png', 'webp'], 
                        help='Output format')
    parser.add_argument('-q', '--quality', type=int, default=95, 
                        help='Quality for JPEG/WebP (1-100, default: 95)')
    
    args = parser.parse_args()
    
    # Validate input folder exists
    if not os.path.exists(args.input_folder):
        print(f"Error: Input folder '{args.input_folder}' does not exist")
        return
    
    # Run resizer
    resize_images(
        input_folder=args.input_folder,
        output_folder=args.output_folder,
        width=args.width,
        height=args.height,
        scale_percent=args.scale,
        format=args.format,
        quality=args.quality
    )


# Example usage in code
if __name__ == '__main__':
    # Uncomment and modify for direct usage without command line
    """
    resize_images(
        input_folder='./input_images',
        output_folder='./resized_images',
        width=800,  # Resize to 800px width, maintain aspect ratio
        format='jpg',
        quality=90
    )
    """
    
    # Or use command-line interface
    main()
    