import sys
import os
from PIL import Image, ImageDraw, ImageFont, ImageOps
from importlib import import_module
from birdbox.config import DISPLAY_DRIVER, DISPLAY_WIDTH as WIDTH, DISPLAY_HEIGHT as HEIGHT, WAVESHARE_LIB_PATH

# Add the Waveshare driver path to sys.path dynamically
lib_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '../../external/lib'))
sys.path.append(lib_path)

def draw_wrapped_text(draw, text, font, x, y, max_width, line_spacing=4, fill=0):
    import textwrap
    lines = textwrap.wrap(text, width=40)  # adjust wrap width for your layout
    for line in lines:
        draw.text((x, y), line, font=font, fill=fill)
        bbox = draw.textbbox((x, y), line, font=font)
        line_height = bbox[3] - bbox[1]
        y += line_height + line_spacing

def render_bird_display(bird, image_path, mock=True, output_path="bird_display_mock.png", epd=None):
    black_img = Image.new('1', (WIDTH, HEIGHT), 255)
    red_img = Image.new('1', (WIDTH, HEIGHT), 255)

    draw_black = ImageDraw.Draw(black_img)
    draw_red = ImageDraw.Draw(red_img)

    try:
        font_bold = ImageFont.truetype("/usr/share/fonts/truetype/open-sans/OpenSans-Bold.ttf", 30)
        font_italic = ImageFont.truetype("/usr/share/fonts/truetype/open-sans/OpenSans-Italic.ttf", 22)
        font_body = ImageFont.truetype("/usr/share/fonts/truetype/open-sans/OpenSans-Regular.ttf", 18)
    except:
        font_bold = font_italic = font_body = ImageFont.load_default()

    # Image in right column
    image_x = WIDTH - 160
    image_y = 20
    image_width = 150
    image_height = 120

    if os.path.exists(image_path):
        try:
            bird_img = Image.open(image_path).convert("L")  # grayscale
            bird_img = bird_img.point(lambda p: 0 if p < 128 else 255, mode='1')  # threshold to remove background
            bird_img = bird_img.resize((image_width, image_height))
            red_img.paste(bird_img, (image_x, image_y))
        except Exception as e:
            print(f"[ERROR] Failed to load image: {e}")
    else:
        print(f"[WARNING] Image not found: {image_path}")
        draw_red.rectangle([(image_x, image_y), (image_x + image_width, image_y + image_height)], outline=0)

    # Align title text with image top
    title_y = image_y
    draw_black.text((10, title_y), bird["name"], font=font_bold, fill=0)
    draw_black.text((10, title_y + 40), bird["scientific_name"], font=font_italic, fill=0)
    draw_wrapped_text(draw_black, bird["description"], font_body, x=10, y=title_y + 120, max_width=WIDTH - image_width - 40)

    if mock:
        preview = Image.new("RGB", (WIDTH, HEIGHT), "white")
        for y in range(HEIGHT):
            for x in range(WIDTH):
                if black_img.getpixel((x, y)) == 0:
                    preview.putpixel((x, y), (0, 0, 0))
                elif red_img.getpixel((x, y)) == 0:
                    preview.putpixel((x, y), (255, 0, 0))
        preview = preview.convert("RGB")  # Ensure compatible format for thumbnail generation
        preview.save(output_path)
        print(f"Mock display saved to {output_path}")
        preview.show(title=bird["name"])

    else:
        #epd_driver = import_module(DISPLAY_DRIVER)
        #epd = epd_driver.EPD()
        #print("[DEBUG] Initializing EPD...")
        #epd.init()

        print("[DEBUG] Clearing display...")
        epd.Clear()

        print("[DEBUG] Sending image buffers to display...")
        epd.display(epd.getbuffer(black_img), epd.getbuffer(red_img))

        print("[DEBUG] Display update complete")
        #epd.sleep()
