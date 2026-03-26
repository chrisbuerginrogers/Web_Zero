# We're using InventZero.
import iz

# A magic incantation needed for the magic to happen.
await iz.setup(globals())

header = iz.text("""Honking in Italy""",name="heading")
image = iz.image(name="moped_image", image="./assets/moped.jpg", width='50%')
#plot = iz.plot(name="myPlot", label="Growth", data = [(1,1),(2,2),(3,3)], xLabel = 'time', yLabel = 'value')
slider1 = iz.slider(name="volume", label="Volume", min=0, max=100)
slider2 = iz.slider(name="speed", label="Speed", min=0, max=200)
sep = iz.separator()
go = iz.button(name="honk", label="Honk! 🚗")
menu = iz.dropdown(name="vehicle", label="Choose vehicle", 
                   options=[("moped", "Moped"),("car", "Car"),("bike", "Bike")])
nav = iz.navbar(name="mainnav",items=[("Home", "home"),("Services", [("Web Design", "web"),
                ("Branding", "branding"),("Illustration", "illustration")]),("Contact", "contact")])
toggle = iz.toggle(name="mute", label="Mute")
text = iz.text_input(name="username", placeholder="Enter name")
color = iz.color_picker(name="bgcolor")

mode = iz.radio_group(
    name="mode",
    options=[
        ("eco", "Eco Mode"),
        ("normal", "Normal Mode"),
        ("sport", "Sport Mode")
    ]
)
status = iz.text("""No mode selected""", name="status")

#dropdown = iz.dropdown(name="drop", font_size=16, width=14, height=10, margin=20)

# The display function draws things on the screen.
iz.display(
    header,
    image,
    mode, 
    status,
    text,
    sep,
    slider1,
    slider2,
    toggle,
    color,
    go
    )

def press_honk():
    myChannel.post('/honk',True)


def change_mode():
    if mode.value:
        status._dom_element.innerHTML = f"Mode: {mode.value}"
    else:
        status._dom_element.innerHTML = "No mode selected"


myChannel = iz.CEEO_Channel(channel="hackathon", user="@chrisrogers", project="talking-on-a-channel")
myChannel.connect()


