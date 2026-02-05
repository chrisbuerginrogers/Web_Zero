# We're using InventZero.
import iz

# A magic incantation needed for the magic to happen.
await iz.setup(globals())

header = iz.text("""Honking in Italy""",name="heading")
image = iz.image(name="car_image", image="https://www.vivovenetia.com/wp-content/uploads/2018/11/H-Le-Betulle-OSLO-Norway-1024x749.jpg")
#plot = iz.plot(name="myPlot", label="Growth", data = [(1,1),(2,2),(3,3)], xLabel = 'time', yLabel = 'value')
slider1 = iz.slider(name="volume", label="Volume", min=0, max=100)
slider2 = iz.slider(name="speed", label="Speed", min=0, max=200)
go = iz.button(name="honk", label="Honk! 🚗")

# The display function draws things on the screen.
iz.display(
    header,
    image,
    slider1,
    slider2,
    go
    )

def press_honk():
    myChannel.post('/honk',True)

myChannel = iz.CEEO_Channel(channel="hackathon", user="@chrisrogers", project="talking-on-a-channel")
myChannel.setupSocket()
