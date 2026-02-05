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

# The display function draws things on the screen.
iz.display(
    header,
    image,
    sep,
    slider1,
    slider2,
    go
    )

def press_honk():
    myChannel.post('/honk',True)

myChannel = iz.CEEO_Channel(channel="hackathon", user="@chrisrogers", project="talking-on-a-channel")
myChannel.connect()
