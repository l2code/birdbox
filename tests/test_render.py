from birdbox.display.render_dynamic import render_bird_display

bird = {
    "name": "American Robin",
    "scientific_name": "Turdus migratorius",
    "description": (
        "Also known as the robin, is a migratory songbird of the "
        "true thrush genus and Turdidae, the wider thrush family. "
        "It is distributed throughout North America, where it is "
        "very common in residential areas."
    )
}

#image_path = "assets/images/robin.png"
render_bird_display(bird, image_path="assets/images/robin.png", mock=True)
