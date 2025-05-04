#import RPi.GPIO as GPIO
import time
import os
import argparse
from birdbox.display.render_dynamic import render_bird_display

# List of birds to cycle through
birds = [
    {
        "name": "American Robin",
        "scientific_name": "Turdus migratorius",
        "description": (
            "Also known as the robin, is a migratory songbird of the "
            "true thrush genus and Turdidae, the wider thrush family. "
            "It is distributed throughout North America, where it is "
            "very common in residential areas."
        ),
        "image_path": "assets/images/robin.png"
    },
    {
        "name": "Northern Cardinal",
        "scientific_name": "Cardinalis cardinalis",
        "description": (
            "The Northern Cardinal is a bird in the genus Cardinalis. It is "
            "found in woodlands, gardens, shrublands, and wetlands. The male "
            "is known for its bright red color."
        ),
        "image_path": "assets/images/cardinal.png"
    },
    {
        "name": "Blue Jay",
        "scientific_name": "Cyanocitta cristata",
        "description": (
            "The Blue Jay is a passerine bird in the family Corvidae, native to "
            "North America. It is known for its intelligence and complex social behavior."
        ),
        "image_path": "assets/images/bluejay.png"
    }
]

index = 0

def auto_cycle_birds(interval_sec=10, mock=True):
    global index
    print(f"Auto-cycling bird display every {interval_sec} seconds...")
    try:
        while True:
            bird = birds[index]
            print(f"Displaying: {bird['name']}")
            output_dir = "output/mock"
            os.makedirs(output_dir, exist_ok=True)
            output_path = os.path.join(output_dir, f"bird_display_{index}.png")
            render_bird_display(bird, image_path=bird["image_path"], mock=mock, output_path=output_path)
            #render_bird_display(bird, image_path=bird["image_path"], mock=True, output_path=f"bird_display_{index}.png")  # Ensure preview image is saved as RGB
            index = (index + 1) % len(birds)
            time.sleep(interval_sec)
    except KeyboardInterrupt:
        print("Exiting...")
        #GPIO.cleanup()

if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser()
    parser.add_argument("--mock", action="store_true", help="Enable mock mode")
    parser.add_argument("--interval", type=int, default=10, help="Time between cycles")
    args = parser.parse_args()

    auto_cycle_birds(interval_sec=args.interval, mock=args.mock)

