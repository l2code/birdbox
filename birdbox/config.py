# birdbox/config.py

# Display resolution for your specific Waveshare panel
DISPLAY_WIDTH = 400
DISPLAY_HEIGHT = 300

# Module name of the Waveshare driver you want to use
# Must match the .py file in external/lib/waveshare_epd/
#DISPLAY_DRIVER = "epd4in2b_V2"
DISPLAY_DRIVER = "waveshare_epd.epd4in2b_V2"
WAVESHARE_LIB_PATH = "external/lib/waveshare_epd"


# Path to the local copy of the Waveshare library
# Used to patch sys.path at runtime
#WAVESHARE_LIB_PATH = "../../external/lib/waveshare_epd"