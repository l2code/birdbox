from birdbox.services.bird_service import get_current_bird
from birdbox.display.render import render_bird

def update_display():
    bird = get_current_bird()
    render_bird(bird)