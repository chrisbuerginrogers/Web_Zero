"""
Invent Zero!

Maximum invention from minimum code.

Nicholas H.Tollervey and Chris Rogers.
"""

import sys
from pyscript import web, js_import, when
from pyscript.ffi import create_proxy

marked = None
purify = None
_TARGET = web.page["iz"]
_CURRENT_WIDGETS = set()
_APP_GLOBALS = None


async def load_js_modules():
    """
    Load the JavaScript modules required by the Invent framework.
    """
    global marked, purify
    (marked, purify) = await js_import(
        "https://cdn.jsdelivr.net/npm/marked/lib/marked.esm.js",
        "https://esm.run/dompurify",
    )


async def setup(g):
    """
    Get everything ready! The `g` argument is the `globals` dict from the
    calling module. This is used for all the magic lookups.
    """
    global _APP_GLOBALS
    _APP_GLOBALS = g
    await load_js_modules()


def from_markdown(raw_markdown):
    """
    Convert markdown to sanitized HTML.
    """
    result = raw_markdown
    if marked:
        result = purify.default().sanitize(marked.parse(raw_markdown))
    return result


def display(*args):
    """
    Add items to the DOM replacing everything that was already there.
    """
    # Remove the current children.
    _TARGET.replaceChildren()
    # Delete the old references.
    for name in _CURRENT_WIDGETS:
        del _APP_GLOBALS[name]
    # Now just add the passed items to the DOM.
    add(*args)


def add(*args):
    """
    Append items to the DOM.
    """
    for element in args:
        # Ensure the reference to the element is available in the original
        # module (referenced by name).
        _APP_GLOBALS[element.name] = element
        # Add the element to the target div in the dom.
        _TARGET.append(element)


def slider(name, label = None, min = 1, max = 10, value=0):
    """
    Create a slider.
    """
    label = name if not label else label

    def handle_slide(e):
        # The heuristic for handler functions for sliders is
        # "move_slider_name"
        handler = f"move_{name}"
        # If such a named function exists in the originating Python module,
        # call it!
        if handler in _APP_GLOBALS:
            _APP_GLOBALS[handler]()


    class Slider(web.Element):
        """
        This is a complicated widget, i.e. it's not just a 1-1 mapping with an
        HTML element. It requires both an input "range" element and a label
        element, along with means to reach into these child objects to get
        things like a value.
        """

        def __init__(self, name, label, min, max, value):
            self._name = name
            self._container = web.div()
            super().__init__(dom_element=self._container._dom_element)
            self._name = name
            self._range = web.input_(
                type="range", name=name, id=name, min=min, max=max, value=value
            )
            self._label = web.label(label, for_=name)
            self._container.append(self._range, self._label)
            self._range._dom_element.addEventListener("change", create_proxy(handle_slide))

        @property
        def name(self):
            return self._name

        @property
        def value(self):
            return int(self._range.value)

    return Slider(name, label, min, max, value)


def button(name, label):
    """
    Create a button.
    """
    button = web.button(label, name=name)

    def handle_click(e):
        """
        Called when the button is clicked.
        """
        # The heuristic for handler functions for buttons is
        # "press_button_name"
        handler = f"press_{name}"
        # If such a named function exists in the originating Python module,
        # call it!
        if handler in _APP_GLOBALS:
            _APP_GLOBALS[handler]()

    button._dom_element.addEventListener("click", create_proxy(handle_click))

    return button


def text(content, name):
    """
    Create Markdown text.
    """
    return web.div(from_markdown(content), name=name)

def image(name, image, width='100%', height='auto'):
    """
    Create an image.
    """
    style = {"max-width": width, "height": height}
    return web.img(src=image, name=name, style=style)
def separator():
    """
    Create a separator.
    """
    return web.hr(name="foo")

# make sure you have <div id='all_things_channels'></div> on your index.html

from pyscript import WebSocket
import json
from time import sleep

class CEEO_Channel():
    def __init__(self, channel, user, project):
        self.filter = None
        self.value = 0
        self.reply = ''
        self.callback = None
        self.color = 'green'

        self.url = ''
        self.socket = None
        self.is_connected = False
        self.reconnect_attempts = 0
        self.max_reconnect_attempts = 5
        self.reconnect_delay = 2

        self.channel, self.user, self.project = channel, user, project

    def connect_disconnect(self, event):   
        if self.c_btn.innerText == 'connect':
            self.setupSocket()
            self.c_btn.innerText = 'disconnect'
        else:
            self.c_btn.innerText = 'connect'
            self.close()

    def setupSocket(self):
        self.url = f"wss://{self.user}.pyscriptapps.com/{self.project}/api/channels/{self.channel}"
        print(self.url)
        self.is_connected = False
        self._web_socket = None
        self.connect()
        
    async def onmessage(self, event):
        try:
            message = json.loads(event.data)
            print('received ',message)
            self.on_received(message)
        except:
            print('on receive error: ',message)
        
    def on_received(self, message):
        if message['type'] == 'welcome':
            self.connected = True
        if message['type'] == 'data':
            if message['payload']:
                try:
                    self.reply = json.loads(message['payload'])
                    self.value = self.reply['value']
                    if self.callback:
                            self.callback(message)
                except Exception as e:
                    print('load error ',message)

    def post(self, filter, value):
        if not self.is_connected:
            print('not connected')
            return
        payload = {'topic':filter,'value':value}
        print(payload)
        try:
            self.socket.send(json.dumps(payload))
        except Exception as e:
            print('post error ',e) 

    def connect(self):
        def onopen(event):
            self.is_connected = True
            self.reconnect_attempts = 0
        def onclose(event):
            self.is_connected = False
            self.reconnect()
        self.socket = WebSocket(url=self.url, onopen=onopen, onclose=onclose, onmessage=self.onmessage)

    def reconnect(self):
        if self.reconnect_attempts < self.max_reconnect_attempts:
            self.reconnect_attempts += 1
            sleep(self.reconnect_delay)
            self.connect()

    def close(self):
        self.socket.close()
        self.reconnect_attempts = self.max_reconnect_attempts
        self.is_connected = False
