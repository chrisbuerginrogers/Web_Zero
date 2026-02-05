# We're using InventZero.
import iz

# Needed for the Python k-nearest neighbour search.
import math


# A magic incantation needed for the magic to happen.
await iz.setup(globals())

def myView():
    header = iz.text("""# FilmFinder 🎥❓
        Move the sliders to indicate your mood.

        Press "Find Films" to see suggestions.""",name="heading")
    romance = iz.slider(name="romance")
    comedy = iz.slider(name="comedy")
    action = iz.slider(name="action")
    feel = iz.slider(name="feel_good")
    intel = iz.slider(name="intellect")
    fright = iz.slider(name="fright")
    go = iz.button(name="go_button", label="Find Films 🔍")

    # The display function draws things on the screen.
    iz.display(header,romance, comedy,action,feel,intel,fright,go)
myView()

def press_go_button():
    """
    Handles when the go_button is pressed.

    It reads the values from the sliders (by using their name), and uses
    these to do a k-nearest neighbour look up using the movie database.
    """
    # The suggest_films function is "real" Python.
    films = suggest_films(
        romance.value,
        comedy.value,
        action.value,
        feel_good.value,
        intellect.value,
        fright.value,
    )
    # Display the results.
    iz.display(iz.text("# Results", name="header"))
    for film in films:
        # If you "add" widgets, they're appended to the UI.
        # (Display, deletes and then adds.)
        iz.add(
            iz.text(f'## {film["title"]}', name="film_name"),
            iz.image(name="film_poster", image=film["metadata"]["Poster"]),
            iz.text(f'{film["metadata"]["Plot"]}', name="film_description"),
            iz.separator(),
        )
    iz.add(iz.button(name="search", label="Search Again 🔍"))

def press_search():
    """
    Handles when the search button is pressed.

    It just re-displays the original view.
    """
    myView()
    
def distance(film1, film2):
    """
    Calculate the Euclidean distance between two points (films) in 6D space.
    """
    return math.sqrt(
        (film1["romance"] - film2["romance"]) ** 2
        + (film1["comedy"] - film2["comedy"]) ** 2
        + (film1["action"] - film2["action"]) ** 2
        + (film1["feel-good"] - film2["feel-good"]) ** 2
        + (film1["intellect"] - film2["intellect"]) ** 2
        + (film1["fright"] - film2["fright"]) ** 2
    )


def suggest_films(romance, comedy, action, feel_good, intellect, fright):
    """
    k-nearest neighbour results from films dataset.

    This is just standard Python and should be ignored.
    """
    # Import the dataset with JSON.
    import json

    with open("film_data.json") as f:
        films_data = json.load(f)
    # The target values for your hoped-for film matches (from user input).
    target = {
        "romance": romance,
        "comedy": comedy,
        "action": action,
        "feel-good": feel_good,
        "intellect": intellect,
        "fright": fright,
    }
    # A list to hold the results.
    distances = []
    # Iterate over each film...
    for film in films_data:
        # ... then calculate its distance from the target,
        dist = distance(target, film["attributes"])
        # and append it to the list as a tuple of two values representing
        # the distance and film data.
        distances.append((dist, film))
    # Now we have all the distances for each film, order the list so the
    # nearest are at the start.
    distances.sort(key=lambda x: x[0])
    # Return the "size" first items in the list (the nearest matches).
    return [film for _, film in distances[:10]]
