from birdbox.storage.local_store import load_latest_bird, save_bird_data

def get_current_bird():
    return load_latest_bird()

def save_bird(bird):
    save_bird_data(bird)