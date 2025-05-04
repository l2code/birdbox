from PIL import Image, ImageDraw, ImageFont
import os
import logging

WIDTH, HEIGHT = 400, 300  # Adjust for your actual Waveshare display

logging.basicConfig(level=logging.INFO)

args = None
if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Weather Display")
    parser.add_argument('--mock', action='store_true', help='Use mock display instead of real Waveshare e-Paper')
    args = parser.parse_args()
else:
    class Args:
        mock = False
    args = Args()

def render_bird_display(bird, image_path, mock=True, output_path="bird_display_mock.png"):
    # Create black and red image buffers
    black_img = Image.new('1', (WIDTH, HEIGHT), 255)
    red_img = Image.new('1', (WIDTH, HEIGHT), 255)

    draw_black = ImageDraw.Draw(black_img)
    draw_red = ImageDraw.Draw(red_img)

    # Load fonts
    try:
        font_bold = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", 30)
        font_italic = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans-Oblique.ttf", 22)
        font_body = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf", 18)
    except:
        font_bold = font_italic = font_body = ImageFont.load_default()

    # Draw text
    draw_black.text((10, 10), bird["name"], font=font_bold, fill=0)
    draw_black.text((10, 50), bird["scientific_name"], font=font_italic, fill=0)
    draw_black.text((10, 90), bird["description"], font=font_body, fill=0)

    # Add image to red layer
    if os.path.exists(image_path):
        bird_img = Image.open(image_path).convert("1").resize((150, 120))
        red_img.paste(bird_img, (WIDTH - 160, 10))

    if mock:
        # Create RGB preview for desktop
        preview = Image.new("RGB", (WIDTH, HEIGHT), "white")
        for y in range(HEIGHT):
            for x in range(WIDTH):
                if black_img.getpixel((x, y)) == 0:
                    preview.putpixel((x, y), (0, 0, 0))
                elif red_img.getpixel((x, y)) == 0:
                    preview.putpixel((x, y), (255, 0, 0))
        preview.save(output_path)
        print(f"Mock display saved to {output_path}")
    else:
        import epd4in2b_V2 as epd_driver  # Adjust to your Waveshare driver
        epd = epd_driver.EPD()
        epd.init()
        epd.Clear()
        epd.display(epd.getbuffer(black_img), epd.getbuffer(red_img))
        epd.sleep()